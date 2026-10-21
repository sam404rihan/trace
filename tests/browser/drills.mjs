// Intuition drills: routine repeats play themselves, and two clean runs make a drill solid.
import { open, check, summary, sleep } from "./cdp.mjs";

const BASE = process.argv.at(-1);
const p = await open(BASE + "/");
await p.eval(`fetch("/api/placement", { method: "POST", headers: { "Content-Type": "application/json" }, body: '{"door":"skip"}' })`);
const topic = await p.eval(`Trace.topics.find((t) => t.drills.some((d) => d.id === "pair-sum")).id`);
await p.reload(BASE + `/#/d/${topic}/pair-sum`);

// Answer every question correctly, the way a fluent learner would, and count what was asked vs played.
const state = () => p.eval(`document.querySelector(".board").parentElement.drillState()`);
async function cleanRun() {
  let asked = 0;
  for (let guard = 0; guard < 80; guard++) {
    const st = await state();
    if (st.done) return { asked, auto: st.auto };
    if (st.playing) { await sleep(250); continue; }
    const want = String(Array.isArray(st.answer) ? st.answer[0] : st.answer);
    const ok = await p.eval(`(() => { const st = document.querySelector(".board").parentElement.drillState();
      const i = (st.options || []).indexOf(${JSON.stringify(want)});
      const el = i >= 0 ? document.querySelector('.options [data-i="' + i + '"]') : document.querySelector('[data-pick="${want}"]');
      if (!el) return false; el.dispatchEvent(new MouseEvent("click", { bubbles: true })); return true; })()`);
    if (!ok) return { asked, auto: -1, stuck: want };
    asked++;
    await sleep(80);
  }
  return { asked, auto: -2 };
}

// Routine repeats play themselves: over a few clean runs, some steps are played for the learner.
const runs = [];
for (let k = 0; k < 6; k++) {
  runs.push(await cleanRun());
  if (runs.some((r) => r.auto > 0) && k >= 1) break;
  await p.eval(`document.querySelector(".options .opt.primary").click()`);   // Next example
  await sleep(300);
}
check("fluent runs finish", runs.every((r) => r.auto >= 0), JSON.stringify(runs));
check("routine repeats play themselves", runs.some((r) => r.auto > 0), JSON.stringify(runs));
check("played steps don't count as slips", (await p.eval(`document.querySelector(".dprompt .result")?.textContent`)) === "Clean run.");

// Two clean runs make the drill solid.
check("two clean runs make it solid", (await p.eval(`document.querySelector(".dprompt").textContent`)).includes("This drill is solid."),
  await p.eval(`document.querySelector(".dprompt").textContent`));
check("the drill tab shows two of two", (await p.eval(`document.querySelectorAll('.drill-tab[aria-selected="true"] .pips i').length`)) === 2);

// A number question never plays itself (its options change every time): the bars drill asks counts.
check("no console errors", p.logs.length === 0, p.logs.join(" | "));
await p.close();
summary();
