"use strict";
/* Home and roadmap. Home is one next step: a stage-coloured card with the topic's drawing, what comes
   next, and one button. The roadmap holds the whole course. app.js owns the course state and passes
   in what to show. */
(function () {
  const T = window.Trace;
  const { h, s } = T;

  const go = () => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M5 12h13M13 6l6 6-6 6" }));

  // ctx: { target, started, stageNo, stageName, topicTitle, topicDone, topicTotal }
  // target is resumeTarget() from app.js; null when the whole course is done.
  T.mountHome = (host, ctx) => {
    const t = ctx.target;
    if (!t) {
      host.replaceChildren(h("div", { class: "home" },
        h("section", { class: "hero", "data-stage": "6", "aria-labelledby": "hero-title" },
          h("div", { class: "hero-text" },
            h("h1", { id: "hero-title" }, "You've finished the course"),
            h("p", { class: "hero-next" }, "Every topic, every problem. Keep it sharp with the review drill, or work through a study plan."),
            h("a", { class: "btn primary hero-go", href: "#/roadmap" }, "Open the roadmap", go()),
            h("p", { class: "hero-also" }, h("a", { href: "#/d/spot-pattern/spot" }, "Or start the review drill"))),
          h("div", { class: "hero-art" }, T.topicArt(34)))));
      build(host);
      return { unmount() {} };
    }
    host.replaceChildren(h("div", { class: "home" },
      h("section", { class: "hero", "data-stage": String(ctx.stageNo), "aria-labelledby": "hero-title" },
        h("div", { class: "hero-text" },
          h("h1", { id: "hero-title" }, ctx.topicTitle),
          h("p", { class: "hero-stage" }, t.plan ? `From ${t.plan.title}` : `Stage ${ctx.stageNo} · ${ctx.stageName}`),
          h("p", { class: "hero-next" }, h("strong", {}, t.title), h("span", { class: "hero-kind" }, t.itemLabel)),
          h("a", { class: "btn primary hero-go", href: t.href }, ctx.started ? "Continue" : "Start", go())),
        h("div", { class: "hero-art" }, T.topicArt(t.topic.n))),
      h("div", { class: "home-under" },
        h("p", { class: "hero-progress" },
          h("span", { class: "meter", style: `--share:${ctx.topicTotal ? ctx.topicDone / ctx.topicTotal : 0}`, "aria-hidden": "true" }, h("i")),
          `${ctx.topicDone} of ${ctx.topicTotal} in ${ctx.topicTitle}`),
        h("a", { class: "home-road", href: "#/roadmap" }, "See the roadmap", go()))));
    build(host);
    return { unmount() {} };
  };

  // Crop the drawing to what it actually draws, so it fills the card, then let it build itself in.
  // Measured before the build-in starts, since the parts begin moved and shrunk.
  function build(host) {
    const svg = host.querySelector(".hero-art svg");
    if (!svg) return;
    if (svg.isConnected) {
      const b = svg.getBBox(), pad = 10;
      if (b.width && b.height) svg.setAttribute("viewBox", `${b.x - pad} ${b.y - pad} ${b.width + 2 * pad} ${b.height + 2 * pad}`);
    }
    svg.classList.add("build");
  }

  const check = () => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M5 12.5l4.5 4.5L19 7.5" }));
  const chevron = () => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M6 9l6 6 6-6" }));

  // ctx: { stages: [{ no, name, topics: [{ id, n, title, done, total, placedOut }] }], hereTopicId, extras: Node[] }
  // The current stage is the one holding hereTopicId (the last stage once everything is done). Folded stages
  // keep their topics as a compact row of numbered links, so every topic stays one click away.
  T.mountRoadmap = (host, ctx) => {
    const finished = (t) => t.placedOut || (t.total > 0 && t.done === t.total);
    const current = ctx.stages.find((st) => st.topics.some((t) => t.id === ctx.hereTopicId)) || ctx.stages[ctx.stages.length - 1];
    const stage = (st) => {
      const state = st === current ? "current" : st.topics.every(finished) ? "done" : "ahead";
      const doneCount = st.topics.filter(finished).length;
      const li = h("li", { class: "road-stage", "data-state": state, "data-stage": String(st.no), "data-open": st === current ? "" : null });
      const listId = `road-${st.no}`;
      const toggle = h("button", { class: "road-toggle", type: "button", "aria-expanded": String(st === current), "aria-controls": listId,
        onclick: () => {
          const open = !li.hasAttribute("data-open");
          li.toggleAttribute("data-open", open);
          toggle.setAttribute("aria-expanded", String(open));
        } }, h("span", { class: "sr-only" }, `Show or hide ${st.name}`), chevron());
      li.append(
        h("span", { class: "road-marker", "aria-hidden": "true" }, state === "done" ? check() : String(st.no)),
        h("div", { class: "road-body" },
          h("div", { class: "road-head" },
            h("h2", {}, st.name),
            h("span", { class: "road-count" }, `${doneCount} of ${st.topics.length} topics`),
            toggle),
          h("ol", { class: "road-stops", id: listId }, st.topics.map((t) => h("li", {},
            h("a", { class: "road-stop" + (finished(t) ? " done" : "") + (t.id === ctx.hereTopicId ? " here" : ""), href: `#/t/${t.id}`,
              title: t.title, "aria-current": t.id === ctx.hereTopicId ? "step" : null },
              h("span", { class: "road-n" }, finished(t) ? check() : String(t.n).padStart(2, "0")),
              h("span", { class: "road-title" }, t.title),
              t.id === ctx.hereTopicId ? h("span", { class: "road-here" }, "You're here") : null,
              t.placedOut ? h("span", { class: "badge placed" }, "Placed out") : null,
              h("span", { class: "road-progress" }, `${t.done}/${t.total}`)))))));
      return li;
    };
    host.replaceChildren(h("div", { class: "page road-page" },
      h("h1", {}, "Your roadmap"),
      h("p", { class: "lede" }, `${ctx.stages.reduce((n, st) => n + st.topics.length, 0)} topics in ${ctx.stages.length} stages, from the basics to specialist techniques. Open any stage to see its topics.`),
      h("ol", { class: "road" }, ctx.stages.map(stage)),
      ctx.extras));
    return { unmount() {} };
  };
})();
