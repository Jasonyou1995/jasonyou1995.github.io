#!/usr/bin/env python3
import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


DEFAULT_LANGUAGES = ["zh-CN", "zh-TW", "es", "fr", "pt", "ru"]
DEFAULT_SOURCE_FILE = "index.html"
DEFAULT_NAMES_FILE = "names.txt"
ENV_FILE = ".env"
LANG_MAP_JS_TOKEN = "const LANG_PAGE_MAP = {"
SKIP_PARENTS = {"script", "style", "noscript"}
MAX_RETRIES = 2
REQUEST_TIMEOUT_SECONDS = 15
PROTECTED_TOKEN_PREFIX = "__PROTECTED_TERM_"
DEFAULT_PROTECTED_TERMS = [
    "Shengwei You",
    "Andrey Kuehlkamp",
    "Jarek Nabrzyski",
    "Kristina Radivojevic",
    "Paul Brenner",
    "Aditya Joshi",
]


@dataclass
class TranslationItem:
    key: str
    value: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate translated static HTML pages from index.html."
    )
    parser.add_argument(
        "--provider",
        choices=["google_free", "deepseek", "anthropic"],
        default="google_free",
        help="Translation provider. 'google_free' is API-key free.",
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE_FILE,
        help="Source HTML file (default: index.html).",
    )
    parser.add_argument(
        "--languages",
        default=",".join(DEFAULT_LANGUAGES),
        help="Comma-separated language codes (e.g. zh-CN,es,fr).",
    )
    parser.add_argument(
        "--names-file",
        default=DEFAULT_NAMES_FILE,
        help="Optional newline-delimited protected terms file (default: names.txt).",
    )
    parser.add_argument(
        "--deepseek-model",
        default="deepseek-chat",
        help="DeepSeek model name.",
    )
    parser.add_argument(
        "--anthropic-model",
        default="claude-3-5-haiku-latest",
        help="Anthropic model name.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip language output file if it already exists.",
    )
    return parser.parse_args()


