// The topic page and study-plan pages, calmed like home; and the shell (sidebar, crumbs, palette,
// console) drawn with SVG icons, in weights the vendored fonts actually have.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const course = (p) => p.eval(`fetch("/api/course").then(r => r.json())`);

// Characters that must never stand in for an icon, marker or bullet in the shell.
const GLYPHS = "›‹»«▾▸▴◂▼▶▲◀✓✔✗✕✖★☆◇◆≡⌂•●○■□→←↑↓⟶";
// Glyphs found in the text of `sel` and in any ::before / ::after content inside it.
const glyphsIn = (p, sel) => p.eval(`(() => {
  const bad = ${JSON.stringify(GLYPHS)}, out = [];
  for (const root of document.querySelectorAll(${JSON.stringify(sel)})) {
    for (const ch of root.textContent) if (bad.includes(ch)) out.push(ch + " in text of " + ${JSON.stringify(sel)});
    for (const el of [root, ...root.querySelectorAll("*")]) for (const pe of ["::before", "::after"]) {
      const c = getComputedStyle(el, pe).content;
      if (c && c !== "none" && c !== "normal" && [...c].some((ch) => bad.includes(ch))) out.push(c + " in " + pe + " of " + (el.className?.baseVal ?? el.className));
    }
  }
  return out; })()`);
// Every element's computed weight: the grotesk is vendored 400 to 700, Plex Mono 400 to 600.
const heavy = (p) => p.eval(`(() => {
  const out = [];
  for (const el of document.querySelectorAll("body *")) {
    if (!el.getClientRects().length) continue;
    const cs = getComputedStyle(el), w = Number(cs.fontWeight), mono = /^"?IBM Plex Mono/.test(cs.fontFamily);
    if (w > (mono ? 600 : 700)) out.push((el.className?.baseVal ?? el.className) + " " + el.tagName + " " + w + (mono ? " mono" : ""));
  }
  return [...new Set(out)].slice(0, 12); })()`);
// Stylesheet rules asking for a weight no vendored face has.
const heavyRules = (p) => p.eval(`(() => {
  const out = [];
  const walk = (rules) => { for (const r of rules) { if (r.cssRules) walk(r.cssRules);
    if (r.style && Number(r.style.fontWeight) > 700) out.push(r.selectorText + " " + r.style.fontWeight); } };
  for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch { /* cross-origin */ } }
  return out; })()`);
// Text that reads below 4.5:1 against what's actually behind it (alpha backgrounds composited), or is faded by opacity.
const lowContrast = (p, sel) => p.eval(`(() => {
  const parse = (c) => { const n = (c.match(/[0-9.]+/g) || []).map(Number); const f = c.startsWith("color(") ? 255 : 1;
    return { r: n[0] * f, g: n[1] * f, b: n[2] * f, a: n.length > 3 ? n[3] : 1 }; };
  const behind = (el) => { const layers = []; for (let e = el; e; e = e.parentElement) {
      const c = parse(getComputedStyle(e).backgroundColor); if (c.a > 0) { layers.push(c); if (c.a >= 1) break; } }
    let base = { r: 255, g: 255, b: 255 };
    for (const c of layers.reverse()) base = { r: c.r * c.a + base.r * (1 - c.a), g: c.g * c.a + base.g * (1 - c.a), b: c.b * c.a + base.b * (1 - c.a) };
    return base; };
  const lum = ({ r, g, b }) => [r, g, b].map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; })
    .reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0);
  const out = [];
  for (const root of document.querySelectorAll(${JSON.stringify(sel)})) for (const el of [root, ...root.querySelectorAll("*")]) {
    if (!el.getClientRects().length || el.closest("svg")) continue;
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility !== "visible") continue;
    let faded = false; for (let e = el; e && e !== root.parentElement; e = e.parentElement) if (Number(getComputedStyle(e).opacity) < 1) faded = true;
    const fg = parse(cs.color), bg = behind(el);
    const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x), ratio = (a + 0.05) / (b + 0.05);
    if (ratio < 4.5 || faded) out.push(el.tagName + "." + el.className + " '" + el.textContent.trim().slice(0, 24) + "' " + ratio.toFixed(2) + (faded ? " faded" : ""));
  }
  return [...new Set(out)].slice(0, 10); })()`);
