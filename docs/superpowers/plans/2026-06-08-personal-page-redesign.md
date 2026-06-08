# Personal Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild jasonyou1995.github.io as one fast, recruiter-first static page (plus its 简体 and 繁體 versions) built around four shipped research systems and their verifiable numbers.

**Architecture:** Three self-contained static HTML files (inline CSS and a small inline script), no build step, no backend. Keep the existing visual system. Add a Numbers strip, a 4-project grid, a "Currently open to" block, full SEO and accessibility, and an optimized headshot.

**Tech Stack:** Hand-written HTML5, inline CSS, vanilla JS (IntersectionObserver), macOS `sips` for image optimization. Hosted on GitHub Pages.

**Source of truth for content (read before starting):**
- Copy, numbers, defense lines, privacy rules: `docs/superpowers/specs/2026-06-08-personal-page-redesign-design.md`.
- Visual system to preserve (colors, fonts, `.pcard`, `.strip`, `.tl` timeline, `.fade` observer, media queries): the current `index.html` at commit before this branch.

**Hard style rule (applies to every file and commit message):** No em-dashes ("—"), no en-dash separators ("–"), no three-dash dividers in prose. No "leverage / robust / navigate / delve". Ranges as "2024 to Present". Chinese files use full-width punctuation (，。、), never "—".

**Branch:** Already on `personal-page-redesign`. Keep all commits here.

---

### Task 1: Optimize the headshot and add a favicon

**Files:**
- Modify: `photo.png` (remove from working tree after converting)
- Create: `photo.jpg` (optimized headshot)
- Create: `favicon.svg`

- [ ] **Step 1: Convert the 24MB headshot to an optimized JPEG**

The original is 3995x3995 PNG, 24MB. A headshot is photographic, so JPEG at display size is the right format.

Run:
```bash
cd "/Users/mac14/Library/Mobile Documents/com~apple~CloudDocs/Main-IC/Business/_Online_Education线上教育/jasonyou1995.github.io"
sips -s format jpeg -s formatOptions 82 -Z 800 photo.png --out photo.jpg
du -h photo.jpg
```
Expected: `photo.jpg` exists and `du -h` shows a value in KB (target under ~150K), not MB.

- [ ] **Step 2: Remove the heavy original from the working tree**

Run:
```bash
git rm photo.png
```
Expected: `photo.png` staged for deletion. It stays in git history if ever needed.

- [ ] **Step 3: Create `favicon.svg`**

Write `favicon.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0f0e0c"/>
  <text x="50%" y="50%" dy="0.35em" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-weight="700"
        font-size="34" fill="#e0612f">SY</text>
</svg>
```

- [ ] **Step 4: Commit**

```bash
git add photo.jpg favicon.svg
git commit -m "Optimize headshot to JPEG and add favicon"
```

---

### Task 2: Rewrite the head, nav, and hero of `index.html`

**Files:**
- Modify: `index.html` (the `<head>`, `<nav>`, and hero `<section>`)

This task keeps the existing `<style>` block intact and updates markup. Add new CSS only where a new component needs it (Tasks 4, 5, 6 reuse existing classes).

- [ ] **Step 1: Replace the `<head>` contents with full SEO, social, and structured-data tags**

