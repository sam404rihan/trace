// The drill, "Read the code" and starting-check pages in the design system: no eyebrow labels, drawn icons,
// the stage colour on drill boards, chunky buttons that press, and everything still answers, records and places.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const get = (p, path) => p.eval(`fetch("${path}").then(r => r.json())`);

// Page-side helpers: contrast of a real element against what it sits on, eyebrow labels, glyph icons.
const HELP = `
  const rgb = (c) => { const el = document.createElement("i"); el.style.color = c; document.body.append(el);
    const v = getComputedStyle(el).color.match(/[0-9.]+/g).map(Number); el.remove(); return v; };
  const lum = ([r, g, b]) => [r, g, b].map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; })
    .reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0);
  const ratio = (fg, bg) => { const [a, b] = [lum(rgb(fg)), lum(rgb(bg))].sort((x, y) => y - x); return (a + 0.05) / (b + 0.05); };
  const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor;
    const v = c.match(/[0-9.]+/g).map(Number); if (v.length < 4 || v[3] > 0.99) return c; } return getComputedStyle(document.body).backgroundColor; };
  const pair = (sel) => { const el = typeof sel === "string" ? document.querySelector(sel) : sel; return el ? ratio(getComputedStyle(el).color, bgOf(el)) : -1; };
  const labelsAbove = () => [...document.querySelectorAll("#app h1, #app h2")].filter((hd) => {
    const p = hd.previousElementSibling; if (!p) return false; const t = p.textContent.trim();
    return t && t.length < 60 && !p.matches("nav, ol, ul, pre, figure, section, .btn") && !p.querySelector("a, button, input")
      && parseFloat(getComputedStyle(p).fontSize) < parseFloat(getComputedStyle(hd).fontSize); }).map((hd) => hd.textContent);
  const GLYPHS = [..."♛♕✓✔✗✘✕✖▾▸▴▶◀►◄›‹»«★☆●○◆◇■□▲▼⟶➜➔✚✎"];
  const glyphs = () => { const found = []; const w = document.createTreeWalker(document.querySelector("#app"), NodeFilter.SHOW_TEXT);
    while (w.nextNode()) for (const g of GLYPHS) if (w.currentNode.textContent.includes(g)) found.push(g);
    for (const el of document.querySelectorAll("#app *")) for (const pe of ["::before", "::after"]) {
      const c = getComputedStyle(el, pe).content; if (c && c !== "none" && GLYPHS.some((g) => c.includes(g))) found.push(c); }
    return found; };
`;
const ev = (p, expr) => p.eval(`(() => { ${HELP} return (${expr}); })()`);
const noEyebrows = async (p, where) => {
  const above = await ev(p, `labelsAbove()`);
  check(`${where}: no label above a heading`, above.length === 0 && await ev(p, `!document.querySelector(".wt-label, .start-label, .eyebrow, .kicker")`), above.join(" | "));
  const g = await ev(p, `glyphs()`);
  check(`${where}: icons are drawn, not characters`, g.length === 0, g.join(" "));
};
const themes = async (p, fn) => {
  for (const mode of ["light", "dark"]) { await p.eval(`document.documentElement.dataset.theme = "${mode}"`); await fn(mode); }
  await p.eval(`delete document.documentElement.dataset.theme`);
};
const readable = (name, pairs) => {
  const bad = Object.entries(pairs).filter(([, v]) => !(v >= 4.5));
  check(name, bad.length === 0, bad.map(([k, v]) => `${k} ${v.toFixed ? v.toFixed(2) : v}`).join(", ") || "all >= 4.5");
};
const noSideways = (p) => p.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// ── Intuition drills ──────────────────────────────────────────────────────────
await p.reload(BASE + "/#/d/two-pointers/pair-sum");
const state = () => p.eval(`document.querySelector(".board").parentElement.drillState()`);
check("drill page wears its stage", (await p.eval(`document.body.dataset.stage`)) === "2");
await noEyebrows(p, "drill");
check("drill: the subtitle sits below the title", await p.eval(`document.querySelector(".drill-top h1 + .drill-sub")?.textContent.includes("Intuition drills")`));
const probe = (v) => `(() => { const i = document.createElement("i"); i.style.color = "${v}"; document.body.append(i); const c = getComputedStyle(i).color; i.remove(); return c; })()`;
check("the board is tinted in the stage colour", await p.eval(`getComputedStyle(document.querySelector(".board")).backgroundColor === ${probe("var(--stage-soft)")}`));
check("the your-move console is the stage colour", await p.eval(`getComputedStyle(document.querySelector(".dconsole")).backgroundColor === ${probe("var(--stage)")}`));
check("array cells are drawn tiles with an edge", await p.eval(`(() => { const c = getComputedStyle(document.querySelector(".board .cell"));
  return parseFloat(c.borderTopLeftRadius) >= 6 && c.boxShadow !== "none" && c.borderTopStyle === "none"; })()`));
