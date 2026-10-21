// Calm home: the C3 look and stage colours, topic drawings, where you stopped, the home, the roadmap, the sidebar.
import { open, check, summary } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
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

// ── Every topic has a drawing of its data structure ──
const art = await p.eval(`Array.from({ length: 34 }, (_, k) => { const s = Trace.topicArt(k + 1);
  return { n: k + 1, kind: Trace.ART_KINDS[k + 1], svg: s instanceof SVGSVGElement, hidden: s.getAttribute("aria-hidden"),
           parts: s.querySelectorAll("[style*='--i']").length }; })`);
check("every topic has a drawing", art.every((a) => a.svg && a.hidden === "true" && a.parts >= 4),
  JSON.stringify(art.filter((a) => !(a.svg && a.hidden === "true" && a.parts >= 4))));
check("at least 15 kinds of drawing", new Set(art.map((a) => a.kind)).size >= 15, String(new Set(art.map((a) => a.kind)).size));

// ── Continue resumes where you stopped ──
const target = () => p.eval(`Trace.resumeTarget()`);
await p.eval(`localStorage.removeItem("trace.lastStop")`);    // the checks above opened pages too
await p.reload(BASE + "/#/");
const first = (await target()).href;                        // the course's next step: nothing stored yet
await p.reload(BASE + "/#/p/slide_sum");                    // topic 07's snippet: open, never locked
check("resumes the last problem opened", (await target()).href === "#/p/slide_sum", (await target()).href);
await p.reload(BASE + "/#/p/two_sum/plan/blind75");
const inPlan = await target();
check("resumes a plan problem inside its plan", inPlan.href === "#/p/two_sum/plan/blind75" && inPlan.plan?.title === "Blind 75", JSON.stringify(inPlan));
check("solve two_sum", await solve(p, "two_sum"));
check("solve slide_sum", await solve(p, "slide_sum"));
await p.reload(BASE + "/#/");
check("a solved plan problem falls back to the path", (await target()).href === first, (await target()).href);
await p.reload(BASE + "/#/p/max_sum_subarray_k");           // topic 07 solo: lock screen until the guided one is solved
check("a lock screen is not a stop", (await target()).href === first, (await target()).href);
await p.eval(`localStorage.setItem("trace.lastStop", JSON.stringify({ hash: "#/p/no_such_problem" }))`);
check("a stale stop falls back", (await target()).href === first);
await p.eval(`localStorage.setItem("trace.lastStop", "not json")`);
check("an unreadable stop falls back", (await target()).href === first);
await p.reload(BASE + "/#/d/spot-pattern/spot");
check("the review drill is not a stop", (await target()).href === first);

// ── Home: just the next step ──
const heroContrast = (page) => page.eval(`[getComputedStyle(document.querySelector(".hero h1")).color,
  getComputedStyle(document.querySelector(".hero")).backgroundColor]`).then(([fg, bg]) => contrast(page, fg, bg));
await p.reload(BASE + "/#/");
check("home has one primary action", (await p.eval(`document.querySelectorAll("#app .btn.primary").length`)) === 1);
check("Continue goes to the resume target", (await p.eval(`document.querySelector(".hero-go")?.getAttribute("href")`)) === (await target()).href);
check("Continue says Continue once you've started", (await p.eval(`document.querySelector(".hero-go")?.textContent.trim()`)) === "Continue");
check("home has the topic drawing", await p.eval(`!!document.querySelector(".hero-art svg.art")`));
check("home names the next item", (await p.eval(`document.querySelector(".hero-next")?.textContent || ""`)).includes((await target()).title));
check("home links to the roadmap", await p.eval(`!!document.querySelector('#app a[href="#/roadmap"]')`));
check("home shows no topic list or stats", await p.eval(`!document.querySelector("#app .topic-row, #app .stats, #app .topic-list")`));
check("no starting-check link once placed", !(await p.eval(`document.querySelector("#app").textContent.includes("starting check")`)));
for (const mode of ["light", "dark"]) {
  await p.eval(`document.documentElement.dataset.theme = "${mode}"`);
  const c = await heroContrast(p);
  check(`hero text is readable (${mode})`, c >= 4.5, c.toFixed(2));
}
await p.eval(`delete document.documentElement.dataset.theme`);
await p.reload(BASE + "/#/p/two_sum/plan/blind75");
check("solve contains_duplicate", await solve(p, "contains_duplicate"));
await p.reload(BASE + "/#/p/max_profit/plan/blind75");
await p.reload(BASE + "/#/");
check("a plan stop says which plan", (await p.eval(`document.querySelector(".hero")?.textContent || ""`)).includes("Blind 75"));
const done = await p.eval(`(() => { const el = document.createElement("div"); Trace.mountHome(el, { target: null, started: true, placement: true });
  return el.querySelector("h1")?.textContent; })()`);
