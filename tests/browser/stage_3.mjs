// Stage 3 audit on screen: topic 17's techniques, a re-ranked teacher, a lock that walks its teachers in order,
// and a banner back to Stage 2.
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

// Topic 17 lists its five techniques in teaching order.
await p.reload(BASE + "/#/t/17_heaps");
const list17 = await techList(p);
check("topic 17 lists its techniques in teaching order",
  list17.join(" | ") === "Keeping the k largest | Max-heap by negating | Two heaps for the median | Lazy deletion | Merging sorted lists with a heap",
  list17.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve push_keep_k", await solve(p, "push_keep_k"));
check("solve last_stone", await solve(p, "last_stone"));

// The re-ranked median_finder teaches two heaps.
await p.reload(BASE + "/#/p/median_finder");
check("median_finder shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Two heaps for the median");

// sliding_window_median needs two teachers from this topic: the lock names them one at a time, in order.
await p.reload(BASE + "/#/p/sliding_window_median");
const lock1 = await text(p, ".reveal-box");
check("sliding_window_median names its first basic problem",
  lock1.includes("This uses Two heaps for the median") && lock1.includes("Find Median from Data Stream teaches it"), lock1);
check("solve median_finder", await solve(p, "median_finder"));
await p.reload(BASE + "/#/p/sliding_window_median");
const lock2 = await text(p, ".reveal-box");
check("then it names the next one",
  lock2.includes("This uses Lazy deletion") && lock2.includes("Max With Removals teaches it"), lock2);

// A Stage 2 technique shows as a banner on a linked-list problem.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve insert_after", await solve(p, "insert_after"));
check("solve reverse_between", await solve(p, "reverse_between"));
await p.reload(BASE + "/#/p/merge_two_lists");
const banner = await text(p, ".tech-banner");
check("merge_two_lists points back to topic 06",
  banner.includes("This uses One pointer per list") && banner.includes("Is It a Subsequence?"), banner);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
