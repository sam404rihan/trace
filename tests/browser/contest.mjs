// Contest mode: a timed set of problems in a fullscreen that stays locked until you submit.
// Headless Chrome won't grant fullscreen without a real gesture, so the lock is checked by stubbing
// document.fullscreenElement and dispatching fullscreenchange; the clock is advanced through Trace.now.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const hash = (p) => p.eval(`location.hash`);
const shown = (p, sel) => p.eval(`(() => { const el = document.querySelector(${JSON.stringify(sel)}); return !!el && getComputedStyle(el).display !== "none" && !el.closest("[hidden]"); })()`);
const contrast = (p, sel) => p.eval(`(() => {
  const el = document.querySelector(${JSON.stringify(sel)});
  const rgb = (c) => c.match(/[0-9.]+/g).slice(0, 3).map(Number);
  const lum = ([r, g, b]) => [r, g, b].map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; })
    .reduce((s, x, i) => s + x * [0.2126, 0.7152, 0.0722][i], 0);
  let bg = "rgba(0, 0, 0, 0)", n = el;
  while (n && /rgba\\(0, 0, 0, 0\\)|transparent/.test(bg)) { bg = getComputedStyle(n).backgroundColor; n = n.parentElement; }
  if (/rgba\\(0, 0, 0, 0\\)/.test(bg)) bg = getComputedStyle(document.body).backgroundColor;
  const [a, b] = [lum(rgb(getComputedStyle(el).color)), lum(rgb(bg))].sort((x, y) => y - x);
  return (a + 0.05) / (b + 0.05); })()`);
// Fullscreen, simulated: window.__fs is the fullscreen element; request and exit flip it and fire the event.
const STUB_FS = `(() => {
  Object.defineProperty(document, "fullscreenElement", { configurable: true, get: () => window.__fs || null });
  document.documentElement.requestFullscreen = () => { window.__fs = document.documentElement; document.dispatchEvent(new Event("fullscreenchange")); return Promise.resolve(); };
  document.exitFullscreen = () => { window.__exited = (window.__exited || 0) + 1; window.__fs = null; document.dispatchEvent(new Event("fullscreenchange")); return Promise.resolve(); };
})()`;
const fsEnter = `(() => { window.__fs = document.documentElement; document.dispatchEvent(new Event("fullscreenchange")); })()`;
const fsLeave = `(() => { window.__fs = null; document.dispatchEvent(new Event("fullscreenchange")); })()`;
const stored = (p) => p.eval(`(() => { try { return JSON.parse(localStorage.getItem("trace.contest")); } catch { return "unreadable"; } })()`);
const history = (p) => p.eval(`(() => { try { return JSON.parse(localStorage.getItem("trace.contests")) || []; } catch { return "unreadable"; } })()`);
async function waitRun(p) {
  await sleep(300);
  for (let i = 0; i < 60 && (await p.eval(`document.querySelector(".console-bar .summary")?.textContent`)) === "Running…"; i++) await sleep(250);
  await sleep(300);
}
async function start(p, minutes, scope = "started") {
  await p.reload(BASE + "/#/contest");
  await p.eval(`document.querySelector('input[name="minutes"][value="${minutes}"]').click()`);
  await p.eval(`document.querySelector('input[name="scope"][value="${scope}"]').click()`);
  await p.eval(`document.querySelector(".contest-start").click()`);
  await sleep(1500);
}

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });
const course = await p.eval(`fetch("/api/course").then(r => r.json()).then(d => ({
  problems: Object.fromEntries(Object.entries(d.problems).map(([k, v]) => [k, { kind: v.kind, difficulty: v.difficulty, topic: v.topic_id }])),
  stage: Object.fromEntries(d.topics.map(t => [t.id, t.stage_n])) }))`);
const RANK = { easy: 0, medium: 1, hard: 2 };
const rising = (names) => names.every((n, i) => !i || RANK[course.problems[names[i - 1]].difficulty] <= RANK[course.problems[n].difficulty]);

// ── Tucked away: the sidebar and the roadmap, never home ──
await p.reload(BASE + "/#/");
check("home has no contest link", await p.eval(`!document.querySelector('#app a[href="#/contest"]')`));
check("sidebar links the contest with a drawn icon", await p.eval(`!!document.querySelector('#side-nav a[href="#/contest"] .n svg')`));
check("sidebar contest link sits with Home and Roadmap", await p.eval(`(() => { const a = document.querySelector('#side-nav a[href="#/contest"]');
  return !!a && !!a.parentElement.querySelector('a[href="#/roadmap"]'); })()`));
