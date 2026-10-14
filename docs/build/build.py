#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for jasonyou1995.github.io.

Local-only step. GitHub Pages serves the generated files as plain HTML, CSS and JS.
Run from the repo root:  python3 docs/build/build.py
Needs: python3 and `pip install opencc-python-reimplemented` (only for zh-HK derivation).

Outputs (all committed):
  index.html, <locale>/index.html          home pages, one crawlable URL per locale
  cyberport/index.html, zh-hk/cyberport/   one-pager (EN, zh-HK)
  index.md, <locale>/index.md              plain Markdown twin of each home page
  llms.txt, robots.txt, sitemap.xml, 404.html
  index.zh-CN.html, index.zh-TW.html       redirect stubs for the old URLs
"""
import html
import json
import os
import re
import sys
import posixpath
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C  # noqa: E402

ROOT = os.path.abspath(os.environ.get("SITE_ROOT", os.path.join(HERE, "..", "..")))

# ---- deploy-time settings (fill these after the twin proxy is deployed) ----
TWIN_ENDPOINT = os.environ.get("TWIN_ENDPOINT", "")        # e.g. https://twin.example.workers.dev/chat
TURNSTILE_SITEKEY = os.environ.get("TURNSTILE_SITEKEY", "")  # public site key, safe to commit
ASSET_VER = C.UPDATED

BASE = C.BASE
B = BASE
LOCALES = C.LOCALES
BYKEY = {l["key"]: l for l in LOCALES}
REQUIRED_KEYS = set(C.S["en"].keys())


def e(s):
    return html.escape(s, quote=True)


def em(s):
    """Escape then turn [[word]] into <em>word</em>."""
    return re.sub(r"\[\[(.+?)\]\]", r"<em>\1</em>", e(s))


def plain(s):
    return re.sub(r"\[\[(.+?)\]\]", r"\1", s)


def rel(from_dir, to_path):
    """Relative URL from a page living in from_dir ('' or 'zh-hk/') to to_path (repo-relative)."""
    start = from_dir.rstrip("/") or "."
    out = posixpath.relpath(to_path.rstrip("/") or ".", start)
    if to_path.endswith("/") or to_path == "":
        out = (out + "/") if out != "." else "./"
    return out


def mailto(subject, body):
    return "mailto:%s?subject=%s&body=%s" % (C.EMAIL, quote(subject, safe=""), quote(body, safe=""))


def check_keys():
    for k, s in C.S.items():
        need = REQUIRED_KEYS if k in C.CYBERPORT_LOCALES or k == "zh-hans" else {x for x in REQUIRED_KEYS if not x.startswith("cp_")}
        missing = need - set(s.keys())
        if missing:
            sys.exit("locale %s missing keys: %s" % (k, sorted(missing)))


# --------------------------------------------------------------------------
# JSON-LD
# --------------------------------------------------------------------------
def nodes_for(loc, s, page="home"):
    page_url = B + loc["path"] + ("cyberport/" if page == "cyberport" else "")
    person = {"@id": B + "#person"}
    codes = [l["code"] for l in LOCALES]
    terms = []
    for i in range(1, 6):
        terms.append({
            "@type": "DefinedTerm",
            "@id": B + "#term-" + ["aeo", "agentic-commerce", "product-digital-twin", "ai-financial-compliance", "ai-agent-security"][i - 1],
            "name": s["g%d_t" % i],
            "description": s["g%d_d" % i],
            "inDefinedTermSet": {"@id": B + "#glossary"},
        })
    term_refs = [{"@id": t["@id"]} for t in terms]

    website = {
        "@type": "WebSite", "@id": B + "#website", "url": B, "name": "Shengwei You",
        "inLanguage": codes, "publisher": person,
    }
    webpage = {
        "@type": "WebPage", "@id": page_url + "#webpage", "url": page_url,
        "name": s["cp_title"] if page == "cyberport" else s["meta_title"],
        "description": s["cp_desc"] if page == "cyberport" else s["meta_desc"],
        "inLanguage": loc["code"], "isPartOf": {"@id": B + "#website"},
        "about": person, "mainEntity": person,
        "primaryImageOfPage": {"@id": B + "#headshot"},
        "dateModified": C.UPDATED,
    }
    headshot = {
        "@type": "ImageObject", "@id": B + "#headshot",
        "url": B + "assets/photo.jpg", "contentUrl": B + "assets/photo.jpg",
        "width": 660, "height": 660, "caption": s["img_alt"],
    }
    person_node = {
        "@type": "Person", "@id": B + "#person",
        "name": "Shengwei You", "alternateName": ["游盛巍", "Jason You"],
        "jobTitle": s["job"], "description": s["meta_desc"],
        "url": B, "image": {"@id": B + "#headshot"}, "email": C.EMAIL,
        "homeLocation": {"@type": "Place", "name": "Hong Kong"},
        "knowsAbout": term_refs,
        "knowsLanguage": ["en", "zh-Hans"],
        "affiliation": [{"@type": "CollegeOrUniversity", "name": "University of Notre Dame", "url": "https://www.nd.edu/"}],
        "alumniOf": [
            {"@type": "CollegeOrUniversity", "name": "Purdue University", "url": "https://www.purdue.edu/"},
            {"@type": "CollegeOrUniversity", "name": "University of Washington", "url": "https://www.washington.edu/"},
        ],
        "sameAs": [C.LINKEDIN, C.GITHUB],
    }

    def offer(idn, name, desc_item):
        return {
            "@type": "Offer", "@id": B + "#offer-" + idn, "name": name,
            "itemOffered": {"@type": "Service", "name": name, "description": desc_item},
        }

    aeo = {
        "@type": "Service", "@id": B + "#service-aeo", "name": s["svc_aeo"],
        "serviceType": s["g1_t"], "description": s["d1_do"],
        "provider": person, "areaServed": "Worldwide",
        "audience": {"@type": "BusinessAudience", "audienceType": s["d1_tag"]},
        "url": page_url + "#doors", "hasOfferCatalog": {"@id": B + "#catalog-aeo"},
    }
    aeo_cat = {
        "@type": "OfferCatalog", "@id": B + "#catalog-aeo", "name": s["svc_aeo"],
        "itemListElement": [
            offer("aeo-data-pack", s["off1"], s["a2"]),
            offer("aeo-rfq-agent", s["off2"], s["a2"]),
            offer("lamp-sourcing", s["off3"], s["d1_do"]),
        ],
    }
    fin = {
        "@type": "Service", "@id": B + "#service-finprov", "name": s["svc_fin"],
        "serviceType": s["g4_t"], "description": s["d2_do"],
        "provider": person, "areaServed": "Worldwide",
        "audience": {"@type": "BusinessAudience", "audienceType": s["d2_tag"]},
        "url": page_url + "#doors", "hasOfferCatalog": {"@id": B + "#catalog-finprov"},
    }
    fin_cat = {
        "@type": "OfferCatalog", "@id": B + "#catalog-finprov", "name": s["svc_fin"],
        "itemListElement": [
            offer("finprov-waitlist", s["off4"], s["a3"]),
            offer("finprov-design-partner", s["off5"], s["d2_do"]),
        ],
    }
    props = [("material", "per-factory record"), ("rated power (W)", "per-factory record"),
             ("CE status", "per-factory record"), ("UL status", "per-factory record"),
             ("minimum order quantity", "per-factory record"), ("lead time", "per-factory record")]
    specimen = {
        "@type": "Product", "@id": B + "#product-specimen", "name": s["specimen_name"],
        "description": s["specimen_desc"], "category": "Lighting",
        "additionalProperty": [{"@type": "PropertyValue", "name": n, "value": v} for n, v in props],
    }
    faq = {
        "@type": "FAQPage", "@id": B + "#faq", "inLanguage": loc["code"],
        "mainEntity": [
            {"@type": "Question", "name": s["q%d" % i],
             "acceptedAnswer": {"@type": "Answer", "text": s["a%d" % i]}}
            for i in range(1, 6)
        ],
    }
    glossary = {
        "@type": "DefinedTermSet", "@id": B + "#glossary", "name": s["gloss_title"],
        "inLanguage": loc["code"], "hasDefinedTerm": terms,
    }

    papers = []
    for i, p in enumerate(C.PAPERS, 1):
        node = {
            "@type": "ScholarlyArticle", "@id": B + "#" + p["id"], "name": p["title"],
            "headline": p["title"], "description": s["p%d" % i], "inLanguage": "en",
            "author": person, "creativeWorkStatus": p["status"],
            "isPartOf": {"@type": "CreativeWork", "name": p["venue"]},
        }
        if p["status"] == "Published":
            node["datePublished"] = p["year"]
        if p["url"]:
            node["url"] = p["url"]
            node["sameAs"] = p["url"]
        papers.append(node)
    if page == "cyberport":
        person_node["knowsAbout"] = [x["name"] for x in terms]
        return [website, webpage, person_node, headshot, aeo, aeo_cat, fin, fin_cat]
    return [website, webpage, person_node, headshot, aeo, aeo_cat, fin, fin_cat, specimen] + papers + [faq, glossary]


def jsonld(loc, s, page="home"):
    g = {"@context": "https://schema.org", "@graph": nodes_for(loc, s, page)}
    return json.dumps(g, ensure_ascii=False, indent=2).replace("</", "<\\/")


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------
LAMP_SVG = """<svg viewBox="0 0 360 520" aria-hidden="true" focusable="false">
<defs>
<radialGradient id="lamp-glow" cx="50%" cy="52%" r="55%"><stop offset="0%" stop-color="#F7C46B" stop-opacity=".95"/><stop offset="55%" stop-color="#F2A33A" stop-opacity=".35"/><stop offset="100%" stop-color="#F2A33A" stop-opacity="0"/></radialGradient>
<linearGradient id="lamp-body" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FFF4DC" stop-opacity=".95"/><stop offset="100%" stop-color="#F2A33A" stop-opacity=".45"/></linearGradient>
</defs>
<circle class="halo" cx="180" cy="290" r="170"/>
<line class="cord" x1="180" y1="0" x2="180" y2="92" stroke-width="2"/>
<rect class="cap" x="154" y="92" width="52" height="22"/>
<polygon class="body" points="180,114 120,206 96,300 140,400 180,438 220,400 264,300 240,206"/>
<g class="facets"><path d="M180 114 L180 438"/><path d="M120 206 L240 206"/><path d="M96 300 L264 300"/><path d="M120 206 L180 300 L240 206"/><path d="M96 300 L180 438 L264 300"/><path d="M140 400 L180 300 L220 400"/><path d="M180 114 L120 206"/><path d="M180 114 L240 206"/></g>
<polygon class="drop" points="148,438 158,456 148,474 138,456"/><polygon class="drop" points="180,448 190,470 180,492 170,470"/><polygon class="drop" points="212,438 222,456 212,474 202,456"/>
<g class="nodes"><circle cx="120" cy="206" r="6"/><circle cx="240" cy="206" r="6"/><circle cx="96" cy="300" r="6"/><circle cx="264" cy="300" r="6"/><circle cx="180" cy="438" r="6"/></g>
</svg>"""


def head_common(loc, s, page, title, desc):
    here = loc["path"] + ("cyberport/" if page == "cyberport" else "")
    r = rel(here, "")
    r = "" if r == "./" else r
    url = B + here
    lines = []
    lines.append('<meta charset="utf-8">')
    lines.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    lines.append("<title>%s</title>" % e(title))
    lines.append('<meta name="description" content="%s">' % e(desc))
    lines.append('<meta name="robots" content="index,follow,max-image-preview:large">')
    lines.append('<meta name="theme-color" content="#F2EFE8">')
    lines.append('<link rel="canonical" href="%s">' % url)
    if page == "cyberport":
        alts = [(BYKEY[k]["code"], B + BYKEY[k]["path"] + "cyberport/") for k in C.CYBERPORT_LOCALES]
        for code, u in alts:
            lines.append('<link rel="alternate" hreflang="%s" href="%s">' % (code, u))
        lines.append('<link rel="alternate" hreflang="x-default" href="%scyberport/">' % B)
    else:
        for l in LOCALES:
            lines.append('<link rel="alternate" hreflang="%s" href="%s">' % (l["code"], B + l["path"]))
        lines.append('<link rel="alternate" hreflang="x-default" href="%s">' % B)
        lines.append('<link rel="alternate" type="text/markdown" href="%sindex.md" title="Markdown">' % (B + loc["path"]))
        lines.append('<link rel="alternate" type="text/plain" href="%sllms.txt" title="llms.txt">' % B)
    lines.append('<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">' % r)
    lines.append('<meta property="og:type" content="website">')
    lines.append('<meta property="og:site_name" content="Shengwei You">')
    lines.append('<meta property="og:title" content="%s">' % e(title))
    lines.append('<meta property="og:description" content="%s">' % e(desc))
    lines.append('<meta property="og:url" content="%s">' % url)
    lines.append('<meta property="og:image" content="%sassets/og.png">' % B)
    lines.append('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
    lines.append('<meta property="og:locale" content="%s">' % loc["og"])
    for l in LOCALES:
        if l["key"] != loc["key"]:
            lines.append('<meta property="og:locale:alternate" content="%s">' % l["og"])
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    lines.append('<meta name="twitter:title" content="%s">' % e(title))
    lines.append('<meta name="twitter:description" content="%s">' % e(desc))
    lines.append('<meta name="twitter:image" content="%sassets/og.png">' % B)
    lines.append('<link rel="preload" href="%sassets/fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>' % r)
    lines.append('<link rel="preload" href="%sassets/fonts/hanken-grotesk-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>' % r)
    lines.append('<link rel="stylesheet" href="%sassets/css/site.css?v=%s">' % (r, ASSET_VER))
    return "\n".join(lines), r, here


def header_html(loc, s, r, here, page):
    home = rel(here, loc["path"]) if page == "cyberport" else "./"
    if home == ".":
        home = "./"
    # language switcher
    items = []
    for l in LOCALES:
        if page == "cyberport":
            if l["key"] not in C.CYBERPORT_LOCALES:
                continue
            target = l["path"] + "cyberport/"
        else:
            target = l["path"]
        href = rel(here, target) if target else rel(here, "")
        if href in (".", ""):
            href = "./"
        cur = ' aria-current="true"' if l["key"] == loc["key"] else ""
        items.append('<li><a href="%s" hreflang="%s" lang="%s"%s>%s</a></li>' % (href, l["code"], l["lang"], cur, e(l["name"])))
    navlinks = ""
    if page == "home":
        navlinks = (
            '<a href="#doors">%s</a><a href="#proof">%s</a><a href="#twin">%s</a><a href="#faq">%s</a><a href="#contact">%s</a>'
            % (e(s["nav_doors"]), e(s["nav_proof"]), e(s["nav_twin"]), e(s["nav_faq"]), e(s["nav_contact"]))
        )
    else:
        navlinks = '<a href="%s">%s</a>' % (home, e(s["cp_back"]))
    return """<header class="top" data-ld="website" data-ld-type="WebSite">
