"use strict";
/* "Read the code": a topic's pattern built up one layer at a time. Each layer shows why, the code so
   far (numbered, this layer's lines tinted, reuse layers coloured by role), a Run button, and one check question. */
(function () {
  const T = window.Trace;
  const { h, s } = T;
  const icon = (d) => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d }));
  T.markIcon = (right) => icon(right ? "M5 12.5l4.5 4.5L19 7.5" : "M6.5 6.5l11 11M17.5 6.5l-11 11");

  // wt: /api/walkthrough payload. done: layers already answered. run(code) -> /api/run reply.
  T.mountWalkthrough = function mountWalkthrough(container, wt, { done = 0, run, onAnswer, problemHref, topicHref }) {
    const n = wt.layers.length;
    const base = wt.layers.filter((l) => !l.reuse).length;
    const answered = new Set(T.range(Math.min(done, n)));
    let i = Math.min(done, n - 1);

    function codeBlock(layer) {
      const roles = Object.keys(layer.roles || {});
      const roleOf = {};
      roles.forEach((r, k) => (layer.marks[r] || []).forEach((ln) => (roleOf[ln] = k % 4)));
      const added = new Set(layer.added);
      return h("pre", { class: "wt-code" }, layer.code.split("\n").map((text, k) => {
        const ln = k + 1;
        return h("span", { class: "ln" + (added.has(ln) ? " add" : "") + (ln in roleOf ? ` r${roleOf[ln]}` : "") },
          h("span", { class: "no", "aria-hidden": "true" }, ln), h("span", { class: "tx" }, text || " "));
      }));
    }

    function render() {
      const layer = wt.layers[i];
      const check = layer.check;
      const last = i === n - 1;

      const out = h("pre", { class: "run-out", hidden: true });
      const runBtn = h("button", { class: "btn small", type: "button" }, "Run it");
      runBtn.onclick = async () => {
        runBtn.disabled = true;
        out.hidden = false;
        out.textContent = "Running in a fresh sandbox…";
        try {
          const r = await run(layer.code);
          out.textContent = r.docker_error || (r.output || "(no output)") + (r.killed ? "\n" + r.killed : "");
        } catch (err) { out.textContent = err.message; }
        runBtn.disabled = false;
      };

      const next = h("button", { class: "btn primary", type: "button", disabled: !answered.has(i),
        onclick: () => (last ? (location.hash = topicHref) : go(i + 1)) }, last ? "Back to the topic" : "Continue");
      const hint = h("span", { class: "wt-hint" }, answered.has(i) ? "" : "Answer the question to continue.");
      const explain = h("p", { class: "wt-explain", "aria-live": "polite", hidden: true });
      const opts = check.options.map((text, k) => h("button", { type: "button", class: "opt", "data-i": k, onclick: () => choose(k) },
        h("kbd", {}, k + 1), h("span", {}, T.inline(text))));

      function choose(k) {
        if (opts[0].disabled) return;
        const right = k === check.answer;
        T.markOptions(opts, check.answer, k);
        explain.hidden = false;
        explain.className = "wt-explain " + (right ? "ok" : "bad");
        explain.replaceChildren(h("span", { class: "explain-mark" }, T.markIcon(right)),
          h("p", {}, h("strong", {}, right ? "Right. " : "Not quite. "), ...T.inline(check.explain)));
        answered.add(i);
        if (onAnswer) onAnswer(i + 1);
        next.disabled = false;
        hint.textContent = "";
        next.focus({ preventScroll: true });
      }

      const roles = Object.keys(layer.roles || {});
      const qid = `wt-q-${i}`;
      const lines = layer.code.split("\n").length;
      container.replaceChildren(...[
        h("h1", {}, layer.title),
        h("div", { class: "wt-meta" },
          h("span", {}, layer.reuse ? "Same skeleton, new problem" : `Layer ${i + 1} of ${base}`),
          h("span", { class: "wt-track", role: "progressbar", "aria-label": "Layers", "aria-valuemin": 1, "aria-valuemax": n, "aria-valuenow": i + 1 },
            wt.layers.map((l, k) => h("i", { class: [k === i ? "here" : answered.has(k) ? "done" : "", l.reuse ? "reuse" : ""].join(" ").trim() || null })))),
        h("div", { class: "prose wt-why" }, T.renderMarkdown(layer.why)),
        h("section", { class: "wt-codecard", "aria-label": "The code so far" },
          h("div", { class: "wt-codebar" },
            roles.length ? h("div", { class: "wt-legend" }, roles.map((r, k) => h("span", { class: `r${k % 4}` }, layer.roles[r])))
              : layer.added.length ? h("span", { class: "wt-key" }, layer.added.length >= lines - 1 ? "All new" : "New in this layer") : h("span"),
            h("div", { class: "wt-run" },
              layer.reuse && problemHref ? h("a", { class: "link", href: problemHref(layer.reuse) }, "Open the problem") : null, runBtn)),
          codeBlock(layer),
          out),
        h("section", { class: "wt-check", "aria-labelledby": qid },
          h("h2", { id: qid }, T.inline(check.question)), h("div", { class: "wt-opts" }, opts), explain),
        h("nav", { class: "wt-nav" },
          i > 0 ? h("button", { class: "btn ghost", type: "button", onclick: () => go(i - 1) }, "Back") : h("span"),
          h("span", { class: "wt-next" }, hint, next)),
      ].filter(Boolean));
    }

    function go(j) {
      i = j;
      render();
      const scroller = container.closest("#app");
      if (scroller) scroller.scrollTop = 0;
    }

    function onKey(e) {
      if (e.ctrlKey || e.metaKey || e.altKey || e.target.matches?.("input, select, textarea")) return;
      if (/^[1-9]$/.test(e.key)) {
        const btn = container.querySelector(`.wt-opts [data-i="${Number(e.key) - 1}"]`);
        if (btn && !btn.disabled) { e.preventDefault(); btn.click(); }
      } else if (e.key === "Enter" && !e.target.matches?.("button, a")) {
        const btn = container.querySelector(".wt-nav .btn.primary");
        if (btn && !btn.disabled) { e.preventDefault(); btn.click(); }
      }
    }
    document.addEventListener("keydown", onKey);

    render();
    return { unmount: () => document.removeEventListener("keydown", onKey) };
  };

  // After a choice: the right answer turns green with a check, a wrong pick red with a cross, the rest settle.
  T.markOptions = (opts, answer, picked) => opts.forEach((b, j) => {
    b.disabled = true;
    if (j === answer) b.classList.add("right");
    else if (j === picked) b.classList.add("wrong");
    if (j === answer || j === picked) b.append(T.markIcon(j === answer));
  });
})();