// Rendered rows: inside a shut <details> Chrome keeps the boxes but hides them, so ask checkVisibility.
const shown = (p, sel) => p.eval(`[...document.querySelectorAll(${JSON.stringify(sel)})].filter((e) => e.checkVisibility()).length`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });
const data = await course(p);
const topic06 = data.topics.find((t) => t.id === "06_two_pointers");
const drills06 = await p.eval(`(() => { const d = Trace.topics.find((x) => x.n === 6); return { id: d.id, drills: d.drills.map((x) => x.id) }; })()`);

// ── A fresh topic: its colour and drawing, and one obvious next step ──
await p.reload(BASE + "/#/t/06_two_pointers");
check("the topic leads in its stage colour", await p.eval(`(() => { const h = document.querySelector("#app .topic-hero"); if (!h) return false;
  const i = document.createElement("i"); i.style.color = "var(--stage)"; h.append(i); const want = getComputedStyle(i).color; i.remove();
  return getComputedStyle(h).backgroundColor === want && document.body.dataset.stage === "2"; })()`));
check("the topic's drawing is in the lead, cropped", await p.eval(`(() => { const s = document.querySelector(".topic-hero svg.art"); if (!s) return false;
  const v = s.viewBox.baseVal; return v.width < 320 || v.height < 200; })()`));
check("the title is the topic", (await p.eval(`document.querySelector(".topic-hero h1")?.textContent`)) === "Two pointers");
check("the stage line follows the title", await p.eval(`(() => { const h = document.querySelector(".topic-hero h1"), s = h && h.nextElementSibling;
  return !!s && s.textContent.includes("Core patterns"); })()`));
check("one primary action on the topic page", (await p.eval(`document.querySelectorAll("#app .btn.primary").length`)) === 1);
const go = () => p.eval(`(() => { const b = document.querySelector("#app .btn.primary"); return b ? { href: b.getAttribute("href"), text: b.textContent.trim() } : {}; })()`);
const fresh = await go();
check("a fresh topic starts with its first drill", fresh.href === `#/d/${drills06.id}/${drills06.drills[0]}` && fresh.text.startsWith("Start"), JSON.stringify(fresh));
check("the next step is named", (await p.eval(`document.querySelector(".topic-hero")?.textContent || ""`)).length > 20);

// The whole ladder stays reachable, folded: only the rung you're on is open.
check("every rung is there", (await p.eval(`document.querySelectorAll("#app details.rung").length`)) === 5);
check("only the current rung is open", (await p.eval(`[...document.querySelectorAll("#app details.rung")].map((d) => d.open ? 1 : 0).join("")`)) === "10000");
check("every problem is linked", await p.eval(`${JSON.stringify(topic06.items)}.every((n) => document.querySelector('#app a[href="#/p/' + n + '"]'))`));
check("every drill is linked", await p.eval(`${JSON.stringify(drills06.drills)}.every((d) => document.querySelector('#app a[href="#/d/${drills06.id}/' + d + '"]'))`));
check("techniques are listed", (await p.eval(`document.querySelectorAll(".tech-list .item").length`)) >= 2);
check("the lesson sheet is there", await p.eval(`!!document.querySelector("#app details.sheet")`));
check("no wall of rows", (await shown(p, "#app .item")) <= 6, String(await shown(p, "#app .item")));
check("a folded rung opens to its items", await p.eval(`(() => { const r = [...document.querySelectorAll("#app details.rung")].find((d) => !d.open && d.querySelector(".item"));
  if (!r) return false; r.querySelector("summary").click(); return r.open && [...r.querySelectorAll(".item")].every((i) => i.checkVisibility()); })()`));
