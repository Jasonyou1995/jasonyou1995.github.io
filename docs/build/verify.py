#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Weekly 5-minute check. Run from the repo root: python3 docs/build/verify.py

Checks (all offline):
  1. JSON-LD parses on every page and every @id reference resolves inside the same graph
  2. Only core schema.org types are used
  3. hreflang is complete and reciprocal on every locale page
  4. No em dash, en dash or three-dash dividers; banned English words; no dash in Chinese copy
  5. No private data patterns (phone, GPA, street address words)
  6. Every internal link and asset exists; JS under 200 KB; page weight report
  7. Text contrast of the design tokens meets WCAG AA
Still manual: run https://validator.schema.org on the live URL, and time the page from Shenzhen.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

CORE_TYPES = {
    "WebSite", "WebPage", "Person", "ImageObject", "Service", "OfferCatalog", "Offer", "Product",
    "PropertyValue", "FAQPage", "Question", "Answer", "DefinedTermSet", "DefinedTerm", "Place",
    "CollegeOrUniversity", "BusinessAudience",
}
fails = []
notes = []


def fail(msg):
    fails.append(msg)


def pages():
    out = []
    for l in C.LOCALES:
        out.append(os.path.join(ROOT, l["path"], "index.html"))
    for k in C.CYBERPORT_LOCALES:
        out.append(os.path.join(ROOT, [l for l in C.LOCALES if l["key"] == k][0]["path"], "cyberport", "index.html"))
    return out


def walk_ids(node, found, refs, top=True):
    if isinstance(node, dict):
        if "@id" in node:
            if len(node) == 1:
                refs.add(node["@id"])
            else:
                found.add(node["@id"])
        for v in node.values():
            walk_ids(v, found, refs, False)
    elif isinstance(node, list):
        for v in node:
            walk_ids(v, found, refs, False)


def types_in(node, acc):
    if isinstance(node, dict):
        t = node.get("@type")
        if t:
            acc.update(t if isinstance(t, list) else [t])
        for v in node.values():
            types_in(v, acc)
    elif isinstance(node, list):
        for v in node:
            types_in(v, acc)


def check_jsonld(path, text):
    m = re.search(r'<script type="application/ld\+json" id="graph">\s*(.*?)\s*</script>', text, re.S)
    if not m:
        return fail("%s: no JSON-LD graph" % path)
    try:
        g = json.loads(m.group(1))
    except Exception as ex:
        return fail("%s: JSON-LD invalid: %s" % (path, ex))
    found, refs = set(), set()
    walk_ids(g["@graph"], found, refs)
    # refs to entities that live on other pages (none expected) would be listed here
    unresolved = {r for r in refs if r not in found}
    if unresolved:
        fail("%s: unresolved @id refs %s" % (path, sorted(unresolved)))
    ts = set()
    types_in(g["@graph"], ts)
    bad = ts - CORE_TYPES
    if bad:
        fail("%s: non-core types %s" % (path, sorted(bad)))
    names = [n.get("name") for n in g["@graph"] if n.get("@type") == "Person"]
    if names != ["Shengwei You"]:
        fail("%s: Person name unexpected %s" % (path, names))
    blob = m.group(1)
    if "Dr." in blob or "Dr " in blob:
        fail("%s: title Dr. must not appear until the defense" % path)
    return len(g["@graph"])


def check_hreflang():
    expect = {l["code"] for l in C.LOCALES}
    for l in C.LOCALES:
        t = open(os.path.join(ROOT, l["path"], "index.html"), encoding="utf-8").read()
        codes = set(re.findall(r'rel="alternate" hreflang="([^"]+)"', t))
        if codes != expect | {"x-default"}:
            fail("hreflang mismatch on %s: %s" % (l["key"], sorted(codes ^ (expect | {"x-default"}))))
        canon = re.search(r'rel="canonical" href="([^"]+)"', t).group(1)
        if canon != C.BASE + l["path"]:
            fail("canonical wrong on %s: %s" % (l["key"], canon))
        if 'hreflang="%s" href="%s"' % (l["code"], C.BASE + l["path"]) not in t:
            fail("self hreflang missing on %s" % l["key"])