<div class="wrap">
<a class="brand" href="%s"><span class="brand-mark" aria-hidden="true">SY</span><span translate="no">Shengwei You</span></a>
<nav class="nav" aria-label="Primary">%s
<details class="lang"><summary aria-label="%s">%s</summary><ul>%s</ul></details>
</nav>
</div>
</header>""" % (home, navlinks, e(s["lang_label"]), e(loc["name"]), "".join(items))


def cyberport_href(loc, here):
    k = loc["key"]
    tk = k if k in C.CYBERPORT_LOCALES else C.CYBERPORT_FALLBACK.get(k, "en")
    target = BYKEY[tk]["path"] + "cyberport/"
    return rel(here, target)


def home_page(loc):
    s = C.S[loc["key"]]
    head, r, here = head_common(loc, s, "home", s["meta_title"], s["meta_desc"])
    i18n = json.dumps({k: s[k] for k in ("xray_on", "xray_off", "twin_hello", "twin_offline", "twin_breach", "twin_wait", "twin_error")}, ensure_ascii=False)
    cp = cyberport_href(loc, here)

    specimen_rows = "".join(
        "<div><dt>%s</dt> <dd>per-factory record</dd></div>" % e(n)
        for n in ["material", "rated power (W)", "CE status", "UL status", "minimum order quantity", "lead time"]
    )

    doors = [
        ("lamps", 1, mailto(s["rfq_subject"], s["rfq_body"]), "service-aeo", "Service"),
        ("finance", 2, mailto(s["fin_subject"], s["fin_body"]), "service-finprov", "Service"),
        ("hiring", 3, mailto(s["cv_subject"], s["cv_body"]), None, None),
        ("cyberport", 4, cp, None, None),
    ]
    tabs_html, panels_html = [], []
    for idx, (slug, n, href, ld, ldt) in enumerate(doors):
        sel = "true" if idx == 0 else "false"
        tabs_html.append(
            '<button type="button" role="tab" class="pick-tab" id="tab-%s" aria-controls="panel-%s" aria-selected="%s" tabindex="%s" data-door="%s"><span class="pick-n" aria-hidden="true">%d</span><span>%s</span></button>'
            % (slug, slug, sel, "0" if idx == 0 else "-1", slug, n, e(s["d%d_tag" % n])))
        alt = ""
        if n == 1:
            alt = '<a class="alt" href="%s">%s</a>' % (e(mailto(s["factory_subject"], s["factory_body"])), e(s["d1_alt"]))
        ldattr = ' data-ld="%s" data-ld-type="%s"' % (ld, ldt) if ld else ""
        panels_html.append(
            """<article class="pick-panel" role="tabpanel" id="panel-%(slug)s" aria-labelledby="tab-%(slug)s" tabindex="0"%(ldattr)s>
