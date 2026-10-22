"use strict";
/* "Where are you starting?": three doors, a short adaptive check, and where it places you. */
(function () {
  const T = window.Trace;
  const { h, s } = T;
  const icon = (d) => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d }));
  const ICON = { go: "M5 12h13M13 6l6 6-6 6", check: "M5 12.5l4.5 4.5L19 7.5", out: "M14 5h5v5M19 5l-8 8M18 14v4a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h4" };
  // A small staircase of tiles: how far into programming each door starts you.
  const stairs = (k) => s("svg", { class: "door-art", viewBox: "0 0 64 50", "aria-hidden": "true" },
    T.range(3).map((j) => s("rect", { x: 2 + j * 21, y: 46 - (j + 1) * 14, width: 18, height: (j + 1) * 14, rx: 5, class: j < k ? "on" : null })));

  const COURSES = [
    ["The official Python tutorial", "https://docs.python.org/3/tutorial/"],
    ["Harvard's CS50P", "https://cs50.harvard.edu/python/"],
    ["Python for Everybody", "https://www.py4e.com/"],
  ];
  const SKILLS = [
    "Give names to values and change them",
    "Use if/else and loops (for, while, range)",
    "Write functions that return a result",
    "Index, slice and loop over lists",
    "Count and look things up with a dict",
    "Make a small class and follow references between objects",
  ];

  // check: the /api/starting-check payload. place(payload) -> Promise of the new progress.
  // stageOf(id) and topicNo(id) let the result draw where you start on its stage colour.
  T.mountStart = function mountStart(container, check, { place, topicTitle, startHref, stageOf = () => 1, topicNo = (id) => parseInt(id, 10) || 1 }) {
    let door = null, gen = null, count = 0, busy = false;
    let ready = {}, answers = {};

    function page(...kids) {
      container.replaceChildren(...kids.flat(Infinity).filter(Boolean));
      const scroller = container.closest("#app");
      if (scroller) scroller.scrollTop = 0;
    }

    function doors() {
      const choice = (id, title, sub, k) => h("button", { class: "door", type: "button", onclick: () => begin(id) },
        stairs(k), h("span", { class: "door-text" }, h("strong", {}, title), h("span", { class: "door-sub" }, sub)), icon(ICON.go));
      page(h("h1", {}, "Where are you starting?"),
        h("p", { class: "lede" }, "Pick the closest. A few questions find where to begin, and every topic stays open whatever you choose."),
        h("div", { class: "doors" },
          choice("new", "I'm new to programming", "Start from the very beginning.", 1),
          choice("python", "I can write some Python", "Six Python questions, then the first two stages.", 2),
          choice("dsa", "I've done DSA before", "One question per topic, to find your gaps.", 3)),
        h("p", { class: "start-skip" }, h("button", { class: "link", type: "button", onclick: () => finish("skip") }, "I can program, show me everything")));
    }

    function begin(id) {
      if (id === "new") return finish("new");
      door = id;
      count = 0;
      ready = {};
      answers = {};
      gen = flow(id);
      step(undefined);
    }

    // Yields one question (or the "learn Python first?" screen) at a time; receives true/false back.
    function* flow(id) {
      if (id === "python") {
        let missed = 0;
        for (const q of check.ready) {
          ready[q.skill] = yield { label: "Python basics", q };
          if (!ready[q.skill]) missed++;
        }
        if (missed >= 2 && !(yield { suggest: missed })) return "new";
      }
      let failed = 0;
      for (const t of check.topics) {
        if (id === "python" && t.stage_n > 2) break;
        const label = topicTitle(t.id);
        const got = [yield { label, q: t.questions[0] }];
        if (got[0] && id === "python") got.push(yield { label, q: t.questions[1] });
        answers[t.id] = got;
        if (id === "python" && !got.every(Boolean) && ++failed >= 2) break;
      }
      return "done";
    }

    function step(value) {
      const r = gen.next(value);
      if (r.done) return finish(r.value === "new" ? "new" : door);
      if (r.value.suggest) return suggest(r.value.suggest);
      question(r.value);
    }

    function question({ label, q }) {
      count++;
      let answered = null;
      const explain = h("p", { class: "wt-explain", "aria-live": "polite", hidden: true });
      const next = h("button", { class: "btn primary", type: "button", disabled: true, onclick: () => step(answered) }, "Continue");
      const opts = q.options.map((text, k) => h("button", { type: "button", class: "opt", "data-i": k, onclick: () => choose(k) },
        h("kbd", {}, k + 1), h("span", {}, T.inline(text))));
      function choose(k) {
        if (answered !== null) return;
        answered = k === q.answer;
        T.markOptions(opts, q.answer, k);
        explain.hidden = false;
        explain.className = "wt-explain " + (answered ? "ok" : "bad");
        explain.replaceChildren(h("span", { class: "explain-mark" }, T.markIcon(answered)),
          h("p", {}, h("strong", {}, answered ? "Right. " : "Not quite. "), ...T.inline(q.explain)));
        next.disabled = false;
        next.focus({ preventScroll: true });
      }
      page(h("h1", { class: "start-q" }, T.inline(q.question)),
        h("p", { class: "start-sub" }, `${label} · question ${count}`),
        q.code ? h("pre", { class: "start-code" }, q.code) : null,
        h("section", { class: "wt-check", "aria-label": "Answers" }, h("div", { class: "wt-opts" }, opts), explain),
        h("nav", { class: "wt-nav" }, h("button", { class: "link", type: "button", onclick: () => finish(door) }, "Stop here"), next));
    }

    function suggest(missed) {
      page(h("h1", {}, `You missed ${missed} of the ${check.ready.length} Python questions`),
        h("p", { class: "lede" }, "Trace expects you to read and write small Python programs. A short Python course first might help more, but it's your call."),
        h("div", { class: "start-actions" },
          h("button", { class: "btn primary", type: "button", onclick: () => step(false) }, "Show me where to learn Python"),
          h("button", { class: "btn", type: "button", onclick: () => step(true) }, "Continue anyway")));
    }

    async function finish(chosen) {
      if (busy) return;
      busy = true;
      try {
        const progress = await place(chosen === "new" || chosen === "skip" ? { door: chosen } : { door: chosen, ready, answers });
        if (chosen === "skip") location.hash = "#/";
        else if (chosen === "new") newcomer();
        else result(progress.placement);
      } catch (err) {
        page(h("h1", {}, "That didn't save"), h("p", { class: "lede" }, err.message),
          h("div", { class: "start-actions" },
            h("button", { class: "btn primary", type: "button", onclick: () => finish(chosen) }, "Try again"),
            h("a", { class: "link", href: "#/roadmap" }, "Go to the roadmap")));
      } finally {
        busy = false;
      }
    }

    function newcomer() {
      page(h("h1", {}, "Start with Python"),
        h("p", { class: "lede" }, "Trace teaches data structures and algorithms in Python, so it expects you to read and write small programs first. You're ready when you can:"),
        h("ul", { class: "start-skills" }, SKILLS.map((skill) => h("li", {}, h("span", { class: "start-tick" }, icon(ICON.check)), skill))),
        h("h2", {}, "Free courses that teach exactly that"),
        h("ul", { class: "start-courses" }, COURSES.map(([name, url]) =>
          h("li", {}, h("a", { href: url, target: "_blank", rel: "noopener" }, h("span", {}, name), icon(ICON.out))))),
        h("div", { class: "start-actions" },
          h("button", { class: "btn primary", type: "button", onclick: () => begin("python") }, "Take the ready check"),
          h("a", { class: "link", href: "#/" }, "Look around first")));
    }

    function result(placement) {
      const placed = placement.placed_out || [];
      const start = placement.start;
      const stage = start ? stageOf(start) : 1;
      page(h("h1", {}, start ? "Here's where to start" : "You placed out of everything we asked about"),
        start ? h("section", { class: "start-card", "data-stage": String(stage), "aria-label": "Where you start" },
          h("div", { class: "start-card-text" },
            h("h2", {}, topicTitle(start)),
            h("p", {}, `Stage ${stage}` + (T.stageNames && T.stageNames[stage - 1] ? ` · ${T.stageNames[stage - 1]}` : "")),
            h("a", { class: "btn primary hero-go", href: startHref(start) }, "Start here", icon(ICON.go))),
          h("div", { class: "start-card-art" }, T.topicArt ? T.topicArt(topicNo(start)) : null)) : null,
        placed.length ? h("section", { class: "start-placed" },
          h("h2", {}, "You placed out of these"),
          h("ul", {}, placed.map((id) => h("li", {}, h("span", { class: "start-tick" }, icon(ICON.check)), topicTitle(id)))),
          h("p", { class: "start-note" }, "They stay open any time.")) : null,
        h("div", { class: "start-actions" },
          start ? h("a", { class: "link", href: "#/roadmap" }, "See the roadmap")
            : h("a", { class: "btn primary", href: "#/roadmap" }, "Go to the roadmap")));
      if (T.cropArt) T.cropArt(container.querySelector(".start-card-art svg"));
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

    doors();
    return { unmount: () => document.removeEventListener("keydown", onKey) };
  };

  // The four stages Trace uses everywhere. Shown on your first problem; "I'm stuck" (Phase 3) reuses it.
  const HOW = [
    ["Understand.", "Work the example by hand, then make up a smaller input and solve that too."],
    ["Plan.", "Say the brute force first, then look for the work it repeats."],
    ["Code.", "Write the slow version and get one test passing, then change one thing at a time."],
    ["Check.", "Open the first failing test, run your function on it with Try a call, and find where it differs from your plan."],
  ];
  T.howToCard = ({ onClose } = {}) => h("section", { class: "howto", "aria-label": "How to work a problem" },
    h("div", { class: "howto-head" }, h("h4", {}, "How to work a problem"),
      onClose ? h("button", { class: "btn ghost small", type: "button", onclick: onClose }, "Got it") : null),
    h("ol", {}, HOW.map(([stage, text]) => h("li", {}, h("strong", {}, stage), " ", text))));
})();
