// Stage 2 audit on screen: topic 07's and 10's techniques, a re-ranked teacher, locks and a banner across topics.
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

// Topics 07 and 10 list their techniques in teaching order.
await p.reload(BASE + "/#/t/07_sliding_window");
const list07 = await techList(p);
check("topic 07 lists its techniques in teaching order",
  list07.join(" | ") === "Fixed-size window | Growing and shrinking a window | Shortest window | Counting with a window", list07.join(" | "));
await p.reload(BASE + "/#/t/10_sorting_and_intervals");
const list10 = await techList(p);
check("topic 10 lists its techniques in teaching order",
  list10.join(" | ") === "Do two intervals overlap? | Absorbing an overlap | Merge sort, counting while merging | Sort by start, then compare neighbours | Earliest end first", list10.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve slide_sum", await solve(p, "slide_sum"));
check("solve longest_k_distinct", await solve(p, "longest_k_distinct"));

// The re-ranked min_subarray_len teaches the shortest window.
await p.reload(BASE + "/#/p/min_subarray_len");
check("min_subarray_len shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Shortest window");

// The hard is locked behind the new basic problem.
await p.reload(BASE + "/#/p/subarrays_k_distinct");
const lock = await text(p, ".reveal-box");
check("subarrays_k_distinct names the technique and its basic problem",
  lock.includes("This uses Counting with a window") && lock.includes("Subarrays With k Odd Numbers teaches it"), lock);

check("solve nice_subarrays", await solve(p, "nice_subarrays"));
await p.reload(BASE + "/#/t/07_sliding_window");
check("solving nice_subarrays ticks Counting with a window", (await techList(p)).includes("✓Counting with a window"));

// A later topic gets a banner for 07's techniques, not a lock.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve lower_bound", await solve(p, "lower_bound"));
check("solve ship_capacity", await solve(p, "ship_capacity"));
await p.reload(BASE + "/#/p/smallest_distance_pair");
const banner = await text(p, ".tech-banner");
check("smallest_distance_pair points back to topic 07",
  banner.includes("This uses Counting with a window") && banner.includes("Subarrays With k Odd Numbers"), banner);

// min_k_bit_flips also uses 08's difference array, which is unsolved: that one is a banner, the lock names 11's teacher.
check("solve extend_or_restart", await solve(p, "extend_or_restart"));
check("solve min_jumps", await solve(p, "min_jumps"));
await p.reload(BASE + "/#/p/min_k_bit_flips");
const lock11 = await text(p, ".reveal-box");
check("min_k_bit_flips names The forced first move and its basic problem",
  lock11.includes("This uses The forced first move") && lock11.includes("Minimum Suffix Flips teaches it"), lock11);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
