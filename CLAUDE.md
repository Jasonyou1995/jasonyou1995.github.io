# AGENTS.md: single reference for jasonyou1995.github.io

Read this first. Every next AI agent that touches this repo starts here.
Updated 2026-10-14 for the Trust Layer redesign (v2). The June 2026 FDE recruiter spec is superseded.

## What this site is

A static GitHub Pages brand page for Shengwei You (游盛巍 / Jason You), Ph.D. candidate in AI agent security, Hong Kong and Shenzhen.
One promise: he makes Chinese manufacturers and financial firms trustworthy and readable to AI agents.
Two live offers only: AEO for crystal and marble lamps, and FinProv (AI financial compliance).

Four readers, one door each, one call to action each:
1. Lamp buyers: "I source lamps" leads to an RFQ by email. Factory owners get a 14-day AEO deployment link.
2. Finance teams: "I need AI compliance" leads to the FinProv waitlist by email.
3. Hiring managers: "I'm hiring" leads to a CV request by email.
4. Cyberport admins: "One page for the panel" leads to /cyberport/ (EN and zh-HK).

Signature interaction: the Agent X-ray switch (the page flips to what an agent reads, built live from the page's own JSON-LD) and a guarded digital twin that visitors can try to jailbreak.

## Hard platform rule

GitHub Pages serves this repo as plain files. HTML, CSS, JS only at the public surface. No runtime Python, no Node build step on Pages, no API calls from the browser except to the twin proxy.
Generation is local: `python3 docs/build/build.py` writes every HTML page, Markdown twin, llms.txt, sitemap and robots. Commit the output.
Every file in this repo is potentially public. Treat it as such.

## Source of truth

- All copy, all 8 locales, offers, FAQ, glossary: `docs/build/content.py`. Never hand edit a generated page.
- Layout and JSON-LD: `docs/build/build.py`. Styles: `assets/css/site.css`. Script: `assets/js/site.js`.
- Checks: `python3 docs/build/verify.py` (JSON-LD graph, hreflang, dashes, banned words, links, contrast, JS budget).
- Facts the twin may say: `twin/facts.md`. Twin proxy code: `twin/` (Cloudflare Worker, see twin/README.md).
- Design canvas (visual source): the Claude Design artifact "Shengwei You: Trust Layer Page".
- Publications: `docs/research.bib`. Design spec: `docs/superpowers/specs/2026-10-14-trust-layer-page-design.md`.

## Locales

8 crawlable URLs, one folder each, linked by hreflang, no JavaScript language toggle:
`/` (en-US, x-default), `/zh-hans/`, `/zh-hk/`, `/ar/` (RTL), `/ja/`, `/ru/`, `/fr/`, `/es/`.
Old `index.zh-CN.html` and `index.zh-TW.html` are redirect stubs. Arabic and zh-HK copy need a native speaker review.
All locales must keep the same keys. build.py refuses to run otherwise.

## Keep off the page (hard rules)

- The Intent Solver, FleetOS, BridgeOS internals and crypto positioning. They confuse the buyers above.
- Dubai buyer names or any buyer names. Testimonials unless a written one exists.
- The title "Dr." until the defense. Use "Ph.D. candidate".
- Home address, phone, GPA, grades, visa details, family context, budgets, prices (quotes are by RFQ only).
- The product record in the page is a labelled format specimen. Never publish invented specs, CE or UL claims.

## 10 percent rule

Show 10 percent of the key information publicly. Visible: name, headline, the two offers, three verifiable proof numbers, contact, LinkedIn, GitHub, schools, languages, one human line.
When in doubt, leave it out. The user can always add, never silently include private context.

## Style rules

- Human notation. No em dash, en dash or three-dash dividers in any copy. Chinese files use ，。、 only.
- Banned words in copy: leverage, robust, navigate, delve.
- One-sentence lead per section, then evidence. Outcomes and verifiable numbers, not adjectives.
- Ranges: "2024 to Present", never "2024-Present".
- Every proof number must trace to something the owner can defend. Do not add a number without a source.

## 10-year insurance for agents

- Stable `@id` URLs under `https://jasonyou1995.github.io/#...`. Never rename an @id.
- Core schema.org types only (stable since 2011): WebSite, WebPage, Person, Service, OfferCatalog, Offer, Product, FAQPage, DefinedTermSet.
- `llms.txt` at the root and a plain Markdown twin (`index.md`) beside every home page.
- Add `ProfessionalService` once the Hong Kong company is registered. Add `VideoObject` once the HyperFrames video is rendered and hosted. Add ORCID to `sameAs` once the owner supplies it.
- Moving off the github.io domain: change `BASE` in `docs/build/content.py`, rebuild, add a CNAME, keep 301s impossible on Pages so keep old pages as canonical-pointing stubs.

## Allowed and forbidden

Allowed: edit content.py, build.py, CSS, JS; add locales through content.py; update facts.md and research.bib.
Forbidden: server-side code on Pages; committing keys or `.env` (a gitleaks hook is provided in `.githooks`); adding focus areas the owner has not shipped; adding top-level folders without updating this file.

## Update protocol

1. Read this file, then `docs/superpowers/specs/2026-10-14-trust-layer-page-design.md`.
2. Edit `content.py` (EN first, mirror all 8), rebuild, run `verify.py`.
3. Run `git status`. Only public-tracked files should appear.
4. Commit with a message that names the page and the change.
5. After deploy: run https://validator.schema.org on the live URL and time the load from Shenzhen.

## Weekly 5 minutes

Update `twin/facts.md` if anything changed, glance at twin counters, rerun `verify.py`, rerun the Schema Markup Validator.
