"use strict";
/* Home and roadmap. Home is one next step: a stage-coloured card with the topic's drawing, what comes
   next, and one button. The roadmap holds the whole course. app.js owns the course state and passes
   in what to show. */
(function () {
  const T = window.Trace;
  const { h, s } = T;

  const go = () => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M5 12h13M13 6l6 6-6 6" }));

  // ctx: { target, started, stageNo, stageName, topicTitle, topicDone, topicTotal, placement }
  // target is resumeTarget() from app.js; null when the whole course is done.
  T.mountHome = (host, ctx) => {
    const t = ctx.target;
    const drawing = (n) => { const svg = T.topicArt(n); svg.classList.add("build"); return svg; };
    if (!t) {
      host.replaceChildren(h("div", { class: "home" },
        h("section", { class: "hero", "data-stage": "6" },
          h("div", { class: "hero-art" }, drawing(34)),
          h("div", { class: "hero-text" },
            h("h1", {}, "You've finished the course"),
            h("p", { class: "hero-next" }, "Every topic, every problem. Keep it sharp with the review drill, or work through a study plan."),
            h("a", { class: "btn primary hero-go", href: "#/roadmap" }, "Open the roadmap", go())))));
      return { unmount() {} };
    }
    host.replaceChildren(h("div", { class: "home" },
      h("section", { class: "hero", "data-stage": String(ctx.stageNo), "aria-labelledby": "hero-title" },
        h("div", { class: "hero-text" },
          h("h1", { id: "hero-title" }, ctx.topicTitle),
          h("p", { class: "hero-stage" }, t.plan ? `From ${t.plan.title}` : `Stage ${ctx.stageNo} · ${ctx.stageName}`),
          h("p", { class: "hero-next" }, h("span", { class: "hero-kind" }, t.itemLabel), h("strong", {}, t.title)),
          h("a", { class: "btn primary hero-go", href: t.href }, ctx.started ? "Continue" : "Start", go())),
        h("div", { class: "hero-art" }, drawing(t.topic.n))),
      h("div", { class: "home-under" },
        h("p", { class: "hero-progress" },
          h("span", { class: "meter", style: `--share:${ctx.topicTotal ? ctx.topicDone / ctx.topicTotal : 0}`, "aria-hidden": "true" }, h("i")),
          `${ctx.topicDone} of ${ctx.topicTotal} in ${ctx.topicTitle}`),
        h("a", { class: "home-road", href: "#/roadmap" }, "See the roadmap", go())),
      ctx.placement ? null
        : h("p", { class: "home-check" }, "Not sure where to start? ", h("a", { class: "link", href: "#/start" }, "Take the starting check"))));
    return { unmount() {} };
  };
})();
