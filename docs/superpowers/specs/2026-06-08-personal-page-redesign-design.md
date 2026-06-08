# Personal Page Redesign: Design Spec

Date: 2026-06-08
Repo: jasonyou1995.github.io
Owner: Shengwei You (游盛巍 / Jason)

## Goal

Evolve the existing single static page into the best possible recruiter-first personal page: faster, more credible, and built around the four shipped research systems and their verifiable numbers. Keep the strong existing design language. No backend, no new dependencies, deploys on GitHub Pages exactly as today.

## Audience (write to all of these, in this priority order)

1. Top-firm recruiters and HR screening for AI Deployment Engineer / FDE roles. Primary.
2. Top-firm CEOs, CxOs, and hiring managers who skim for outcomes and credibility.
3. People who would engage him directly: consulting on FDE work, AI x crypto, solutions, the course, DevRel, and community building.

Copy is outcome-led and credible on a 20 second skim. Every claim is verifiable. He must be able to defend every number when challenged.

## Decisions locked (from brainstorming)

- Scope: one fast static page. No Cloudflare Worker, no live AI demo, no backend.
- Positioning: recruiters first (AI Deployment / FDE), with AI x Crypto and DevRel / course visible but secondary.
- Visual system: keep it. Warm near-black background, orange and gold accents, Fraunces plus Spline Sans, grain wash, floating cards, scroll fade-ins.
- Contact: shengwei.you@gmail.com and linkedin.com/in/shengwei-you/ and github.com/Jasonyou1995. These match the live site and stay.
- Languages: keep all three (EN canonical, 简体中文, 繁體中文) as separate static files with hreflang.
- Style: human notation only. No em-dashes, no en-dash separators, no three-dash dividers. No "leverage / robust / navigate / delve". Short, scannable.

## Architecture

Three static HTML files, self-contained (inline CSS and a small inline script), no build step:

```
index.html          EN, canonical
index.zh-CN.html    Simplified Chinese
index.zh-TW.html    Traditional Chinese
photo.png           optimized headshot (replaces the 24MB original)
favicon.svg         generated initials mark
docs/superpowers/specs/   this spec
```

Each file links to the other two with `rel="alternate" hreflang="..."` and a visible EN / 简 / 繁 switch in the nav. The EN file carries `hreflang="x-default"`.

## Page structure (top to bottom)

### 1. Nav (fixed)
Name logo. Anchors: Work, Numbers, Research, Experience, Contact. Language switch EN / 简 / 繁.

### 2. Hero
- Name: Shengwei You · 游盛巍 (Jason). The name block is `notranslate`.
- Headline (recruiter and builder framing, replaces the consulting headline): "I build, I measure, I ship: AI agents that take real actions, verified."
- Sub line: PhD candidate (Hong Kong) · AI Deployment Engineer / FDE · Trilingual EN / 普通话 / 粤语 · 4 shipped research systems.
- Lead paragraph: he builds the full reliability layer around frontier model calls (multi-provider orchestration, retrieval grounding, on-chain execution, provable safety gating) and verifies every claim with seeds, logs, and receipts.
- CTAs: "See the work" (scrolls to Numbers / Work). "Get in touch" (scrolls to Contact).
- Optimized headshot with two floating cards: Focus = Agent safety and deployment. Open to = FDE and AI roles.

### 3. Numbers strip (NEW)
A single row of four large numbers that count up on scroll. Each links to its project card. Each carries a short, honest source label directly under it so the number is self-defending.

| Number | Label under it | Defense line (what he says when challenged) |
|---|---|---|
| 18,400+ | lines of production Python, shipped solo | "One flagship system, built end to end alone, with 14 test suites and one-command reproducibility. The line count is scope delivered, the tests are the quality." |
| 5.8M | TLA+ states model-checked, 0 violations | "Exact figure 5,866,037 from the TLC model check of the safety state machine. The kill-circuit provably cannot enter an unsafe state. Reproducible from the spec." |
| 62% | peak peg deviation cut, IEEE ICBC 2026 | "Peer-reviewed and presented. Measured across 1,200 reproducible simulations against the industry-standard baseline, seed and commit captured per run." |
| 21x | cheaper oracle vs committee baseline | "About 0.04 USD per update on L2 versus incumbent committee oracles. 76 passing tests including fuzz, 100% Byzantine detection to a 37.5% adversary fraction." |

Defensibility is a hard requirement. No number appears without a source label, and the matching project card repeats the verifiable detail.