check("rung markers are drawn", await p.eval(`[...document.querySelectorAll(".rung-dot")].every((d) => d.querySelector("svg") || /^[0-9]+$/.test(d.textContent.trim()))`));
check("no glyph icons on the topic page", (await glyphsIn(p, "#app .topic-hero, #app details.rung > summary, #app .item, #app details.sheet > summary, #app details.fold > summary")).length === 0,
  (await glyphsIn(p, "#app .topic-hero, #app details.rung > summary, #app .item, #app details.sheet > summary, #app details.fold > summary")).join(" | "));

// Started: the next unsolved rung is the one open, and its item is marked.
check("solve pointer_step", await solve(p, "pointer_step"));
await p.reload(BASE + "/#/t/06_two_pointers");
const started = await go();
check("Continue goes to the next unsolved problem", started.href === "#/p/count_pairs_below" && started.text.startsWith("Continue"), JSON.stringify(started));
check("its rung is the open one", await p.eval(`(() => { const open = [...document.querySelectorAll("#app details.rung")].filter((d) => d.open);
  return open.length === 1 && !!open[0].querySelector('a.item[href="#/p/count_pairs_below"]'); })()`));
check("the next item is marked in the ladder", await p.eval(`!!document.querySelector('#app a.item.next[href="#/p/count_pairs_below"]')`));
check("done rungs show a drawn check", await p.eval(`(() => { const d = document.querySelector("#app details.rung.done .rung-dot"); return !!d && !!d.querySelector("svg") && !d.textContent.trim(); })()`));
check("locked items aren't faded with opacity", await p.eval(`[...document.querySelectorAll("#app .item.locked")].every((i) => getComputedStyle(i).opacity === "1")
  && document.querySelectorAll("#app .item.locked").length > 0`));

// Where you stopped wins, so the topic page and home agree.
await p.reload(BASE + `/#/d/${drills06.id}/${drills06.drills[1]}`);
await p.reload(BASE + "/#/t/06_two_pointers");
const stop = await go();
check("the topic resumes where you stopped", stop.href === `#/d/${drills06.id}/${drills06.drills[1]}`, JSON.stringify(stop));
check("same place as home's Continue", stop.href === (await p.eval(`Trace.resumeTarget().href`)));

// A finished topic points on to the next one.
const small = data.topics.find((t) => t.id === "13_queues_and_deques");
for (const n of small.items) check(`solve ${n}`, await solve(p, n));
await p.reload(BASE + "/#/t/13_queues_and_deques");
const after = await go();
check("a finished topic leads to the next topic", after.href === "#/t/14_linked_lists", JSON.stringify(after));
check("a finished topic folds every rung", (await p.eval(`[...document.querySelectorAll("#app details.rung")].filter((d) => d.open).length`)) === 0);

// ── Study plans: the same calm, in the default stage colour ──
await p.reload(BASE + "/#/plan/blind75");
const blind = data.plans.plans.find((x) => x.id === "blind75");
const items75 = blind.sections.flatMap((s) => s.items);
check("plan leads with a stage-1 band", await p.eval(`(() => { const h = document.querySelector("#app .plan-hero"); if (!h) return false;
  const i = document.createElement("i"); i.style.color = "var(--st1)"; document.body.append(i); const want = getComputedStyle(i).color; i.remove();
  return getComputedStyle(h).backgroundColor === want; })()`));
check("one primary action on a plan", (await p.eval(`document.querySelectorAll("#app .btn.primary").length`)) === 1);
const planGo = await go();
check("the plan's button opens its next problem in plan mode", planGo.href?.endsWith("/plan/blind75") && planGo.href.startsWith("#/p/"), JSON.stringify(planGo));
check("plan sections fold", (await p.eval(`document.querySelectorAll("#app details.plan-section").length`)) === blind.sections.length);
check("only the section with the next problem is open", await p.eval(`(() => { const open = [...document.querySelectorAll("#app details.plan-section")].filter((d) => d.open);
  return open.length === 1 && !!open[0].querySelector('a.item[href="${planGo.href}"]'); })()`));
