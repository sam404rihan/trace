"use strict";
/* "Where are you starting?": three doors, a short adaptive check, and where it places you. */
(function () {
  const T = window.Trace;
  const { h } = T;

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
  T.mountStart = function mountStart(container, check, { place, topicTitle, startHref }) {
    let door = null, gen = null, count = 0, busy = false;
    let ready = {}, answers = {};

    function page(...kids) {
      container.replaceChildren(...kids.flat(Infinity).filter(Boolean));
      const scroller = container.closest("#app");
      if (scroller) scroller.scrollTop = 0;
    }

    function doors() {
      const choice = (id, title, sub) => h("button", { class: "door", type: "button", onclick: () => begin(id) },
        h("strong", {}, title), h("span", {}, sub));
      page(h("h1", {}, "Where are you starting?"),
        h("p", { class: "lede" }, "Pick the closest. A few questions find where to begin, and every topic stays open whatever you choose."),
        h("div", { class: "doors" },
          choice("new", "I'm new to programming", "Start from the very beginning."),
          choice("python", "I can write some Python", "Six Python questions, then the first two stages."),
          choice("dsa", "I've done DSA before", "One question per topic, to find your gaps.")),
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
        opts.forEach((b, j) => {
          b.disabled = true;
          if (j === q.answer) b.classList.add("right");
          else if (j === k) b.classList.add("wrong");
        });
        explain.hidden = false;
        explain.className = "wt-explain " + (answered ? "ok" : "bad");
        explain.replaceChildren(h("strong", {}, answered ? "Right. " : "Not quite. "), ...T.inline(q.explain));
        next.disabled = false;
        next.focus({ preventScroll: true });
      }
      page(h("p", { class: "start-label" }, `${label}, question ${count}`),
        q.code ? h("pre", { class: "start-code" }, q.code) : null,
        h("section", { class: "wt-check" }, h("p", { class: "wt-q" }, T.inline(q.question)), h("div", { class: "wt-opts" }, opts), explain),
        h("nav", { class: "wt-nav" }, h("button", { class: "link", type: "button", onclick: () => finish(door) }, "Stop here"), next));
    }

    function suggest(missed) {
      page(h("p", { class: "start-label" }, "Python basics"),
        h("h1", {}, `You missed ${missed} of the ${check.ready.length} Python questions`),
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
        h("ul", { class: "start-list" }, SKILLS.map((s) => h("li", {}, s))),
        h("p", { class: "start-note" }, "These free courses teach exactly that:"),
        h("ul", { class: "start-list" }, COURSES.map(([name, url]) =>
          h("li", {}, h("a", { class: "link", href: url, target: "_blank", rel: "noopener" }, name)))),
        h("div", { class: "start-actions" },
          h("button", { class: "btn primary", type: "button", onclick: () => begin("python") }, "Take the ready check"),
          h("a", { class: "link", href: "#/" }, "Look around first")));
    }

    function result(placement) {
      const placed = placement.placed_out || [];
      page(h("h1", {}, placement.start ? "Here's where to start" : "You placed out of everything we asked about"),
        placement.start ? h("p", { class: "lede" }, "Start with ", h("strong", {}, topicTitle(placement.start)), ".") : null,
        placed.length ? [h("p", { class: "start-label" }, "Placed out (still open any time)"),
          h("ul", { class: "start-list" }, placed.map((id) => h("li", {}, topicTitle(id))))] : null,
        h("div", { class: "start-actions" },
          h("a", { class: "btn primary", href: placement.start ? startHref(placement.start) : "#/roadmap" }, placement.start ? "Start here" : "Go to the roadmap"),
          placement.start ? h("a", { class: "link", href: "#/" }, "See all topics") : null));
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