<h3>%(title)s</h3>
<ol class="flow">
<li><span class="flow-k">%(k1)s</span><p>%(have)s</p></li>
<li><span class="flow-k">%(k2)s</span><p>%(do)s</p></li>
<li><span class="flow-k">%(k3)s</span><p>%(get)s</p></li>
</ol>
<div class="pick-cta"><a class="btn go" href="%(href)s">%(cta)s<span class="arrow" aria-hidden="true"></span></a>%(alt)s</div>
</article>""" % dict(slug=slug, ldattr=ldattr, title=e(s["d%d_title" % n]), k1=e(s["door_have"]), k2=e(s["door_do"]), k3=e(s["door_get"]),
                     have=e(s["d%d_have" % n]), do=e(s["d%d_do" % n]), get=e(s["d%d_get" % n]), href=e(href), cta=e(s["d%d_cta" % n]), alt=alt))
    tabs_html = "\n".join(tabs_html)
    panels_html = "\n".join(panels_html)

    papers_cards = []
    for i, p in enumerate(C.PAPERS, 1):
        link = ""
        if p["url"]:
            link = '<a class="paper-link" href="%s" rel="noopener">%s<span class="arrow" aria-hidden="true"></span></a>' % (e(p["url"]), e(s["papers_read"]))
        papers_cards.append(
            """<li class="paper" data-ld="%(id)s" data-ld-type="ScholarlyArticle">