Keep the existing font `<link>` and the entire `<style>` block. Replace the title, description, and add the rest. Use exactly:
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shengwei You (Jason You) · AI Deployment Engineer / FDE</title>
<meta name="description" content="Shengwei You (游盛巍 / Jason You). AI Deployment Engineer and Forward Deployed Engineer. PhD candidate in Hong Kong. Four shipped, verifiable AI agent systems: TLA+-verified safety, on-chain multi-agent debate, IEEE ICBC 2026 stablecoin controller, and a SNARK oracle.">
<link rel="canonical" href="https://jasonyou1995.github.io/">
<link rel="alternate" hreflang="en" href="https://jasonyou1995.github.io/index.html">
<link rel="alternate" hreflang="zh-Hans" href="https://jasonyou1995.github.io/index.zh-CN.html">
<link rel="alternate" hreflang="zh-Hant" href="https://jasonyou1995.github.io/index.zh-TW.html">
<link rel="alternate" hreflang="x-default" href="https://jasonyou1995.github.io/index.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="Shengwei You · AI Deployment Engineer / FDE">
<meta property="og:description" content="Four shipped, verifiable AI agent systems. PhD candidate, Hong Kong. Open to AI Deployment / FDE roles.">
<meta property="og:url" content="https://jasonyou1995.github.io/">
<meta property="og:image" content="https://jasonyou1995.github.io/photo.jpg">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Shengwei You · AI Deployment Engineer / FDE">
<meta name="twitter:description" content="Four shipped, verifiable AI agent systems. PhD candidate, Hong Kong.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Shengwei You",
  "alternateName": ["游盛巍", "Jason You"],
  "jobTitle": "AI Deployment Engineer / Forward Deployed Engineer",
  "email": "mailto:shengwei.you@gmail.com",
  "url": "https://jasonyou1995.github.io/",
  "homeLocation": {"@type": "Place", "name": "Hong Kong"},
  "knowsLanguage": ["en", "zh-Hans", "zh-Hant"],
  "sameAs": [
    "https://www.linkedin.com/in/shengwei-you/",
    "https://github.com/Jasonyou1995"
  ],
  "alumniOf": [
    {"@type": "CollegeOrUniversity", "name": "University of Notre Dame"},
    {"@type": "CollegeOrUniversity", "name": "Purdue University"},
    {"@type": "CollegeOrUniversity", "name": "University of Washington"}
  ]
}
</script>
```

- [ ] **Step 2: Update the nav anchors and keep the language switch**

In `<nav>`, set the menu items to: About, Numbers, Work, Research, Experience, Contact (hrefs `#about`, `#numbers`, `#work`, `#research`, `#experience`, `#contact`). Keep the existing `.lang` dropdown with the three language links. Add `aria-label="Language"` to the `.lang` container.

- [ ] **Step 3: Rewrite the hero section**

Use the hero copy from the spec section "2. Hero". Concretely:
- Tag chip text: `Open to AI Deployment / FDE roles`.
- `h1`: keep the `notranslate` name block `Shengwei You · 游盛巍 (Jason)` using the existing `.sur` and `.cn` styles.
- `.sub`: `AI Deployment Engineer / FDE`.
- `.lead`: "I build the full reliability layer around frontier model calls: multi-provider orchestration, retrieval grounding, on-chain execution, and provable safety gating. I verify every claim with seeds, logs, and receipts, and I treat my own results with a reviewer's skepticism." Bold the phrase "provable safety gating".
- Buttons: `See the work` to `#numbers` (btn-1), `Get in touch` to `#contact` (btn-2).
- Portrait `img src="photo.jpg"`, with `width` and `height` attributes set to the displayed size and `alt="Shengwei You (游盛巍)"`.
- Float card 1: Focus = "Agent safety and deployment". Float card 2: Open to = "FDE and AI roles".

- [ ] **Step 4: Verify the head and hero in a browser**

Run:
```bash
open index.html
```
Expected: page loads, headshot is sharp and small, hero shows the new headline and two buttons, language dropdown still works.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Rewrite head, nav, and hero for recruiter-first positioning"
```

---

### Task 3: Add the Numbers strip with count-up and source labels

**Files:**
- Modify: `index.html` (add a new `#numbers` section after the hero; add CSS for the number labels; extend the inline script)

- [ ] **Step 1: Add CSS for the numbers section**

Inside the `<style>` block, after the `.strip` rules, add:
```css
.nums { display:grid; grid-template-columns:repeat(4,1fr); gap:0; border:1px solid var(--border); border-radius:14px; overflow:hidden; }
.nums a { padding:2rem 1.2rem; text-align:center; text-decoration:none; color:inherit; transition:.25s; }
.nums a:not(:last-child){ border-right:1px solid var(--border); }
.nums a:hover{ background:var(--bg2); }
.nums .big{ font-family:'Fraunces',serif; font-weight:900; font-size:2.6rem; color:var(--accent); line-height:1; }
.nums .lab{ color:var(--text-dim); font-size:.8rem; margin-top:.6rem; }
@media(max-width:900px){ .nums{ grid-template-columns:1fr 1fr; } .nums a:nth-child(2){border-right:none;} .nums a:nth-child(1),.nums a:nth-child(2){border-bottom:1px solid var(--border);} }
```