def check_copy():
    files = [p for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True)
             if p.endswith((".html", ".md", ".txt", ".css", ".js")) and
             not any(x in p for x in ("/.git/", "/.venv/", "/tools/", "/docs/superpowers/", "/research/", "/projects/", "index.zh-CN.html", "index.zh-TW.html"))]
    dash = re.compile("[—–]")
    triple = re.compile(r"^\s*---+\s*$", re.M)
    banned = re.compile(r"\b(leverage|robust|navigate|delve)\b", re.I)
    priv = re.compile(r"(\+\d[\d\s\-]{8,}\d)|\b\d{3}[\s\-]\d{3,4}[\s\-]\d{4}\b|\bGPA\b|\bstreet\b|\bphone\b", re.I)
    for p in files:
        rel = os.path.relpath(p, ROOT)
        if rel.startswith("twin/node_modules"):
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        if dash.search(t):
            fail("%s: contains em or en dash" % rel)
        if rel.endswith(".md") and rel != "CLAUDE.md" and "twin/" not in rel and triple.search(t):
            fail("%s: three-dash divider" % rel)
        if banned.search(t) and rel.endswith((".html", ".md", ".txt")) and rel != "CLAUDE.md":
            fail("%s: banned word" % rel)
        if rel.endswith((".html", ".md")) and priv.search(re.sub(r"https?://\S+|mailto:\S+|sitemap|\d{4}-\d{2}-\d{2}|5,866,037", "", t)):
            notes.append("%s: private-data pattern matched, check by eye: %s" % (rel, priv.search(re.sub(r"https?://\S+|mailto:\S+|\d{4}-\d{2}-\d{2}|5,866,037", "", t)).group(0)))


def check_links():
    for p in pages():
        t = open(p, encoding="utf-8").read()
        d = os.path.dirname(p)
        for m in re.finditer(r'(?:href|src)="([^"#?:][^"#?]*)(?:\?[^"]*)?(?:#[^"]*)?"', t):
            u = m.group(1)
            if u.startswith(("http", "mailto", "//", "data:")):
                continue
            tgt = os.path.normpath(os.path.join(d, u))
            if u.endswith("/") or u in ("", "."):
                tgt = os.path.join(tgt, "index.html")
            if not os.path.exists(tgt):
                fail("%s: broken link %s" % (os.path.relpath(p, ROOT), u))


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def check_contrast():
    pairs = [("#17140F", "#F2EFE8", "ink on marble"), ("#4A453C", "#F2EFE8", "ink2 on marble"),
             ("#A04F00", "#F2EFE8", "accent on marble"), ("#A04F00", "#FAF8F3", "accent on surface"),
             ("#4A453C", "#FAF8F3", "ink2 on surface"), ("#F2EFE8", "#17140F", "button text"),
             ("#E9E4D8", "#0C0B09", "xray ink"), ("#B9B3A5", "#0C0B09", "xray ink2"),
             ("#F2A33A", "#0C0B09", "xray accent"), ("#5EE0D2", "#0C0B09", "xray agent"),
             ("#D9D3C5", "#17140F", "twin lead"), ("#17140F", "#F2A33A", "twin bubble")]
    for fg, bg, name in pairs:
        r = ratio(fg, bg)
        if r < 4.5:
            fail("contrast %s %.2f < 4.5" % (name, r))
        else:
            notes.append("contrast ok %-18s %.2f" % (name, r))


def check_budget():
    js = os.path.getsize(os.path.join(ROOT, "assets/js/site.js"))
    css = os.path.getsize(os.path.join(ROOT, "assets/css/site.css"))
    if js > 200 * 1024:
        fail("JS over 200 KB: %d" % js)
    fonts = sum(os.path.getsize(f) for f in glob.glob(os.path.join(ROOT, "assets/fonts/*.woff2")))
    notes.append("js %d B, css %d B, fonts %d B, home html %d B" % (js, css, fonts, os.path.getsize(os.path.join(ROOT, "index.html"))))


def check_lockstep():
    base = set(C.S["en"].keys())
    for k, s in C.S.items():
        need = base if k in C.CYBERPORT_LOCALES or k == "zh-hans" else {x for x in base if not x.startswith("cp_")}
        if need - set(s):
            fail("locale %s missing %s" % (k, sorted(need - set(s))))
    cn = re.compile("[一-鿿]")
    for k in ("zh-hans", "zh-hk"):
        for key, v in C.S[k].items():
            if "—" in v or "--" in v:
                fail("%s.%s: dash in Chinese copy" % (k, key))


if __name__ == "__main__":
    for p in pages():
        t = open(p, encoding="utf-8").read()
        n = check_jsonld(os.path.relpath(p, ROOT), t)
        notes.append("%s: JSON-LD ok, %s nodes" % (os.path.relpath(p, ROOT), n))
    check_hreflang()
    check_copy()
    check_links()
    check_contrast()
    check_budget()
    check_lockstep()
    for n in notes:
        print("  ", n)
    if fails:
        print("\nFAIL")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("\nALL CHECKS PASSED")