await p.reload(BASE + "/#/roadmap");
check("roadmap has a contest section", await p.eval(`!!document.querySelector('#app section a[href="#/contest"]')`));
check("roadmap contest row uses a drawn icon", await p.eval(`!!document.querySelector('#app a[href="#/contest"] svg')`));

// ── The draw: three problems, rising in difficulty ──
const draws = await p.eval(`Array.from({ length: 12 }, () => Trace.drawContest("started", 90))`);
check("a draw is three different problems", draws.every((d) => d.length === 3 && new Set(d).size === 3), JSON.stringify(draws[0]));
check("drawn problems are standalone problems", draws.flat().every((n) => course.problems[n]?.kind === "solo"));
check("drawn problems rise in difficulty", draws.every(rising), JSON.stringify(draws.find((d) => !rising(d))));
check("a new learner draws from the early topics", draws.flat().every((n) => course.stage[course.problems[n].topic] === 1),
  JSON.stringify(draws.flat().filter((n) => course.stage[course.problems[n].topic] !== 1)));
const short = await p.eval(`Array.from({ length: 12 }, () => Trace.drawContest("started", 30))`);
check("a 30-minute contest has no hard problem", short.flat().every((n) => course.problems[n].difficulty !== "hard"));
const whole = await p.eval(`Array.from({ length: 12 }, () => Trace.drawContest("all", 60))`);
check("the whole course reaches past the first stage", whole.flat().some((n) => course.stage[course.problems[n].topic] > 1));
check("solve slide_sum", await solve(p, "slide_sum"));       // topic 07 is now started
await p.reload(BASE + "/#/");
const started = await p.eval(`Array.from({ length: 12 }, () => Trace.drawContest("started", 60))`);
check("started topics are drawn from", started.flat().every((n) => course.problems[n].topic === "07_sliding_window"),
  JSON.stringify(started.flat().filter((n) => course.problems[n].topic !== "07_sliding_window")));

// ── Setup: few, plain choices ──
await p.reload(BASE + "/#/contest");
check("contest page crumb", (await p.eval(`document.querySelector("#crumbs").textContent`)).includes("Contest"));
check("three lengths, 60 minutes by default", await p.eval(`(() => { const r = [...document.querySelectorAll('input[name="minutes"]')];
  return r.map((x) => x.value).join() === "30,60,90" && r.find((x) => x.checked)?.value === "60"; })()`));
check("started topics by default, whole course on offer", await p.eval(`(() => { const r = [...document.querySelectorAll('input[name="scope"]')];
  return r.map((x) => x.value).join() === "started,all" && r.find((x) => x.checked)?.value === "started"; })()`));
check("choices have visible labels", await p.eval(`[...document.querySelectorAll('.contest-setup input[type="radio"]')].every((x) => x.closest("label")?.textContent.trim())`));
check("one Start button", await p.eval(`document.querySelectorAll("#app .btn.primary").length === 1 && !!document.querySelector(".contest-start")`));
check("no past contests yet", await p.eval(`!document.querySelector(".contest-history a")`));

// ── Running ──
await p.eval(`window.__dialogs = 0; window.alert = window.confirm = window.prompt = () => { window.__dialogs++; return true; }`);
await p.eval(`document.querySelector(".contest-start").click()`);
await sleep(1500);
const state = await stored(p);
const names = state?.problems?.map((x) => x.name) || [];
check("Start opens the first problem in contest mode", (await hash(p)) === `#/p/${names[0]}/contest`, await hash(p));
check("the contest is stored locally", names.length === 3 && rising(names), JSON.stringify(names));
check("the sidebar is hidden", await p.eval(`getComputedStyle(document.querySelector(".side")).display === "none"`));
check("breadcrumbs are hidden", await p.eval(`getComputedStyle(document.querySelector(".main > .bar")).display === "none"`));
check("contest bar with three problem tabs", await p.eval(`document.querySelectorAll(".contest-bar .contest-tab").length === 3`));
check("the current tab is marked", await p.eval(`document.querySelector(".contest-tab[aria-current='page']")?.getAttribute("href") === location.hash`));
check("the countdown shows the length", /^(59|60):[0-9][0-9]$/.test(await p.eval(`document.querySelector(".contest-clock [data-contest-clock]")?.textContent`)),
  await p.eval(`document.querySelector(".contest-clock")?.textContent`));