check("option buttons have a pressed edge", await p.eval(`getComputedStyle(document.querySelector(".dconsole .opt")).boxShadow !== "none"`));
check("option buttons press down", await p.eval(`[...document.styleSheets].flatMap((s) => [...s.cssRules]).some((r) => /\\.dconsole \\.opt[^,]*:active/.test(r.selectorText || ""))`));

// Answer by click and by number key; a wrong key is a slip.
const indexOf = async () => { const st = await state(); return st.options ? st.options.indexOf(String(Array.isArray(st.answer) ? st.answer[0] : st.answer)) : -1; };
let st0 = await state(), i = await indexOf();
await p.eval(`document.querySelector('.options [data-i="${i}"]').click()`);
await sleep(120);
let st1 = await state();
check("a drill answers by click", st1.steps === st0.steps + 1 && st1.slips === 0, JSON.stringify([st0, st1]));
for (let guard = 0; guard < 10 && (await state()).playing; guard++) await sleep(250);
i = await indexOf();
st0 = await state();
await p.key(String(i + 1));
st1 = await state();
check("a drill answers by number key", i >= 0 && st1.steps === st0.steps + 1 && st1.slips === 0, JSON.stringify([i, st0, st1]));
for (let guard = 0; guard < 10 && (await state()).playing; guard++) await sleep(250);
i = await indexOf();
const n = (await state()).options.length;
await p.key(String(((i + 1) % n) + 1));
check("a wrong key is a slip", (await state()).slips === 1 && await p.eval(`!!document.querySelector(".options .opt.miss")`));
const fb = await ev(p, `[pair(".feedback.bad"), getComputedStyle(document.querySelector(".feedback.bad")).backgroundColor !== getComputedStyle(document.querySelector(".dconsole")).backgroundColor]`);
check("a slip's reason sits in its own box", fb[1] && fb[0] >= 4.5, fb[0].toFixed(2));
await p.key("n");                                   // a new example starts a fresh run

// A clean run, answered the way a fluent learner would, records and celebrates.
async function cleanRun() {
  for (let guard = 0; guard < 80; guard++) {
    const st = await state();
    if (st.done) return st;
    if (st.playing) { await sleep(250); continue; }
    const want = String(Array.isArray(st.answer) ? st.answer[0] : st.answer);
    const k = (st.options || []).indexOf(want);
    if (k >= 0 && k < 9 && guard % 2) await p.key(String(k + 1));
    else await p.eval(`(() => { const el = ${k} >= 0 ? document.querySelector('.options [data-i="${k}"]') : document.querySelector('[data-pick="${want}"]');
      el.dispatchEvent(new MouseEvent("click", { bubbles: true })); })()`);
    await sleep(60);
  }
  return null;
}
const done = await cleanRun();
check("a clean run finishes", done && done.slips === 0, JSON.stringify(done));
check("a clean run says so", (await p.eval(`document.querySelector(".dprompt .result")?.textContent`)) === "Clean run.");
check("a clean run is recorded", (await p.eval(`JSON.parse(localStorage.getItem("trace.v1")).drills["two-pointers/pair-sum"].clean`)) === 1);
check("a clean run gets a drawn check mark", await p.eval(`!!document.querySelector(".dprompt .clean-mark svg")`));
check("a clean run shows the way to solid", (await p.eval(`document.querySelectorAll(".dprompt .solid-track i").length`)) === 2
  && (await p.eval(`document.querySelectorAll(".dprompt .solid-track i.on").length`)) === 1);
