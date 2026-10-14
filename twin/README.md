# Digital twin proxy (Cloudflare Worker)

The page works without this: the widget degrades to a prefilled email. Deploy when ready.

1. `cd twin && npm i -g wrangler` then `npx wrangler login`
2. `npx wrangler kv namespace create RL` and paste the id into `wrangler.toml`
3. Secrets (never committed): `npx wrangler secret put LLM_API_KEY`, `TURNSTILE_SECRET`, `CANARY`
4. Create a Cloudflare Turnstile widget for jasonyou1995.github.io. The site key is public.
5. `npx wrangler deploy`, then rebuild the site with the two public values:
   `TWIN_ENDPOINT=https://shengwei-twin.<you>.workers.dev TURNSTILE_SITEKEY=<site key> python3 docs/build/build.py`
6. Fund the model account with a small prepaid balance. That balance is the hard daily wallet cap.

Three stacked limits: per-IP (10 per hour), global daily cap (300), prepaid balance.
No tools, so a successful attack produces words, never actions. Message text and IPs are never logged.

Model routing: `LLM_*` serves the general twin (DeepSeek by default, reachable from the mainland).
Set `FINPROV_LLM_*` to route the FinProv door to a provider you can defend when a buyer asks where chat data goes,
and pass `topic: "finprov"` from that door.

Jailbreak test before launch: run 50 attempts (prompt extraction, price quotes, role-play, other languages).
Pass = 0 key leaks, 0 prices, 0 promises. Rotate `CANARY` after any breach.
