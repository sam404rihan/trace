"use strict";
/* The intuition-drill host: mounts one drill (a generator of questions) into a container,
   runs the question loop, and records clean runs in localStorage. */
(function () {
  const T = window.Trace;
  const { h } = T;

  // ── drill progress (per browser) ───────────────────────────────────────────
  const GOAL = 2; // clean runs that make a drill "solid"
  const AUTO_AFTER = 2; // the same move made correctly this many times in a row, then its repeats play themselves
  const AUTO_MS = 650;
  const KEY = "trace.v1";
  let store = (() => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } })();
  store.drills ||= {};
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch { /* storage unavailable */ } };

  const Progress = {
    GOAL,
    rec: (topic, drill) => store.drills[`${topic.id}/${drill.id}`] || { runs: 0, clean: 0 },
    solid: (topic, drill) => Progress.rec(topic, drill).clean >= GOAL,
    topicSolid: (topic) => topic.drills.every((d) => Progress.solid(topic, d)),
    record(topic, drill, clean) {
      const r = Progress.rec(topic, drill);
      r.runs++;
      if (clean) r.clean++;
      store.drills[`${topic.id}/${drill.id}`] = r;
      save();
      return r;
    },
    reset() { store = { drills: {} }; save(); },
  };
  T.DrillProgress = Progress;

  T.pips = (n, of = GOAL) => h("span", { class: "pips", "aria-label": `${Math.min(n, of)} of ${of} clean runs` },
    T.range(of).map((i) => h("i", { class: i < n ? "on" : "" })));

  // ── the question loop ──────────────────────────────────────────────────────
  T.mountDrill = function mountDrill(container, topic, drill, { onFinish } = {}) {
    const els = {
      blurb: h("p", { class: "blurb" }),
      view: h("div", { class: "view" }),
      prompt: h("div", { class: "dprompt", "aria-live": "polite" }),
      options: h("div", { class: "options" }),
      feedback: h("p", { class: "feedback", "aria-live": "polite" }),
      slips: h("span", { class: "slips" }),
    };
    els.showBtn = h("button", { class: "btn ghost small", type: "button", onclick: () => showMe() }, h("kbd", {}, "H"), "Show me");
    els.newBtn = h("button", { class: "btn ghost small", type: "button", onclick: () => start() }, h("kbd", {}, "N"), "New example");
    container.replaceChildren(
      h("section", { class: "board", "aria-label": "Board" }, els.blurb, els.view),
      h("section", { class: "dconsole", "aria-label": "Your move" }, els.prompt, els.options, els.feedback,
        h("div", { class: "dtools" }, els.showBtn, els.newBtn, els.slips)));

    let sess = null;
    const slipText = () => (sess.slips ? `${sess.slips} slip${sess.slips > 1 ? "s" : ""} so far` : "");

    // A routine repeat: the same question (same choices) with the same answer as the last few, which the
    // learner got right first time. Those play themselves, so a run is about the decisions that change.
    const formOf = (ask) => (ask.options ? ask.options.map((o) => String(o.value)).join("|") : ask.picks ? "pick" : null);
    const keyOf = (ask) => JSON.stringify(ask.answer);
    function routine(ask) {
      const f = formOf(ask);
      return !!f && sess.streak >= AUTO_AFTER && sess.last && sess.last.form === f && sess.last.key === keyOf(ask);
    }

    function start() {
      clearTimeout(sess && sess.timer);
      sess = { slips: 0, ask: null, done: false, revealed: false, streak: 0, last: null, missed: false, auto: 0, playing: false, timer: null };
      els.blurb.textContent = drill.blurb;
      els.view.replaceChildren();
      setFeedback("");
      const ctx = { view: els.view, draw: (...nodes) => els.view.replaceChildren(...nodes.flat(Infinity).filter(Boolean)) };
      sess.gen = drill.play(ctx);
      step(undefined);
    }

    function step(input) {
      let r;
      try {
        r = sess.gen.next(input);
      } catch (err) {
        console.error(err);
        els.prompt.replaceChildren(h("p", {}, "This example broke. Press N for a new one."));
        els.options.replaceChildren();
        return;
      }
      if (r.done) return finish(r.value || {});
      sess.ask = r.value;
      sess.revealed = false;
      const ask = sess.ask;
      els.prompt.replaceChildren(ask.prompt instanceof Node ? ask.prompt : h("p", {}, ask.prompt));
      els.options.replaceChildren(...(ask.options || []).map((o, i) =>
        h("button", { type: "button", class: "opt", "data-i": i, onclick: (e) => answer(o.value, e.currentTarget) },
          i < 9 ? h("kbd", {}, i + 1) : null, h("span", {}, o.label))));
      els.view.classList.toggle("picking", ask.picks);
      els.view.querySelectorAll(".reveal, .miss").forEach((el) => el.classList.remove("reveal", "miss"));
      els.slips.textContent = slipText();
      els.showBtn.disabled = false;
      sess.missed = false;
      if (routine(ask)) play(ask);
    }

    // Show the move, highlighted, then make it.
    function play(ask) {
      sess.playing = true;
      sess.auto++;
      els.showBtn.disabled = true;
      const value = Array.isArray(ask.answer) ? ask.answer[0] : ask.answer;
      let target = null;
      if (ask.options) target = els.options.querySelector(`[data-i="${ask.options.findIndex((o) => String(o.value) === String(value))}"]`);
      else if (ask.picks) target = els.view.querySelector(`[data-pick="${CSS.escape(String(value))}"]`);
      if (target) target.classList.add("auto");
      els.options.querySelectorAll(".opt").forEach((b) => { b.disabled = true; });
      setFeedback("Same move again, so it plays itself.", "hint");
      sess.timer = setTimeout(() => {
        sess.playing = false;
        if (sess.ask !== ask) return;
        sess.ask = null;
        step(value);
      }, AUTO_MS);
    }

    function answer(value, el) {
      if (!sess || !sess.ask || sess.done) return;
      const ask = sess.ask;
      if (sess.playing) return;
      if (ask.accept(value)) {
        const same = sess.last && sess.last.form === formOf(ask) && sess.last.key === keyOf(ask);
        sess.streak = sess.missed || sess.revealed ? 0 : same ? sess.streak + 1 : 1;
        sess.last = { form: formOf(ask), key: keyOf(ask) };
        const note = typeof ask.note === "function" ? ask.note(value) : ask.note;
        setFeedback(note || "", "ok");
        sess.ask = null;
        step(value);
      } else {
        sess.slips++;
        sess.missed = true;
        setFeedback(ask.why(value), "bad");
        if (el) {
          el.classList.remove("miss");
          void el.getBoundingClientRect();
          el.classList.add("miss");
        }
        els.slips.textContent = slipText();
      }
    }

    function showMe() {
      if (!sess || !sess.ask || sess.done || sess.playing) return;
      const ask = sess.ask;
      if (!sess.revealed) {
        sess.revealed = true;
        sess.slips++;
        els.slips.textContent = slipText();
      }
      let target = null;
      if (ask.options) {
        const i = ask.options.findIndex((o) => String(o.value) === String(ask.answer));
        target = els.options.querySelector(`[data-i="${i}"]`);
      }
      if (!target && ask.picks) target = els.view.querySelector(`[data-pick="${CSS.escape(String(ask.answer))}"]`);
      if (target) {
        target.classList.add("reveal");
        target.focus?.({ preventScroll: true });
      }
      setFeedback("Highlighted. Work out why it's right before you press it.", "hint");
    }

    function finish(result) {
      sess.done = true;
      els.view.classList.remove("picking");
      const clean = sess.slips === 0;
      const r = Progress.record(topic, drill, clean);
      const left = Math.max(0, GOAL - r.clean);
      els.prompt.replaceChildren(
        h("p", { class: "result " + (clean ? "clean" : "") }, clean ? "Clean run." : `Done, with ${sess.slips} slip${sess.slips > 1 ? "s" : ""}.`),
        result.summary ? h("p", { class: "summary" }, result.summary) : null,
        h("p", { class: "summary dim" }, left ? `${left} more clean run${left > 1 ? "s" : ""} make this drill solid.` : "This drill is solid."));
      const next = h("button", { type: "button", class: "opt primary", onclick: start }, h("kbd", {}, "Enter"), h("span", {}, "Next example"));
      els.options.replaceChildren(next);
      els.slips.textContent = "";
      els.showBtn.disabled = true;
      next.focus({ preventScroll: true });
      onFinish && onFinish(r);
    }

    function setFeedback(text, tone) {
      els.feedback.textContent = text;
      els.feedback.className = "feedback" + (tone && text ? " " + tone : "");
    }

    function pickFrom(target) {
      const el = target.closest && target.closest("[data-pick]");
      if (!el || !els.view.contains(el) || !sess || !sess.ask || !sess.ask.picks) return;
      if (sess.ask.onPick) return sess.ask.onPick(el.getAttribute("data-pick"));
      answer(el.getAttribute("data-pick"), el);
    }
    els.view.addEventListener("click", (e) => pickFrom(e.target));
    els.view.addEventListener("keydown", (e) => {
      if ((e.key === "Enter" || e.key === " ") && e.target.matches?.("g[data-pick]")) {
        e.preventDefault();
        pickFrom(e.target);
      }
    });

    function onKey(e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.target.matches?.("input, select, textarea, .CodeMirror textarea")) return;
      if (sess && sess.done && e.key === "Enter" && !e.target.matches?.("button, a")) { e.preventDefault(); start(); return; }
      if (/^[1-9]$/.test(e.key) && sess && !sess.done && sess.ask?.options) {
        const btn = els.options.querySelector(`[data-i="${Number(e.key) - 1}"]`);
        if (btn) { e.preventDefault(); btn.click(); }
        return;
      }
      if (e.key === "h" || e.key === "H") showMe();
      else if (e.key === "n" || e.key === "N") start();
    }
    document.addEventListener("keydown", onKey);

    // Read-only view of the run, for the browser checks.
    container.drillState = () => ({
      answer: sess.ask && sess.ask.answer, options: sess.ask && sess.ask.options ? sess.ask.options.map((o) => String(o.value)) : null,
      done: sess.done, auto: sess.auto, playing: sess.playing,
    });

    start();
    return { unmount: () => { clearTimeout(sess && sess.timer); document.removeEventListener("keydown", onKey); } };
  };
})();
