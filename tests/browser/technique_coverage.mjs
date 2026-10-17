// Technique coverage: the box, the Uses row, the in-topic lock, plan mode, placement, the topic list.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const text = (p, sel) => p.eval(`document.querySelector(${JSON.stringify(sel)})?.textContent || ""`);
const isOpen = (p) => p.eval(`![...document.querySelectorAll(".reveal-box button")].some(b => b.textContent === "Open anyway")`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// A teaching problem shows its "New technique" box and no Uses row.
await p.reload(BASE + "/#/p/open_neighbors");
check("teaching problem shows the New technique box", (await text(p, ".tech-new h4")) === "New technique: Grid neighbours");
check("a problem with no USES has no Uses row", !(await p.eval(`!!document.querySelector(".tech-uses")`)));
check("no stray null or [object] text in the statement", !/null|\[object/.test(await text(p, ".statement")));

// Solve the snippet and the guided problem, then hit the technique lock.
check("solve open_neighbors", await solve(p, "open_neighbors"));
check("solve distance_to_exit", await solve(p, "distance_to_exit"));
await p.reload(BASE + "/#/p/count_enclosed");
const lock = await text(p, ".reveal-box");
check("in-topic lock names the technique and its teacher", lock.includes("This uses Flood fill") && lock.includes("Flood Fill teaches it"), lock);
check("lock offers Open anyway", (await p.eval(`[...document.querySelectorAll(".reveal-box button")].some(b => b.textContent === "Open anyway")`)));

// A problem the learner already started (some tests passing) never gets a new technique lock.
const tried = await p.eval(`fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "count_enclosed", code: "def count_enclosed(grid):\\n    return 0\\n" }) })
  .then(r => r.json()).then(r => r.progress.problems.count_enclosed)`);
check("partial attempt recorded", tried && tried.passed > 0 && !tried.solved, JSON.stringify(tried));
await p.reload(BASE + "/#/p/count_enclosed");
check("an attempted problem stays open", await isOpen(p));
await post(p, "/api/reset", { name: "count_enclosed" });

// Solved problems stay open even with an unsolved same-topic teacher.
check("solve max_area_island directly", await solve(p, "max_area_island"));
await p.reload(BASE + "/#/p/max_area_island");
check("solved problems stay open", !(await p.eval(`!!document.querySelector(".reveal-box button")`)) && (await text(p, ".statement h1")) === "Max Area of Island");

// Solving the teacher opens the problem; the chip is known and explains itself.
check("solve flood_fill", await solve(p, "flood_fill"));
await p.reload(BASE + "/#/p/count_enclosed");
check("problem opens once its teacher is solved", await isOpen(p));
const floodChip = `[...document.querySelectorAll(".tech-chip")].find(b => b.textContent.includes("Flood fill"))`;
check("Uses chip shows as known", await p.eval(`${floodChip}?.classList.contains("known") || false`));
check("teaching box for the new technique", (await text(p, ".tech-new h4")) === "New technique: Searching back from the targets");
await p.eval(`${floodChip}.click()`); await sleep(200);
check("chip opens its explanation and teacher link", (await text(p, ".tech-detail")).includes("Learned in Flood Fill"));

// Plan mode: no lock, chips still show what's missing.
const planned = await p.eval(`fetch("/api/course").then(r => r.json()).then(d => { for (const pl of d.plans.plans) for (const s of pl.sections) if (s.items.includes("clone_graph")) return pl.id; return null; })`);
if (planned) {
  await p.reload(BASE + `/#/p/clone_graph/plan/${planned}`);
  check("plan mode skips the technique lock", await isOpen(p));
  check("plan mode chip shows the unlearned technique", (await text(p, ".tech-chip:not(.known)")).includes("Walking a graph from its edges"));
}

// The topic page lists the techniques in teaching order, with ticks for learned ones.
await p.reload(BASE + "/#/t/19_graph_traversal");
const list = await p.eval(`[...document.querySelectorAll(".tech-list .item")].map(a => (a.classList.contains("solved") ? "✓" : "") + a.querySelector(".t").textContent)`);
check("topic lists 11 techniques", list.length === 11, list.join(" | "));
check("learned techniques are ticked", list[0] === "✓Grid neighbours" && list.includes("✓Flood fill") && list.includes("Rebuilding the path"), list.join(" | "));

// The banner, through the helper with a technique taught in another topic.
const banner = await p.eval(`(() => { const el = Trace.techniqueBanner({ uses: ["x.y"] }, { id: "19_graph_traversal" }, {
  techniques: { "x.y": { name: "Sliding window", explain: "e" } }, known: () => false,
  teacherHref: () => "#/p/max_sum_subarray_k", teacherTitle: () => "Maximum Sum of k in a Row",
  teacherTopic: () => ({ id: "07_sliding_window" }), topicTitle: () => "Sliding window" }); return el ? el.textContent : ""; })()`);
check("banner names the technique, its topic and its teacher", banner.includes("This uses Sliding window (Sliding window)") && banner.includes("Maximum Sum of k in a Row"), banner);

// Placed-out topics have no technique locks.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "dsa", ready: {}, answers: { "19_graph_traversal": [true] } });
await p.reload(BASE + "/#/p/count_enclosed");
check("placed-out topic: no technique lock", await isOpen(p));

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.shot("technique_coverage.png");
await p.close();
summary();