### 4. How I engineer (reframed from "What I do")
Four cards, reframed away from consulting-sales toward how he builds. Each is one short paragraph.
- Reliability layer around frontier models: multi-provider orchestration (OpenAI, Anthropic, local) with automatic failover, content-hashed caching, and per-call cost, latency, and token telemetry.
- Formal verification: safety state machines specified and model-checked in TLA+, so safety is proven, not hoped.
- Adversarial red-teaming: a Q-learning adversary used to attack his own systems, with failure modes documented honestly.
- Reproducibility: every reported number traces to a seed, an LLM trace, and a result file. One command reruns everything. "I document the limits of my own evidence."

One slim line keeps the delivery path visible: available for AI deployment delivery work (Lion Protocol), scope to live system in about 90 days.

### 5. The 4 projects (NEW, the core upgrade)
A 2x2 grid on desktop, stacked on mobile. Each card: project name, one-line subtitle, three bullets (what was built, what was measured, what is verifiable), and a link to the repo or "view the artifact".

1. OC1: Autonomous LLM Agent Safety Control System.
   - Built: multi-provider LLM orchestration with auto-failover; a TLA+ safety state machine; prompt-injection detection; an EVM execution layer; a RAG policy oracle. Solo: 18,400+ lines of Python, 7 Solidity contracts, 14 test suites, 13 reproducible experiments.
   - Measured: P95 about 3.9s with sub-5ms safety gating; 5,866,037 TLA+ states, 0 violations; prompt-injection F1 0.765 at 5% false-positive rate; survived 100/100 adaptive RL attack episodes; EVM cross-validated to under 5% error, about 80,963 gas per swap; RAG citation precision 92.9%, recall 88%.
   - Verifiable: one-command pipeline, seed-controlled, claim-to-artifact traceability.

2. OC2: On-Chain Multi-Agent LLM Debate.
   - Built: a 3-role debate (Proposer, Challenger, Judge) that vets DeFi actions before execution, committed on-chain via 4 Foundry-tested Solidity contracts with ECDSA verification and transcript hashing.
   - Measured: 90.2% verdict accuracy [87.6, 92.8], 95% expert agreement on real on-chain actions, 16.8s end to end, 8.7% cheaper gas than the Optimism fault-proof baseline (1.95M vs 2.13M gas), 76 Foundry tests.
   - Verifiable: public contracts and tests.

3. MVF-Composer: Multi-Agent Stablecoin Reserve Controller. Accepted and presented at IEEE ICBC 2026.
   - Built: 12 concurrent LLM agents across 4 archetypes over OpenAI, Anthropic, and DeepSeek, with Pydantic-validated outputs and a constrained mean-variance optimizer. About 12,500 lines of typed Python, 46 modules.
   - Measured: across 1,200 reproducible simulations, 62% peak peg deviation reduction and 3.1x faster crisis recovery versus the industry baseline.
   - Verifiable: peer-reviewed, seed, commit, and timestamp per run.

4. NOC: Cryptographically Verifiable Blockchain Oracle.
   - Built: a Solidity 0.8.23 oracle with on-chain Groth16 and BN254 verification, plus staking, slashing, and reputation-weighted consensus.
   - Measured: about 0.04 USD per update on L2 (about 21x cheaper than incumbent committee oracles), 100% Byzantine detection up to a 37.5% adversary fraction, 76 passing tests (unit, adversarial, 100-epoch scenario, 256-run fuzz, gas benchmarks).
   - Verifiable: public test suite.

Links: each project card reads "Code available on request". No public repo links on the cards, per owner decision (double-blind anonymization rules).

### 6. Research and publications
Dissertation theme paragraph (trust and systemic risk in decentralized systems, multi-agent architectures for calibrated safety-aware automation), then the four peer-reviewed papers, each linking to its public DOI only:
- 2026, book chapter, Hybrid Stabilization Protocol for Cross-Chain Digital Assets Using Adaptor Signatures and AI-Driven Arbitrage, You, Kuehlkamp, Nabrzyski, DOI 10.1007/978-3-032-00495-6_8.
- 2024, Cluster Computing, Persona-Preserving Reputation Protocol (P2RP), You, Radivojevic, Nabrzyski, Brenner, DOI 10.1007/s10586-023-04222-4.
- 2023, IEEE BCCA, Mining User Behavior in Decentralized Applications, You, Joshi, Kuehlkamp, Nabrzyski, DOI 10.1109/BCCA58897.2023.10338860.
- 2022, IEEE BCCA, Trust in the Context of Blockchain Applications, You, Radivojevic, Nabrzyski, Brenner, DOI 10.1109/BCCA55292.2022.9922068.

Titles, authors, and DOIs come from my_researchs.bib (source of truth). See Open Questions on the 2026 title.