check("Submit is in the bar", await p.eval(`!!document.querySelector(".contest-bar .contest-submit")`));
check("ladder locks don't apply", await p.eval(`!!document.querySelector(".CodeMirror") && document.querySelector(".CodeMirror").CodeMirror.getOption("readOnly") === false
  && ![...document.querySelectorAll("#app button")].some((b) => b.textContent.includes("Open anyway"))`));
check("no reference solution in a contest", await p.eval(`![...document.querySelectorAll(".pane-left .tab")].some((t) => t.textContent.includes("Solution"))`));
check("no topic link out of the contest", await p.eval(`!document.querySelector(".pane-left a.ws-topic")`));
check("statement and Run tests are there", await p.eval(`!!document.querySelector(".statement h1") && [...document.querySelectorAll("button")].some((b) => b.textContent.includes("Run tests"))`));

// Ctrl+Enter still runs; a run marks the tab tried, a pass marks it solved.
await p.eval(`document.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", ctrlKey: true, bubbles: true }))`);
await waitRun(p);
check("Ctrl+Enter runs the tests", (await p.eval(`document.querySelector(".console-bar .summary").textContent`)) !== "", await p.eval(`document.querySelector(".console-bar .summary").textContent`));
check("a run marks the problem tried", (await p.eval(`document.querySelector(".contest-tab[aria-current='page']").dataset.state`)) === "tried");
const sol = await p.eval(`fetch("/api/solution?name=${names[0]}").then((r) => r.json()).then((s) => s.code)`);
await p.eval(`document.querySelector(".CodeMirror").CodeMirror.setValue(${JSON.stringify(sol)})`);
await p.eval(`[...document.querySelectorAll("button")].find((b) => b.textContent.includes("Run tests")).click()`);
await waitRun(p);
check("a pass marks the problem solved", (await p.eval(`document.querySelector(".contest-tab[aria-current='page']").dataset.state`)) === "solved");
check("the solved card points to the next contest problem", (await p.eval(`document.querySelector(".solved-card a.btn")?.getAttribute("href")`)) === `#/p/${names[1]}/contest`);
check("tab states have names for screen readers", await p.eval(`[...document.querySelectorAll(".contest-tab")].every((t) => (t.getAttribute("aria-label") || "").length > 3)`)
  && (await p.eval(`document.querySelector(".contest-tab[aria-current='page']").getAttribute("aria-label")`)).includes("solved"));
await p.eval(`document.querySelectorAll(".contest-tab")[1].click()`);
await sleep(1200);
check("tabs move between contest problems", (await hash(p)) === `#/p/${names[1]}/contest`);

// ── Kept inside: hash navigation, the palette, leaving the page ──
await p.eval(`location.hash = "#/roadmap"`);
await sleep(900);
check("navigating away returns to the contest", (await hash(p)) === `#/p/${names[1]}/contest`, await hash(p));
await p.eval(`location.hash = "#/p/two_sum"`);
await sleep(900);
check("other problems return to the contest", (await hash(p)) === `#/p/${names[1]}/contest`, await hash(p));
await p.eval(`document.dispatchEvent(new KeyboardEvent("keydown", { key: "k", ctrlKey: true, bubbles: true }))`);
check("Go to anything stays shut", await p.eval(`document.querySelector("#palette").hidden`));
check("leaving the page asks first", await p.eval(`(() => { const e = new Event("beforeunload", { cancelable: true }); window.dispatchEvent(e); return e.defaultPrevented; })()`));

// ── The fullscreen lock ──
await p.eval(STUB_FS);
await p.eval(fsEnter);
await sleep(200);
check("no cover while in fullscreen", !(await shown(p, "#contest-lock")));
await p.eval(fsLeave);
await sleep(200);
check("leaving fullscreen covers the screen", await shown(p, "#contest-lock"));
check("the cover is a modal dialog", await p.eval(`(() => { const d = document.querySelector("#contest-lock"); return d.getAttribute("role") === "dialog" && d.getAttribute("aria-modal") === "true"; })()`));
check("the cover asks to go back to fullscreen", (await p.eval(`document.querySelector("#contest-lock").textContent`)).includes("Back to fullscreen"));
check("the page under the cover is inert", await p.eval(`document.querySelector(".main").inert === true`));
check("focus moves to the cover's button", await p.eval(`document.activeElement === document.querySelector("#contest-lock .contest-lock-go")`));
check("each exit is counted", (await stored(p)).exits === 1, JSON.stringify((await stored(p)).exits));
const before = await p.eval(`document.querySelector("#contest-lock [data-contest-clock]")?.textContent`);
await sleep(1300);
check("the clock keeps running under the cover", before && before !== (await p.eval(`document.querySelector("#contest-lock [data-contest-clock]")?.textContent`)), before);
await p.eval(`document.querySelector("#contest-lock .contest-lock-go").click()`);
await sleep(300);
check("the button goes back to fullscreen", !(await shown(p, "#contest-lock")) && await p.eval(`document.fullscreenElement === document.documentElement`));
check("the page is usable again", await p.eval(`document.querySelector(".main").inert === false`));