<p class="paper-meta"><span class="paper-year">%(year)s</span><span>%(venue)s</span></p>
<p class="paper-plain">%(plain)s</p>
<p class="paper-title" translate="no" lang="en">%(title)s</p>
%(link)s
</li>""" % dict(id=p["id"], year=p["year"], venue=e(p["venue"]), plain=e(s["p%d" % i]), title=e(p["title"]), link=link))
    papers_html = "\n".join(papers_cards)

    body = """<a class="skip" href="#main">%(skip)s</a>
%(header)s
<main id="main" data-ld="webpage" data-ld-type="WebPage">

<section class="hero" id="top">
<div class="wrap">
<div class="hero-copy" data-ld="person" data-ld-type="Person">
<p class="eyebrow">%(hero_eyebrow)s</p>
<h1>%(hero_h1)s</h1>
<p class="hero-sub">%(hero_sub)s</p>
<div class="xray-row">
<button type="button" class="xray-btn" id="xray-toggle" role="switch" aria-checked="false" aria-controls="xray-panel"><span class="sw" aria-hidden="true"></span>%(xray_btn)s</button>
<p class="xray-note"><span id="xray-label">%(xray_off)s</span><br>%(xray_note)s</p>
</div>
<p class="hero-meta">%(hero_meta)s</p>
</div>
<div class="lamp">%(lamp)s</div>
</div>
</section>