check("the tab counts the clean run", (await p.eval(`document.querySelectorAll('.drill-tab[aria-selected="true"] .pips i.on').length`)) === 1);

// Every text pair on the board and in the console, on every stage, in both themes.
const pairs = { light: {}, dark: {} };
await themes(p, async (mode) => {
  for (let s = 1; s <= 6; s++) {
    await p.eval(`document.body.dataset.stage = "${s}"`);
    Object.assign(pairs[mode], await ev(p, `({
      "s${s} result": pair(".dprompt .result"), "s${s} summary": pair(".dprompt .summary"), "s${s} next": pair(".options .opt.primary span"),
      "s${s} next key": pair(".options .opt.primary kbd"), "s${s} tool": pair(".dtools .btn"),
    })`));
  }
});
await p.key("n");
await themes(p, async (mode) => {
  for (let s = 1; s <= 6; s++) {
    await p.eval(`document.body.dataset.stage = "${s}"`);
    Object.assign(pairs[mode], await ev(p, `(() => { const board = bgOf(document.querySelector(".board")); const out = {
      "s${s} blurb": pair(".blurb"), "s${s} index": pair(".board .idx"), "s${s} cell": pair(".board .cell"), "s${s} pointer": pair(".board .ptr"),
      "s${s} line": pair(".board .line"), "s${s} prompt": pair(".dprompt p"), "s${s} option": pair(".options .opt span"),
      "s${s} key": pair(".options .opt kbd") };
      for (const m of ["pa", "pb", "pc", "pd"]) out["s${s} " + m + " on board"] = ratio("var(--" + m + ")", board);
      const c = document.querySelector(".dconsole");
      for (const t of ["ok", "bad", "hint"]) { const f = document.createElement("p"); f.className = "feedback " + t; f.textContent = "x"; c.append(f); out["s${s} feedback " + t] = pair(f); f.remove(); }
      const sl = document.createElement("span"); sl.className = "slips"; sl.textContent = "1 slip"; document.querySelector(".dtools").append(sl); out["s${s} slips"] = pair(sl); sl.remove();
      return out; })()`));
  }
  readable(`drill text is readable on every stage (${mode})`, pairs[mode]);
});
await p.eval(`document.body.dataset.stage = "2"`);

// Trees and graphs draw their nodes as tiles; the queens are drawn, not typed.
await p.reload(BASE + "/#/d/trees/traverse");
check("tree nodes are drawn tiles", await p.eval(`getComputedStyle(document.querySelector(".board .node circle")).filter !== "none"`));
check("a tree node answers by click", await p.eval(`(() => { const st = document.querySelector(".board").parentElement.drillState();
  document.querySelector('[data-pick="' + st.answer + '"]').dispatchEvent(new MouseEvent("click", { bubbles: true }));
  return document.querySelector(".board").parentElement.drillState().steps === st.steps + 1; })()`));
check("a queen is a drawn piece", await p.eval(`(() => { const g = Trace.V.grid(1, 2, (r, c) => (c ? { t: "\u265b", cls: "queen" } : {}));
  return !g.textContent.includes("\u265b") && !!g.querySelector(".queen svg"); })()`));
await noEyebrows(p, "tree drill");
const phone = await open(BASE + "/#/d/two-pointers/pair-sum", { width: 390, height: 844 });
check("drill: no sideways scroll at 390px", await noSideways(phone));
await phone.go(BASE + "/#/d/weighted/dijkstra");
check("graph drill: no sideways scroll at 390px", await noSideways(phone));