check("finished state", done === "You've finished the course", done);
const phone = await open(BASE + "/#/", { width: 390, height: 844 });
check("no sideways scroll at 390px", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`));
check("phone: hero fits", await phone.eval(`document.querySelector(".hero").getBoundingClientRect().right <= 390`));
await phone.close();
// A learner who skipped the check and has done nothing yet sees Start.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
await p.eval(`localStorage.clear()`);
await p.reload(BASE + "/#/");
check("Start before anything is done", (await p.eval(`document.querySelector(".hero-go")?.textContent.trim()`)) === "Start");
// One with progress but no starting check is offered it, quietly.
await post(p, "/api/reset-progress", {});
check("solve two_sum after reset", await solve(p, "two_sum"));
await p.reload(BASE + "/#/");
check("offers the starting check before placement", await p.eval(`!!document.querySelector('#app a[href="#/start"]')`));
await post(p, "/api/placement", { door: "skip" });

// ── The roadmap holds the whole course ──
await p.eval(`localStorage.removeItem("trace.lastStop")`);
await p.reload(BASE + "/#/roadmap");
const here = await p.eval(`Trace.resumeTarget().topic.id`);       // no stop stored: the course position
check("six stages", (await p.eval(`document.querySelectorAll(".road-stage").length`)) === 6);
check("one current stage, open", await p.eval(`(() => { const c = document.querySelectorAll('.road-stage[data-state="current"]');
  return c.length === 1 && c[0].hasAttribute("data-open"); })()`));
check("every topic one click from the roadmap", (await p.eval(`new Set([...document.querySelectorAll("a.road-stop")].map(a => a.getAttribute("href"))).size`)) === 34);
check("You're here is the course position", (await p.eval(`document.querySelector(".road-here")?.closest("a.road-stop")?.getAttribute("href")`)) === "#/t/" + here);
check("a folded stage opens", await p.eval(`(() => { const b = document.querySelector('.road-stage:not([data-open]) .road-toggle');
  if (!b || b.getAttribute("aria-expanded") !== "false") return false;
  b.click(); return b.closest(".road-stage").hasAttribute("data-open") && b.getAttribute("aria-expanded") === "true"; })()`));
check("study plans are on the roadmap", await p.eval(`document.querySelectorAll("#plans a.topic-row").length === 3`));
check("the review drill is on the roadmap", await p.eval(`document.querySelector("#app").textContent.includes("Spot the pattern")`));
check("retake and reset are on the roadmap", await p.eval(`[...document.querySelectorAll("#app a, #app button")].some(a => /Reset all progress/.test(a.textContent))
  && !!document.querySelector('#app a[href="#/start"]')`));
check("roadmap crumb", (await p.eval(`document.querySelector("#crumbs").textContent`)).includes("Roadmap"));

// ── A quieter sidebar ──
await p.reload(BASE + "/#/");
check("sidebar links the roadmap", await p.eval(`!!document.querySelector('#side-nav a[href="#/roadmap"]')`));
check("sidebar lists one stage's topics", (await p.eval(`document.querySelectorAll('#side-nav a[href^="#/t/"]').length`)) <= 7);
check("sidebar keeps the study plans", (await p.eval(`document.querySelectorAll('#side-nav a[href^="#/plan/"]').length`)) === 3);
check("sidebar icons are drawn, not characters", await p.eval(`[...document.querySelectorAll("#side-nav .side-link .n")].every(n => n.querySelector("svg") || /^[0-9]+$/.test(n.textContent.trim()))`));
await p.reload(BASE + "/#/t/30_number_theory");
check("the viewed topic is in the sidebar", await p.eval(`!!document.querySelector('#side-nav a[href="#/t/30_number_theory"][aria-current="page"]')`));


// ── Review fixes ──
const lum = (page, c) => page.eval(`(() => { const el = document.createElement("i"); el.style.color = ${JSON.stringify(c)}; document.body.append(el);
  const v = getComputedStyle(el).color.match(/[0-9.]+/g).slice(0, 3).map(Number); el.remove();
  return v.map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }).reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0); })()`);
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
await p.eval(`localStorage.clear()`);
await p.reload(BASE + "/#/");
const course = (await target()).href;                          // the course's next step after a fresh start

// A stored stop on a locked problem never sends you to a lock screen.
await p.eval(`localStorage.setItem("trace.lastStop", JSON.stringify({ hash: "#/p/max_sum_subarray_k" }))`);
check("a locked stop falls back", (await target()).href === course, (await target()).href);
// Odd stored names never break home.
for (const hash of ["#/d/constructor/x", "#/p/constructor", "#/w/toString"]) {
  await p.eval(`localStorage.setItem("trace.lastStop", JSON.stringify({ hash: ${JSON.stringify(hash)} }))`);
  check(`stop ${hash} falls back`, await p.eval(`(() => { try { return Trace.resumeTarget().href; } catch (e) { return "threw " + e.message; } })()`) === course);
}
// Reset forgets where you stopped.
await p.reload(BASE + "/#/p/slide_sum");
await p.reload(BASE + "/#/roadmap");
await p.eval(`(() => { const b = [...document.querySelectorAll("#app button")].find((x) => /Reset all progress/.test(x.textContent)); b.click(); b.click(); })()`);
await new Promise((r) => setTimeout(r, 800));
check("reset forgets where you stopped", (await p.eval(`localStorage.getItem("trace.lastStop")`)) === null);
await post(p, "/api/placement", { door: "skip" });

// "You're here" follows where Continue goes, unless that's a study-plan detour.
await p.reload(BASE + "/#/p/slide_sum");
await p.reload(BASE + "/#/roadmap");
check("You're here follows the resume point", (await p.eval(`document.querySelector(".road-here")?.closest("a")?.getAttribute("href")`)) === "#/t/07_sliding_window");
await p.reload(BASE + "/#/");
check("sidebar shows the resume point's stage", await p.eval(`!!document.querySelector('#side-nav a[href="#/t/07_sliding_window"]')`));
await p.reload(BASE + "/#/p/two_sum/plan/blind75");
await p.reload(BASE + "/#/roadmap");
const pathTopic = await p.eval(`(() => { const keep = localStorage.getItem("trace.lastStop"); localStorage.removeItem("trace.lastStop");
  const id = Trace.resumeTarget().topic.id; localStorage.setItem("trace.lastStop", keep); return id; })()`);
check("a plan detour doesn't move You're here", (await p.eval(`document.querySelector(".road-here")?.closest("a")?.getAttribute("href")`)) === "#/t/" + pathTopic, pathTopic);

// The sidebar doesn't count problems you haven't started.
await p.reload(BASE + "/#/");
check("no zero counts in the sidebar", await p.eval(`![...document.querySelectorAll("#side-nav .side-link .f")].some((f) => f.textContent.startsWith("0/"))`));
// Walkthrough pages keep their topic in the sidebar.
const wt = await p.eval(`fetch("/api/course").then((r) => r.json()).then((d) => d.topics.filter((t) => t.has_walkthrough).map((t) => t.id).at(-1))`);
await p.reload(BASE + "/#/w/" + wt);
check("walkthrough topic is in the sidebar", await p.eval(`!!document.querySelector('#side-nav a[href="#/t/${wt}"][aria-current="page"]')`), wt);

// The starting check's result links to the roadmap, not the one-card home.
const links = await p.eval(`(async () => {
  const el = document.createElement("div");
  const q = { question: "q", options: ["a", "b"], answer: 0, explain: "e" };
  Trace.mountStart(el, { ready: [], topics: [{ id: "06_two_pointers", stage_n: 2, questions: [q, q] }] },
    { place: async () => ({ placement: { start: "06_two_pointers", placed_out: [] } }), topicTitle: (id) => id, startHref: () => "#/t/06_two_pointers" });
  el.querySelectorAll(".door")[2].click();
  [...el.querySelectorAll("button")].find((b) => b.textContent === "Stop here").click();
  await new Promise((r) => setTimeout(r, 50));
  return [...el.querySelectorAll("a")].map((a) => a.textContent + " -> " + a.getAttribute("href")); })()`);
check("starting check result links to the roadmap", links.some((l) => l.endsWith("-> #/roadmap")) && !links.some((l) => l.endsWith("-> #/")), links.join(" | "));

// Finished home points to the review drill too.
check("finished home links the review drill", await p.eval(`(() => { const el = document.createElement("div");
  Trace.mountHome(el, { target: null, started: true, placement: true }); return !!el.querySelector('a[href^="#/d/spot-pattern"]'); })()`));

// Every topic draws itself, not a neighbour's picture.
// Faded notes in drawings still read at 4.5:1: no opacity, and the colour itself passes on every stage.
check("drawing notes are never faded by opacity", await p.eval(`(() => { const box = document.createElement("div"); box.dataset.stage = "2";
  box.append(Trace.topicArt(11)); document.body.append(box);
  const ok = [...box.querySelectorAll(".a-note")].every((n) => getComputedStyle(n).opacity === "1"); box.remove(); return ok; })()`));
check("34 different drawings", (await p.eval(`new Set(Object.values(Trace.ART_KINDS)).size`)) === 34);

// Home: the drawing leads; only the button looks pressable; the kind follows the title.
await p.reload(BASE + "/#/");
check("hero card has no pressed edge", (await p.eval(`getComputedStyle(document.querySelector(".hero")).boxShadow`)) === "none");
check("the drawing is large", await p.eval(`document.querySelector(".hero-art svg").getBoundingClientRect().width >= 0.45 * document.querySelector(".hero").getBoundingClientRect().width`));
check("the drawing is cropped to what it shows", await p.eval(`(() => { const v = document.querySelector(".hero-art svg").viewBox.baseVal; return v.width < 320 || v.height < 200; })()`));
check("the next item's title comes first", await p.eval(`document.querySelector(".hero-next").firstElementChild?.tagName === "STRONG"`));
await p.reload(BASE + "/#/roadmap");
check("stage markers don't look pressable", await p.eval(`[...document.querySelectorAll(".road-marker")].every((m) => getComputedStyle(m).boxShadow === "none")`));
check("folded stages wear their own colour", await p.eval(`(() => { const li = document.querySelector('.road-stage[data-state="ahead"]');
  const probe = document.createElement("i"); probe.style.color = "var(--stage-soft)"; li.append(probe);
  const want = getComputedStyle(probe).color; probe.remove();
  return getComputedStyle(li.querySelector(".road-marker")).backgroundColor === want; })()`));

// Dark: stage colours are deepened, and done checks stay visible.
for (let n = 1; n <= 6; n++) {
  await p.eval(`document.documentElement.dataset.theme = "light"`); const light = await lum(p, `var(--st${n})`);
  await p.eval(`document.documentElement.dataset.theme = "dark"`); const dark = await lum(p, `var(--st${n})`);
  check(`stage ${n} is deeper in dark`, dark <= light, `${light.toFixed(3)} -> ${dark.toFixed(3)}`);
}
for (const mode of ["light", "dark"]) {
  await p.eval(`document.documentElement.dataset.theme = "${mode}"`);
  const c = await contrast(p, "var(--on-ok)", "var(--ok)");
  check(`done check is visible (${mode})`, c >= 3, c.toFixed(2));
}
await p.eval(`delete document.documentElement.dataset.theme`);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
