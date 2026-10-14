// Test-only: lets Node import facts.md as text, the way wrangler bundles it.
import { readFile } from "node:fs/promises";
export async function load(url, ctx, next) {
  if (url.endsWith(".md")) return { format: "module", shortCircuit: true, source: "export default " + JSON.stringify(await readFile(new URL(url), "utf8")) };
  return next(url, ctx);
}