def load_env(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_protected_terms(file_path: Path) -> List[str]:
    terms = list(DEFAULT_PROTECTED_TERMS)
    if file_path.exists():
        for raw_line in file_path.read_text(encoding="utf-8").splitlines():
            candidate = raw_line.strip()
            if not candidate or candidate.startswith("#"):
                continue
            terms.append(candidate)

    unique_terms = []
    seen = set()
    for term in terms:
        if term in seen:
            continue
        seen.add(term)
        unique_terms.append(term)

    return sorted(unique_terms, key=len, reverse=True)


def protect_terms(text: str, protected_terms: List[str]) -> tuple[str, Dict[str, str]]:
    protected_text = text
    token_map: Dict[str, str] = {}
    token_index = 0
    for term in protected_terms:
        if term not in protected_text:
            continue
        token = f"{PROTECTED_TOKEN_PREFIX}{token_index}__"
        protected_text = protected_text.replace(term, token)
        token_map[token] = term
        token_index += 1
    return protected_text, token_map


def restore_terms(text: str, token_map: Dict[str, str]) -> str:
    restored_text = text
    for token, term in token_map.items():
        restored_text = restored_text.replace(token, term)
    return restored_text


def should_translate(text: str) -> bool:
    candidate = text.strip()
    if not candidate:
        return False
    return bool(re.search(r"[A-Za-z]", candidate))


def collect_translatable_items(soup: BeautifulSoup) -> List[TranslationItem]:
    items: List[TranslationItem] = []
    node_index = 0

    for node in soup.find_all(string=True):
        parent = node.parent
        if parent and parent.name in SKIP_PARENTS:
            continue
        raw_text = str(node)
        if not should_translate(raw_text):
            continue
        node_index += 1
        key = f"text::{node_index}"
        items.append(TranslationItem(key=key, value=raw_text))
        node.replace_with(f"__I18N_TEXT_{node_index}__")

    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description.get("content"):
        content = str(meta_description["content"])
        if should_translate(content):
            items.append(TranslationItem(key="meta::description", value=content))
            meta_description["content"] = "__I18N_META_DESCRIPTION__"

    for img_index, img_tag in enumerate(soup.find_all("img"), start=1):
        alt_value = img_tag.get("alt")
        if alt_value and should_translate(alt_value):
            key = f"img::{img_index}::alt"
            items.append(TranslationItem(key=key, value=alt_value))
            img_tag["alt"] = f"__I18N_IMG_ALT_{img_index}__"

    return items


def apply_translations(
    html_template: str, lang_code: str, translated_map: Dict[str, str]
) -> str:
    output = html_template
    output = output.replace('<html lang="en">', f'<html lang="{lang_code}">', 1)

    for key, translated in translated_map.items():
        if key.startswith("text::"):
            marker = f"__I18N_TEXT_{key.split('::')[1]}__"
            output = output.replace(marker, translated)
        elif key == "meta::description":
            output = output.replace("__I18N_META_DESCRIPTION__", translated)
        elif key.startswith("img::"):
            image_id = key.split("::")[1]
            marker = f"__I18N_IMG_ALT_{image_id}__"
            output = output.replace(marker, translated)

    output = output.replace("__I18N_META_DESCRIPTION__", "")
    output = re.sub(r"__I18N_TEXT_\d+__", "", output)
    output = re.sub(r"__I18N_IMG_ALT_\d+__", "", output)
    return output


def split_chunks(values: List[str], chunk_size: int) -> List[List[str]]:
    return [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]


def parse_json_array(raw_text: str) -> List[str]:
    try:
        data = json.loads(raw_text)
        if isinstance(data, list):
            return [str(item) for item in data]
    except json.JSONDecodeError:
        pass
    match = re.search(r"\[(.|\n|\r)*\]", raw_text)
    if not match:
        raise ValueError("No JSON array found in model response.")
    data = json.loads(match.group(0))
    if not isinstance(data, list):
        raise ValueError("Model response is not a JSON array.")
    return [str(item) for item in data]


def build_batch_prompt(texts: List[str], target_lang: str) -> str:
    payload = json.dumps(texts, ensure_ascii=False)
    return (
        f"Translate this JSON array of UI strings from English to {target_lang}. "
        "Return ONLY a JSON array with the same length and order. "
        "Keep placeholders, punctuation, symbols, capitalization style, and brand/tool names unchanged.\n"
        f"{payload}"
    )


def call_deepseek(prompt: str, model: str) -> str:
    if requests is None:
        raise ImportError("Missing dependency: requests. Install with `pip install -r requirements.txt`.")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing DEEPSEEK_API_KEY in environment.")
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "You are a precise translator."},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def call_anthropic(prompt: str, model: str) -> str:
    if requests is None:
        raise ImportError("Missing dependency: requests. Install with `pip install -r requirements.txt`.")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY in environment.")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "max_tokens": 4096,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()
    return data["content"][0]["text"]


def translate_with_llm(
    unique_texts: List[str], lang_code: str, provider: str, model: str
) -> Dict[str, str]:
    translated: Dict[str, str] = {}
    chunks = split_chunks(unique_texts, chunk_size=40)
    for chunk in chunks:
        prompt = build_batch_prompt(chunk, lang_code)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                if provider == "deepseek":
                    raw = call_deepseek(prompt, model)
                else:
                    raw = call_anthropic(prompt, model)
                values = parse_json_array(raw)
                if len(values) != len(chunk):
                    raise ValueError(
                        f"Unexpected translated array length ({len(values)} vs {len(chunk)})."
                    )
                for src, dst in zip(chunk, values):
                    translated[src] = dst
                break
            except Exception:
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(attempt * 1.5)
    return translated