check("every plan problem is linked", (await p.eval(`new Set([...document.querySelectorAll('#app a.item[href$="/plan/blind75"]')].map((a) => a.getAttribute("href"))).size`)) === items75.length);
check("no wall of plan rows", (await shown(p, "#app .item")) <= 20, String(await shown(p, "#app .item")));
check("no faded button text", !(await p.eval(`!!document.querySelector('#app .btn [style*="opacity"]')`)));
check("no glyph icons on the plan page", (await glyphsIn(p, "#app")).length === 0, (await glyphsIn(p, "#app")).join(" | "));

// The roadmap's plan rows and extras carry drawn icons.
await p.reload(BASE + "/#/roadmap");
check("plan rows have drawn icons", await p.eval(`[...document.querySelectorAll("#plans a.topic-row")].length === 3
  && [...document.querySelectorAll("#plans a.topic-row .num")].every((n) => n.querySelector("svg"))`));
check("no glyph icons on the roadmap", (await glyphsIn(p, "#app .road-extra")).length === 0, (await glyphsIn(p, "#app .road-extra")).join(" | "));

// ── The shell: sidebar, crumbs, palette and console ──
await p.reload(BASE + "/#/t/06_two_pointers");
check("no glyph icons in the sidebar or crumbs", (await glyphsIn(p, "#side, #crumbs")).length === 0, (await glyphsIn(p, "#side, #crumbs")).join(" | "));
check("sidebar groups have a drawn chevron", await p.eval(`[...document.querySelectorAll(".side-group > button")].every((b) => b.querySelector("svg") || getComputedStyle(b, "::after").maskImage?.includes("svg"))`));
check("sidebar groups say whether they're open", await p.eval(`[...document.querySelectorAll(".side-group > button")].every((b) => ["true", "false"].includes(b.getAttribute("aria-expanded")))`));
check("crumb separators are drawn", await p.eval(`[...document.querySelectorAll("#crumbs .sep")].length > 0 && [...document.querySelectorAll("#crumbs .sep")].every((s) => s.querySelector("svg") && !s.textContent.trim())`));
await p.eval(`document.querySelector("#search-btn").click()`);
await sleep(200);
check("palette is open", await p.eval(`!document.querySelector("#palette").hidden && document.querySelectorAll("#palette-list li").length > 10`));
await p.eval(`(() => { const i = document.querySelector("#palette-input"); i.value = "blind"; i.dispatchEvent(new Event("input")); })()`);
check("palette plan entries have a drawn icon", await p.eval(`[...document.querySelectorAll("#palette-list li")].some((li) => li.textContent.includes("Blind 75") && li.querySelector(".pk svg"))`));
await p.eval(`(() => { const i = document.querySelector("#palette-input"); i.value = "pair"; i.dispatchEvent(new Event("input")); })()`);
check("palette drill and problem entries have drawn icons", await p.eval(`[...document.querySelectorAll("#palette-list li")].every((li) => li.querySelector(".pk svg") || /^[0-9]+$/.test(li.querySelector(".pk").textContent))`));
await p.eval(`(() => { const i = document.querySelector("#palette-input"); i.value = "pointer step"; i.dispatchEvent(new Event("input")); })()`);
check("a solved entry is marked with a drawn check", await p.eval(`(() => { const li = [...document.querySelectorAll("#palette-list li")].find((l) => l.textContent.includes("One pointer step"));
  return !!li && !!li.querySelector(".ps svg"); })()`));
check("no glyph icons in the palette", (await glyphsIn(p, ".palette")).length === 0, (await glyphsIn(p, ".palette")).join(" | "));
const paletteLow = { light: [], dark: [] };
for (const mode of ["light", "dark"]) {
  await p.eval(`document.documentElement.dataset.theme = "${mode}"`);
  paletteLow[mode] = await lowContrast(p, ".palette, #side");
}
check("palette and sidebar text is readable", !paletteLow.light.length && !paletteLow.dark.length, JSON.stringify(paletteLow));
await p.eval(`delete document.documentElement.dataset.theme`);
await p.eval(`document.querySelector("#palette").hidden = true`);