### 7. Experience (timeline, kept and lightly updated)
- 2024 to Present: AI Deployment work, Lion Protocol, Hong Kong.
- 2025 to Present: Guest Lecturer, Financial Computing, School of Business, Hong Kong Baptist University.
- 2019: Blockchain Full-Stack Engineer (Internship), The Linux Foundation, San Francisco. Hyperledger Fabric dashboard (MERN), Caliper-CLI docs, work presented at Hyperledger Global Forum 2020.
- 2018 to 2019: Graduate Student Researcher, Purdue University CSE. Secure HD wallet in Go, adversarial ML attack on CNNs.

### 8. Education and Skills
- Education: PhD Candidate, Computer Science, University of Notre Dame (advisor Jarek Nabrzyski). M.S., Computer Science (Information Security), Purdue, 2018 to 2019. B.A., Mathematics, University of Washington, 2014 to 2018.
- Skills, refreshed: agents and AI (multi-provider orchestration, LangGraph, RAG, prompt-injection detection, eval-harness design), engineering (Python, FastAPI, asyncio, Pydantic v2, pytest), rigor (TLA+ model checking, BCa bootstrap CIs, pre-registered experiments), blockchain (Solidity, Foundry, Hardhat, gas profiling, EVM).

### 9. Currently open to
One clean block listing the three role tracks, primary first:
- AI Deployment Engineer / FDE (primary): OpenAI, Anthropic, Crypto.com.
- AI x Crypto, Pioneer / Innovation Engineer: Binance, OKX, Crypto.com.
- DevRel / DevX (Mandarin): OpenAI DevX, MiniMax, Mistral, Qwen, DeepSeek, Zhipu.
Plus one line: building a Mandarin-first course, "Your First AI Employee", and a weekly Skill Studio at Lion Protocol OPC.

### 10. Contact and footer
- Email shengwei.you@gmail.com, LinkedIn /in/shengwei-you/, GitHub Jasonyou1995.
- Footer: copyright, plus a one-line privacy note: this is a static site, no tracking, no cookies, no data collected.

## Privacy (applied from the spec checklist)

- No phone number anywhere.
- No street address. Location shown as "Hong Kong" only.
- Headshot is a professional headshot, not a casual selfie.
- Publication links point to public DOIs only.
- No collaborator names beyond published co-authors.
- No images of IDs, passport, or visa.
- Repos linked are public-or-anonymized per double-blind rules.

## Modern and technical touches (all static, zero infra)

- Animated count-up for the Numbers strip, via IntersectionObserver (the page already uses one for fade-ins).
- `prefers-reduced-motion`: disables count-up and float animations when set.
- SEO: meta description, canonical, Open Graph and Twitter card tags, JSON-LD Person schema, hreflang alternates.
- favicon.svg with his initials.
- Accessibility: semantic landmarks, alt text, visible focus rings, sufficient contrast, aria on the language switch and nav.
- Performance: photo.png downscaled to a reasonable display size (target the visual size used, roughly 600 to 800px) and compressed. Target full page load under 1 second and a Lighthouse score 95+ on mobile and desktop.

## Image optimization plan

Original photo.png is 3995x3995, 24MB. Downscale to roughly 700px on the long edge and compress, replacing photo.png in place (or add an optimized file and point the img at it). Keep aspect ratio. Verify the result is tens of KB, not MB.

## Internationalization plan

Author the EN page first. Then re-author index.zh-CN.html and index.zh-TW.html with natural translations, keeping the name block, code terms, product names, company names, and numbers untranslated (`notranslate` where needed). Add hreflang alternates to all three. The lost translation script is not recreated.

## Out of scope (do not build)

- No Cloudflare Worker, no serverless functions, no live AI agent demo.
- No personal RAG over the resume, no chatbot that impersonates him.
- No multi-page blog, no CMS, no login or dashboard.
- No phone number, no contact form backend.

## Success criteria

- One static page per language, no backend, deploys on GitHub Pages unchanged.
- Hero, Numbers, the 4 project cards, Research, Experience, Education, Skills, Currently open to, and Contact all present and recruiter-first.
- Every headline number has a source label on the page and a defense line he can say out loud.
- No em-dashes, en-dash separators, or banned words anywhere in the copy.
- Photo is optimized to tens of KB. Page loads fast.
- SEO tags, hreflang, JSON-LD, favicon, accessibility pass present.
- zh-CN and zh-TW match the EN content.
- Privacy checklist satisfied.

## Open questions (resolved 2026-06-08)

1. 2026 book chapter title: use "Hybrid Stabilization Protocol for Cross-Chain Digital Assets Using Adaptor Signatures and AI-Driven Arbitrage" (the .bib version). The live site's "Coordination" is wrong and gets fixed.
2. Repo links: all four project cards read "Code available on request". No public repo links.