<section id="doors" class="band"><div class="wrap pad stack">
<div class="sec-head"><p class="eyebrow">%(doors_eyebrow)s</p><h2>%(doors_title)s</h2><p class="lead door-lead">%(doors_lead)s</p></div>
<div class="picker" id="picker">
<div class="pick-tabs" role="tablist" aria-label="%(doors_pick)s">
%(tabs)s
</div>
<div class="pick-stage">
%(panels)s
</div>
</div>
<div class="specimen" data-ld="product-specimen" data-ld-type="Product">
<h3>%(specimen_name)s</h3>
<dl>%(specimen_rows)s</dl>
</div>
</div></section>

<section id="proof"><div class="wrap pad stack">
<div class="split"><h2>%(proof_title)s</h2><p class="lead">%(proof_lead)s</p></div>
<div class="nums">
<div class="num"><b>%(n1_val)s</b><span>%(n1_text)s</span></div>
<div class="num"><b>%(n2_val)s</b><span>%(n2_text)s</span></div>
<div class="num"><b>%(n3_val)s</b><span>%(n3_text)s</span></div>
</div>
<div id="papers" class="papers-head"><h3>%(papers_title)s</h3><p>%(papers_lead)s</p></div>
<ol class="papers">
%(papers)s
</ol>
<div class="stages"><h3>%(stages_title)s</h3><ul>%(stages)s</ul></div>
<ul class="facts"><li>%(proof_l1)s</li><li>%(proof_l2)s</li><li>%(proof_l3)s</li></ul>
</div></section>

<section id="twin" class="dark"><div class="wrap pad twin-grid">
<div class="twin-copy">
<p class="eyebrow">%(twin_eyebrow)s</p>
<h2>%(twin_title)s</h2>
<p class="lead">%(twin_lead)s</p>
</div>
<div class="twin" id="twin-app">
<div class="tw-modes" role="group" aria-label="%(twin_eyebrow)s">
<button type="button" data-mode="ask" aria-pressed="true">%(twin_ask)s</button>
<button type="button" data-mode="break" aria-pressed="false">%(twin_break)s</button>
</div>
<p class="tw-hint" id="tw-hint" hidden>%(twin_hint)s</p>
<div class="tw-log" id="tw-log" aria-live="polite"></div>
<form class="tw-form" id="tw-form" autocomplete="off">
<label for="tw-input" class="sr" style="position:absolute;inset-inline-start:-9999px">%(twin_placeholder)s</label>
<input id="tw-input" type="text" maxlength="500" placeholder="%(twin_placeholder)s">
<div id="tw-ts"></div>
<button type="submit" id="tw-send">%(twin_send)s</button>
</form>
</div>
</div></section>

<section id="faq" data-ld="faq" data-ld-type="FAQPage"><div class="wrap pad stack">
<div class="faq">
<h2 style="font-size:clamp(34px,4.6vw,56px);line-height:1.1">%(faq_title)s</h2>
<div class="qa">%(qa)s</div>
</div>
<div class="sec-head" data-ld="glossary" data-ld-type="DefinedTermSet">
<p class="eyebrow">%(gloss_title)s</p>
<dl class="terms">%(terms)s</dl>
</div>
</div></section>

</main>

<footer id="contact" class="contact band"><div class="wrap">
<div class="contact-row">
<h2>%(contact_title)s</h2>
<div class="person"><img class="portrait" src="%(r)sassets/img/portrait.jpg" width="176" height="220" alt="%(img_alt)s" loading="lazy" decoding="async">
<div class="links"><a href="mailto:%(email)s">%(email)s</a><a href="%(linkedin)s" rel="me noopener">LinkedIn</a><a href="%(github)s" rel="me noopener">GitHub</a></div></div>
</div>
<p class="human">%(human_line)s</p>
<p class="foot">&copy; 2026 <span translate="no">Shengwei You</span> &middot; Hong Kong. %(footer)s %(updated)s: <time datetime="%(updated_iso)s">%(updated_iso)s</time></p>
</div></footer>