// A guided problem's console: one group per step, opened and closed with a drawn chevron.
await p.reload(BASE + "/#/p/count_pairs_below");
const sol = await p.eval(`fetch("/api/solution?name=count_pairs_below").then((r) => r.json()).then((s) => s.code)`);
await p.eval(`document.querySelector(".CodeMirror").CodeMirror.setValue(${JSON.stringify(sol)})`);
await p.eval(`[...document.querySelectorAll("button")].find((b) => b.textContent.includes("Run tests")).click()`);
for (let i = 0; i < 40 && (await p.eval(`document.querySelector(".console-bar .summary").textContent`)) === "Running…"; i++) await sleep(250);
await sleep(300);
check("the console groups tests by step", (await p.eval(`document.querySelectorAll(".console details.step-group").length`)) >= 1);
check("step groups have a drawn chevron", await p.eval(`[...document.querySelectorAll(".step-group > summary")].every((s) => s.querySelector("svg"))`));
check("no glyph icons in the console", (await glyphsIn(p, ".console")).length === 0, (await glyphsIn(p, ".console")).join(" | "));
check("passing tests show a drawn check", await p.eval(`[...document.querySelectorAll(".console details.test.pass .dot")].every((d) => d.querySelector("svg"))`));
check("no glyph icons in the problem's steps", (await glyphsIn(p, ".steps .step-num")).length === 0);

// ── Weights the fonts have ──
check("no stylesheet asks for a weight above 700", (await heavyRules(p)).length === 0, (await heavyRules(p)).join(" | "));
for (const page of ["", "roadmap", "t/06_two_pointers", "plan/blind75", "p/count_pairs_below"]) {
  await p.reload(BASE + "/#/" + page);
  const h = await heavy(p);
  check(`weights are ones the fonts have (${page || "home"})`, h.length === 0, h.join(" | "));
}

// ── Readable in both themes ──
for (const mode of ["light", "dark"]) {
  await p.eval(`localStorage.setItem("trace.theme", '"${mode}"')`);
  await p.reload(BASE + "/#/t/06_two_pointers");
  await p.eval(`document.querySelectorAll("#app details").forEach((d) => d.open = true)`);
  const t = await lowContrast(p, "#app .topic-hero, #app .topic-under, #app details.rung, #app details.fold, #app details.sheet > summary");
  check(`topic page text is readable (${mode})`, t.length === 0, t.join(" | "));
  await p.reload(BASE + "/#/plan/blind75");
  await p.eval(`document.querySelectorAll("#app details").forEach((d) => d.open = true)`);
  const pl = await lowContrast(p, "#app .plan-hero, #app .topic-under, #app details.plan-section");
  check(`plan page text is readable (${mode})`, pl.length === 0, pl.join(" | "));
  await p.reload(BASE + "/#/roadmap");
  const rm = await lowContrast(p, "#app .road-extra");
  check(`roadmap extras are readable (${mode})`, rm.length === 0, rm.join(" | "));
}
await p.eval(`localStorage.removeItem("trace.theme")`);

// ── Phone width ──
const phone = await open(BASE + "/#/t/06_two_pointers", { width: 390, height: 844 });
check("topic page: no sideways scroll at 390px", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`),
  String(await phone.eval(`document.querySelector("#app").scrollWidth`)));
check("topic page: the drawing comes first and the button spans the card", await phone.eval(`(() => { const h = document.querySelector(".topic-hero"); if (!h) return false;
  const art = h.querySelector("svg.art").getBoundingClientRect(), t = h.querySelector("h1").getBoundingClientRect(), b = h.querySelector(".btn.primary").getBoundingClientRect();
  return art.top < t.top && b.width > h.getBoundingClientRect().width * 0.7 && h.getBoundingClientRect().right <= 390; })()`));
await phone.reload(BASE + "/#/plan/blind75");
check("plan page: no sideways scroll at 390px", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`),
  String(await phone.eval(`document.querySelector("#app").scrollWidth`)));
await phone.close();

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
