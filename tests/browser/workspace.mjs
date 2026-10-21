// The problem workspace: the topic band, the ladder track, the test strip, the solved card, phone width.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
// The colour a CSS value resolves to inside `sel`, for comparing against a computed background.
const resolve = (p, sel, value) => p.eval(`(() => { const host = document.querySelector(${JSON.stringify(sel)}); const i = document.createElement("i");
  i.style.color = ${JSON.stringify(value)}; host.append(i); const c = getComputedStyle(i).color; i.remove(); return c; })()`);
const bg = (p, sel) => p.eval(`getComputedStyle(document.querySelector(${JSON.stringify(sel)})).backgroundColor`);
async function run(p, code) {
  await p.eval(`document.querySelector(".CodeMirror").CodeMirror.setValue(${JSON.stringify(code)})`);
  await p.eval(`[...document.querySelectorAll("button")].find((b) => b.textContent.includes("Run tests")).click()`);
  for (let i = 0; i < 40 && (await p.eval(`document.querySelector(".console-bar .summary").textContent`)) === "Running…"; i++) await sleep(250);
  await sleep(300);
}

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });
await p.reload(BASE + "/#/p/pointer_step");                  // topic 06's snippet: stage 2, always open

// The topic band ties the workspace to home: the topic's name and its drawing, in the stage colour.
check("topic band with the drawing", await p.eval(`!!document.querySelector(".ws-topic svg.art")`));
check("topic band names the topic", (await p.eval(`document.querySelector(".ws-topic")?.textContent || ""`)).includes("Two pointers"));
check("topic band is the stage colour", (await bg(p, ".ws-topic").catch(() => "")) === (await resolve(p, "body", "var(--stage)")));

// The ladder is a track: the current rung wears the stage colour.
check("current rung is the stage colour", (await bg(p, '.step-pill[aria-current="page"]')) === (await resolve(p, "body", "var(--stage)")));

// Callouts are calm: a neutral surface, the stage colour only in their heading.
check("callouts sit on a neutral surface", (await bg(p, ".howto")) === (await resolve(p, "body", "var(--fill)")));

// A wrong answer: one square per test, failures marked, and a square opens its test.
const sol = await p.eval(`fetch("/api/solution?name=pointer_step").then((r) => r.json()).then((s) => s.code)`);
await run(p, sol.replace("return left + 1, right", "return left, right - 1"));
const strip = await p.eval(`[...document.querySelectorAll(".test-strip .cell")].map((c) => c.dataset.status)`);
const tests = await p.eval(`document.querySelectorAll("details.test").length`);
check("one square per test", strip.length === tests && tests > 0, `${strip.length} squares, ${tests} tests`);
check("failing squares are marked", strip.includes("fail") && strip.includes("pass"), strip.join(","));
check("a square opens its test", await p.eval(`(() => { const all = [...document.querySelectorAll("details.test")];
  all.forEach((d) => d.open = false);
  const k = [...document.querySelectorAll(".test-strip .cell")].findIndex((c) => c.dataset.status === "fail");
  document.querySelectorAll(".test-strip .cell")[k].click(); return all[k].open; })()`));
check("squares are buttons with names", await p.eval(`[...document.querySelectorAll(".test-strip .cell")].every((c) => c.tagName === "BUTTON" && c.getAttribute("aria-label"))`));

// The right answer: every square passes and the solved card offers the next rung.
await run(p, sol);
check("all squares pass", await p.eval(`[...document.querySelectorAll(".test-strip .cell")].every((c) => c.dataset.status === "pass")`));
check("solved card with Next", await p.eval(`!!document.querySelector(".solved-card a.btn.primary")`));

// Phone width: the panes stack and nothing is clipped at the right edge.
const phone = await open(BASE + "/#/p/pointer_step", { width: 390, height: 844 });
check("no sideways scroll at 390px", await phone.eval(`document.documentElement.scrollWidth <= 390 && document.querySelector("#app").scrollWidth <= 390`),
  await phone.eval(`document.querySelector("#app").scrollWidth`));
check("statement fits at 390px", await phone.eval(`[...document.querySelectorAll(".statement > *")].every((e) => e.getBoundingClientRect().right <= 391)`));
await phone.close();

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