<aside class="xp" id="xray-panel" hidden aria-label="%(xp_title)s">
<div class="xp-head"><div><strong>%(xp_title)s</strong> <span><span id="xp-count">0</span> nodes &middot; %(xp_hint)s</span></div>
<button type="button" class="xp-close" id="xp-close" aria-label="%(xp_close)s">&times;</button></div>
<div class="xp-body"><ul class="xp-list" id="xp-list"></ul><pre class="xp-json" id="xp-json" tabindex="0"></pre></div>
</aside>
""" % dict(
        skip=e(s["skip"]), header=header_html(loc, s, r, here, "home"),
        hero_eyebrow=e(s["hero_eyebrow"]), hero_h1=em(s["hero_h1"]), hero_sub=e(s["hero_sub"]),
        xray_btn=e(s["xray_btn"]), xray_off=e(s["xray_off"]), xray_note=e(s["xray_note"]), hero_meta=e(s["hero_meta"]),
        lamp=LAMP_SVG,
        doors_eyebrow=e(s["doors_eyebrow"]), doors_title=e(s["doors_title"]), doors_lead=e(s["doors_lead"]),
        doors_pick=e(s["doors_pick"]), tabs=tabs_html, panels=panels_html,
        specimen_name=e(s["specimen_name"]), specimen_rows=specimen_rows,
        papers_title=e(s["papers_title"]), papers_lead=e(s["papers_lead"]), papers=papers_html,
        stages_title=e(s["stages_title"]), stages="".join("<li>%s</li>" % e(s["st%d" % i]) for i in range(1, 6)),
        proof_title=e(s["proof_title"]), proof_lead=e(s["proof_lead"]),
        n1_val=e(s["n1_val"]), n1_text=e(s["n1_text"]), n2_val=e(s["n2_val"]), n2_text=e(s["n2_text"]),
        n3_val=e(s["n3_val"]), n3_text=e(s["n3_text"]),
        proof_l1=e(s["proof_l1"]), proof_l2=e(s["proof_l2"]), proof_l3=e(s["proof_l3"]),
        twin_eyebrow=e(s["twin_eyebrow"]), twin_title=e(s["twin_title"]), twin_lead=e(s["twin_lead"]),
        twin_ask=e(s["twin_ask"]), twin_break=e(s["twin_break"]), twin_hint=e(s["twin_hint"]),
        twin_placeholder=e(s["twin_placeholder"]), twin_send=e(s["twin_send"]),
        faq_title=e(s["faq_title"]),
        qa="".join('<div><h3>%s</h3><p>%s</p></div>' % (e(s["q%d" % i]), e(s["a%d" % i])) for i in range(1, 6)),
        gloss_title=e(s["gloss_title"]),
        terms="".join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(s["g%d_t" % i]), e(s["g%d_d" % i])) for i in range(1, 6)),
        contact_title=e(s["contact_title"]), r=r, img_alt=e(s["img_alt"]), email=C.EMAIL,
        linkedin=C.LINKEDIN, github=C.GITHUB, human_line=e(s["human_line"]), footer=e(s["footer"]),
        updated=e(s["updated"]), updated_iso=C.UPDATED,
        xp_title=e(s["xp_title"]), xp_hint=e(s["xp_hint"]), xp_close=e(s["xp_close"]),
    )

    script = '<script id="site-js" src="%sassets/js/site.js?v=%s" defer data-i18n=\'%s\' data-twin-endpoint="%s" data-turnstile="%s" data-mail="%s"></script>' % (
        r, ASSET_VER, i18n.replace("'", "&#39;"), e(TWIN_ENDPOINT), e(TURNSTILE_SITEKEY), C.EMAIL)
    return """<!doctype html>
<html lang="%s" dir="%s" data-locale="%s">
<head>
%s
<script type="application/ld+json" id="graph">
%s
</script>
</head>
<body>
%s
%s
</body>
</html>
""" % (loc["lang"], loc["dir"], loc["key"], head, jsonld(loc, s), body, script)


def cyberport_page(loc):
    s = C.S[loc["key"]]
    head, r, here = head_common(loc, s, "cyberport", s["cp_title"], s["cp_desc"])
    mail = mailto("Cyberport", "")
    body = """<a class="skip" href="#main">%(skip)s</a>