- [ ] **Step 2: Add the `#numbers` section markup**

After the hero `</section>`, add (each number links to its project card and carries the spec's source label):
```html
<section id="numbers"><div class="container">
  <div class="sh fade"><span class="st">By the numbers</span>
    <h2 class="stitle">Verifiable, not claimed</h2>
    <p class="ssub">Every figure traces to a seed, a log, and a result file. Click through to the system that produced it.</p>
  </div>
  <div class="nums fade">
    <a href="#p-oc1"><div class="big" data-count="18400" data-decimals="0" data-suffix="+">0</div><div class="lab">lines of production Python, shipped solo</div></a>
    <a href="#p-oc1"><div class="big" data-count="5.8" data-decimals="1" data-suffix="M">0</div><div class="lab">TLA+ states model-checked, 0 violations</div></a>
    <a href="#p-mvf"><div class="big" data-count="62" data-decimals="0" data-suffix="%">0</div><div class="lab">peak peg deviation cut, IEEE ICBC 2026</div></a>
    <a href="#p-noc"><div class="big" data-count="21" data-decimals="0" data-suffix="x">0</div><div class="lab">cheaper oracle vs committee baseline</div></a>
  </div>
</div></section>
```

- [ ] **Step 3: Add the count-up script (with reduced-motion guard) to the inline `<script>`**

Append to the existing inline script at the bottom of `index.html`:
```javascript
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function animateCount(el){
  const target = parseFloat(el.dataset.count);
  const dec = parseInt(el.dataset.decimals || '0');
  const suffix = el.dataset.suffix || '';
  const fmt = (n) => (dec>0 ? n.toFixed(dec) : Math.round(n).toLocaleString('en-US')) + suffix;
  if (reduce){ el.textContent = fmt(target); return; }
  const dur = 1100; const t0 = performance.now();
  function tick(now){
    const p = Math.min((now - t0)/dur, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = fmt(target * eased);
    if (p < 1) requestAnimationFrame(tick); else el.textContent = fmt(target);
  }
  requestAnimationFrame(tick);
}
const numObs = new IntersectionObserver((es)=>{es.forEach(e=>{ if(e.isIntersecting){ animateCount(e.target); numObs.unobserve(e.target);} });},{threshold:.4});
document.querySelectorAll('.nums .big[data-count]').forEach(el=>numObs.observe(el));
```

- [ ] **Step 4: Verify count-up animates and respects reduced motion**

Run:
```bash
open index.html
```
Expected: scrolling to the Numbers strip animates 0 to each target; "5.8M", "18,400+", "62%", "21x" render correctly. With macOS Reduce Motion on, numbers appear at final value with no animation.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Add animated Numbers strip with defensible source labels"
```

---

### Task 4: Reframe "How I engineer" and add the 4-project grid

**Files:**
- Modify: `index.html` (rewrite the `#work` / offer section; add the project grid)

- [ ] **Step 1: Reframe the existing "What I Do" pillars into "How I engineer"**

Reuse the existing `.offer` / `.pillars` / `.pcard` markup. Replace the four pillar bodies with the spec section "4. How I engineer": reliability layer, formal verification, adversarial red-teaming, reproducibility. Section heading: "How I engineer". Subhead: "Production AI you can verify, not proofs-of-concept." Add one slim closing line under the grid: "Available for AI deployment delivery work (Lion Protocol): scope to live system in about 90 days."

- [ ] **Step 2: Add CSS for project cards**

Inside `<style>`, after the `.pcard` rules, add:
```css
.projs{ display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }
.proj{ background:var(--bg2); border:1px solid var(--border); border-radius:16px; padding:2rem; transition:.3s; }
.proj:hover{ border-color:var(--accent); transform:translateY(-4px); }
.proj h3{ font-family:'Fraunces',serif; font-size:1.35rem; font-weight:600; margin-bottom:.2rem; }
.proj .tagline{ color:var(--accent-2); font-size:.92rem; margin-bottom:1rem; }
.proj ul{ list-style:none; display:flex; flex-direction:column; gap:.6rem; margin-bottom:1.1rem; }
.proj li{ color:var(--text-dim); font-size:.9rem; padding-left:1.1rem; position:relative; }
.proj li::before{ content:"▹"; color:var(--accent); position:absolute; left:0; }
.proj li b{ color:var(--text); font-weight:600; }
.proj .note{ font-size:.82rem; color:var(--text-dim); border-top:1px solid var(--border); padding-top:.8rem; }
@media(max-width:900px){ .projs{ grid-template-columns:1fr; } }
```

- [ ] **Step 3: Add the `#work` project grid section**

Add a new section (id `work` if not already used by the reframed offer; otherwise id `projects`). Build four `.proj` cards with anchor ids `p-oc1`, `p-oc2`, `p-mvf`, `p-noc`, using the bullets from the spec section "5. The 4 projects". Each card ends with `<p class="note">Code available on request.</p>`. Pattern for one card:
```html
<div class="proj fade" id="p-oc1">
  <h3>OC1: Autonomous LLM Agent Safety Control System</h3>
  <p class="tagline">Multi-provider agent stack with a formally verified safety circuit.</p>
  <ul>
    <li><b>Built:</b> multi-provider LLM orchestration with auto-failover, a TLA+ safety state machine, prompt-injection detection, an EVM execution layer, and a RAG policy oracle. Solo: 18,400+ lines of Python, 7 Solidity contracts, 14 test suites.</li>
    <li><b>Measured:</b> P95 about 3.9s with sub-5ms safety gating; 5,866,037 TLA+ states, 0 violations; prompt-injection F1 0.765 at 5% false-positive rate; survived 100/100 adaptive RL attack episodes.</li>
    <li><b>Verifiable:</b> one-command pipeline, seed-controlled, claim-to-artifact traceability.</li>
  </ul>
  <p class="note">Code available on request.</p>
</div>
```
Repeat with the spec's content for `p-oc2` (On-Chain Multi-Agent LLM Debate: 90.2% verdict accuracy, 95% expert agreement, 8.7% cheaper gas than the Optimism baseline, 76 Foundry tests), `p-mvf` (MVF-Composer, IEEE ICBC 2026: 12 agents over OpenAI/Anthropic/DeepSeek, 1,200 sims, 62% peg deviation cut, 3.1x faster recovery), and `p-noc` (NOC oracle: Groth16/BN254 on-chain, about 0.04 USD per update, 21x cheaper, 100% Byzantine detection to 37.5% adversary, 76 tests).

- [ ] **Step 4: Verify**

Run:
```bash
open index.html
```
Expected: "How I engineer" reads as build practice not sales; four project cards in a 2x2 grid; the Numbers strip links jump to the matching card.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Reframe engineering section and add 4-project evidence grid"
```

---

### Task 5: Update research, experience, education, skills, open-to, and contact

**Files:**
- Modify: `index.html` (the remaining sections)

- [ ] **Step 1: Fix the 2026 publication title**

In the research section, change the 2026 paper title to "Hybrid Stabilization Protocol for Cross-Chain Digital Assets Using Adaptor Signatures and AI-Driven Arbitrage". Keep the other three papers and all DOIs as they are (they match `my_researchs.bib`).

- [ ] **Step 2: Keep experience and education sections, light touch**

Leave the timeline and education content as-is except: confirm date ranges read with "to" not a dash (for example "2024 to Present", "2018 to 2019"). Replace any `&ndash;` or `&mdash;` in these sections with "to" or "·" or a colon as the spec describes.

- [ ] **Step 3: Refresh the skills chips**

Update the skills section per the spec section "8": agents and AI (multi-provider orchestration, LangGraph, RAG, prompt-injection detection, eval-harness design), engineering (Python, FastAPI, asyncio, Pydantic v2, pytest), rigor (TLA+ model checking, BCa bootstrap CIs, pre-registered experiments), blockchain (Solidity, Foundry, Hardhat, gas profiling, EVM).

- [ ] **Step 4: Add the "Currently open to" block before Contact**

Add a section using the existing `.grid3` / `.scat` styling or a simple list, with the three role tracks from spec section "9" (AI Deployment / FDE primary; AI x Crypto; DevRel / DevX Mandarin) and the one course line. Markup pattern:
```html
<section id="open"><div class="container">
  <div class="sh fade"><span class="st">Currently open to</span>
    <h2 class="stitle">Where I can plug in</h2>
  </div>
  <div class="grid3">
    <div class="scat fade"><h3>AI Deployment Engineer / FDE</h3><p style="color:var(--text-dim);font-size:.9rem;">Primary focus. OpenAI, Anthropic, Crypto.com.</p></div>
    <div class="scat fade"><h3>AI x Crypto, Innovation Engineer</h3><p style="color:var(--text-dim);font-size:.9rem;">Binance, OKX, Crypto.com.</p></div>
    <div class="scat fade"><h3>DevRel / DevX (Mandarin)</h3><p style="color:var(--text-dim);font-size:.9rem;">OpenAI DevX, MiniMax, Mistral, Qwen, DeepSeek, Zhipu.</p></div>
  </div>
  <p class="ssub fade" style="margin-top:1.5rem;">Also building a Mandarin-first course, "Your First AI Employee", and a weekly Skill Studio at Lion Protocol OPC.</p>
</div></section>
```

- [ ] **Step 5: Update contact and footer**

In the contact section set the email link to `shengwei.you@gmail.com`, LinkedIn `https://www.linkedin.com/in/shengwei-you/`, GitHub `https://github.com/Jasonyou1995`. In the footer add a privacy line: "This is a static site. No tracking, no cookies, no data collected. Hong Kong." Keep the copyright.

- [ ] **Step 6: Verify the whole EN page and scan for forbidden marks**

Run:
```bash
open index.html
grep -n "—\|–" index.html || echo "no em/en dashes"
grep -niE "leverage|robust|navigate|delve" index.html || echo "no banned words"
grep -n "&mdash;\|&ndash;" index.html || echo "no html dash entities"
```
Expected: page reads top to bottom correctly; all three greps report none.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "Update research, skills, open-to, and contact; fix paper title and remove dashes"
```

---

### Task 6: Re-author the Simplified Chinese page

**Files:**
- Modify: `index.zh-CN.html` (replace its body content to match the new `index.html`)

- [ ] **Step 1: Copy the new structure and translate to Simplified Chinese**

Start from the finished `index.html`. Set `<html lang="zh-CN">`. Set `<link rel="canonical">` to the zh-CN URL and keep the same three hreflang alternates plus x-default pointing at the EN file. Translate all prose to natural Simplified Chinese. Keep untranslated (wrap in `notranslate` where needed): the name block, all numbers and units, code and product terms (TLA+, LangGraph, FastAPI, Pydantic, Solidity, Foundry, Groth16, RAG, OpenAI, Anthropic, DeepSeek, IEEE ICBC 2026, paper titles, DOIs, OC1/OC2/MVF-Composer/NOC, emails, URLs). Use full-width punctuation (，。、：；（）), never "—".

- [ ] **Step 2: Set the active language and keep the JS**

Update the `.lang` button label to show 简体中文 active. Keep the same inline script (count-up works language-agnostic). Keep `photo.jpg` and `favicon.svg` references.

- [ ] **Step 3: Verify**

Run:
```bash
open index.zh-CN.html
grep -n "—\|–" index.zh-CN.html || echo "no em/en dashes"
grep -n "&mdash;\|&ndash;" index.zh-CN.html || echo "no html dash entities"
```
Expected: page renders in Simplified Chinese with numbers and code terms intact; greps report none; the count-up animates.

- [ ] **Step 4: Commit**

```bash
git add index.zh-CN.html
git commit -m "Re-author Simplified Chinese page to match new EN page"
```

---

### Task 7: Re-author the Traditional Chinese page

**Files:**
- Modify: `index.zh-TW.html`

- [ ] **Step 1: Produce the Traditional Chinese version**

Start from the finished `index.zh-CN.html` content and convert to Traditional Chinese characters, or translate from `index.html` directly. Set `<html lang="zh-TW">`, canonical to the zh-TW URL, keep the three hreflang alternates plus x-default. Same `notranslate` rules and full-width punctuation as Task 6. Use Hong Kong / Taiwan standard Traditional forms.

- [ ] **Step 2: Set the active language and keep the JS**

Update the `.lang` button label to show 繁體中文 active. Keep the inline script and `photo.jpg` / `favicon.svg`.

- [ ] **Step 3: Verify**

Run:
```bash
open index.zh-TW.html
grep -n "—\|–" index.zh-TW.html || echo "no em/en dashes"
grep -n "&mdash;\|&ndash;" index.zh-TW.html || echo "no html dash entities"
```
Expected: page renders in Traditional Chinese, numbers and code terms intact, greps report none.

- [ ] **Step 4: Commit**

```bash
git add index.zh-TW.html
git commit -m "Re-author Traditional Chinese page to match new EN page"
```

---

### Task 8: Cross-file verification and final pass

**Files:**
- Modify: any of the three HTML files if checks fail

- [ ] **Step 1: Confirm the three language switchers cross-link correctly**

Run:
```bash
grep -n 'index.html\|index.zh-CN.html\|index.zh-TW.html' index.html index.zh-CN.html index.zh-TW.html
```
Expected: every page links to the other two and itself in the `.lang` dropdown and in `hreflang` tags.

- [ ] **Step 2: Confirm the heavy asset is gone and the light one is referenced**

Run:
```bash
ls -la photo.jpg; test ! -f photo.png && echo "png removed from tree"; grep -c "photo.jpg" index.html index.zh-CN.html index.zh-TW.html
```
Expected: `photo.jpg` present and small; `photo.png` absent; each HTML references `photo.jpg`.

- [ ] **Step 3: Full forbidden-mark sweep across all three files**

Run:
```bash
grep -n "—\|–\|&mdash;\|&ndash;" index.html index.zh-CN.html index.zh-TW.html || echo "clean"
grep -niE "leverage|robust|navigate|delve" index.html || echo "clean"
```
Expected: both report clean.

- [ ] **Step 4: Responsive and accessibility eyeball check**

Run:
```bash
open index.html
```
In the browser: resize to mobile width and confirm the Numbers strip, project grid, and nav collapse correctly; tab through the page and confirm focus is visible on links and buttons; confirm the headshot has alt text.

- [ ] **Step 5: Optional Lighthouse audit if available**

Run (only if `lighthouse` is installed):
```bash
command -v lighthouse >/dev/null && lighthouse "file://$(pwd)/index.html" --only-categories=performance,accessibility,seo --quiet --chrome-flags="--headless" || echo "lighthouse not installed, skipping"
```
Expected: if it runs, performance, accessibility, and SEO are high (target 95+). If not installed, skip.

- [ ] **Step 6: Final commit**

```bash
git add -A
git commit -m "Final verification pass for personal page redesign"
```

---

## Self-review notes

- Spec coverage: head/SEO (T2), nav + lang (T2, T6, T7, T8), hero (T2), Numbers strip with defense labels (T3), How I engineer (T4), 4 projects (T4), research with corrected title (T5), experience/education/skills (T5), Currently open to (T5), contact + privacy footer (T5), photo optimization (T1), favicon (T1), accessibility + reduced motion (T2, T3, T8), trilingual + hreflang (T2, T6, T7), no-dash rule (T5, T6, T7, T8). All sections map to a task.
- The bulk copy lives in the committed spec by design (DRY); tasks reference exact spec sections and give exact code for every new technical element (head block, numbers markup, count-up JS, project card pattern, open-to markup, favicon, image command).
- Anchor ids are consistent across tasks: `p-oc1`, `p-oc2`, `p-mvf`, `p-noc`, and the Numbers links point at them.
