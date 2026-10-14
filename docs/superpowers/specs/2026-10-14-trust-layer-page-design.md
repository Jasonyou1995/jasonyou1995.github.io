# Trust Layer Page: Design Spec (v2)

Date: 2026-10-14. Owner: Shengwei You. Supersedes the 2026-06-08 recruiter-first spec.

## The one sentence

One page, one promise: he makes Chinese manufacturers and financial firms trustworthy and readable to AI agents, proven by two live offers (AEO for crystal and marble lamps, FinProv for AI financial compliance) and anchored by an AI agent security Ph.D. It speaks to four readers in eight locales as separate crawlable pages, wrapped in schema.org JSON-LD with stable IDs so an agent in 2036 can still parse it.

## Binary exit (done means all true)

- Live in 8 locales (en-US, zh-Hans, zh-HK, ar, ja, ru, fr, es). The "9" in the brief counted Chinese twice.
- 0 errors in the Schema Markup Validator on the live URL.
- Loads under 3 seconds from Shenzhen (GitHub Pages is spotty there: plan the Hong Kong static mirror).
- At least 1 booked call from a target reader within 30 days.
- 90-day stretch: ChatGPT, Perplexity or Claude cite the page for "who does AEO for lighting factories in Foshan".

## Decisions made in auto mode (change freely)

- Brand name: the person leads ("Shengwei You"). BridgeOS stays an internal name until the company is registered.
- Visual system: "Marble and Light". Human view: warm marble ground #F2EFE8, ink #17140F, lamp amber accent. Agent view: near-black with amber and teal glow. Type: Instrument Serif display, Hanken Grotesk body, JetBrains Mono for machine text, all self-hosted (Google Fonts is blocked in mainland China). CJK and Arabic use system stacks.
- Offers show no prices. Quotes are by RFQ only. The 14-day deployment is the only commercial fact shown.
- Honest language claim: fluent English and Mandarin, learning Cantonese, Spanish and Japanese.
- Proof numbers (5,866,037 TLA+ states with 0 violations, 100/100 adaptive attack episodes, 4 peer-reviewed papers) come from the owner's published work and the previous page. Crypto context is left out.
- The sample lamp is a labelled format specimen with placeholder values, never real specs.

## Minimal loop (progress bar)

| # | Quest | Binary exit | Status |
|---|---|---|---|
| 1 | Four-door copy in English | Each door fits one phone screen, one call to action | done |
| 2 | Static page and JSON-LD | Validator shows 0 errors | built, run validator live |
| 3 | 8 locale URLs with hreflang | All 8 live; native review of ar and zh-HK | built, review pending |
| 4 | Agent X-ray toggle | A non-technical friend explains AEO back after 10 seconds | built, test with a friend |
| 5 | Twin proxy and guardrails | 50 jailbreak attempts: 0 key leaks, 0 off-script promises | code ready in twin/, deploy pending |
| 6 | HyperFrames video and China mirrors | Plays from a Shenzhen phone | not started |
| 7 | Cursor light shader, n8n voice agent | You actually want it | later, optional |

## Rest protocol

Three focused sessions a week, one quest per session. Every quest can be redone in under an hour. Do-overs are allowed.