def translate_with_google_free(unique_texts: List[str], lang_code: str) -> Dict[str, str]:
    if requests is None:
        raise ImportError("Missing dependency: requests. Install with `pip install -r requirements.txt`.")

    def translate_single_with_timeout(text: str) -> str:
        endpoint = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": lang_code,
            "dt": "t",
            "q": text,
        }
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(
                    endpoint,
                    params=params,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                )
                response.raise_for_status()
                payload = response.json()
                chunks = payload[0] if isinstance(payload, list) and payload else []
                translated_parts = [
                    str(chunk[0]) for chunk in chunks if isinstance(chunk, list) and chunk
                ]
                translated_text = "".join(translated_parts).strip()
                if translated_text:
                    return translated_text
            except Exception:
                if attempt == MAX_RETRIES:
                    return text
                time.sleep(attempt * 1.5)
        return text

    translated: Dict[str, str] = {}
    for text in unique_texts:
        cleaned = normalize_whitespace(text)
        translated_value = translate_single_with_timeout(cleaned)
        translated[text] = translated_value
    return translated


def build_lang_map_js_block(languages: List[str]) -> str:
    lines = ["const LANG_PAGE_MAP = {", "            'en': 'index.html',"]
    for lang in languages:
        lines.append(f"            '{lang}': 'index.{lang}.html',")
    lines.append("        };")
    return "\n".join(lines)


def inject_lang_map(html: str, languages: List[str]) -> str:
    start_idx = html.find(LANG_MAP_JS_TOKEN)
    if start_idx == -1:
        return html
    end_idx = html.find("};", start_idx)
    if end_idx == -1:
        return html
    end_idx += 2
    return html[:start_idx] + build_lang_map_js_block(languages) + html[end_idx:]


def main() -> None:
    args = parse_args()
    source_path = Path(args.source).resolve()
    root_dir = source_path.parent
    load_env(root_dir / ENV_FILE)

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    language_codes = [code.strip() for code in args.languages.split(",") if code.strip()]
    if not language_codes:
        raise ValueError("No target languages provided.")
    if "en" in language_codes:
        language_codes = [code for code in language_codes if code != "en"]

    source_html = source_path.read_text(encoding="utf-8")
    source_html = inject_lang_map(source_html, language_codes)
    protected_terms = load_protected_terms(root_dir / args.names_file)
    if BeautifulSoup is None:
        raise ImportError("Missing dependency: beautifulsoup4. Install with `pip install -r requirements.txt`.")
    soup = BeautifulSoup(source_html, "html.parser")
    items = collect_translatable_items(soup)
    template_html = str(soup)

    if not items:
        print("No translatable text found.")
        return

    unique_texts = sorted({item.value for item in items})
    protected_inputs: Dict[str, str] = {}
    token_maps: Dict[str, Dict[str, str]] = {}
    for text in unique_texts:
        normalized_text = normalize_whitespace(text)
        protected_text, token_map = protect_terms(normalized_text, protected_terms)
        protected_inputs[text] = protected_text
        token_maps[text] = token_map
    unique_protected_texts = sorted({value for value in protected_inputs.values()})
    print(f"Found {len(items)} translatable nodes ({len(unique_texts)} unique).")

    for lang_code in language_codes:
        output_path = root_dir / f"index.{lang_code}.html"
        if args.skip_existing and output_path.exists():
            print(f"[skip] {output_path.name} already exists.")
            continue

        if args.provider == "google_free":
            protected_translation_cache = translate_with_google_free(unique_protected_texts, lang_code)
        elif args.provider == "deepseek":
            protected_translation_cache = translate_with_llm(
                unique_protected_texts, lang_code, provider="deepseek", model=args.deepseek_model
            )
        else:
            protected_translation_cache = translate_with_llm(
                unique_protected_texts, lang_code, provider="anthropic", model=args.anthropic_model
            )

        translation_cache: Dict[str, str] = {}
        for source_text in unique_texts:
            protected_source = protected_inputs[source_text]
            translated_protected = protected_translation_cache[protected_source]
            translation_cache[source_text] = restore_terms(
                translated_protected, token_maps[source_text]
            )

        translated_map = {item.key: translation_cache[item.value] for item in items}
        translated_html = apply_translations(template_html, lang_code, translated_map)
        output_path.write_text(translated_html, encoding="utf-8")
        print(f"[ok] Generated {output_path.name}")


if __name__ == "__main__":
    main()
