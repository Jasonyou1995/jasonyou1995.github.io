# Digital twin proxy (Cloudflare Worker)

Does the twin work on GitHub Pages? The page itself is static, so it cannot hold a key or call a model safely.
The twin therefore lives in this tiny separate Worker (free tier is enough), and the page only talks to it.
Until you deploy it, the chat box degrades to a prefilled email, so nothing is ever broken.

## Deploy in about 15 minutes

1. `cd twin && npm i -g wrangler` then `npx wrangler login`
2. `npx wrangler kv namespace create RL` and paste the id into `wrangler.toml`
3. Secrets (never committed): `npx wrangler secret put LLM_API_KEY`, `TURNSTILE_SECRET`, `CANARY`
   The canary must be nonsense with a few digits, for example `xq7-velm-ouro-4417` (make your own, do not reuse this one). Never a real word.
4. Create a Cloudflare Turnstile widget for jasonyou1995.github.io. The site key is public.
5. `npx wrangler deploy`, then rebuild the site with the two public values:
   `TWIN_ENDPOINT=https://shengwei-twin.<you>.workers.dev TURNSTILE_SITEKEY=<site key> python3 docs/build/build.py`
6. Fund the model account with a small prepaid balance. That balance is the hard daily wallet cap.

## Model

DeepSeek is the default: base `https://api.deepseek.com`, model `deepseek-flash` (set in `wrangler.toml`).
The Worker sends `thinking: disabled` to DeepSeek so there is no hidden reasoning, and it never reads `reasoning_content`.
Model names change. If a call fails with a model error, check https://api-docs.deepseek.com and edit `LLM_MODEL`.
Mainland reachability of `workers.dev` is not guaranteed. If visitors there cannot chat, the mailto fallback still works;
for a fix, put the Worker on a custom domain behind Cloudflare, or move the same code to a Hong Kong host.
Set `FINPROV_LLM_*` to route the FinProv door to a provider you can defend when a buyer asks where chat data goes,
and pass `topic: "finprov"` from that door.

## Why it holds against strong attackers with so few moving parts

The design removes what an attacker needs, then checks what comes out.

- Nothing to steal: no key in the browser, no secret except the canary, no tools, no files, no memory, no browsing.
- One stateless turn: no chat history, so slow multi-turn "crescendo" attacks have nothing to build on.
- Input: strict origin match, 2 KB body cap, Unicode clean-up (hidden characters, look-alike letters, fake tags), long encoded blobs refused.
- Prompt: the rules are repeated after the untrusted text, and the visitor's text is wrapped as data.
- Output (the part that does not depend on the model behaving): canary in any disguise (plain, spaced, reversed, base64, hex, rot13, fragments), rule text leaks, prices, promises, any link or email that is not Shengwei's own, and any markup or code. Anything blocked becomes a fixed polite reply.
- Fail closed: a missing Turnstile secret, canary, key or KV store refuses every request.
- Cost: per-IP limit, global daily cap, prepaid balance. Message text and IPs are never logged, only counters.

A fully jailbroken model can still only produce vetted words. That is the point: guard the exit, not the model's manners.

## Test before launch and after any edit

`node --import ./register.mjs test.mjs` runs 75 checks, including 60 attacks against a model that obeys every injection.
Then do the human round: 50 real attempts in the "break it" mode. Pass = 0 canary, 0 prices, 0 promises.
Rotate `CANARY` after any breach. The weekly 5 minutes: look at the `breach` counter in KV.
