// Stage 6 audit on screen: topic 32's techniques, a teacher's box, its lock, and a banner from 33 back to topic 21.
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

// Topic 32 lists its five techniques in teaching order.
await p.reload(BASE + "/#/t/32_advanced_trees");
const list32 = await techList(p);
check("topic 32 lists its techniques in teaching order",
  list32.join(" | ") === "Jumping with a lifting table | Building a lifting table | Bottom-up without recursion | Lowest common ancestor with lifting | Rerooting",
  list32.join(" | "));

// Solo problems open once the snippet and guided problem are solved (a locked page shows no box).
check("solve lift_jump", await solve(p, "lift_jump"));
check("solve tree_ancestor", await solve(p, "tree_ancestor"));

// subtree_sizes teaches bottom-up without recursion, and sum_of_distances is locked behind it.
await p.reload(BASE + "/#/p/subtree_sizes");
check("subtree_sizes shows its New technique box", (await text(p, ".tech-new h4")) === "New technique: Bottom-up without recursion");
await p.reload(BASE + "/#/p/sum_of_distances");
const lock = await text(p, ".reveal-box");
check("sum_of_distances names the technique and its basic problem",
  lock.includes("This uses Bottom-up without recursion") && lock.includes("Subtree Sizes teaches it"), lock);

// A topic 33 problem gets a banner for Bellman-Ford from topic 21.
await post(p, "/api/reset-progress", {});
await post(p, "/api/placement", { door: "skip" });
check("solve bottleneck", await solve(p, "bottleneck"));
check("solve max_flow", await solve(p, "max_flow"));
await p.reload(BASE + "/#/p/min_cost_flow");
const banner = await text(p, ".tech-banner");
check("min_cost_flow points back to topic 21",
  banner.includes("This uses Bellman-Ford") && banner.includes("Shortest Paths With Negative Roads"), banner);

check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
