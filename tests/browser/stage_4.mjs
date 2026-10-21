// Stage 4 audit on screen: topic 23's techniques, a re-ranked teacher, its lock, and a banner from 24 back to 23.
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

// Topic 23 lists its six techniques in teaching order.
await p.reload(BASE + "/#/t/23_dynamic_programming_1d");
const list23 = await techList(p);
check("topic 23 lists its techniques in teaching order",
  list23.join(" | ") === "Building answers from smaller ones | DP over prefixes | DP over amounts | Longest increasing subsequence with tails | Expanding around a centre | 0/1 knapsack: reachable sums",
  list23.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve robber_step", await solve(p, "robber_step"));
check("solve decode_ways", await solve(p, "decode_ways"));

// The re-ranked coin_change teaches DP over amounts, and the medium that needs it is locked behind it.
await p.reload(BASE + "/#/p/coin_change");
check("coin_change shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: DP over amounts");
await p.reload(BASE + "/#/p/combination_sum_iv");
const lock = await text(p, ".reveal-box");
check("combination_sum_iv names the technique and its basic problem",
  lock.includes("This uses DP over amounts") && lock.includes("Coin Change teaches it"), lock);

// A topic 24 problem gets a banner for 23's knapsack.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve lcs_cell", await solve(p, "lcs_cell"));
check("solve min_path_sum", await solve(p, "min_path_sum"));
await p.reload(BASE + "/#/p/target_sum");
const banner = await text(p, ".tech-banner");
check("target_sum points back to topic 23",
  banner.includes("This uses 0/1 knapsack: reachable sums") && banner.includes("Partition Equal Subset Sum"), banner);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