%(header)s
<main id="main" class="onepager" data-ld="webpage" data-ld-type="WebPage"><div class="wrap pad stack">
<div class="sec-head"><p class="eyebrow">Cyberport &middot; <span translate="no">Shengwei You</span></p><h1>%(cp_h1)s</h1></div>
<div>
<section><h2>%(cp_s1_t)s</h2><p>%(cp_s1)s</p></section>
<section data-ld="service-aeo" data-ld-type="Service"><h2>%(cp_s2_t)s</h2><div><p>%(cp_s2a)s</p><p style="margin-top:12px" data-ld="service-finprov" data-ld-type="Service">%(cp_s2b)s</p></div></section>
<section data-ld="person" data-ld-type="Person"><h2>%(cp_s3_t)s</h2><ul><li>%(cp_b1)s</li><li>%(cp_b2)s</li><li>%(cp_b3)s</li><li>%(cp_b4)s</li></ul></section>
<section><h2>%(cp_s4_t)s</h2><p>%(cp_s4)s</p></section>
<section><h2>%(cp_s5_t)s</h2><p>%(cp_s5)s</p></section>
</div>
<p><a class="btn" style="margin-top:0" href="%(mail)s">%(cp_cta)s: %(email)s</a></p>
<p class="foot">&copy; 2026 <span translate="no">Shengwei You</span> &middot; Hong Kong. %(footer)s %(updated)s: <time datetime="%(updated_iso)s">%(updated_iso)s</time></p>
</div></main>
<aside class="xp" id="xray-panel" hidden></aside>
""" % dict(
        skip=e(s["skip"]), header=header_html(loc, s, r, here, "cyberport"),
        cp_h1=e(s["cp_h1"]), cp_s1_t=e(s["cp_s1_t"]), cp_s1=e(s["cp_s1"]), cp_s2_t=e(s["cp_s2_t"]),
        cp_s2a=e(s["cp_s2a"]), cp_s2b=e(s["cp_s2b"]), cp_s3_t=e(s["cp_s3_t"]),
        cp_b1=e(s["cp_b1"]), cp_b2=e(s["cp_b2"]), cp_b3=e(s["cp_b3"]), cp_b4=e(s["cp_b4"]),
        cp_s4_t=e(s["cp_s4_t"]), cp_s4=e(s["cp_s4"]), cp_s5_t=e(s["cp_s5_t"]), cp_s5=e(s["cp_s5"]),
        cp_cta=e(s["cp_cta"]), mail=e(mail), email=C.EMAIL, footer=e(s["footer"]),
        updated=e(s["updated"]), updated_iso=C.UPDATED,
    )
    return """<!doctype html>
