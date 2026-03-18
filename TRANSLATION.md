# Local Translation Workflow

## 1) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Configure keys (optional)

```bash
cp .env.example .env
```

Only fill keys for the provider you use.

## 3) Generate translated pages

API-free mode:

```bash
python3 translate_site.py --provider google_free
```

DeepSeek mode:

```bash
python3 translate_site.py --provider deepseek
```

Anthropic mode:

```bash
python3 translate_site.py --provider anthropic
```

Custom language list:

```bash
python3 translate_site.py --provider google_free --languages zh-CN,zh-TW,es,fr,pt,ru,ja,ko,de
```

The script outputs static files like `index.zh-CN.html`, `index.es.html`, etc.

## 4) Preserve names and proper nouns

Add one protected term per line in `names.txt` (for example: personal names, institutions, tools).
These terms are preserved during translation. If `names.txt` is missing or lines are omitted, built-in defaults are used.

Use a custom file if needed:

```bash
python3 translate_site.py --provider google_free --names-file names.txt
```
