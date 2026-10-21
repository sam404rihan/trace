"use strict";
/* Contest: a few problems against a countdown, in a fullscreen that stays locked until you submit.
   Browsers can't stop Esc, so the lock is a cover: leaving fullscreen hides the work behind a "Back to
   fullscreen" screen while the clock keeps running, and each exit is counted on the results. The live
   contest is kept in localStorage, so a reload resumes it with the right time left. app.js owns the
   course and the workspace; this file owns the clock, the lock, the bar, and the setup and results pages. */
(function () {
  const T = window.Trace;
  const { h, s } = T;
  const KEY = "trace.contest", HISTORY = "trace.contests", KEEP = 20;
  const WARN_MS = 5 * 60000;
  const LENGTHS = [30, 60, 90];
  // What each length draws, easiest first. A short contest never asks for a hard one.
  const MIX = { 30: ["easy", "easy", "medium"], 60: ["easy", "medium", "medium"], 90: ["easy", "medium", "hard"] };
  T.CONTEST_MIX = MIX;
  T.now = () => Date.now();         // the contest's clock; the browser check advances it

  const local = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
    del(k) { try { localStorage.removeItem(k); } catch { /* storage unavailable */ } },
  };
  const icon = (paths) => s("svg", { class: "icon", viewBox: "0 0 24 24", "aria-hidden": "true" }, [].concat(paths).map((d) => s("path", { d })));
  const ICON = {
    clock: ["M12 6a7.5 7.5 0 1 0 0 15a7.5 7.5 0 1 0 0-15", "M12 13.5V10", "M10 2.5h4", "M12 2.5V6", "M18 7l1.5-1.5"],
    expand: ["M4 9V4h5", "M20 9V4h-5", "M4 15v5h5", "M20 15v5h-5"],
    check: "M5 12.5l4.5 4.5L19 7.5",
  };
  T.CONTEST_ICON = ICON.clock;

  const valid = (c) => c && typeof c === "object" && Array.isArray(c.problems) && c.problems.length
    && c.problems.every((p) => p && typeof p.name === "string") && Number.isFinite(c.endsAt) && Number.isFinite(c.startedAt);
  let state = local.get(KEY, null);
  if (!valid(state)) state = null;
  let hooks = { onEnd: null };
  const save = () => { if (state) local.set(KEY, state); };

  // mm:ss. The countdown rounds up, so it reads 60:00 at the start and 0:01 in the last second.
  const clockText = (ms) => { const sec = Math.max(0, Math.ceil(ms / 1000)); return `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, "0")}`; };
  const usedText = (ms) => { const sec = Math.max(0, Math.floor(ms / 1000)); return `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, "0")}`; };
  const minutesLeft = (ms) => { const m = Math.max(1, Math.ceil(ms / 60000)); return `${m} minute${m === 1 ? "" : "s"}`; };
  const times = (n) => (n === 1 ? "once" : `${n} times`);
  const tabState = (p) => (p.solved ? "solved" : p.attempts ? "tried" : "");

  // ── fullscreen ─────────────────────────────────────────────────────────────
  const canFullscreen = () => !!(document.fullscreenEnabled && document.documentElement.requestFullscreen);
  function requestFullscreen() {
    const el = document.documentElement;
    if (!el.requestFullscreen) return Promise.resolve(false);
    try { return Promise.resolve(el.requestFullscreen()).then(() => true, () => false); } catch { return Promise.resolve(false); }
  }
  function exitFullscreen() {
    if (!document.fullscreenElement || !document.exitFullscreen) return;
    try { Promise.resolve(document.exitFullscreen()).catch(() => {}); } catch { /* already out */ }
  }

  // The live region for the few things worth saying aloud (five minutes left, one minute left).
  const say = h("p", { id: "contest-say", class: "sr-only", "aria-live": "polite" });
  // The cover over the screen while a running contest is out of fullscreen.
  const lockGo = h("button", { class: "btn primary contest-lock-go", type: "button" }, icon(ICON.expand), "Back to fullscreen");
  const lockExits = h("p", { class: "contest-lock-note" });
  const lockEl = h("div", { id: "contest-lock", class: "contest-lock", role: "dialog", "aria-modal": "true", "aria-labelledby": "contest-lock-title", hidden: true },
    h("div", { class: "contest-lock-card" },
      h("span", { class: "contest-lock-mark", "aria-hidden": "true" }, icon(ICON.expand)),
      h("h2", { id: "contest-lock-title" }, "Back to fullscreen to keep going"),
      h("p", {}, "The contest stays in fullscreen until you submit. The clock is still running."),
      h("p", { class: "contest-lock-time" }, h("span", { "data-contest-clock": "" }, ""), " left"),
      lockGo, lockExits));
  document.body.append(say, lockEl);
  let lastFocus = null;
  const shell = () => [document.querySelector(".main"), document.querySelector(".side")].filter(Boolean);

  function lock() {
    if (!state) return;
    lockExits.textContent = `You've left fullscreen ${times(state.exits)}. It's noted on your results.`;
    if (lockEl.hidden) lastFocus = document.activeElement;
    lockEl.hidden = false;
    shell().forEach((el) => { el.inert = true; });
    paint();
    lockGo.focus();
  }
  function unlock() {
    if (lockEl.hidden) return;
    lockEl.hidden = true;
    shell().forEach((el) => { el.inert = false; });
    if (lastFocus && lastFocus.isConnected) lastFocus.focus();
    lastFocus = null;
  }
  lockGo.onclick = async () => {
    const ok = await requestFullscreen();
    // Refused (no fullscreen here after all): let the learner carry on in the window. The exit is already counted.
    if (!ok || !document.fullscreenElement) unlock();
  };

  document.addEventListener("fullscreenchange", () => {
    if (!state) return;
    if (document.fullscreenElement) {
      state.fsUsed = true;
      state.inFs = true;
      save();
      unlock();
    } else if (state.inFs) {
      state.inFs = false;
      state.exits = (state.exits || 0) + 1;
      save();
      lock();
    }
  });
  window.addEventListener("beforeunload", (e) => {
    if (!state) return;
    e.preventDefault();
    e.returnValue = "";
  });

  // ── the clock ──────────────────────────────────────────────────────────────
  let timer = null;
  function paint() {
    if (!state) return;
    const ms = state.endsAt - T.now();
    const text = clockText(ms);
    document.querySelectorAll("[data-contest-clock]").forEach((el) => { if (el.textContent !== text) el.textContent = text; });
    const label = `Time left: ${minutesLeft(ms)}`;
    document.querySelectorAll(".contest-clock").forEach((el) => {
      el.toggleAttribute("data-warn", ms <= WARN_MS);
      if (el.getAttribute("aria-label") !== label) el.setAttribute("aria-label", label);
    });
    if (ms <= 60000 && !state.saidOne) { state.saidOne = state.saidFive = true; save(); say.textContent = "1 minute left."; }
    else if (ms <= WARN_MS && !state.saidFive) { state.saidFive = true; save(); say.textContent = `${minutesLeft(ms)} left.`; }
  }
  function tick() {
    if (!state) return stopClock();
    if (state.endsAt - T.now() <= 0) return C.end("time");
    paint();
  }
  function startClock() { if (!timer) timer = setInterval(tick, 1000); }
  function stopClock() { clearInterval(timer); timer = null; }

  // ── history ────────────────────────────────────────────────────────────────
  function history() {
    const list = local.get(HISTORY, []);
    return Array.isArray(list) ? list.filter((e) => e && typeof e.id === "string" && Array.isArray(e.problems)) : [];
  }

  // ── the bar over the workspace ─────────────────────────────────────────────
  let paintTabs = null;
  function bar(name) {
    const tabs = h("nav", { class: "contest-tabs", "aria-label": "Contest problems" });
    paintTabs = () => {
      if (!state) return;
      tabs.replaceChildren(...state.problems.map((p, k) => {
        const st = tabState(p);
        return h("a", { class: "contest-tab", href: `#/p/${p.name}/contest`, "data-state": st, "aria-current": p.name === name ? "page" : null,
          "aria-label": `Problem ${k + 1}: ${p.title}, ${p.difficulty}${st === "solved" ? ", solved" : st === "tried" ? ", tried" : ""}`, title: p.title },
          h("span", { class: "contest-tab-n", "aria-hidden": "true" }, st === "solved" ? icon(ICON.check) : String(k + 1)),
          h("span", { class: "contest-tab-t", "aria-hidden": "true" }, p.title));
      }));
    };
    paintTabs();
    const clock = h("span", { class: "contest-clock", role: "timer", "aria-live": "off", "aria-label": "Time left" },
      icon(ICON.clock), h("span", { "data-contest-clock": "", "aria-hidden": "true" }, ""));
    const submit = h("button", { class: "btn primary small contest-submit", type: "button" }, "Submit");
    const yes = h("button", { class: "btn primary small contest-confirm-yes", type: "button" }, "Submit and finish");
    const no = h("button", { class: "btn ghost small contest-confirm-no", type: "button" }, "Keep going");
    const confirmBox = h("div", { class: "contest-confirm", role: "group", "aria-labelledby": "contest-confirm-q", hidden: true },
      h("span", { id: "contest-confirm-q" }, "End the contest now?"), yes, no);
    const ask = (open) => {
      confirmBox.hidden = !open;
      submit.hidden = open;
      (open ? no : submit).focus();
    };
    submit.onclick = () => ask(true);
    no.onclick = () => ask(false);
    yes.onclick = () => C.end("submitted");
    confirmBox.addEventListener("keydown", (e) => { if (e.key === "Escape") { e.preventDefault(); ask(false); } });
    const el = h("div", { class: "contest-bar" }, tabs, clock, h("div", { class: "contest-end" }, submit, confirmBox));
    setTimeout(paint, 0);
    return el;
  }

  // ── setup page ─────────────────────────────────────────────────────────────
  // ctx: { startedTopics, draw(scope, minutes) -> [{ name, title, difficulty, total }] }
  function mountSetup(host, ctx) {
    let minutes = 60, scope = "started";
    const opt = (group, value, title, sub, checked, onPick) =>
      h("label", { class: "contest-opt" },
        h("input", { type: "radio", name: group, value: String(value), checked: checked || null, onchange: onPick }),
        h("strong", {}, title), h("span", {}, sub));
    const mixText = (m) => { const mix = MIX[m]; return mix.map((d, k) => (k ? d : d[0].toUpperCase() + d.slice(1))).join(", "); };
    const startBtn = h("button", { class: "btn primary contest-start", type: "button" }, icon(ICON.clock), "Start the contest");
    const fail = h("p", { class: "contest-note", role: "status" });
    startBtn.onclick = () => {
      const problems = ctx.draw(scope, minutes);
      if (problems.length < 1) { fail.textContent = "There are no problems to draw from yet."; return; }
      C.begin({ minutes, scope, problems });
    };
    const past = history();
    const n = ctx.startedTopics;
    host.replaceChildren(h("div", { class: "page contest-page contest-setup" },
      h("h1", {}, "Contest"),
      h("p", { class: "lede" }, "Three problems against the clock, easiest first. The screen goes fullscreen and stays that way until you submit, like a real test."),
      h("fieldset", { class: "contest-choice" }, h("legend", {}, "How long"),
        h("div", { class: "contest-opts" }, LENGTHS.map((m) => opt("minutes", m, `${m} minutes`, mixText(m), m === minutes, () => { minutes = m; })))),
      h("fieldset", { class: "contest-choice" }, h("legend", {}, "Problems from"),
        h("div", { class: "contest-opts" },
          opt("scope", "started", "Topics you've started", n ? `${n} topic${n === 1 ? "" : "s"} so far` : "The first stage, until you start more", true, () => { scope = "started"; }),
          opt("scope", "all", "The whole course", "Any topic, any stage", false, () => { scope = "all"; }))),
      h("p", { class: "contest-rules" }, "Ladder locks are off and your code is saved as usual. Hints and reference solutions wait until you've submitted."),
      h("div", { class: "hero-actions" }, startBtn),
      canFullscreen() ? null : h("p", { class: "contest-note" }, "This screen can't go fullscreen, so the contest runs in the window."),
      fail,
      past.length ? [
        h("h2", { class: "section-title" }, "Past contests"),
        h("div", { class: "topic-list contest-history" }, past.map((e) => {
          const solvedN = e.problems.filter((p) => p.solved).length;
          const when = new Date(e.startedAt);
          return h("a", { class: "topic-row", href: `#/contest/${e.id}` },
            h("span", { class: "num" }, `${solvedN}/${e.problems.length}`),
            h("span", { class: "name" }, `${when.toLocaleDateString(undefined, { day: "numeric", month: "short" })}, ${when.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })}`,
              h("span", { class: "sub" }, `${e.minutes} minutes. Solved ${solvedN} of ${e.problems.length}.${e.exits ? ` Left fullscreen ${times(e.exits)}.` : ""}`)),
            h("span"));
        })),
      ] : null));
    return { unmount() {} };
  }

  // ── results page ───────────────────────────────────────────────────────────
  function mountResults(host, e) {
    const solvedN = e.problems.filter((p) => p.solved).length;
    const used = (e.endedAt || e.startedAt) - e.startedAt;
    const lede = solvedN === e.problems.length ? `You solved all ${e.problems.length}.`
      : solvedN ? `You solved ${solvedN} of ${e.problems.length}. The rest stay open in the course, with hints and solutions.`
        : "None solved this time. Every attempt is practice, and the problems stay open in the course, with hints and solutions.";
    host.replaceChildren(h("div", { class: "page contest-page contest-results" },
      h("h1", {}, e.reason === "time" ? "Time's up" : "Contest submitted"),
      h("p", { class: "lede" }, lede),
      h("dl", { class: "facts contest-facts" },
        h("div", {}, h("dt", {}, "Time used"), h("dd", { class: "contest-used" }, `${usedText(used)} of ${e.minutes}:00`)),
        h("div", {}, h("dt", {}, "Fullscreen"), h("dd", { class: "contest-exits" },
          !e.fsUsed ? "Ran in the window" : e.exits ? `Left it ${times(e.exits)}` : "Stayed in fullscreen the whole time"))),
      h("h2", { class: "section-title" }, "Problems"),
      h("div", { class: "items" }, e.problems.map((p, k) => {
        const st = tabState(p);
        return h("a", { class: "item contest-result-row" + (p.solved ? " solved" : p.best ? " partial" : ""), href: `#/p/${p.name}`, "data-state": st,
          style: `--p:${p.total ? Math.round((100 * (p.best || 0)) / p.total) : 0}` },
          h("span", { class: "state", "aria-hidden": "true" }),
          h("span", { class: "t" }, `${k + 1}. ${p.title}`),
          h("span", { class: "meta" }, p.attempts
            ? `${p.best || 0} of ${p.total} tests${p.solved && p.solvedAt != null ? `, solved at ${usedText(p.solvedAt)}` : ""}`
            : "Not tried"),
          h("span", { class: "badge " + p.difficulty }, p.difficulty[0].toUpperCase() + p.difficulty.slice(1)));
      })),
      h("div", { class: "hero-actions" },
        h("a", { class: "btn primary", href: "#/contest" }, "Back to contests"),
        h("a", { class: "link", href: "#/roadmap" }, "Go to the roadmap"))));
    return { unmount() {} };
  }

  // ── the contest itself ─────────────────────────────────────────────────────
  const C = T.contest = {
    get: () => state,
    configure(next) { Object.assign(hooks, next); },
    canFullscreen,
    history,
    find: (id) => history().find((e) => e.id === id) || null,
    bar, mountSetup, mountResults,
    // Start: ask for fullscreen first, while the click still counts as a user gesture.
    begin({ minutes, scope, problems }) {
      const asked = canFullscreen() ? requestFullscreen() : Promise.resolve(false);
      const now = T.now();
      state = {
        id: now.toString(36), minutes, scope, startedAt: now, endsAt: now + minutes * 60000,
        problems: problems.map((p) => ({ ...p, best: 0, attempts: 0, solved: false, solvedAt: null })),
        exits: 0, fsUsed: false, inFs: !!document.fullscreenElement, current: problems[0].name,
      };
      save();
      startClock();
      location.hash = `#/p/${state.current}/contest`;
      return asked;
    },
    // After a page load: a contest that was in fullscreen has lost it, so that counts as leaving.
    resume() {
      if (!state) return;
      startClock();
      if (state.endsAt - T.now() <= 0) return;
      if (state.inFs && !document.fullscreenElement) {
        state.inFs = false;
        state.exits = (state.exits || 0) + 1;
        save();
        lock();
      }
    },
    open(name) { if (state && state.current !== name) { state.current = name; save(); } },
    // One run's tests: any run counts as tried; the best pass count and a full pass are kept.
    record(name, tests) {
      const p = state && state.problems.find((x) => x.name === name);
      if (!p) return;
      p.attempts += 1;
      const passed = tests.filter((t) => t.status === "pass").length;
      const todo = tests.length > 0 && tests.every((t) => t.status === "todo");
      if (tests.length) p.total = tests.length;
      p.best = Math.max(p.best || 0, passed);
      if (!todo && tests.length && passed === tests.length && !p.solved) { p.solved = true; p.solvedAt = T.now() - state.startedAt; }
      save();
      if (paintTabs) paintTabs();
    },
    // The next problem still to solve after this one, in contest order; null once all are solved.
    nextOpen(name) {
      if (!state) return null;
      const list = state.problems, i = list.findIndex((p) => p.name === name);
      for (let k = 1; k < list.length; k++) { const p = list[(i + k) % list.length]; if (!p.solved) return p.name; }
      return null;
    },
    end(reason) {
      if (!state) return null;
      const done = state;
      state = null;
      stopClock();
      paintTabs = null;
      local.del(KEY);
      const entry = {
        id: done.id, minutes: done.minutes, scope: done.scope, reason, startedAt: done.startedAt,
        endedAt: Math.min(T.now(), done.endsAt), exits: done.exits || 0, fsUsed: !!done.fsUsed,
        problems: done.problems.map(({ name, title, difficulty, total, best, attempts, solved, solvedAt }) => ({ name, title, difficulty, total, best, attempts, solved, solvedAt })),
      };
      local.set(HISTORY, [entry, ...history().filter((e) => e.id !== entry.id)].slice(0, KEEP));
      unlock();
      exitFullscreen();
      say.textContent = reason === "time" ? "Time's up." : "";
      if (hooks.onEnd) hooks.onEnd(entry);
      return entry;
    },
  };
})();
