"use strict";
/* Techniques: the "New technique" box on teaching problems, the "Uses" row on every problem, the
   banner for techniques taught in other topics, and a topic's list of techniques. */
(function () {
  const T = window.Trace;
  const { h, s } = T;
  const check = () => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M5 12.5l4.5 4.5L19 7.5" }));

  // ctx comes from app.js: techniques, known(id), teacherHref(id), teacherTitle(id), teacherTopic(id),
  // topicTitle(topic), taughtIn(topic). Ids missing from the registry are skipped everywhere.
  T.techniqueBoxes = (problem, ctx) => (problem.teaches || []).filter((id) => ctx.techniques[id]).map((id) =>
    h("section", { class: "tech-new", "aria-label": "New technique" },
      h("h4", {}, "New technique: ", ctx.techniques[id].name),
      h("p", {}, T.inline(ctx.techniques[id].explain))));

  T.usesRow = (problem, ctx) => {
    const ids = (problem.uses || []).filter((id) => ctx.techniques[id]);
    if (!ids.length) return null;
    const detail = h("div", { class: "tech-detail", hidden: true });
    let open = null;
    const chips = ids.map((id) => h("button", {
      type: "button", class: "tech-chip" + (ctx.known(id) ? " known" : ""), "aria-expanded": "false",
      onclick: (e) => {
        open = open === id ? null : id;
        chips.forEach((b) => b.setAttribute("aria-expanded", String(b === e.currentTarget && open === id)));
        detail.hidden = !open;
        if (open) detail.replaceChildren(h("p", {}, T.inline(ctx.techniques[id].explain)),
          ctx.teacherHref(id) ? h("p", { class: "tech-teacher" }, ctx.known(id) ? "Learned in " : "Taught in ",
            h("a", { class: "link", href: ctx.teacherHref(id) }, ctx.teacherTitle(id))) : null);
      },
    }, ctx.known(id) ? check() : null, ctx.techniques[id].name));
    return h("div", { class: "tech-uses-wrap" }, h("div", { class: "tech-uses" }, h("span", { class: "tech-label" }, "Uses"), chips), detail);
  };

  T.techniqueBanner = (problem, topic, ctx) => {
    const missing = (problem.uses || []).filter((id) => ctx.techniques[id] && !ctx.known(id)
      && ctx.teacherTopic(id) && ctx.teacherTopic(id).id !== topic.id);
    if (!missing.length) return null;
    return h("div", { class: "tech-banner" }, missing.map((id) => h("p", {}, "This uses ", h("strong", {}, ctx.techniques[id].name),
      ` (${ctx.topicTitle(ctx.teacherTopic(id))}). If it's new to you, try `,
      h("a", { class: "link", href: ctx.teacherHref(id) }, ctx.teacherTitle(id)), " first.")));
  };

  T.topicTechniques = (topic, ctx) => {
    const ids = ctx.taughtIn(topic);
    if (!ids.length) return null;
    // Folded on the topic page: a reference to look things up in, not another list to work through.
    const chevron = s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, s("path", { d: "M6 9l6 6 6-6" }));
    return h("details", { class: "fold tech-fold" },
      h("summary", {}, h("span", { class: "fold-title" }, "Techniques in this topic"),
        h("span", { class: "fold-sub" }, `${ids.filter(ctx.known).length} of ${ids.length} learned`), chevron),
      h("div", { class: "fold-body" },
        h("div", { class: "items tech-list" }, ids.map((id) => h("a", { class: "item" + (ctx.known(id) ? " solved" : ""), href: ctx.teacherHref(id) },
          h("span", { class: "state" }), h("span", { class: "t" }, ctx.techniques[id].name),
          h("span", { class: "meta" }, ctx.teacherTitle(id)), h("span"))))));
  };
})();
