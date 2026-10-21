// Stage 5 audit on screen: topic 26's techniques, a new teacher, a lock, and a banner back to topic 10's merge sort.
import { open, check, summary } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const solve = (p, name) => p.eval(`fetch("/api/solution?name=${name}").then(r => r.json()).then(s =>
  fetch("/api/test", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: "${name}", code: s.code }) }))
  .then(r => r.json()).then(r => r.progress.problems["${name}"].solved)`);
const post = (p, path, body) => p.eval(`fetch("${path}", { method: "POST", headers: { "Content-Type": "application/json" }, body: ${JSON.stringify(JSON.stringify(body))} }).then(r => r.json())`);
const text = (p, sel) => p.eval(`document.querySelector(${JSON.stringify(sel)})?.textContent || ""`);
const techList = (p) => p.eval(`[...document.querySelectorAll(".tech-list .item")].map(a => (a.classList.contains("solved") ? "✓" : "") + a.querySelector(".t").textContent)`);

const p = await open(BASE + "/");
await post(p, "/api/placement", { door: "skip" });

// Topic 26 lists its four techniques in teaching order.
await p.reload(BASE + "/#/t/26_range_queries");
const list26 = await techList(p);
check("topic 26 lists its techniques in teaching order",
  list26.join(" | ") === "Fenwick tree: prefix sums | Fenwick tree: updates | Segment tree | Compressing values to ranks",
  list26.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve fenwick_prefix", await solve(p, "fenwick_prefix"));
check("solve num_array", await solve(p, "num_array"));

// The new range_max_updates teaches the segment tree.
await p.reload(BASE + "/#/p/range_max_updates");
check("range_max_updates shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Segment tree");

// count_smaller is locked behind the new rank problem.
await p.reload(BASE + "/#/p/count_smaller");
const lock = await text(p, ".reveal-box");
check("count_smaller names the technique and its basic problem",
  lock.includes("This uses Compressing values to ranks") && lock.includes("Rank Transform of an Array teaches it"), lock);

// reverse_pairs needs merge sort from topic 10: a banner, not a lock.
await p.reload(BASE + "/#/p/reverse_pairs");
const banner = await text(p, ".tech-banner");
check("reverse_pairs points back to topic 10",
  banner.includes("This uses Merge sort, counting while merging") && banner.includes("Count Inversions"), banner);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
