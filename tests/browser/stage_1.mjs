// Stage 1 audit on screen: topic 01's technique list, a moved teacher, the lock and banner it causes.
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

// Topic 01 lists its four techniques in teaching order.
await p.reload(BASE + "/#/t/01_big_o_in_practice");
const list = await techList(p);
check("topic 01 lists its techniques in teaching order",
  list.join(" | ") === "Set for fast lookups | Best so far | Counting pairs with a dict | Separating i from j", list.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve halvings", await solve(p, "halvings"));
check("solve common_count", await solve(p, "common_count"));

// The moved max_profit teaches Best so far.
await p.reload(BASE + "/#/p/max_profit");
check("max_profit shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Best so far");

// The hard is locked behind the new basic problem.
await p.reload(BASE + "/#/p/count_bad_pairs");
const lock = await text(p, ".reveal-box");
check("count_bad_pairs names the technique and its basic problem",
  lock.includes("This uses Counting pairs with a dict") && lock.includes("Matching Pairs teaches it"), lock);

// Progress follows the name: solving max_profit ticks Best so far on topic 01.
check("solve max_profit", await solve(p, "max_profit"));
await p.reload(BASE + "/#/t/01_big_o_in_practice");
check("solving max_profit ticks Best so far on topic 01", (await techList(p)).includes("✓Best so far"));

// A technique from an earlier topic shows a banner, not a lock.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve last_seen", await solve(p, "last_seen"));
check("solve word_frequencies", await solve(p, "word_frequencies"));
await p.reload(BASE + "/#/p/second_largest");
const banner = await text(p, ".tech-banner");
check("second_largest points back to topic 01", banner.includes("This uses Best so far") && banner.includes("Best Time to Buy and Sell Stock"), banner);

// The new recursion teacher, once 05's snippet and guided problem are solved.
check("solve digit_sum", await solve(p, "digit_sum"));
check("solve count_paths", await solve(p, "count_paths"));
await p.reload(BASE + "/#/p/min_max_expr");
check("min_max_expr shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Parsing with recursion");

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