// ── The clock: a name, no chatter, a warning near the end ──
check("the countdown is a timer with a name", await p.eval(`(() => { const c = document.querySelector(".contest-clock");
  return c.getAttribute("role") === "timer" && (c.getAttribute("aria-label") || "").startsWith("Time left") && !["polite", "assertive"].includes(c.getAttribute("aria-live")); })()`));
await p.eval(`Trace.now = () => Date.now() + 29.5 * 60000`);
await sleep(1100);
const l1 = await p.eval(`document.querySelector(".contest-clock").getAttribute("aria-label")`);
await sleep(1100);
const l2 = await p.eval(`document.querySelector(".contest-clock").getAttribute("aria-label")`);
check("the countdown's name doesn't change every second", l1 === l2, `${l1} / ${l2}`);
check("no warning with time to spare", await p.eval(`!document.querySelector(".contest-clock").hasAttribute("data-warn")`));
await p.eval(`Trace.now = () => Date.now() + 55.5 * 60000`);
await sleep(1300);
check("the last five minutes turn the clock to the warning colour", await p.eval(`(() => { const c = document.querySelector(".contest-clock");
  const i = document.createElement("i"); i.style.color = "var(--warn)"; document.body.append(i); const want = getComputedStyle(i).color; i.remove();
  return c.hasAttribute("data-warn") && getComputedStyle(c).color === want; })()`));
check("five minutes left is said once, politely", (await p.eval(`document.querySelector("#contest-say")?.getAttribute("aria-live")`)) === "polite"
  && (await p.eval(`document.querySelector("#contest-say").textContent`)).includes("5 minutes"));
for (const mode of ["light", "dark"]) {
  await p.eval(`document.documentElement.dataset.theme = "${mode}"`);
  const c = await contrast(p, ".contest-clock");
  check(`the warning clock is readable (${mode})`, c >= 4.5, c.toFixed(2));
  const s = await contrast(p, ".contest-submit");
  check(`Submit is readable (${mode})`, s >= 4.5, s.toFixed(2));
}
await p.eval(`delete document.documentElement.dataset.theme`);
await p.eval(`Trace.now = () => Date.now()`);

// ── A reload resumes the contest ──
await p.reload(BASE + "/#/roadmap");
check("a reload stays in the contest", (await hash(p)).endsWith("/contest") && await p.eval(`document.body.classList.contains("contest")`), await hash(p));
check("the same problems after a reload", JSON.stringify((await stored(p)).problems.map((x) => x.name)) === JSON.stringify(names));
check("the right time left after a reload", /^5[0-9]:[0-9][0-9]$/.test(await p.eval(`document.querySelector(".contest-clock [data-contest-clock]")?.textContent`)),
  await p.eval(`document.querySelector(".contest-clock [data-contest-clock]")?.textContent`));
check("solved state survives a reload", (await p.eval(`document.querySelectorAll(".contest-tab")[0].dataset.state`)) === "solved");
check("a reload out of fullscreen covers the screen", await shown(p, "#contest-lock"));
check("a reload counts as leaving fullscreen", (await stored(p)).exits === 2);
await p.eval(`document.querySelector("#contest-lock .contest-lock-go").click()`);    // refused here: no real gesture
await sleep(400);
check("a refused fullscreen lets you keep going", !(await shown(p, "#contest-lock")));

// ── Submit, with a confirm step that isn't a browser dialog ──
await p.eval(`window.__dialogs = 0; window.alert = window.confirm = window.prompt = () => { window.__dialogs++; return true; }`);
await p.eval(`document.querySelector(".contest-submit").click()`);
await sleep(200);
check("Submit asks first", await shown(p, ".contest-confirm"));
check("focus moves to the question", await p.eval(`!!document.activeElement?.closest(".contest-confirm")`));
await p.eval(`document.querySelector(".contest-confirm-no").click()`);
await sleep(200);
check("Keep going carries on", !(await shown(p, ".contest-confirm")) && (await hash(p)).endsWith("/contest"));
await p.eval(`document.querySelector(".contest-submit").click()`);
await sleep(200);
await p.eval(`document.querySelector(".contest-confirm-yes").click()`);
await sleep(1200);
check("no browser dialogs", (await p.eval(`window.__dialogs`)) === 0);
check("results after submitting", (await hash(p)).startsWith("#/contest/") && await p.eval(`!!document.querySelector(".contest-results")`), await hash(p));
check("the contest is over", await p.eval(`!document.body.classList.contains("contest") && getComputedStyle(document.querySelector(".side")).display !== "none"`));
check("results list each problem", (await p.eval(`document.querySelectorAll(".contest-result-row").length`)) === 3);
check("results show tests passed", (await p.eval(`document.querySelectorAll(".contest-result-row")[0].textContent`)).match(/([0-9]+) of \1 tests/) !== null,
  await p.eval(`document.querySelectorAll(".contest-result-row")[0].textContent`));