// ── Read the code ─────────────────────────────────────────────────────────────
const WT = "07_sliding_window";
const wt = await get(p, `/api/walkthrough?topic=${WT}`);
await p.reload(BASE + "/#/w/" + WT);
await noEyebrows(p, "walkthrough");
check("walkthrough: the layer sits below the title", await p.eval(`document.querySelector(".wt-page h1 + .wt-meta")?.textContent.includes("Layer 1 of")`));
check("walkthrough: a track shows the layers", (await p.eval(`document.querySelectorAll(".wt-track i").length`)) === wt.layers.length);
check("walkthrough: code has line numbers", await p.eval(`(() => { const ln = [...document.querySelectorAll(".wt-code .ln")];
  return ln.length > 3 && ln.every((l, k) => l.querySelector(".no")?.textContent === String(k + 1)); })()`));
check("walkthrough: new lines are marked", await p.eval(`document.querySelectorAll(".wt-code .ln.add").length > 0 && !!document.querySelector(".wt-key")`));
check("walkthrough: copying code leaves out the numbers", await p.eval(`document.querySelector(".wt-code .no") && getComputedStyle(document.querySelector(".wt-code .no")).userSelect === "none"`));
check("walkthrough: Run sits with the code", await p.eval(`!!document.querySelector(".wt-codecard .wt-run button")`));
check("walkthrough: the check is a heading", await p.eval(`document.querySelector(".wt-check h2")?.textContent.length > 5`));
check("walkthrough: options have a pressed edge", await p.eval(`getComputedStyle(document.querySelector(".wt-opts .opt")).boxShadow !== "none"`));
await p.key(String(wt.layers[0].check.answer + 1));
check("walkthrough: a number key answers", (await p.eval(`document.querySelector(".wt-explain")?.textContent || ""`)).startsWith("Right."));
await sleep(400);
check("walkthrough: the answer is recorded", (await get(p, "/api/course")).progress.walkthroughs[WT] === 1);
await p.eval(`document.querySelector(".wt-nav .btn.primary").click()`);
check("walkthrough: Continue reveals the next layer", (await p.eval(`document.querySelector(".wt-page h1").textContent`)) === wt.layers[1].title);
check("walkthrough: the track moves on", (await p.eval(`[...document.querySelectorAll(".wt-track i")].map((x) => x.className).join(" ")`)) .startsWith("done here"));
await themes(p, async (mode) => {
  const pairs = await ev(p, `({ title: pair(".wt-page h1"), meta: pair(".wt-meta"), why: pair(".wt-why p"), code: pair(".wt-code .ln .tx"),
    added: pair(".wt-code .ln.add .tx"), number: pair(".wt-code .ln .no"), "added number": pair(".wt-code .ln.add .no"), key: pair(".wt-key"),
    question: pair(".wt-check h2"), option: pair(".wt-opts .opt span"), "option key": pair(".wt-opts .opt kbd") })`);
  readable(`walkthrough text is readable (${mode})`, pairs);
});
const reuse = wt.layers.findIndex((l) => l.reuse);
if (reuse > 0) {
  await p.eval(`(async () => { for (let k = 1; k < ${reuse}; k++) {
    document.querySelector('.wt-opts [data-i="' + ${JSON.stringify(wt.layers.map((l) => l.check.answer))}[k] + '"]').click();
    document.querySelector(".wt-nav .btn.primary").click(); } })()`);
  await sleep(300);
  await noEyebrows(p, "walkthrough reuse layer");
  check("walkthrough: a reuse layer says so below the title", (await p.eval(`document.querySelector(".wt-meta")?.textContent || ""`)).includes("Same skeleton"));
  await themes(p, async (mode) => readable(`walkthrough roles are readable (${mode})`,
    await ev(p, `Object.fromEntries([...document.querySelectorAll(".wt-legend span")].map((s, k) => ["role " + k, pair(s)]))`)));
}
await phone.go(BASE + "/#/w/" + WT);
check("walkthrough: no sideways scroll at 390px", await noSideways(phone));

