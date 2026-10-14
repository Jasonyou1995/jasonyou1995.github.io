# AGENTS.md — single reference for jasonyou1995.github.io

Read this first. Every next AI agent that touches this repo starts here.

## What this site is

A static GitHub Pages personal site for Shengwei You (游盛巍 / Jason You).
Positioning: AI Deployment Engineer / Forward Deployed Engineer. PhD candidate in Hong Kong.
Goal: recruiter-first, scannable in 20 seconds, every claim verifiable.

Audience priority:
1. Recruiters and HR screening for FDE / AI Deployment roles (primary)
2. CEOs, CxOs, hiring managers (secondary)
3. People who would engage directly: consulting, AI x crypto, DevRel, course, community (tertiary)

## Hard platform rule

This is GitHub Pages. Everything served at jasonyou1995.github.io comes from this repo at build time.

- HTML, CSS, JS only at the public surface.
- No runtime Python, no Node build step, no API calls.
- Inline CSS and JS are allowed (current pattern). External `assets/`, `css/`, `js/` folders are reserved for the next redesign.
- Every file in this repo is potentially public. Treat it as such.

## 10 percent rule

Show 10 percent of the key information publicly. Hide or omit the rest.

- Visible: name, headline, 4 shipped systems with verifiable numbers, contact, linkedin, github, alumni schools, languages.
- Hidden: home address, phone, GPA, partial grades, personal context beyond what serves the recruiter pitch, anything that does not defend a claim.
- When in doubt: leave it out. The user can always add, never silently include private context.

## Folder layout

```
jasonyou1995.github.io/
├── index.html              EN canonical home
├── index.zh-CN.html        简体中文 home
├── index.zh-TW.html        繁體中文 home
├── projects/
│   ├── index.html          EN
│   ├── index.zh-CN.html
│   └── index.zh-TW.html
├── research/
│   ├── index.html          EN
│   ├── index.zh-CN.html
│   └── index.zh-TW.html
├── assets/                 favicon.svg, photo.jpg, future design assets
├── docs/                   design plans, specs, source-of-truth data
│   ├── research.bib        BibTeX source for research page (public)
│   └── superpowers/
│       ├── plans/          dated implementation plans
│       └── specs/          dated design specs
├── tools/                  local-only translation toolchain (gitignored)
└── CLAUDE.md               this file
```

## Allowed and forbidden

Allowed:
- Edit, simplify, or rewrite any HTML, CSS, JS.
- Add or update `assets/`.
- Add new design plans under `docs/superpowers/plans/` and specs under `docs/superpowers/specs/`.
- Update `docs/research.bib` to keep publications current.

Forbidden:
- Add server-side code, build tools, or runtime dependencies that GitHub Pages cannot serve.
- Commit private information: phone, address, GPA, partial grades, family context, employer-specific complaints.
- Add new top-level folders without updating this file.
- Use em-dash, en-dash, or three-dash dividers in any copy.
- Use these words in copy: "leverage", "robust", "navigate", "delve".
- Use "—" in Chinese files. Chinese punctuation only: ，。、.

## Style rules (apply to every commit)

- Human notation. No dashes, no AI fluff, scannable in 20 seconds.
- One-sentence story lead per section, then bullet evidence.
- Recruiter framing: outcomes and verifiable numbers, not adjectives.
- Three locales must stay in lockstep content. When EN changes, mirror to zh-CN and zh-TW.
- Ranges: "2024 to Present", never "2024-Present".

## Business focus (apply to all future design updates)

- Primary: AI Deployment Engineer / Forward Deployed Engineer.
- Secondary: AI x crypto intersection (4 shipped research systems anchor this).
- Tertiary: DevRel, course, consulting, community.
- Do not add focus areas the user has not shipped work for.

## GitHub Pages constraints for the next design

- The repo root is the site root. No base URL prefix.
- Canonical URL: `https://jasonyou1995.github.io/`.
- `index.html` is the EN default (`hreflang="x-default"`).
- All asset paths must work without a server (relative paths or absolute `https://jasonyou1995.github.io/...`).
- Three locales, three hreflang declarations per page, visible language switch in nav.
- SEO: per-page `<title>`, `<meta description>`, OG tags, Twitter card, JSON-LD Person schema on home.
- Accessibility: focus-visible outlines, alt text on the headshot, lang attributes on each locale, color contrast that meets WCAG AA on the dark theme.

## Update protocol for the next design

1. Read this file end to end.
2. Read `docs/superpowers/specs/` for the most recent design spec.
3. Edit EN canonical first. Mirror to zh-CN and zh-TW.
4. Run `git status` before commit. Only public-tracked files should appear.
5. Commit with a message that names the page and the change.

## Source of truth files

- Audience and positioning: this file, section "What this site is".
- Visual system and copy rules: most recent file in `docs/superpowers/specs/`.
- Publications: `docs/research.bib`.
- Personal context and bio: `/Users/mac14/.claude/projects/.../memory/MEMORY.md` (Jason's auto memory, private).

## References

1. `/Users/mac14/.claude/CLAUDE.md` — global orchestration rules for all projects
2. `/Users/mac14/CLAUDE.md` — Master Agent Rules for the Jason host
3. `docs/superpowers/specs/2026-06-08-personal-page-redesign-design.md` — most recent design spec
4. `docs/research.bib` — research publications source
5. `.gitignore` — public vs private file boundary