check("results mark what was solved", await p.eval(`document.querySelectorAll(".contest-result-row")[0].dataset.state === "solved" && document.querySelectorAll(".contest-result-row")[2].dataset.state !== "solved"`));
check("results show the time used", /[0-9]+:[0-9][0-9]/.test(await p.eval(`document.querySelector(".contest-used")?.textContent || ""`)));
check("results count the fullscreen exits", (await p.eval(`document.querySelector(".contest-exits")?.textContent || ""`)).includes("2"));
check("the live contest is cleared", (await stored(p)) === null);
check("the contest goes into history", (await history(p)).length === 1);
await p.eval(`location.hash = "#/roadmap"`);
await sleep(700);
check("navigation is free again", (await hash(p)) === "#/roadmap");
await p.reload(BASE + "/#/contest");
check("past contests are on the contest page", await p.eval(`document.querySelectorAll(".contest-history a").length === 1`));
check("a past contest opens its results", await p.eval(`document.querySelector(".contest-history a").getAttribute("href").startsWith("#/contest/")`));
await p.eval(`localStorage.setItem("trace.contests", "not json")`);
await p.reload(BASE + "/#/contest");
check("unreadable history still shows the page", await p.eval(`!!document.querySelector(".contest-start") && !document.querySelector(".contest-history a")`));

// ── Time running out ends it ──
await start(p, 30);
check("a 30-minute contest starts", /^(29|30):[0-9][0-9]$/.test(await p.eval(`document.querySelector(".contest-clock [data-contest-clock]")?.textContent`)));
await p.eval(STUB_FS);
await p.eval(fsEnter);
await p.eval(`Trace.now = () => Date.now() + 31 * 60000`);
await sleep(1800);
check("time running out shows the results", (await hash(p)).startsWith("#/contest/") && (await p.eval(`document.querySelector(".contest-results")?.textContent || ""`)).includes("Time's up"));
check("time running out leaves fullscreen", (await p.eval(`window.__exited || 0`)) >= 1);
check("no cover after the end", !(await shown(p, "#contest-lock")));
check("a full contest's time used is its length", (await p.eval(`document.querySelector(".contest-used")?.textContent || ""`)).includes("30:00"));
await p.eval(`Trace.now = () => Date.now()`);

// Time that ran out while Trace was closed ends it on the next visit.
await start(p, 60);
await p.eval(`(() => { const s = JSON.parse(localStorage.getItem("trace.contest")); s.endsAt = Date.now() - 1000; s.startedAt = s.endsAt - 60 * 60000;
  localStorage.setItem("trace.contest", JSON.stringify(s)); })()`);
await p.reload(BASE + "/#/");
check("a contest that ran out while away shows its results", (await hash(p)).startsWith("#/contest/") && (await p.eval(`document.querySelector(".contest-results")?.textContent || ""`)).includes("Time's up"), await hash(p));
check("history keeps both", (await history(p)).length === 2);

// ── Phone width: no fullscreen to lock, nothing sideways ──
const phone = await open(BASE + "/#/contest", { width: 390, height: 844 });
check("phone: the contest page fits", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`));
await phone.eval(`document.querySelector(".contest-start").click()`);
await sleep(1500);
check("phone: the contest starts without fullscreen", (await phone.eval(`location.hash`)).endsWith("/contest") && !(await shown(phone, "#contest-lock")));
check("phone: the contest bar fits", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector(".contest-bar").getBoundingClientRect().right <= 390
  && document.querySelector(".contest-submit").getBoundingClientRect().right <= 390`));
check("phone: the clock is visible", await phone.eval(`(() => { const r = document.querySelector(".contest-clock").getBoundingClientRect(); return r.width > 0 && r.right <= 390; })()`));
check("phone: no console errors", phone.logs.length === 0, phone.logs.join(" | "));
await phone.close();

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