// ── The starting check ───────────────────────────────────────────────────────
const sc = await get(p, "/api/starting-check");
await p.reload(BASE + "/#/start");
await noEyebrows(p, "starting check");
check("doors are drawn and press", await p.eval(`(() => { const d = [...document.querySelectorAll(".door")];
  return d.length === 3 && d.every((x) => x.tagName === "BUTTON" && x.querySelector("svg") && getComputedStyle(x).boxShadow !== "none"); })()`));
await themes(p, async (mode) => readable(`doors are readable (${mode})`,
  await ev(p, `({ title: pair(".start-page h1"), lede: pair(".start-page .lede"), door: pair(".door strong"), sub: pair(".door .door-sub"), skip: pair(".start-skip .link") })`)));
await p.eval(`document.querySelectorAll(".door")[2].click()`);
await noEyebrows(p, "starting-check question");
check("the question is the heading", (await p.eval(`document.querySelector(".start-page h1")?.textContent`)) === sc.topics[0].questions[0].question.replace(/`/g, ""));
check("where you are sits below the question", (await p.eval(`document.querySelector(".start-page h1 + .start-sub")?.textContent || ""`)).includes("question 1"));
await p.key(String(sc.topics[0].questions[0].answer + 1));
check("a number key answers", (await p.eval(`document.querySelector(".wt-explain").textContent`)).startsWith("Right."));
await themes(p, async (mode) => readable(`a question is readable (${mode})`,
  await ev(p, `({ sub: pair(".start-sub"), option: pair(".wt-opts .opt span"), right: pair(".wt-opts .opt.right span"), explain: pair(".wt-explain") })`)));
await p.eval(`document.querySelector(".wt-nav .btn.primary").click()`);
const q1 = sc.topics[1].questions[0];
await p.key(String(((q1.answer + 1) % q1.options.length) + 1));
await p.eval(`document.querySelector(".wt-nav .btn.primary").click()`);
await p.eval(`[...document.querySelectorAll(".wt-nav button")].find((b) => b.textContent === "Stop here").click()`);
await sleep(600);
const placed = (await get(p, "/api/course")).progress.placement;
check("the check places you", placed?.start === sc.topics[1].id && placed.placed_out.includes(sc.topics[0].id), JSON.stringify(placed));
await noEyebrows(p, "starting-check result");
check("the result draws where you start", await p.eval(`!!document.querySelector(".start-card svg.art")`));
check("the result starts you there", await p.eval(`document.querySelector(".start-card .btn")?.getAttribute("href")?.startsWith("#/")`));
check("placed-out topics are listed under a heading", await p.eval(`document.querySelector(".start-placed h2 + ul li")?.textContent.length > 0`));
await themes(p, async (mode) => readable(`the result is readable (${mode})`,
  await ev(p, `({ card: pair(".start-card h2"), line: pair(".start-card p"), button: pair(".start-card .btn"), placed: pair(".start-placed li") })`)));
await phone.go(BASE + "/#/start");
check("starting check: no sideways scroll at 390px", await noSideways(phone));
await phone.close();

// Python door: missing basics suggests a course first, and the newcomer page lists skills and courses.
await p.reload(BASE + "/#/start");
await p.eval(`document.querySelectorAll(".door")[1].click()`);
for (const q of sc.ready) {
  await p.key(String(((q.answer + 1) % q.options.length) + 1));
  await p.eval(`document.querySelector(".wt-nav .btn.primary").click()`);
}
check("missing basics suggests Python first", (await p.eval(`document.querySelector(".start-page h1")?.textContent || ""`)).startsWith("You missed"));
await noEyebrows(p, "python suggestion");
await p.eval(`document.querySelector(".start-actions .btn.primary").click()`);
await sleep(500);
check("the newcomer page", (await p.eval(`document.querySelector(".start-page h1")?.textContent`)) === "Start with Python");
await noEyebrows(p, "newcomer page");
check("ready skills are drawn checks", await p.eval(`[...document.querySelectorAll(".start-skills li")].every((li) => li.querySelector("svg"))`));

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