<html lang="%s" dir="%s" data-locale="%s">
<head>
%s
<script type="application/ld+json" id="graph">
%s
</script>
</head>
<body>
%s
</body>
</html>
""" % (loc["lang"], loc["dir"], loc["key"], head, jsonld(loc, s, "cyberport"), body)


# --------------------------------------------------------------------------
# Markdown twin, llms.txt, sitemap, robots, 404, redirect stubs
# --------------------------------------------------------------------------
def markdown_twin(loc):
    s = C.S[loc["key"]]
    L = []
    L.append("# Shengwei You")
    L.append("")
    L.append("> %s" % s["meta_desc"])
    L.append("")
    L.append("%s · %s" % (plain(s["hero_eyebrow"]), plain(s["hero_h1"])))
    L.append("")
    L.append(s["hero_sub"])
    L.append("")
    L.append("Canonical: %s" % (B + loc["path"]))
    L.append("Language: %s · %s: %s" % (loc["code"], s["updated"], C.UPDATED))
    L.append("")
    L.append("## %s" % s["doors_title"])
    L.append("")
    L.append(s["doors_lead"])
    L.append("")
    for n, key, subj in ((1, "rfq", None), (2, "fin", None), (3, "cv", None), (4, None, None)):
        L.append("### %s (%s)" % (s["d%d_title" % n], s["d%d_tag" % n]))
        L.append("")
        L.append("- %s: %s" % (s["door_have"], s["d%d_have" % n]))
        L.append("- %s: %s" % (s["door_do"], s["d%d_do" % n]))
        L.append("- %s: %s" % (s["door_get"], s["d%d_get" % n]))
        L.append("")
        if key:
            L.append("- %s: %s" % (s["d%d_cta" % n], mailto(s[key + "_subject"], s[key + "_body"])))
        else:
            tk = loc["key"] if loc["key"] in C.CYBERPORT_LOCALES else C.CYBERPORT_FALLBACK.get(loc["key"], "en")
            L.append("- %s: %s" % (s["d4_cta"], B + BYKEY[tk]["path"] + "cyberport/"))
        if n == 1:
            L.append("- %s: %s" % (s["d1_alt"], mailto(s["factory_subject"], s["factory_body"])))
        L.append("")
    L.append("## %s" % plain(s["proof_title"]))
    L.append("")
    L.append(s["proof_lead"])
    L.append("")
    for n in (1, 2, 3):
        L.append("- %s %s" % (s["n%d_val" % n], s["n%d_text" % n]))
    for n in (1, 2, 3):
        L.append("- %s" % s["proof_l%d" % n])
    L.append("")
    L.append("### %s" % s["papers_title"])
    L.append("")
    for i, p in enumerate(C.PAPERS, 1):
        L.append("- %s, %s. %s %s%s" % (p["year"], p["venue"], s["p%d" % i], p["title"], (" " + p["url"]) if p["url"] else ""))
    L.append("")
    L.append("### %s" % s["stages_title"])
    L.append("")
    for i in range(1, 6):
        L.append("- %s" % s["st%d" % i])
    L.append("")
    L.append("## FAQ")
    L.append("")
    for i in range(1, 6):
        L.append("### %s" % s["q%d" % i])
        L.append("")
        L.append(s["a%d" % i])
        L.append("")
    L.append("## %s" % s["gloss_title"])
    L.append("")
    for i in range(1, 6):
        L.append("- **%s**: %s" % (s["g%d_t" % i], s["g%d_d" % i]))
    L.append("")
    L.append("## %s" % s["contact_title"])
    L.append("")
    L.append("- Email: %s" % C.EMAIL)
    L.append("- LinkedIn: %s" % C.LINKEDIN)
    L.append("- GitHub: %s" % C.GITHUB)
    L.append("")
    L.append(s["human_line"])
    L.append("")
    L.append("Machine-readable data: the HTML page embeds one schema.org JSON-LD @graph (script id=\"graph\") with stable @id URLs under %s#." % B)
    L.append("")
    return "\n".join(L)


def llms_txt():
    en = C.S["en"]
    L = []
    L.append("# Shengwei You")
    L.append("")
    L.append("> %s" % en["meta_desc"])
    L.append("")
    L.append("Facts an assistant may rely on: two live offers only (AEO for crystal and marble lamps, FinProv for AI financial compliance). No prices are published; quotes are by RFQ by email. No testimonials are published. The product record on the page is a labelled format specimen, not a product for sale. Ph.D. candidate, not yet Dr. Updated %s." % C.UPDATED)
    L.append("")
    L.append("## Pages (one crawlable URL per language, Markdown twin of each)")
    L.append("")
    for l in LOCALES:
        L.append("- [%s](%sindex.md): %s" % (l["name"], B + l["path"], l["code"]))
    L.append("")
    L.append("## Offers")
    L.append("")
    L.append("- [AEO for crystal and marble lamps](%sindex.md): %s" % (B, en["d1_do"]))
    L.append("- [FinProv: AI financial compliance](%sindex.md): %s" % (B, en["d2_do"]))
    L.append("")
    L.append("## Optional")
    L.append("")
    L.append("- [Cyberport one-pager](%scyberport/): %s" % (B, en["cp_desc"]))
    L.append("- [Papers in plain words](%s#papers): six accepted peer-reviewed papers, each with a DOI or arXiv link where one exists" % B)
    L.append("- [Structured data](%s): every HTML page embeds a schema.org JSON-LD @graph with stable @id URLs" % B)
    L.append("- Contact: %s" % C.EMAIL)
    L.append("")
    return "\n".join(L)


def sitemap():
    X = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for l in LOCALES:
        X.append("<url><loc>%s</loc><lastmod>%s</lastmod>" % (B + l["path"], C.UPDATED))
        for a in LOCALES:
            X.append('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (a["code"], B + a["path"]))
        X.append('<xhtml:link rel="alternate" hreflang="x-default" href="%s"/></url>' % B)
    for k in C.CYBERPORT_LOCALES:
        l = BYKEY[k]
        X.append("<url><loc>%s</loc><lastmod>%s</lastmod>" % (B + l["path"] + "cyberport/", C.UPDATED))
        for a in C.CYBERPORT_LOCALES:
            X.append('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (BYKEY[a]["code"], B + BYKEY[a]["path"] + "cyberport/"))
        X.append('<xhtml:link rel="alternate" hreflang="x-default" href="%scyberport/"/></url>' % B)
    X.append("</urlset>")
    return "\n".join(X) + "\n"


def robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n# llms.txt: %sllms.txt\n" % (B, B)


def not_found():
    s = C.S["en"]
    links = "".join('<li><a href="%s" lang="%s" hreflang="%s">%s</a></li>' % (l["path"] or "./", l["lang"], l["code"], e(l["name"])) for l in LOCALES)
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found | Shengwei You</title><meta name="robots" content="noindex">
<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="%sassets/css/site.css?v=%s"></head>
<body><main class="wrap pad stack"><h1 style="font-size:clamp(40px,6vw,72px)">Page not found.</h1>
<p class="lead">Try a language home page instead.</p><ul class="facts">%s</ul></main></body></html>
""" % (B, B, ASSET_VER, links)


def redirect_stub(target_path, frag=""):
    url = B + target_path
    go = url + frag
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Redirecting</title>
<meta name="robots" content="noindex,follow"><link rel="canonical" href="%s">
<meta http-equiv="refresh" content="0; url=%s"></head>
<body><p><a href="%s">%s</a></p></body></html>
""" % (url, go, go, go)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path, len(text.encode("utf-8")), "bytes")


def main():
    check_keys()
    for l in LOCALES:
        write(l["path"] + "index.html", home_page(l))
        write(l["path"] + "index.md", markdown_twin(l))
    for k in C.CYBERPORT_LOCALES:
        l = BYKEY[k]
        write(l["path"] + "cyberport/index.html", cyberport_page(l))
    write("llms.txt", llms_txt())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
    write("404.html", not_found())
    write("index.zh-CN.html", redirect_stub("zh-hans/"))
    write("index.zh-TW.html", redirect_stub("zh-hk/"))
    # Retired pages: the old research and projects pages showed work that is not published and
    # roles from the previous positioning. Their URLs now point to the matching home page.
    for name, frag in (("research", "#papers"), ("projects", "#doors")):
        write(name + "/index.html", redirect_stub("", frag))
        write(name + "/index.zh-CN.html", redirect_stub("zh-hans/", frag))
        write(name + "/index.zh-TW.html", redirect_stub("zh-hk/", frag))


if __name__ == "__main__":
    main()
