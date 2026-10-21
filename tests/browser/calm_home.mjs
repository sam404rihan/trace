// Calm home: the C3 look and stage colours, topic drawings, where you stopped, the home, the roadmap, the sidebar.
import { open, check, summary } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);

// WCAG contrast between two CSS colours, read through computed styles so var() and named colours resolve.
const contrast = (p, fg, bg) => p.eval(`(() => {
  const rgb = (c) => { const el = document.createElement("i"); el.style.color = c; document.body.append(el);
    const v = getComputedStyle(el).color.match(/[\\d.]+/g).slice(0, 3).map(Number); el.remove(); return v; };
  const lum = ([r, g, b]) => [r, g, b].map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; })
    .reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0);
  const [a, b] = [lum(rgb(${JSON.stringify(fg)})), lum(rgb(${JSON.stringify(bg)}))].sort((x, y) => y - x);
  return (a + 0.05) / (b + 0.05);
})()`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// ── The look: every page carries its stage's colour ──
await p.reload(BASE + "/#/p/pointer_step");     // topic 06, stage 2
check("problem page sets its stage", (await p.eval(`document.body.dataset.stage`)) === "2");
await p.reload(BASE + "/#/t/15_trees");
check("topic page sets its stage", (await p.eval(`document.body.dataset.stage`)) === "3");
check("six stage colours", await p.eval(`[1,2,3,4,5,6].every(n => getComputedStyle(document.body).getPropertyValue("--st" + n).trim())`));
check("primary button has a pressed edge", (await p.eval(`(() => { const b = document.createElement("a"); b.className = "btn primary"; document.body.append(b);
  const s = getComputedStyle(b).boxShadow; b.remove(); return s; })()`)) !== "none");
// Set the theme outright: headless Chrome follows the machine's own light or dark setting.
for (const mode of ["light", "dark"]) {
  await p.eval(`document.documentElement.dataset.theme = "${mode}"`);
  for (let n = 1; n <= 6; n++) {
    const c = await contrast(p, `var(--on-st${n})`, `var(--st${n})`);
    check(`stage ${n} text is readable (${mode})`, c >= 4.5, c.toFixed(2));
    const t = await contrast(p, `var(--st${n}-text)`, "var(--bg)");
    check(`stage ${n} as text on the page is readable (${mode})`, t >= 4.5, t.toFixed(2));
  }
}
await p.eval(`delete document.documentElement.dataset.theme`);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
