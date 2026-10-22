"use strict";
/* Trace app: home, topic ladders, the coding workspace, and the intuition drills. */
(function () {
  const T = window.Trace;
  const { h } = T;
  const $ = (id) => document.getElementById(id);
  const app = $("app");

  const S = {
    topics: [],            // course topics from the server, in order
    problems: {},          // name -> summary
    progress: { problems: {}, unlocked: [] },
    plans: { plans: [], reported: {}, reported_note: "" },
    docker: { state: "checking" },
    cleanup: null,         // teardown for the current view
  };

  // ── utilities ──────────────────────────────────────────────────────────────
  async function api(path, body) {
    const res = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
    return data;
  }
  const local = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
  };
  const pad2 = (n) => String(n).padStart(2, "0");
  const icon = (d) => {
    const svg = T.s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" });
    for (const path of [].concat(d)) svg.append(T.s("path", { d: path }));
    return svg;
  };
  const ICONS = {
    play: "M7 5l12 7-12 7z",
    reset: ["M4 12a8 8 0 1 0 2.4-5.7", "M4 4v5h5"],
    left: "M15 6l-6 6 6 6",
    right: "M9 6l6 6-6 6",
    lock: ["M6 11h12v9H6z", "M8.5 11V8a3.5 3.5 0 0 1 7 0v3"],
    check: "M5 12.5l4.5 4.5L19 7.5",
    home: ["M4 11l8-6.5 8 6.5", "M6.5 9.5V19h11V9.5"],
    road: ["M9 5L4 7v12l5-2 6 2 5-2V5l-5 2z", "M9 5v12", "M15 7v12"],
    plan: ["M8 6h11", "M8 12h11", "M8 18h11", "M4.5 6h.01", "M4.5 12h.01", "M4.5 18h.01"],
    contest: T.CONTEST_ICON,
    down: "M6 9l6 6 6-6",
    cross: ["M7.5 7.5l9 9", "M16.5 7.5l-9 9"],
    code: ["M9 7l-5 5 5 5", "M15 7l5 5-5 5"],
    idea: ["M9.5 18h5", "M10.5 21h3", "M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3z"],
    review: ["M19.5 10A8 8 0 0 0 5.6 6.4", "M5 3v4h4", "M4.5 14a8 8 0 0 0 13.9 3.6", "M19 21v-4h-4"],
    go: ["M5 12h13", "M13 6l6 6-6 6"],
  };

  // inline `code`
  function inline(text) {
    return String(text).split(/(`[^`]+`)/g).filter(Boolean).map((part) =>
      part.startsWith("`") && part.endsWith("`") ? h("code", {}, part.slice(1, -1)) : part);
  }

  // Problem statements: paragraphs, "  - " lists with indented continuations, and 4-space code blocks.
  function renderStatement(text) {
    const out = [];
    let seg = null;
    const flush = () => {
      if (!seg) return;
      if (seg.type === "p") out.push(h("p", {}, inline(seg.lines.join(" "))));
      if (seg.type === "pre") {
        const indent = Math.min(...seg.lines.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length));
        out.push(h("pre", {}, seg.lines.map((l) => l.slice(indent)).join("\n").replace(/\s+$/, "")));
      }
      if (seg.type === "ul") out.push(h("ul", {}, seg.items.map((it) => h("li", {}, inline(it)))));
      seg = null;
    };
    for (const line of text.split("\n")) {
      if (!line.trim()) {
        if (seg && seg.type === "pre") { seg.lines.push(""); continue; }
        flush();
        continue;
      }
      const li = line.match(/^\s{0,4}- (.*)$/);
      if (li) {
        if (!seg || seg.type !== "ul") { flush(); seg = { type: "ul", items: [] }; }
        seg.items.push(li[1]);
      } else if (seg && seg.type === "ul" && /^\s{3,}\S/.test(line)) {
        seg.items[seg.items.length - 1] += " " + line.trim();
      } else if (/^ {4}/.test(line)) {
        if (!seg || seg.type !== "pre") { flush(); seg = { type: "pre", lines: [] }; }
        seg.lines.push(line);
      } else {
        if (!seg || seg.type !== "p") { flush(); seg = { type: "p", lines: [] }; }
        seg.lines.push(line.trim());
      }
    }
    flush();
    return out;
  }

  // A statement's parts: the problem text, the indented example block after "Example:", and any notes after it.
  function splitStatement(text) {
    const lines = text.split("\n");
    const at = lines.findIndex((l) => /^\s*Examples?:\s*$/.test(l));
    if (at < 0) return { desc: text, example: "", notes: "" };
    let end = at + 1;
    while (end < lines.length && (!lines[end].trim() || /^ {2,}/.test(lines[end]))) end++;
    const block = lines.slice(at + 1, end);
    while (block.length && !block[block.length - 1].trim()) block.pop();
    const indent = Math.min(...block.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length));
    return { desc: lines.slice(0, at).join("\n"), example: block.map((l) => l.slice(indent)).join("\n"), notes: lines.slice(end).join("\n") };
  }

  // Lesson notes: a small markdown subset.
  function renderMarkdown(text) {
    const out = [];
    let para = [], list = null, code = null;
    const flushPara = () => { if (para.length) out.push(h("p", {}, inline(para.join(" ")))); para = []; };
    const flushList = () => { if (list) out.push(h("ul", {}, list.map((i) => h("li", {}, inline(i))))); list = null; };
    for (const line of text.split("\n")) {
      if (code) {
        if (line.trim().startsWith("```")) { out.push(h("pre", {}, h("code", {}, code.join("\n")))); code = null; }
        else code.push(line);
        continue;
      }
      if (line.trim().startsWith("```")) { flushPara(); flushList(); code = []; continue; }
      if (/^# /.test(line)) continue;
      const hm = line.match(/^(#{2,3}) (.*)$/);
      if (hm) { flushPara(); flushList(); out.push(h(hm[1].length === 2 ? "h2" : "h3", {}, hm[2])); continue; }
      const lm = line.match(/^\s*- (.*)$/);
      if (lm) { flushPara(); (list ||= []).push(lm[1]); continue; }
      if (!line.trim()) { flushPara(); flushList(); continue; }
      if (list) { list[list.length - 1] += " " + line.trim(); continue; }
      para.push(line.trim());
    }
    flushPara(); flushList();
    return out;
  }
  T.inline = inline;               // shared with walkthrough.js
  T.renderMarkdown = renderMarkdown;

  // ── course model ───────────────────────────────────────────────────────────
  const drillTopic = (topic) => T.topics.find((d) => d.n === topic.n);
  const topicTitle = (topic) => drillTopic(topic)?.title || topic.title;
  const pstate = (name) => S.progress.problems[name] || {};
  const solved = (name) => !!pstate(name).solved;
  const wtGot = (topic) => (S.progress.walkthroughs || {})[topic.id] || 0;
  const wtDone = (topic) => topic.has_walkthrough && wtGot(topic) >= topic.walkthrough_layers;
  const kindLabel = (p) => (p.kind === "solo" ? p.difficulty[0].toUpperCase() + p.difficulty.slice(1) : p.kind[0].toUpperCase() + p.kind.slice(1));
  function firstStep(topic) {
    const dt = drillTopic(topic);
    if (dt) return `#/d/${dt.id}/${dt.drills[0].id}`;
    if (topic.has_walkthrough) return `#/w/${topic.id}`;
    return topic.items.length ? `#/p/${topic.items[0]}` : `#/t/${topic.id}`;
  }
  const placedOut = (topic) => (S.progress.placement?.placed_out || []).includes(topic.id);
  T.reachedTopics = () => {
    const out = new Set(S.progress.placement?.placed_out || []);
    for (const topic of S.topics) {
      const dt = drillTopic(topic);
      if ((dt && dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0)) || wtGot(topic) > 0
          || topic.items.some((n) => (pstate(n).passed || 0) > 0)) out.add(topic.id);
    }
    return out;
  };
  // A technique is known once its teacher is solved, or its teacher's topic is placed out.
  const techTeacher = (id) => (S.techniques || {})[id]?.teacher || null;
  const techKnown = (id) => { const t = techTeacher(id); return !!t && (solved(t) || placedOut(topicOf(t))); };
  const techCtx = () => ({
    techniques: S.techniques || {}, known: techKnown,
    teacherHref: (id) => (techTeacher(id) ? `#/p/${techTeacher(id)}` : null),
    teacherTitle: (id) => (techTeacher(id) ? S.problems[techTeacher(id)].title : ""),
    teacherTopic: (id) => (techTeacher(id) ? topicOf(techTeacher(id)) : null),
    topicTitle,
    taughtIn: (topic) => topic.items.flatMap((n) => S.problems[n].teaches || []).filter((id) => (S.techniques || {})[id]),
  });

  // Ladder rule: snippet → guided → solos together → build after two solos, and never before a same-topic teacher of a technique it uses.
  function blocker(topic, name) {
    const of = (k) => topic.items.filter((n) => S.problems[n].kind === k);
    const kind = S.problems[name].kind;
    const need = kind === "guided" ? of("snippet") : kind === "solo" || kind === "build" ? [...of("snippet"), ...of("guided")] : [];
    const missing = need.find((n) => !solved(n));
    if (missing) return missing;
    if (kind === "build") {
      const solos = of("solo");
      if (solos.filter(solved).length < Math.min(2, solos.length)) return solos.find((n) => !solved(n));
    }
    if ((pstate(name).passed || 0) > 0 || (pstate(name).steps || 0) > 0) return null;   // already started: never lock it later
    return (S.problems[name].uses || []).map(techTeacher).find((t) => t && t !== name && topic.items.includes(t) && !solved(t)) || null;
  }
  function isUnlocked(topic, name) {
    if (solved(name) || S.progress.unlocked.includes(name) || placedOut(topic)) return true;
    return blocker(topic, name) == null;
  }

  function pillLabel(topic, name) {
    const p = S.problems[name];
    if (p.kind === "snippet") return "S";
    if (p.kind === "guided") return "G";
    if (p.kind === "build") return "B";
    const solos = topic.items.filter((n) => S.problems[n].kind === "solo");
    return String(solos.indexOf(name) + 1);
  }

  function nextUp() {
    for (const topic of S.topics) {
      if (placedOut(topic)) continue;
      const dt = drillTopic(topic);
      const started = dt && dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0);
      const next = topic.items.find((n) => !solved(n));
      if (!next) continue;
      if (dt && !started && topic.items.every((n) => !solved(n))) return { kind: "drill", topic, dt, drill: dt.drills[0] };
      if (topic.has_walkthrough && !wtDone(topic) && topic.items.every((n) => !solved(n))) return { kind: "walkthrough", topic };
      return { kind: "problem", topic, name: next };
    }
    return null;
  }

  // Where you stopped: the last problem, drill or walkthrough that actually opened (a lock screen you
  // backed away from doesn't count, nor does the review drill). Kept per machine, like the theme.
  const recordStop = (hash) => local.set("trace.lastStop", { hash });
  const ITEM_LABEL = { snippet: "Snippet", guided: "Guided problem", build: "Build" };
  function describeStop(t) {
    if (t.kind === "drill") return { href: `#/d/${t.dt.id}/${t.drill.id}`, topic: t.topic, kind: "drill", title: t.drill.name, itemLabel: "Intuition drill", plan: null };
    if (t.kind === "walkthrough") return { href: `#/w/${t.topic.id}`, topic: t.topic, kind: "walkthrough", title: "Build the pattern, one piece at a time", itemLabel: "Read the code", plan: null };
    const p = S.problems[t.name];
    return { href: t.plan ? `#/p/${t.name}/plan/${t.plan.id}` : `#/p/${t.name}`, topic: t.topic, kind: "problem", title: p.title,
      itemLabel: ITEM_LABEL[p.kind] || `${p.difficulty[0].toUpperCase()}${p.difficulty.slice(1)} problem`,
      plan: t.plan ? { id: t.plan.id, title: t.plan.title } : null };
  }
  // What Continue opens: where you stopped if it still exists and isn't finished, else the course's next step.
  function resumeTarget() {
    const stop = local.get("trace.lastStop", null);
    const [, kind, a, b, c] = (stop && typeof stop.hash === "string" ? stop.hash : "").split("/");
    let t = null;
    if (kind === "p" && Object.hasOwn(S.problems, a) && topicOf(a) && !solved(a)) {
      const plan = b === "plan" ? (S.plans.plans || []).find((pl) => pl.id === c && planItemsOf(pl).includes(a)) || null : null;
      if (plan || isUnlocked(topicOf(a), a)) t = { kind: "problem", topic: topicOf(a), name: a, plan };
    } else if (kind === "d" && Object.hasOwn(T.byId, a) && T.byId[a].n !== 99) {
      const dt = T.byId[a], drill = dt.drills.find((d) => d.id === b), topic = S.topics.find((x) => x.n === dt.n);
      if (drill && topic && !T.DrillProgress.solid(dt, drill)) t = { kind: "drill", topic, dt, drill };
    } else if (kind === "w") {
      const topic = S.topics.find((x) => x.id === a);
      if (topic && topic.has_walkthrough && !wtDone(topic)) t = { kind: "walkthrough", topic };
    }
    if (!t) t = nextUp();
    return t ? describeStop(t) : null;
  }
  T.resumeTarget = resumeTarget;
  // Your place on the course path: where Continue goes, unless that's a study-plan detour.
  function pathTopic() {
    const t = resumeTarget();
    return t && !t.plan ? t.topic : nextUp()?.topic || null;
  }

  function topicOf(name) { return S.topics.find((t) => t.items.includes(name)); }
  // 1-based position of the topic's stage among the course's stages, in course order.
  const stageNames = () => [...new Set(S.topics.map((t) => t.stage))];
  const stageOf = (topic) => stageNames().indexOf(topic.stage) + 1;
  function nextItem(name) {
    const topic = topicOf(name);
    const i = topic.items.indexOf(name);
    if (i + 1 < topic.items.length) return { topic, name: topic.items[i + 1] };
    const ti = S.topics.indexOf(topic);
    return ti + 1 < S.topics.length ? { topic: S.topics[ti + 1], name: null } : null;
  }

  // ── chrome: breadcrumbs, docker status, theme ──────────────────────────────
  function crumbs(...parts) {
    const kids = [];
    parts.forEach((p, i) => {
      if (i) kids.push(h("span", { class: "sep", "aria-hidden": "true" }, icon(ICONS.right)));
      kids.push(p.href ? h("a", { href: p.href }, p.label) : h("span", { class: "here" }, p.label));
    });
    $("crumbs").replaceChildren(...kids);
  }

  const DOCKER_TEXT = {
    ready: ["ready", "Sandbox ready"], checking: ["busy", "Checking Docker…"], building: ["busy", "Preparing sandbox…"],
    stopped: ["down", "Docker isn't running"], missing: ["down", "Docker not installed"], broken: ["down", "Sandbox build failed"],
  };
  let dockerTimer = null;
  function showDocker(status) {
    S.docker = status || S.docker;
    const [tone, text] = DOCKER_TEXT[S.docker.state] || DOCKER_TEXT.checking;
    const el = $("sandbox");
    el.className = "sandbox " + tone;
    el.title = S.docker.state === "ready"
      ? (S.docker.mode === "docker" ? "Each Run starts a fresh, locked-down Docker container." : "Each Run starts a fresh Python process with time and memory limits.")
      : (S.docker.detail || text);
    el.lastElementChild.textContent = text;
    clearTimeout(dockerTimer);
    if (S.docker.state !== "ready") dockerTimer = setTimeout(async () => showDocker(await api("/api/docker").catch(() => S.docker)), 3000);
  }

  function applyTheme(t) {
    if (t) document.documentElement.dataset.theme = t;
    else delete document.documentElement.dataset.theme;
  }
  applyTheme(local.get("trace.theme", null));
  $("theme-btn").onclick = () => {
    const dark = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    const next = dark ? "light" : "dark";
    local.set("trace.theme", next);
    applyTheme(next);
  };

  // ── home ───────────────────────────────────────────────────────────────────
  function ladderBar(topic) {
    const dt = drillTopic(topic);
    const kids = [];
    if (dt) dt.drills.forEach((d) => kids.push(h("i", { class: "drill " + (T.DrillProgress.solid(dt, d) ? "on" : T.DrillProgress.rec(dt, d).runs ? "part" : "") })));
    if (topic.has_walkthrough) kids.push(h("i", { class: "drill " + (wtDone(topic) ? "on" : wtGot(topic) ? "part" : ""), title: "Read the code" }));
    kids.push(h("span", { class: "gap" }));
    topic.items.forEach((n) => kids.push(h("i", { class: solved(n) ? "on" : pstate(n).passed ? "part" : "", title: S.problems[n].title })));
    return h("span", { class: "ladder-bar", "aria-hidden": "true" }, kids);
  }

  async function viewStart() {
    document.title = "Where are you starting? | Trace";
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: "Where are you starting?" });
    const host = h("div", { class: "start-page", "aria-busy": "true" }, sk("sk-title"), sk("sk-line", "width:70%"));
    app.replaceChildren(host);
    let check;
    try {
      check = await api("/api/starting-check");
    } catch (err) {
      host.removeAttribute("aria-busy");
      host.replaceChildren(h("h1", {}, "The starting check isn't available"), h("p", { class: "lede" }, err.message),
        h("div", { class: "start-actions" }, h("a", { class: "btn primary", href: "#/roadmap" }, "Go to the roadmap")));
      return;
    }
    if (!host.isConnected) return;               // you navigated away while it loaded
    host.removeAttribute("aria-busy");
    const find = (id) => S.topics.find((t) => t.id === id);
    const m = T.mountStart(host, check, {
      place: async (payload) => (S.progress = (await api("/api/placement", payload)).progress),
      topicTitle: (id) => (find(id) ? topicTitle(find(id)) : id),
      startHref: (id) => (find(id) ? firstStep(find(id)) : "#/"),
      stageOf: (id) => (find(id) ? stageOf(find(id)) : 1),
      topicNo: (id) => (find(id) ? find(id).n : 1),
    });
    S.cleanup = () => m.unmount();
  }

  // Anything done anywhere: a test passed, a drill run, a walkthrough layer. Before that, the button says Start.
  function started() {
    return Object.values(S.progress.problems || {}).some((st) => st.solved || st.passed || st.steps)
      || Object.keys(S.progress.walkthroughs || {}).length > 0
      || T.topics.some((dt) => dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0));
  }

  function viewHome() {
    document.title = "Trace";
    crumbs();
    const target = resumeTarget();
    const topic = target && target.topic;
    T.mountHome(app, {
      target, started: started(),
      stageNo: topic ? stageOf(topic) : 6, stageName: topic ? topic.stage : "",
      topicTitle: topic ? topicTitle(topic) : "", topicDone: topic ? topic.items.filter(solved).length : 0,
      topicTotal: topic ? topic.items.length : 0,
    });
  }

  // The whole course: six stages as a path, then study plans, the review drill, the starting check and reset.
  function viewRoadmap() {
    document.title = "Roadmap | Trace";
    crumbs({ label: "Home", href: "#/" }, { label: "Roadmap" });
    const stages = stageNames().map((name, k) => ({ no: k + 1, name,
      topics: S.topics.filter((t) => t.stage === name).map((t) => ({ id: t.id, n: t.n, title: topicTitle(t),
        done: t.items.filter(solved).length, total: t.items.length, placedOut: placedOut(t) })) }));
    const review = T.topics.find((d) => d.n === 99);
    const spot = review && T.spotStatus ? T.spotStatus() : null;
    T.mountRoadmap(app, {
      stages, hereTopicId: pathTopic()?.id || null,
      extras: [
        h("section", { id: "plans", class: "road-extra" }, plansSection()),
        h("section", { class: "road-extra" },
          h("h2", { class: "section-title" }, "Contest"),
          h("div", { class: "topic-list" }, h("a", { class: "topic-row", href: "#/contest" },
            h("span", { class: "num" }, icon(ICONS.contest)),
            h("span", { class: "name" }, "Timed contest", h("span", { class: "sub" }, "Three problems against the clock, in fullscreen until you submit.")),
            h("span")))),
        review ? h("section", { class: "road-extra" },
          h("h2", { class: "section-title" }, "Review"),
          h("div", { class: "topic-list" }, spot && !spot.ready
            ? h("div", { class: "topic-row disabled" },
              h("span", { class: "num" }, icon(ICONS.review)),
              h("span", { class: "name" }, review.title, h("span", { class: "sub" }, `Opens after four pattern topics (${spot.have} of ${spot.need}).`)),
              h("span"))
            : h("a", { class: "topic-row", href: `#/d/${review.id}/${review.drills[0].id}` },
              h("span", { class: "num" }, icon(ICONS.review)),
              h("span", { class: "name" }, review.title, h("span", { class: "sub" }, "Read a problem, name the technique. Mixes the topics you've started.")),
              h("span", { class: "ladder-bar" }, T.pips(T.DrillProgress.rec(review, review.drills[0]).clean))))) : null,
        h("p", { class: "home-foot" },
          h("a", { class: "link", href: "#/start" }, S.progress.placement ? "Retake the starting check" : "Take the starting check"),
          h("button", { class: "link", type: "button", onclick: resetAll }, "Reset all progress")),
      ],
    });
  }

  async function resetAll(e) {
    const btn = e.currentTarget;
    if (!btn.dataset.armed) {
      btn.dataset.armed = "1";
      btn.textContent = "Press again to erase solved problems and drill progress (your code is kept)";
      setTimeout(() => { delete btn.dataset.armed; btn.textContent = "Reset all progress"; }, 4000);
      return;
    }
    S.progress = (await api("/api/reset-progress", {})).progress;
    T.DrillProgress.reset();
    try { localStorage.removeItem("trace.lastStop"); } catch { /* storage unavailable */ }
    viewRoadmap();
  }

  // ── study plans ────────────────────────────────────────────────────────────
  const planItemsOf = (plan) => plan.sections.flatMap((sec) => sec.items);

  function plansSection() {
    const plans = S.plans.plans || [];
    if (!plans.length) return null;
    return [
      h("h2", { class: "section-title" }, "Study plans"),
      h("div", { class: "topic-list" }, plans.map((pl) => {
        const items = planItemsOf(pl);
        const done = items.filter(solved).length;
        return h("a", { class: "topic-row", href: `#/plan/${pl.id}` },
          h("span", { class: "num" + (done === items.length ? " done" : ""), "aria-hidden": "true" }, icon(done === items.length ? ICONS.check : ICONS.plan)),
          h("span", { class: "name" }, pl.title, h("span", { class: "sub" }, pl.about)),
          h("span", { class: "plan-meter", style: `--share:${items.length ? done / items.length : 0}` },
            h("span", {}, `${done} / ${items.length}`), h("i")));
      })),
    ];
  }

  function planRow(plan, name, next) {
    const p = S.problems[name];
    const st = pstate(name);
    const topic = topicOf(name);
    const reported = (S.plans.reported || {})[name];
    return h("a", { class: "item" + (solved(name) ? " solved" : st.passed ? " partial" : "") + (next ? " next" : ""), href: `#/p/${name}/plan/${plan.id}`,
      style: `--p:${st.total ? Math.round((100 * (st.passed || 0)) / st.total) : 0}`, "aria-current": next ? "step" : null },
      h("span", { class: "state" }),
      h("span", { class: "t" }, p.title, reported ? h("span", { class: "reported-dot", title: `Often reported: ${reported.join(", ")}. ${S.plans.reported_note}` }, reported.join(", ")) : null),
      h("span", { class: "meta" }, topicTitle(topic)),
      h("span", { class: "badge " + (p.difficulty || p.kind) }, kindLabel(p)));
  }

  function viewPlan(id) {
    const plan = (S.plans.plans || []).find((pl) => pl.id === id);
    if (!plan) return viewHome();
    document.title = `${plan.title} | Trace`;
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: plan.title });
    const items = planItemsOf(plan);
    const done = items.filter(solved).length;
    const first = items.find((n) => !solved(n));
    // Plans cut across stages, so they wear stage 1, the default. The drawing is the next problem's topic.
    const drawn = topicOf(first || items[items.length - 1]);
    const stop = first ? describeStop({ kind: "problem", topic: topicOf(first), name: first, plan }) : null;
    app.replaceChildren(h("div", { class: "page plan-page" },
      leadCard({
        cls: "plan-hero", stage: 1, title: plan.title, line: `${items.length} problems in ${plan.sections.length} groups`,
        next: stop ? stop.title : "Every problem in this plan is solved",
        kind: stop ? `${stop.itemLabel} · ${topicTitle(stop.topic)}` : "Pick another plan, or keep going on the roadmap",
        href: stop ? stop.href : "#/roadmap", label: stop ? (done ? "Continue" : "Start") : "Open the roadmap",
        art: T.topicArt(drawn.n),
      }),
      underLine(done, items.length, `${done} of ${items.length} solved`),
      h("p", { class: "lede" }, plan.about),
      h("p", { class: "plan-note" }, "Problems opened from a plan skip the topic ladder's locks. The arrows follow the plan's order."),
      h("h2", { class: "section-title" }, "The problems"),
      h("div", { class: "plan-sections" }, plan.sections.map((sec) => {
        const got = sec.items.filter(solved).length;
        return h("details", { class: "plan-section", open: sec.items.includes(first) ? true : null },
          h("summary", {}, h("span", { class: "plan-section-name" }, sec.name),
            h("span", { class: "plan-meter", style: `--share:${sec.items.length ? got / sec.items.length : 0}` },
              h("span", {}, `${got} / ${sec.items.length}`, h("span", { class: "sr-only" }, " solved")), h("i")),
            icon(ICONS.down)),
          h("div", { class: "items" }, sec.items.map((n) => planRow(plan, n, n === first))));
      })),
      Object.keys(S.plans.reported || {}).length ? h("p", { class: "plan-foot" }, "Company names on problems: ", S.plans.reported_note) : null));
    T.cropArt(app.querySelector(".lead .hero-art svg"));
  }

  // ── contest ────────────────────────────────────────────────────────────────
  // Where a contest draws from: the topics you've started or placed out of, or the whole course. With
  // fewer than three problems to draw from, the first stage joins in.
  const RANK = { easy: 0, medium: 1, hard: 2 };
  const contestable = (n) => S.problems[n].kind === "solo" && !S.problems[n].steps && Object.hasOwn(RANK, S.problems[n].difficulty);
  function contestTopics(scope) {
    if (scope === "all") return S.topics;
    const reached = T.reachedTopics();
    const mine = S.topics.filter((t) => reached.has(t.id));
    if (mine.flatMap((t) => t.items).filter(contestable).length >= 3) return mine;
    return S.topics.filter((t) => reached.has(t.id) || t.stage === stageNames()[0]);
  }
  // Three problems for the length's mix (MIX in contest.js), easiest first. Each slot takes the closest
  // difficulty, preferring problems you haven't touched, then ones you haven't solved.
  function drawContest(scope, minutes) {
    const mix = T.CONTEST_MIX[minutes] || T.CONTEST_MIX[60];
    const order = S.topics.flatMap((t) => t.items);
    const pool = contestTopics(scope).flatMap((t) => t.items).filter(contestable);
    const freshness = (n) => (solved(n) ? 2 : (pstate(n).passed || 0) > 0 ? 1 : 0);
    const picked = [];
    for (const want of mix) {
      const left = pool.filter((n) => !picked.includes(n));
      if (!left.length) break;
      const score = (n) => Math.abs(RANK[S.problems[n].difficulty] - RANK[want]) * 10 + freshness(n);
      const best = Math.min(...left.map(score));
      picked.push(T.pick(left.filter((n) => score(n) === best)));
    }
    return picked.sort((a, b) => RANK[S.problems[a].difficulty] - RANK[S.problems[b].difficulty] || order.indexOf(a) - order.indexOf(b));
  }
  T.drawContest = drawContest;

  function viewContest() {
    document.title = "Contest | Trace";
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: "Contest" });
    const m = T.contest.mountSetup(app, {
      startedTopics: S.topics.filter((t) => T.reachedTopics().has(t.id)).length,
      draw: (scope, minutes) => drawContest(scope, minutes).map((n) => ({ name: n, title: S.problems[n].title, difficulty: S.problems[n].difficulty, total: S.problems[n].tests })),
    });
    S.cleanup = () => m.unmount();
  }

  function viewContestResults(id) {
    const entry = T.contest.find(id);
    if (!entry) return viewContest();
    document.title = "Contest results | Trace";
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: "Contest", href: "#/contest" }, { label: "Results" });
    const m = T.contest.mountResults(app, entry);
    S.cleanup = () => m.unmount();
  }

  // ── topic page ─────────────────────────────────────────────────────────────
  const RUNGS = [
    ["Build the intuition", "Run the algorithm by hand until its decisions feel obvious."],
    ["Read the code", "The pattern's code, built up one piece at a time."],
    ["Snippet", "The core move, in a few lines."],
    ["Guided", "One problem in steps: make it work, handle the edges, make it fast."],
    ["Problems", "On your own, easy to hard."],
    ["Build", "A small, real program that uses the idea."],
  ];

  function itemRow(topic, name, next) {
    const p = S.problems[name];
    const st = pstate(name);
    const locked = !isUnlocked(topic, name);
    const cls = ["item", solved(name) ? "solved" : st.passed ? "partial" : "", locked ? "locked" : "", next ? "next" : ""].filter(Boolean).join(" ");
    const pct = st.total ? Math.round((100 * (p.steps ? st.steps || 0 : st.passed || 0)) / (p.steps || st.total)) : 0;
    return h("a", { class: cls, href: `#/p/${name}`, style: `--p:${pct}`, "aria-current": next ? "step" : null },
      h("span", { class: "state" }),
      h("span", { class: "t" }, p.title),
      h("span", { class: "meta" }, locked ? h("span", { class: "lock-meta" }, icon(ICONS.lock), "locked")
        : p.steps ? `${st.steps || 0} of ${p.steps} steps` : `${p.tests} tests`),
      h("span", { class: "badge " + (p.difficulty || p.kind) }, kindLabel(p)));
  }

  // The reference solution, with the topic's skeleton lines dimmed so the problem-specific part stands out.
  function solutionView({ code, skeleton = [] }) {
    const skel = new Set(skeleton);
    return h("div", { class: "solution-box" },
      skel.size ? h("p", { class: "solution-note" }, "Dimmed lines are the pattern's skeleton. The rest is what this problem adds.") : null,
      h("pre", {}, skel.size ? code.split("\n").map((line, k) => h("span", { class: skel.has(k + 1) ? "dim" : null }, line + "\n")) : code));
  }

  function walkthroughRow(topic, next) {
    const got = wtGot(topic), of = topic.walkthrough_layers;
    return h("a", { class: "item" + (got >= of ? " solved" : got ? " partial" : "") + (next ? " next" : ""), href: `#/w/${topic.id}`,
      style: `--p:${Math.round((100 * got) / of)}`, "aria-current": next ? "step" : null },
      h("span", { class: "state" }),
      h("span", { class: "t" }, "Build the pattern, one piece at a time"),
      h("span", { class: "meta" }, `${got} of ${of} layers`),
      h("span", { class: "badge read" }, "Read"));
  }

  // The lead card on topic and plan pages: home's hero at page scale. A slab in the stage colour, the drawing
  // on one side, and on the other the title, its line, what comes next and the one button that opens it.
  function leadCard({ cls, stage, title, line, next, kind, href, label, art }) {
    return h("section", { class: "hero lead " + cls, "data-stage": String(stage), "aria-labelledby": "lead-title" },
      h("div", { class: "hero-text" },
        h("h1", { id: "lead-title" }, title),
        h("p", { class: "hero-stage" }, line),
        h("p", { class: "hero-next" }, h("strong", {}, next), kind ? h("span", { class: "hero-kind" }, kind) : null),
        h("a", { class: "btn primary hero-go", href }, label, icon(ICONS.go))),
      h("div", { class: "hero-art" }, art));
  }
  const underLine = (done, total, text, note) => h("div", { class: "topic-under" },
    h("p", { class: "hero-progress" },
      h("span", { class: "meter", style: `--share:${total ? done / total : 0}`, "aria-hidden": "true" }, h("i")), text),
    note ? h("p", { class: "under-note" }, note) : null);
  const chevron = () => icon(ICONS.down);

  // What to do next in a topic. Where you stopped, when that's in this topic, so the topic page and home's
  // Continue agree; otherwise the topic's own next step in ladder order; null once every problem is solved.
  function topicNext(topic) {
    const t = resumeTarget();
    if (t && !t.plan && t.topic.id === topic.id) return t;
    const dt = drillTopic(topic);
    const fresh = topic.items.every((n) => !solved(n));
    if (dt && fresh && !dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0)) return describeStop({ kind: "drill", topic, dt, drill: dt.drills[0] });
    if (topic.has_walkthrough && !wtDone(topic) && fresh) return describeStop({ kind: "walkthrough", topic });
    const name = topic.items.find((n) => !solved(n) && isUnlocked(topic, n)) || topic.items.find((n) => !solved(n));
    return name ? describeStop({ kind: "problem", topic, name }) : null;
  }
  const RUNG_OF_KIND = { snippet: 2, guided: 3, solo: 4, build: 5 };

  async function viewTopic(id) {
    const topic = S.topics.find((t) => t.id === id);
    if (!topic) return viewHome();
    const dt = drillTopic(topic);
    document.title = `${topicTitle(topic)} | Trace`;
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: topicTitle(topic) });
    const groups = [
      dt ? dt.drills : [],
      topic.has_walkthrough ? ["walkthrough"] : [],
      topic.items.filter((n) => S.problems[n].kind === "snippet"),
      topic.items.filter((n) => S.problems[n].kind === "guided"),
      topic.items.filter((n) => S.problems[n].kind === "solo"),
      topic.items.filter((n) => S.problems[n].kind === "build"),
    ];
    const rungDone = (i) => (i === 0 ? dt && T.DrillProgress.topicSolid(dt) : i === 1 ? wtDone(topic) : groups[i].length && groups[i].every(solved));
    const shown = RUNGS.map((_, i) => i).filter((i) => groups[i].length);

    // One next step, and the rung it's on is the only one open.
    const next = topicNext(topic);
    const nextName = next && next.kind === "problem" ? next.href.split("/")[2] : null;
    const nextDrill = next && next.kind === "drill" ? next.href.split("/")[3] : null;
    const current = !next ? -1 : next.kind === "drill" ? 0 : next.kind === "walkthrough" ? 1 : RUNG_OF_KIND[S.problems[nextName].kind];
    const begun = topic.items.some((n) => solved(n) || pstate(n).passed || pstate(n).steps) || wtGot(topic) > 0
      || (dt && dt.drills.some((d) => T.DrillProgress.rec(dt, d).runs > 0));
    const after = S.topics[S.topics.indexOf(topic) + 1];
    const done = topic.items.filter(solved).length;
    const lead = leadCard({
      cls: "topic-hero", stage: stageOf(topic), title: topicTitle(topic), line: `Stage ${stageOf(topic)} · ${topic.stage}`,
      next: next ? next.title : "Every problem here is solved",
      kind: next ? next.itemLabel : after ? `Next up: ${topicTitle(after)}` : "That's the whole course",
      href: next ? next.href : after ? `#/t/${after.id}` : "#/roadmap",
      label: next ? (begun ? "Continue" : "Start") : after ? "Next topic" : "Open the roadmap",
      art: T.topicArt(topic.n),
    });

    const count = (i) => (i === 0 ? [dt.drills.filter((d) => T.DrillProgress.solid(dt, d)).length, dt.drills.length]
      : i === 1 ? [Math.min(wtGot(topic), topic.walkthrough_layers), topic.walkthrough_layers]
      : [groups[i].filter(solved).length, groups[i].length]);
    const rung = (i, k) => {
      const [title, sub] = RUNGS[i], [got, of] = count(i);
      return h("details", { class: "rung" + (rungDone(i) ? " done" : "") + (i === current ? " current" : ""), open: i === current ? true : null },
        h("summary", {},
          h("span", { class: "rung-dot", "aria-hidden": "true" }, rungDone(i) ? icon(ICONS.check) : String(k + 1)),
          h("span", { class: "rung-head" }, h("span", { class: "rung-title" }, title), h("span", { class: "rung-sub" }, sub)),
          h("span", { class: "rung-count" }, `${got}/${of}`, h("span", { class: "sr-only" }, " done")),
          chevron()),
        h("div", { class: "rung-body" },
          i === 0
            ? h("div", { class: "drill-chips" }, dt.drills.map((d) =>
              h("a", { class: "chip-link" + (d.id === nextDrill ? " next" : ""), href: `#/d/${dt.id}/${d.id}`, "aria-current": d.id === nextDrill ? "step" : null },
                d.name, T.pips(T.DrillProgress.rec(dt, d).clean))))
            : i === 1 ? h("div", { class: "items" }, walkthroughRow(topic, next && next.kind === "walkthrough"))
            : h("div", { class: "items" }, groups[i].map((n) => itemRow(topic, n, n === nextName)))));
    };

    const sheet = h("details", { class: "fold sheet" },
      h("summary", {}, h("span", { class: "fold-title" }, "Cheat sheet"), h("span", { class: "fold-sub" }, "The topic on one page, with examples to run"), chevron()),
      h("div", { class: "fold-body sheet-body", "aria-busy": "true" }, [90, 75, 82, 40].map((w) => sk("sk-line", `width:${w}%`))));
    const techniques = T.topicTechniques(topic, techCtx());
    app.replaceChildren(h("div", { class: "page topic-page" },
      lead,
      underLine(done, topic.items.length, `${done} of ${topic.items.length} solved`,
        placedOut(topic) ? "You placed out of this. Everything stays open." : null),
      dt ? h("p", { class: "lede" }, dt.idea) : null,
      dt ? h("dl", { class: "facts" },
        h("div", {}, h("dt", {}, "Reach for it when"), h("dd", {}, dt.signals)),
        h("div", {}, h("dt", {}, "True at every step"), h("dd", {}, dt.invariant))) : null,
      h("h2", { class: "section-title" }, "The ladder"),
      h("div", { class: "rungs" }, shown.map(rung)),
      techniques || topic.has_lesson ? [h("h2", { class: "section-title" }, "Notes and techniques"),
        h("div", { class: "folds" }, techniques, topic.has_lesson ? sheet : null)] : null));
    T.cropArt(app.querySelector(".lead .hero-art svg"));
    if (topic.has_lesson) {
      const lesson = await api(`/api/lesson?topic=${encodeURIComponent(topic.id)}`).catch(() => null);
      if (!lesson) return;
      const out = h("pre", { class: "run-out", hidden: true });
      const runBtn = h("button", { class: "btn small", type: "button" }, icon(ICONS.play), "Run these examples");
      runBtn.onclick = async () => {
        runBtn.disabled = true;
        out.hidden = false;
        out.textContent = "Running in a fresh sandbox…";
        try {
          const r = await api("/api/run", { code: lesson.code });
          if (r.docker_error) { out.textContent = r.docker_error; showDocker(r.docker); }
          else out.textContent = (r.output || "(no output)") + (r.killed ? "\n" + r.killed : "");
        } catch (err) { out.textContent = err.message; }
        runBtn.disabled = false;
      };
      const body = sheet.lastElementChild;
      body.removeAttribute("aria-busy");
      body.replaceChildren(h("div", { class: "prose" }, renderMarkdown(lesson.notes)),
        lesson.code ? h("div", { class: "run-box" }, h("h3", { class: "run-title" }, "Runnable examples"),
          h("div", { class: "prose" }, h("pre", {}, h("code", {}, lesson.code))), runBtn, out) : null);
    }
  }

  // ── read the code (walkthrough) ────────────────────────────────────────────
  async function viewWalkthrough(id) {
    const topic = S.topics.find((t) => t.id === id);
    if (!topic || !topic.has_walkthrough) return viewTopic(id);
    document.title = `${topicTitle(topic)}: read the code | Trace`;
    crumbs({ label: "Roadmap", href: "#/roadmap" }, { label: topicTitle(topic), href: `#/t/${topic.id}` }, { label: "Read the code" });
    const host = h("div", { class: "wt-page", "aria-busy": "true" }, sk("sk-title"), sk("sk-line", "width:30%"), sk("sk-line", "width:90%;margin-top:26px"), sk("sk-line", "width:70%"));
    app.replaceChildren(host);
    const wt = await api(`/api/walkthrough?topic=${encodeURIComponent(id)}`);
    if (!host.isConnected) return;               // you navigated away while it loaded
    host.removeAttribute("aria-busy");
    const m = T.mountWalkthrough(host, wt, {
      done: wtGot(topic),
      run: async (code) => {
        const r = await api("/api/run", { code });
        if (r.docker_error) showDocker(r.docker);
        return r;
      },
      onAnswer: async (layers) => {
        if (layers <= wtGot(topic)) return;
        try { S.progress = (await api("/api/walkthrough-progress", { topic: id, layers })).progress; } catch (err) { console.error(err); }
      },
      problemHref: (name) => `#/p/${name}`,
      topicHref: `#/t/${id}`,
    });
    recordStop(`#/w/${topic.id}`);
    S.cleanup = () => m.unmount();
  }

  // ── drill view ─────────────────────────────────────────────────────────────
  function viewDrill(topicId, drillId) {
    const dt = T.byId[topicId];
    if (!dt) return viewHome();
    const drill = dt.drills.find((d) => d.id === drillId) || dt.drills[0];
    const course = S.topics.find((t) => t.n === dt.n);
    document.title = `${dt.title}: ${drill.name} | Trace`;
    crumbs({ label: "Roadmap", href: "#/roadmap" }, course ? { label: topicTitle(course), href: `#/t/${course.id}` } : { label: "Review" }, { label: drill.name });
    if (dt.n === 99 && T.spotStatus && !T.spotStatus().ready) {
      app.replaceChildren(h("div", { class: "page" }, h("h1", {}, dt.title),
        h("p", { class: "lede" }, `This mixes the techniques you've started, so it opens after four pattern topics. You've started ${T.spotStatus().have} so far.`),
        h("p", { style: "margin-top:24px" }, h("a", { class: "btn", href: "#/roadmap" }, "Back to the roadmap"))));
      return;
    }
    if (dt.n !== 99) recordStop(`#/d/${dt.id}/${drill.id}`);
    const tabs = h("div", { class: "drill-tabs", role: "tablist" });
    const renderTabs = () => tabs.replaceChildren(...dt.drills.map((d) =>
      h("a", { class: "drill-tab", role: "tab", href: `#/d/${dt.id}/${d.id}`, "aria-selected": String(d === drill) }, d.name, T.pips(T.DrillProgress.rec(dt, d).clean))));
    renderTabs();
    const host = h("div");
    const first = course && course.items[0];
    app.replaceChildren(h("div", { class: "drill-page" },
      h("div", { class: "drill-top" },
        h("div", { class: "drill-head" }, h("h1", {}, dt.title), h("p", { class: "drill-sub" }, "Intuition drills")),
        first ? h("a", { class: "btn small", href: `#/p/${first}` }, "Start coding", icon(ICONS.right)) : null),
      tabs, host));
    const m = T.mountDrill(host, dt, drill, { onFinish: renderTabs });
    S.cleanup = () => m.unmount();
  }

  // ── problem data: cached, and prefetched when you point at a link ──────────
  const problemCache = new Map();          // name -> Promise of the /api/problem payload
  function fetchProblem(name) {
    if (!problemCache.has(name)) {
      const pending = api(`/api/problem?name=${encodeURIComponent(name)}`);
      pending.catch(() => problemCache.delete(name));
      problemCache.set(name, pending);
    }
    return problemCache.get(name);
  }
  function rememberCode(name, code) {
    const pending = problemCache.get(name);
    if (pending) pending.then((p) => { p.code = code; }).catch(() => {});
  }
  function prefetchFrom(target) {
    const a = target.closest && target.closest('a[href^="#/p/"]');
    if (a) fetchProblem(decodeURIComponent(a.getAttribute("href").slice(4)));
  }
  document.addEventListener("pointerover", (e) => prefetchFrom(e.target), { passive: true });
  document.addEventListener("focusin", (e) => prefetchFrom(e.target));

  const sk = (cls, style) => h("span", { class: "sk " + cls, style });
  function workspaceSkeleton() {
    return h("div", { class: "ws-grid", "aria-busy": "true", "aria-label": "Loading" },
      h("div", { class: "ws-bar" }, h("div", { class: "stepper" }, T.range(7).map(() => sk("", "width:26px;height:26px")))),
      h("div", { class: "split", style: `--left:${local.get("trace.left", 42)}%` },
        h("div", { class: "pane-left" }, h("div", { class: "statement" },
          sk("sk-title"), sk("sk-line", "width:30%"), sk("sk-line", "width:96%;margin-top:26px"), sk("sk-line", "width:90%"),
          sk("sk-line", "width:72%"), sk("", "height:64px;margin-top:20px"), sk("sk-line", "width:85%;margin-top:22px"), sk("sk-line", "width:60%"))),
        h("div", { class: "gutter" }),
        h("div", { class: "pane-right", style: `--console:${local.get("trace.console", 38)}%` },
          h("div", { class: "editor-bar" }, sk("", "width:140px;height:14px"), h("span", { class: "spacer" }), sk("", "width:96px;height:28px")),
          h("div", { class: "sk-editor" }, [62, 48, 70, 35, 55].map((w) => sk("sk-line", `width:${w}%`))),
          h("div", { class: "gutter-h" }),
          h("section", { class: "console" }, h("div", { class: "console-bar" }, sk("", "width:120px;height:14px")), h("div", {})))));
  }

  // ── workspace ──────────────────────────────────────────────────────────────
  async function viewProblem(name, planId, inContest) {
    const topic = topicOf(name);
    if (!topic) return viewHome();
    // Contest mode: the contest's problems, no ladder locks, no hints or solutions until it's submitted.
    const contest = inContest ? T.contest.get() : null;
    const contestItems = contest ? contest.problems.map((x) => x.name) : [];
    // Plan mode: working through a study plan skips the ladder's locks and follows the plan's order.
    const plan = planId ? (S.plans.plans || []).find((pl) => pl.id === planId) : null;
    const planItems = plan ? plan.sections.flatMap((sec) => sec.items) : [];
    const inPlan = plan && planItems.includes(name);
    const unlocked = (n) => (contest && contestItems.includes(n)) || (inPlan && planItems.includes(n)) || isUnlocked(topic, n);
    const link = (n) => (contest ? `#/p/${n}/contest` : inPlan && planItems.includes(n) ? `#/p/${n}/plan/${plan.id}` : `#/p/${n}`);
    const here = contest ? [{ label: "Contest" }]
      : inPlan
      ? [{ label: "Roadmap", href: "#/roadmap" }, { label: plan.title, href: `#/plan/${plan.id}` }]
      : [{ label: "Roadmap", href: "#/roadmap" }, { label: topicTitle(topic), href: `#/t/${topic.id}` }];
    document.body.classList.add("ws");
    crumbs(...here, { label: S.problems[name].title });
    const pending = fetchProblem(name);
    let ready = false;
    pending.then(() => { ready = true; }, () => {});
    await Promise.resolve();
    if (!ready) app.replaceChildren(workspaceSkeleton());   // only flashes when the data isn't cached yet
    const p = await pending;
    if (decodeURIComponent(location.hash).split("/")[2] !== name) return;     // navigated away while loading
    const dt = drillTopic(topic);
    document.title = `${p.title} | Trace`;
    crumbs(...here, { label: p.title });
    if (contest) T.contest.open(name);
    else if (unlocked(name)) recordStop(inPlan ? `#/p/${name}/plan/${plan.id}` : `#/p/${name}`);

    const st = () => pstate(name);
    const stepCount = p.steps.length;
    const stepsDone = () => Math.min(st().steps || 0, stepCount);
    let showHint = false, solution = null, solutionShown = false, tab = "problem";
    let showHowTo = !local.get("trace.howtoSeen", false);

    // stepper across the topic's ladder
    const order = contest ? contestItems : inPlan ? planItems : topic.items;
    const i = order.indexOf(name);
    const prev = order[i - 1], next = order[i + 1];
    const home = inPlan ? `#/plan/${plan.id}` : `#/t/${topic.id}`;
    const stepper = h("nav", { class: "stepper", "aria-label": "Ladder" },
      dt ? [h("a", { class: "step-pill" + (T.DrillProgress.topicSolid(dt) ? " solved" : ""), href: `#/d/${dt.id}/${dt.drills[0].id}`, title: "Intuition drills" }, "I"), h("span", { class: "step-sep" })] : null,
      topic.items.map((n) => h("a", {
        class: "step-pill" + (solved(n) ? " solved" : !isUnlocked(topic, n) ? " locked" : ""),
        href: `#/p/${n}`, title: `${S.problems[n].title} (${kindLabel(S.problems[n])})`, "aria-current": n === name ? "page" : null,
      }, pillLabel(topic, n))));
    const bar = contest ? T.contest.bar(name) : h("div", { class: "ws-bar" }, stepper,
      h("div", { class: "ws-nav" },
        inPlan ? h("span", { class: "plan-pos" }, `${plan.title}: ${i + 1} of ${order.length}`) : null,
        h("a", { class: "btn ghost small", href: prev ? link(prev) : home, "aria-label": "Previous" }, icon(ICONS.left)),
        h("a", { class: "btn ghost small", href: next ? link(next) : home, "aria-label": "Next" }, icon(ICONS.right))));

    // left pane, under a band in the stage colour: the topic's name and its drawing, like the home card
    const left = h("div", { class: "pane-left" });
    const band = contest ? null : h("a", { class: "ws-topic", href: `#/t/${topic.id}`, title: `Back to ${topicTitle(topic)}` },
      h("span", { class: "ws-topic-text" }, h("span", { class: "ws-topic-name" }, topicTitle(topic)),
        h("span", { class: "ws-topic-stage" }, `Stage ${stageOf(topic)} · ${topic.stage}`)),
      T.topicArt(topic.n));
    function renderLeft() {
      const tabs = h("div", { class: "tabs", role: "tablist" },
        (contest ? [["problem", "Problem"]] : [["problem", "Problem"], ["solution", "Solution"]]).map(([id, label]) =>
          h("button", { class: "tab", role: "tab", type: "button", "aria-selected": String(tab === id), onclick: () => { tab = id; renderLeft(); } }, label)));
      const body = h("div", { class: "statement" });
      if (!unlocked(name)) {
        const before = blocker(topic, name);
        body.append(h("h1", {}, p.title),
          h("div", { class: "reveal-box" },
            (S.problems[name].uses || []).some((t) => techTeacher(t) === before)
              ? h("p", {}, "This uses ", h("strong", {}, S.techniques[(S.problems[name].uses || []).find((t) => techTeacher(t) === before)].name),
                ". ", h("strong", {}, S.problems[before].title), " teaches it, so do that one first.")
              : S.problems[name].kind === "build" && S.problems[before].kind === "solo"
              ? h("p", {}, "The build opens once you've solved two of this topic's problems. It combines what they teach.")
              : h("p", {}, `This unlocks after `, h("strong", {}, S.problems[before].title), `. The ladder builds on itself, so each rung makes the next one easier.`),
            h("div", { style: "display:flex;gap:8px;flex-wrap:wrap" },
              h("a", { class: "btn primary small", href: `#/p/${before}` }, `Go to ${S.problems[before].title}`),
              h("button", { class: "btn small", type: "button", onclick: async () => {
                S.progress = (await api("/api/unlock", { name })).progress;
                route();
              } }, "Open anyway"))));
        left.replaceChildren(...[band, tabs, body].filter(Boolean));
        return;
      }
      if (tab === "problem") {
        body.append(h("h1", {}, p.title),
          h("div", { class: "st-meta" }, h("span", { class: "badge " + (p.difficulty || p.kind) }, kindLabel(p)),
            solved(name) && !contest ? h("span", { class: "badge easy" }, "Solved") : null,
            h("span", { class: "badge" }, stepCount ? `${stepCount} steps` : `${p.tests} tests`),
            ...(contest ? [] : p.in_plans || []).map((t) => h("span", { class: "badge plan" }, t)),
            !contest && p.reported && p.reported.length ? h("span", { class: "badge reported", title: p.reported_note }, `Often reported: ${p.reported.join(", ")}`) : null),
          ...(contest ? [] : [T.usesRow(S.problems[name], techCtx()), T.techniqueBanner(S.problems[name], topic, techCtx())].filter(Boolean)),
          showHowTo
            ? T.howToCard({ onClose: () => { showHowTo = false; local.set("trace.howtoSeen", true); renderLeft(); } })
            : h("button", { class: "link howto-link", type: "button", onclick: () => { showHowTo = true; renderLeft(); } }, "How to work a problem"),
          ...(contest ? [] : T.techniqueBoxes(S.problems[name], techCtx())));
        // The problem, then each example as input, output and why (structures drawn), then what to aim for.
        // The written example block shows as it is only when none of its examples could be read.
        const parts = splitStatement(p.statement);
        const examples = p.examples || [];
        body.append(h("section", { class: "st-desc body-text", "aria-label": "Problem" }, renderStatement(parts.desc)));
        if (examples.length) body.append(h("section", { class: "st-examples", "aria-label": "Examples" },
          examples.map((ex, k) => exampleCard(ex, k, examples.length))));
        else if (parts.example) body.append(h("section", { class: "st-example" }, h("h2", {}, "Example"), h("pre", { class: "st-example-code" }, parts.example)));
        if (parts.notes.trim()) body.append(h("div", { class: "body-text st-notes" }, renderStatement(parts.notes)));
        if (p.aim) body.append(h("p", { class: "st-aim" }, h("span", { class: "st-aim-label" }, "Aim for"), h("span", {}, inline(p.aim))));
        if (stepCount) {
          const done = stepsDone();
          body.append(h("div", { class: "steps" }, p.steps.map((s, k) => {
            const state = k < done ? "done" : k === done ? "current" : "locked";
            const open = state === "current";
            return h("section", { class: "step " + state },
              h("div", { class: "step-head" }, h("span", { class: "step-num" }, k < done ? icon(ICONS.check) : k + 1),
                h("span", { class: "step-title" }, s.title),
                h("span", { class: "step-tag" }, state === "done" ? "passed" : state === "locked" ? "locked" : `${s.tests} tests`)),
              open ? h("div", { class: "step-body" }, h("p", {}, inline(s.text)),
                s.hint ? (showHint ? h("div", { class: "callout" }, h("h4", {}, "Hint"), h("p", {}, inline(s.hint)))
                  : h("button", { class: "btn small", type: "button", onclick: () => { showHint = true; renderLeft(); } }, "Show hint")) : null) : null);
          })));
        } else if (p.hint && !contest) {
          body.append(showHint ? h("div", { class: "callout" }, h("h4", {}, "Hint"), h("p", {}, inline(p.hint)))
            : h("button", { class: "btn small hint-btn", type: "button", onclick: () => { showHint = true; renderLeft(); } }, "Show hint"));
        }
      } else {
        body.append(h("h1", {}, "Reference solution"));
        if (!p.has_solution) body.append(h("p", { class: "console-empty" }, "No reference solution for this one yet."));
        else if (solution && (solutionShown || solved(name))) body.append(solutionView(solution));
        else body.append(h("div", { class: "reveal-box" },
          h("p", {}, solved(name) ? "You've solved it. Compare your approach with the reference." : "Reading the answer too early skips the part that builds the skill. Give it a real attempt first: run your code, read the failing test, try once more."),
          h("button", { class: "btn small", type: "button", onclick: async () => {
            solution = await api(`/api/solution?name=${encodeURIComponent(name)}`);
            solutionShown = true;
            renderLeft();
          } }, "Show the solution")));
      }
      left.replaceChildren(...[band, tabs, body].filter(Boolean));
    }
    renderLeft();

    function argsOf(values) {
      return (p.params || []).map((pr, i) => ({ name: pr.name, type: pr.type, value: values[i] }));
    }
    function exampleCard(ex, k, total) {
      const args = argsOf(ex.args);
      return h("article", { class: "st-ex" },
        h("h3", {}, total > 1 ? `Example ${k + 1}` : "Example", ex.source === "tests" ? h("span", { class: "st-ex-src" }, " · the first test") : null),
        h("div", { class: "st-in" }, h("h4", {}, "Input"), args.map((a) => T.valueBlock(a.value, a, args))),
        h("div", { class: "st-out" }, h("h4", {}, "Output"), T.valueBlock(ex.expected, { name: "", type: p.returns || "" }, args)),
        ex.note ? h("p", { class: "st-why" }, inline(ex.note)) : null);
    }

    // editor
    const fileName = h("span", { class: "file-name" }, `${name}.py`);
    const saveState = h("span", { class: "save-state" });
    const runBtn = h("button", { class: "btn run small", type: "button", title: "Ctrl+Enter" }, icon(ICONS.play), "Run tests");
    const resetBtn = h("button", { class: "btn ghost small", type: "button", title: "Put the starter code back" }, icon(ICONS.reset), "Reset");
    const editorWrap = h("div", { class: "editor-wrap" });
    const summary = h("span", { class: "summary" });
    const strip = h("div", { class: "test-strip", role: "group", "aria-label": "Tests" });
    const timing = h("span", { class: "timing" });
    const customToggle = h("button", { class: "btn ghost small", type: "button" }, "Try a call");
    const consoleBody = h("div", {},
      h("p", { class: "console-empty" }, unlocked(name) ? "Press Run tests (Ctrl+Enter). Your code runs in a fresh, isolated Python process." : "Locked."),
      unlocked(name) ? h("p", { class: "console-empty" }, "No imports needed: ",
        ["deque", "Counter", "defaultdict", "heappush", "heappop", "heappush_max", "heappop_max", "MaxHeap", "bisect_left", "lru_cache", "inf", "List", "Optional", "ListNode", "TreeNode"]
          .flatMap((n, k) => [k ? ", " : "", h("code", {}, n)]),
        ", math, itertools, functools and the rest of the usual toolkit are preloaded.") : null);
    const customInput = h("input", {
      type: "text", spellcheck: "false", "aria-label": "Call your code with your own input",
      placeholder: p.is_class ? `e.g.  ${p.name.split("_").map((w) => w[0].toUpperCase() + w.slice(1)).join("")}(…)` : `e.g.  ${name}(…)`,
    });
    const customRow = h("div", { class: "custom-row", hidden: true }, customInput);
    const right = h("div", { class: "pane-right" },
      h("div", { class: "editor-bar" }, fileName, saveState, h("span", { class: "spacer" }), resetBtn, runBtn),
      editorWrap,
      h("div", { class: "gutter-h", role: "separator", "aria-orientation": "horizontal", "aria-label": "Resize console" }),
      h("section", { class: "console", "aria-label": "Results" },
        h("div", { class: "console-bar" }, summary, strip, timing, h("span", { class: "spacer" }), customToggle),
        h("div", { class: "console-body" }, customRow, consoleBody)));

    const split = h("div", { class: "split", style: `--left:${local.get("trace.left", 42)}%` }, left,
      h("div", { class: "gutter", role: "separator", "aria-orientation": "vertical", "aria-label": "Resize panels" }), right);
    right.style.setProperty("--console", `${local.get("trace.console", 38)}%`);
    app.replaceChildren(h("div", { class: "ws-grid" }, bar, split));
    if (band) T.cropArt(band.querySelector("svg"), 6);

    const cm = CodeMirror(editorWrap, {
      value: p.code, mode: "python", theme: "trace", lineNumbers: true, indentUnit: 4, tabSize: 4,
      matchBrackets: true, autoCloseBrackets: true, styleActiveLine: true, readOnly: !unlocked(name),
      extraKeys: {
        Tab: (c) => (c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection("    ", "end")),
        "Shift-Tab": (c) => c.indentSelection("subtract"),
        "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment",
        "Ctrl-Enter": () => run(), "Cmd-Enter": () => run(),
        "Ctrl-S": () => saveNow(), "Cmd-S": () => saveNow(),
      },
    });
    setTimeout(() => cm.refresh(), 0);

    // saving
    let saveTimer = null, errorLine = null;
    async function saveNow() {
      clearTimeout(saveTimer);
      saveState.textContent = "Saving…";
      const code = cm.getValue();
      rememberCode(name, code);
      try { await api("/api/save", { name, code }); saveState.textContent = "Saved"; }
      catch { saveState.textContent = "Not saved"; }
    }
    cm.on("change", () => {
      saveState.textContent = "Edited";
      clearTimeout(saveTimer);
      saveTimer = setTimeout(saveNow, 800);
      if (errorLine != null) { cm.removeLineClass(errorLine, "background", "cm-error-line"); errorLine = null; }
    });
    resetBtn.onclick = async () => {
      if (!resetBtn.dataset.armed) {
        resetBtn.dataset.armed = "1";
        resetBtn.lastChild.textContent = "Click again to reset";
        setTimeout(() => { delete resetBtn.dataset.armed; resetBtn.lastChild.textContent = "Reset"; }, 3000);
        return;
      }
      const r = await api("/api/reset", { name });
      cm.setValue(r.code);
      delete resetBtn.dataset.armed;
      resetBtn.lastChild.textContent = "Reset";
    };
    customToggle.onclick = () => { customRow.hidden = !customRow.hidden; if (!customRow.hidden) customInput.focus(); };
    customInput.addEventListener("keydown", (e) => { if (e.key === "Enter") run(); });

    // running
    let running = false;
    async function run() {
      if (running || !unlocked(name)) return;
      running = true;
      runBtn.disabled = true;
      runBtn.firstChild.replaceWith(h("span", { class: "spinner", "aria-hidden": "true" }));
      summary.className = "summary";
      summary.textContent = "Running…";
      strip.replaceChildren();
      timing.textContent = "in a fresh sandbox";
      consoleBody.replaceChildren(h("div", { "aria-busy": "true" },
        T.range(Math.min(5, stepCount ? p.steps[Math.min(stepsDone(), stepCount - 1)].tests + 1 : p.tests)).map(() => sk("sk-test"))));
      rememberCode(name, cm.getValue());
      const before = stepsDone(), wasSolved = solved(name);
      const upto = stepCount ? Math.min(before + 1, stepCount) : null;
      try {
        const r = await api("/api/test", { name, code: cm.getValue(), upto, custom: customRow.hidden ? "" : customInput.value });
        if (r.docker_error) {
          showDocker(r.docker);
          summary.textContent = "";
          consoleBody.replaceChildren(h("div", { class: "notice bad" }, r.docker_error));
          return;
        }
        if (r.progress) { S.progress = r.progress; renderSide(); }
        if (contest) T.contest.record(name, (r.report && r.report.tests) || []);
        saveState.textContent = "Saved";
        renderResults(r, before, wasSolved);
        if (stepsDone() !== before || solved(name) !== wasSolved) { showHint = false; renderLeft(); refreshStepper(); }
      } catch (err) {
        summary.textContent = "";
        consoleBody.replaceChildren(h("div", { class: "notice bad" }, err.message));
      } finally {
        running = false;
        runBtn.disabled = false;
        runBtn.firstChild.replaceWith(icon(ICONS.play));
      }
    }
    runBtn.onclick = run;
    // The next rung is the likely next click: warm it up.
    if (next) setTimeout(() => fetchProblem(next), 400);

    function refreshStepper() {
      stepper.querySelectorAll("a.step-pill[href^='#/p/']").forEach((a) => {
        const n = a.getAttribute("href").slice(4);
        a.className = "step-pill" + (solved(n) ? " solved" : !isUnlocked(topic, n) ? " locked" : "");
      });
    }

    function markError(text) {
      const m = [...String(text).matchAll(/File "solution\.py", line (\d+)/g)].pop();
      if (!m) return;
      if (errorLine != null) cm.removeLineClass(errorLine, "background", "cm-error-line");
      errorLine = Number(m[1]) - 1;
      cm.addLineClass(errorLine, "background", "cm-error-line");
    }

    function renderResults(r, stepsBefore, wasSolved) {
      const kids = [];
      timing.textContent = `${r.seconds}s in a fresh sandbox`;
      if (r.crash) {
        summary.className = "summary bad";
        summary.textContent = "Crashed";
        kids.push(h("div", { class: "notice bad" }, r.crash));
        return consoleBody.replaceChildren(...kids);
      }
      const rep = r.report;
      if (rep.load_error) {
        summary.className = "summary bad";
        summary.textContent = "Your file didn't load";
        kids.push(h("div", { class: "notice bad" }, rep.load_error));
        if (rep.load_output) kids.push(h("pre", { class: "run-out" }, rep.load_output));
        markError(rep.load_error);
        return consoleBody.replaceChildren(...kids);
      }
      const tests = rep.tests;
      const passed = tests.filter((t) => t.status === "pass").length;
      const todo = tests.length && tests.every((t) => t.status === "todo");
      summary.className = "summary " + (todo ? "" : passed === tests.length ? "ok" : "bad");
      summary.textContent = todo ? "Not started yet" : `${passed} of ${tests.length} passed`;

      if (todo) kids.push(h("div", { class: "notice info" }, "Your function still raises NotImplementedError. Replace that line with your solution."));
      const nowSteps = stepsDone();
      if (contest && passed === tests.length && tests.length && !todo) {
        const nx = T.contest.nextOpen(name);
        kids.push(h("div", { class: "notice ok solved-card" },
          h("span", { class: "solved-mark", "aria-hidden": "true" }, icon(ICONS.check)),
          h("strong", {}, "Solved."),
          nx ? h("a", { class: "btn small primary", href: link(nx) }, `Next: problem ${contestItems.indexOf(nx) + 1}`, icon(ICONS.right))
            : h("span", {}, "That's all of them. Submit when you're ready.")));
      } else if (solved(name) && passed === tests.length && !todo) {
        const nx = inPlan ? (next ? { name: next, plan: true } : { done: true, plan: true }) : nextItem(name);
        kids.push(h("div", { class: "notice ok solved-card" },
          h("span", { class: "solved-mark", "aria-hidden": "true" }, icon(ICONS.check)),
          h("strong", {}, wasSolved ? "All tests pass." : "Solved."),
          nx && nx.name ? h("a", { class: "btn small primary", href: link(nx.name) }, `Next: ${S.problems[nx.name].title}`, icon(ICONS.right))
            : nx && nx.plan ? h("a", { class: "btn small primary", href: home }, `Back to ${plan.title}`, icon(ICONS.right))
              : nx ? h("a", { class: "btn small primary", href: `#/t/${nx.topic.id}` }, `Next topic: ${topicTitle(nx.topic)}`, icon(ICONS.right))
                : h("span", {}, "That was the last one. Everything's done.")));
      } else if (stepCount && nowSteps > stepsBefore) {
        kids.push(h("div", { class: "notice ok" }, h("strong", {}, `Step ${stepsBefore + 1} passed.`),
          h("span", {}, nowSteps < stepCount ? `Step ${nowSteps + 1} is open on the left: ${p.steps[nowSteps].title}.` : "")));
      }
      if (rep.custom) {
        const c = rep.custom;
        kids.push(h("div", { class: "test" + (c.error ? " error" : " pass") },
          h("div", { class: "test-detail", style: "padding:10px 12px" },
            h("div", { class: "kv-line" }, h("span", {}, "your call"), h("code", {}, c.expr)),
            c.error ? h("pre", { class: "err" }, c.error) : h("div", { class: "kv-line" }, h("span", {}, "returned"), h("code", {}, c.value)),
            c.output ? h("pre", { class: "out" }, c.output) : null)));
      }
      let firstFail = null;
      const rows = new Map();
      const testRow = (t) => {
        const bad = ["fail", "error", "timeout"].includes(t.status);
        const det = h("details", { class: "test " + t.status, open: bad && !firstFail ? true : null },
          h("summary", {}, h("span", { class: "dot", "aria-hidden": "true" }, t.status === "pass" ? icon(ICONS.check) : bad ? icon(ICONS.cross) : null),
            h("span", { class: "call" }, t.call),
            h("span", { class: "ms" }, t.status === "pass" ? `${t.ms} ms` : t.status)),
          h("div", { class: "test-detail" },
            h("div", { class: "kv-line" }, h("span", {}, "expected"), h("code", {}, t.expected)),
            t.got != null ? h("div", { class: "kv-line" }, h("span", {}, "got"), h("code", {}, t.got)) : null,
            t.note ? h("p", { class: "test-note" }, t.note) : null,
            t.error ? h("pre", { class: "err" }, t.error) : null,
            t.output ? h("pre", { class: "out" }, t.output) : null));
        if (bad && !firstFail) { firstFail = det; if (t.error) markError(t.error); }
        rows.set(t, det);
        // A test's inputs, drawn the first time its row is open.
        const drawArgs = () => {
          if (!det.open || det.dataset.drawn || !t.args) return;
          det.dataset.drawn = "1";
          const args = argsOf(t.args);
          const figs = args.map((a) => T.drawValue(a.value, a, args) ? T.valueBlock(a.value, a, args) : null).filter(Boolean);
          if (figs.length) det.querySelector(".test-detail").prepend(h("div", { class: "test-figs" }, figs));
        };
        det.addEventListener("toggle", drawArgs);
        drawArgs();
        return det;
      };
      if (stepCount) {
        // One group per step. Steps that fully pass fold into a single line, so the new work stays in view.
        const groups = [];
        for (const t of tests) (groups[t.step] ||= []).push(t);
        groups.forEach((group, k) => {
          if (!group) return;
          const ok = group.every((t) => t.status === "pass");
          const last = k === groups.length - 1;
          kids.push(h("details", { class: "step-group", open: !ok || last ? true : null },
            h("summary", {}, icon(ICONS.down), h("span", { class: "sg-title" }, `Step ${k + 1}: ${p.steps[k].title}`),
              h("span", { class: "sg-count" }, `${group.filter((t) => t.status === "pass").length} of ${group.length} passed`)),
            group.map(testRow)));
        });
      } else {
        tests.forEach((t) => kids.push(testRow(t)));
      }
      // One square per test, like the drawings' cells; a square opens its test.
      const bucket = (st) => (st === "pass" ? "pass" : ["fail", "error", "timeout"].includes(st) ? "fail" : "todo");
      strip.replaceChildren(...tests.map((t, k) => h("button", {
        class: "cell", type: "button", "data-status": bucket(t.status), style: `--i:${k}`,
        "aria-label": `Test ${k + 1}: ${t.status === "pass" ? "passed" : t.status}`, title: t.call,
        onclick: () => { const row = rows.get(t); if (!row) return; row.open = true; row.scrollIntoView({ block: "nearest", behavior: "smooth" }); },
      })));
      consoleBody.replaceChildren(...kids);
      if (firstFail) firstFail.scrollIntoView({ block: "nearest" });
    }

    // resizing
    function drag(handle, onMove, onEnd) {
      handle.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        handle.classList.add("drag");
        handle.setPointerCapture(e.pointerId);
        const move = (ev) => onMove(ev);
        const up = () => { handle.classList.remove("drag"); handle.removeEventListener("pointermove", move); handle.removeEventListener("pointerup", up); onEnd(); cm.refresh(); };
        handle.addEventListener("pointermove", move);
        handle.addEventListener("pointerup", up);
      });
    }
    const gutter = split.querySelector(".gutter"), gutterH = right.querySelector(".gutter-h");
    let leftPct = local.get("trace.left", 42), consolePct = local.get("trace.console", 38);
    drag(gutter, (e) => {
      const box = split.getBoundingClientRect();
      leftPct = Math.min(70, Math.max(22, ((e.clientX - box.left) / box.width) * 100));
      split.style.setProperty("--left", `${leftPct}%`);
    }, () => local.set("trace.left", Math.round(leftPct)));
    drag(gutterH, (e) => {
      const box = right.getBoundingClientRect();
      consolePct = Math.min(75, Math.max(15, ((box.bottom - e.clientY) / box.height) * 100));
      right.style.setProperty("--console", `${consolePct}%`);
    }, () => { local.set("trace.console", Math.round(consolePct)); });

    const onKey = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); run(); }
      if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S")) { e.preventDefault(); saveNow(); }
    };
    document.addEventListener("keydown", onKey);
    S.cleanup = () => {
      document.removeEventListener("keydown", onKey);
      if (saveTimer) { clearTimeout(saveTimer); saveNow(); }
    };
  }

  // ── desktop shell: sidebar ──────────────────────────────────────────────────
  const DESKTOP = new URLSearchParams(location.search).has("app");     // opened by Trace.exe
  const closedGroups = new Set(local.get("trace.closedGroups", []));

  function renderSide() {
    const hash = decodeURIComponent(location.hash);
    const [, kind, a] = hash.split("/");
    const activeTopic = kind === "t" || kind === "w" ? a : kind === "p" ? topicOf(a)?.id : kind === "d" ? S.topics.find((t) => T.byId[a] && t.n === T.byId[a].n)?.id : null;
    const activePlan = kind === "plan" ? a : kind === "p" && hash.split("/")[3] === "plan" ? hash.split("/")[4] : null;
    const group = (id, label, kids) => h("section", { class: "side-group" + (closedGroups.has(id) ? " closed" : "") },
      h("button", { type: "button", "aria-expanded": String(!closedGroups.has(id)), onclick: (e) => {
        const closed = e.currentTarget.parentElement.classList.toggle("closed");
        e.currentTarget.setAttribute("aria-expanded", String(!closed));
        closed ? closedGroups.add(id) : closedGroups.delete(id);
        local.set("trace.closedGroups", [...closedGroups]);
      } }, h("span", {}, label), icon(ICONS.down)),
      h("div", { class: "side-list" }, kids));
    const link = (href, n, t, f, current, done) =>
      h("a", { class: "side-link" + (done ? " done" : ""), href, "aria-current": current ? "page" : null, title: t }, h("span", { class: "n" }, n), h("span", { class: "t" }, t), h("span", { class: "f" }, f));
    // One stage's topics: the one you're viewing, else your place in the course, else the last stage.
    const viewed = activeTopic && S.topics.find((t) => t.id === activeTopic);
    const stageName = (viewed || pathTopic() || S.topics[S.topics.length - 1]).stage;
    $("side-nav").replaceChildren(...[
      h("div", { class: "side-list", style: "margin-top:6px" },
        link("#/", icon(ICONS.home), "Home", "", !kind, false),
        link("#/roadmap", icon(ICONS.road), "Roadmap", "", kind === "roadmap", false),
        link("#/contest", icon(ICONS.contest), "Contest", "", kind === "contest", false)),
      group("plans", "Study plans", (S.plans.plans || []).map((pl) => {
        const items = pl.sections.flatMap((sec) => sec.items);
        const done = items.filter(solved).length;
        return link(`#/plan/${pl.id}`, icon(ICONS.plan), pl.title, done ? `${done}/${items.length}` : "", activePlan === pl.id, done === items.length);
      })),
      group("stage:" + stageName, stageName, S.topics.filter((t) => t.stage === stageName).map((topic) => {
        const done = topic.items.filter(solved).length;
        return link(`#/t/${topic.id}`, pad2(topic.n), topicTitle(topic), done ? `${done}/${topic.items.length}` : "", activeTopic === topic.id, done === topic.items.length);
      })),
    ].flat());
    const current = $("side-nav").querySelector('[aria-current="page"]');
    if (current) current.scrollIntoView({ block: "nearest" });
  }

  function toggleSide() {
    const narrow = matchMedia("(max-width: 900px)").matches;
    if (narrow) document.body.classList.toggle("side-open");
    else {
      document.body.classList.toggle("side-closed");
      local.set("trace.sideClosed", document.body.classList.contains("side-closed"));
    }
  }
  if (local.get("trace.sideClosed", false)) document.body.classList.add("side-closed");
  $("side-btn").onclick = toggleSide;
  $("side-nav").addEventListener("click", (e) => {
    if (e.target.closest("a") && matchMedia("(max-width: 900px)").matches) document.body.classList.remove("side-open");
  });

  // ── desktop shell: Go to anything (Ctrl+K) ────────────────────────────────
  const palette = { el: $("palette"), input: $("palette-input"), list: $("palette-list"), items: [], shown: [], at: 0 };

  function paletteEntries() {
    const out = [];
    // k: a topic's number (data, so mono), or the name of a drawn icon for everything else
    for (const pl of S.plans.plans || []) out.push({ icon: "plan", t: pl.title, m: "Study plan", href: `#/plan/${pl.id}` });
    for (const topic of S.topics) {
      out.push({ k: pad2(topic.n), t: topicTitle(topic), m: "Topic", href: `#/t/${topic.id}` });
      for (const n of topic.items) {
        const pr = S.problems[n];
        out.push({ icon: "code", t: pr.title, m: `${kindLabel(pr)}, ${topicTitle(topic)}`, href: `#/p/${n}`, solved: solved(n) });
      }
    }
    for (const dt of T.topics) for (const d of dt.drills) out.push({ icon: "idea", t: d.name, m: `Drill, ${dt.title}`, href: `#/d/${dt.id}/${d.id}` });
    return out;
  }

  function score(entry, q) {
    if (!q) return 1;
    const t = entry.t.toLowerCase(), m = entry.m.toLowerCase();
    const initials = t.split(/[\s-]+/).filter((w) => !["a", "an", "the", "of", "in", "to"].includes(w)).map((w) => w[0]).join("");
    if (q.length > 1 && initials === q) return 5;                                // "lis" → Longest Increasing Subsequence
    if (t.startsWith(q)) return 4;
    if (t.includes(" " + q)) return 3.5;
    if (t.includes(q)) return 3;
    if (q.length > 1 && initials.startsWith(q)) return 2;
    let i = 0;
    for (const ch of t) if (ch === q[i]) i++;
    if (i === q.length) return 1;
    return m.includes(q) ? 0.5 : 0;
  }

  function renderPalette() {
    const q = palette.input.value.trim().toLowerCase();
    palette.shown = palette.items.map((e) => [score(e, q), e]).filter(([sc]) => sc > 0)
      .sort((x, y) => y[0] - x[0]).slice(0, 60).map(([, e]) => e);
    palette.at = Math.min(palette.at, Math.max(0, palette.shown.length - 1));
    palette.list.replaceChildren(...(palette.shown.length ? palette.shown.map((e, i) =>
      h("li", { role: "option", class: e.solved ? "solved" : "", "aria-selected": String(i === palette.at), onclick: () => openEntry(e),
        onmousemove: () => { if (palette.at !== i) { palette.at = i; renderPalette(); } } },
        h("span", { class: "pk", "aria-hidden": e.icon ? "true" : null }, e.icon ? icon(ICONS[e.icon]) : e.k),
        h("span", { class: "pt" }, h("span", {}, e.t),
          e.solved ? h("span", { class: "ps" }, icon(ICONS.check), h("span", { class: "sr-only" }, "solved")) : null),
        h("span", { class: "pm" }, e.m)))
      : [h("li", { class: "palette-empty" }, "Nothing matches. Try part of a problem name, or its initials.")]));
    palette.list.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: "nearest" });
  }

  function openPalette() {
    palette.items = paletteEntries();
    palette.input.value = "";
    palette.at = 0;
    palette.el.hidden = false;
    renderPalette();
    palette.input.focus();
  }
  function closePalette() { palette.el.hidden = true; }
  function openEntry(e) { closePalette(); location.hash = e.href; }

  palette.input.addEventListener("input", () => { palette.at = 0; renderPalette(); });
  palette.input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); palette.at = Math.min(palette.at + 1, palette.shown.length - 1); renderPalette(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); palette.at = Math.max(palette.at - 1, 0); renderPalette(); }
    else if (e.key === "Enter" && palette.shown[palette.at]) openEntry(palette.shown[palette.at]);
    else if (e.key === "Escape") closePalette();
  });
  palette.el.addEventListener("mousedown", (e) => { if (e.target === palette.el) closePalette(); });
  $("search-btn").onclick = openPalette;

  // ── desktop shell: app-wide keys and behaviours ───────────────────────────
  document.addEventListener("keydown", (e) => {
    const mod = e.ctrlKey || e.metaKey;
    if (T.contest.get() && mod && /^[kKpPbB]$/.test(e.key) && !e.target.closest?.(".CodeMirror")) e.preventDefault();   // a contest has no way out
    else if (T.contest.get()) { /* nothing else to open during a contest */ }
    else if (mod && (e.key === "k" || e.key === "K" || e.key === "p" || e.key === "P")) { e.preventDefault(); openPalette(); }
    else if (mod && (e.key === "b" || e.key === "B") && !e.target.closest?.(".CodeMirror")) { e.preventDefault(); toggleSide(); }
    else if (e.altKey && (e.key === "ArrowLeft" || e.key === "ArrowRight") && document.body.classList.contains("ws")) {
      const btn = document.querySelector(`.ws-nav a[aria-label="${e.key === "ArrowLeft" ? "Previous" : "Next"}"]`);
      if (btn) { e.preventDefault(); location.hash = btn.getAttribute("href"); }
    }
  }, true);
  if (DESKTOP) {
    document.documentElement.classList.add("desktop");
    // An app, not a web page: no browser context menu except where you edit or read text.
    document.addEventListener("contextmenu", (e) => {
      if (!e.target.closest(".CodeMirror, input, textarea, pre, code, .statement, .prose, .test-detail")) e.preventDefault();
    });
  }

  // ── router ─────────────────────────────────────────────────────────────────
  async function route() {
    if (S.cleanup) { try { S.cleanup(); } catch { /* ignore */ } S.cleanup = null; }
    document.body.classList.remove("ws");
    app.scrollTop = 0;
    const [, kind, a, b, c] = decodeURIComponent(location.hash).split("/");
    // A running contest keeps you inside it: anywhere else goes back to the problem you were on.
    const live = T.contest.get();
    if (live && live.endsAt - T.now() <= 0) { T.contest.end("time"); return; }
    document.body.classList.toggle("contest", !!live);
    if (live && !(kind === "p" && b === "contest" && live.problems.some((x) => x.name === a))) {
      location.replace(`#/p/${live.current || live.problems[0].name}/contest`);
      return;
    }
    if (!live && kind === "p" && b === "contest") { location.replace(`#/p/${a}`); return; }
    const viewed = kind === "t" || kind === "w" ? S.topics.find((t) => t.id === a)
      : kind === "p" ? topicOf(a) : kind === "d" && T.byId[a] ? S.topics.find((t) => t.n === T.byId[a].n) : null;
    if (viewed && !live) document.body.dataset.stage = stageOf(viewed);
    else delete document.body.dataset.stage;
    try {
      renderSide();
      if (kind === "t") return await viewTopic(a);
      if (kind === "p") return await viewProblem(a, b === "plan" ? c : null, b === "contest");
      if (kind === "contest") return a ? viewContestResults(a) : viewContest();
      if (kind === "plan") return viewPlan(a);
      if (kind === "d") return viewDrill(a, b);
      if (kind === "w") return await viewWalkthrough(a);
      if (kind === "start") return await viewStart();
      if (kind === "roadmap") return viewRoadmap();
      return viewHome();
    } catch (err) {
      console.error(err);
      app.replaceChildren(h("div", { class: "page" }, h("h1", {}, "Something went wrong"), h("p", { class: "lede" }, err.message),
        h("p", {}, h("a", { class: "btn", href: "#/" }, "Back to home"))));
    }
  }

  async function boot() {
    try {
      const data = await api("/api/course");
      S.topics = data.topics;
      S.problems = data.problems;
      S.progress = data.progress;
      S.plans = data.plans || S.plans;
      S.techniques = data.techniques || {};
      T.stageOf = stageOf;
      T.stageNames = stageNames();
      showDocker(data.docker);
    } catch (err) {
      app.replaceChildren(h("div", { class: "page" }, h("h1", {}, "Can't reach Trace's engine"),
        h("p", { class: "lede" }, new URLSearchParams(location.search).has("app")
          ? "Close Trace and open it again."
          : ["Start it with ", h("code", {}, "npm start"), " (or ", h("code", {}, "python server.py"), ") in the project folder, then reload this page."])));
      $("sandbox").hidden = true;
      return;
    }
    window.addEventListener("hashchange", route);
    T.contest.configure({ onEnd: (entry) => { location.hash = `#/contest/${entry.id}`; } });
    T.contest.resume();
    route();
  }
  boot();
})();
