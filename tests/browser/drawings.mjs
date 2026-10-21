// Contact sheet of every topic drawing on its stage colour (inspection only, not a check).
import { open } from "./cdp.mjs";
const BASE = process.argv.at(-1), OUT = process.argv.at(-2);
for (const theme of ["light", "dark"]) {
  const p = await open(BASE + "/", { width: 1500, height: 1400 });
  await p.eval(`(() => {
    document.documentElement.dataset.theme = "${theme}";
    const stage = (n) => n <= 5 ? 1 : n <= 11 ? 2 : n <= 18 ? 3 : n <= 25 ? 4 : n <= 29 ? 5 : 6;
    const grid = document.createElement("div");
    grid.style.cssText = "position:fixed;inset:0;z-index:99;background:var(--bg);display:grid;grid-template-columns:repeat(6,1fr);gap:10px;padding:10px;overflow:auto";
    for (let n = 1; n <= 34; n++) {
      const c = document.createElement("div"); c.dataset.stage = stage(n);
      c.style.cssText = "background:var(--stage);border-radius:18px;padding:14px;color:var(--on-stage);font:600 12px var(--sans)";
      c.append(n + " " + Trace.ART_KINDS[n], Trace.topicArt(n)); grid.append(c);
    }
    document.body.append(grid);
  })()`);
  await new Promise((r) => setTimeout(r, 400));
  await p.shot(OUT + "-" + theme + ".png");
  await p.close();
}
