// screens.mjs OUTDIR NAME[,NAME...] (home, roadmap, t/15_trees ... without "#/", which Git Bash mangles) : screenshots at 1440 and 390, light and dark (inspection only).
import { open, sleep } from "./cdp.mjs";
const BASE = process.argv.at(-1), OUT = process.argv.at(-3), ROUTES = process.argv.at(-2).split(",");
const setup = await open(BASE + "/");
await setup.eval(`fetch("/api/placement", { method: "POST", headers: { "Content-Type": "application/json" }, body: '{"door":"skip"}' })`);
for (const n of ["pointer_step", "count_pairs_below"]) await setup.eval(`fetch("/api/solution?name=${n}").then(r => r.json()).then(s => fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${n}", code: s.code }) }))`);
await setup.reload(BASE + "/#/p/is_subsequence");
await setup.close();
for (const [w, h] of [[1440, 900], [390, 844]]) for (const theme of ["light", "dark"]) {
  const p = await open(BASE + "/", { width: w, height: h });
  await p.eval(`localStorage.setItem("trace.lastStop", JSON.stringify({ hash: "#/p/is_subsequence" })); localStorage.setItem("trace.theme", '"${theme}"')`);
  for (const r of ROUTES) {
    await p.reload(BASE + "/#/" + (r === "home" ? "" : r));
    await sleep(1200);
    await p.shot(`${OUT}/${r.replace(/\//g, "-")}-${w}-${theme}.png`);
  }
  await p.close();
}
