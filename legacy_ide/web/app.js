"use strict";

const $ = (id) => document.getElementById(id);
const els = {
  nav: $("nav"), tally: $("tally"), tallyCaption: $("tally-caption"), continueBtn: $("continue-btn"),
  title: $("title"), meta: $("meta"),
  lessonPanel: $("lesson-panel"), notes: $("notes"), practiceBtn: $("practice-btn"),
  problemPanel: $("problem-panel"), statement: $("statement"),
  hintBtn: $("hint-btn"), hint: $("hint"), solutionBtn: $("solution-btn"), solution: $("solution"),
  prevBtn: $("prev-btn"), nextBtn: $("next-btn"),
  bench: document.querySelector(".bench"), banner: $("docker-banner"),
  editorTitle: $("editor-title"), editor: $("editor"),
  runBtn: $("run-btn"), customToggle: $("custom-toggle"), customWrap: $("custom-wrap"), custom: $("custom"),
  saveState: $("save-state"), resetBtn: $("reset-btn"),
  splitter: $("splitter"), results: $("results"),
};

const state = {
  stages: [], topics: {}, problems: {}, examples: [],
  progress: { problems: {}, lessons: {} },
  docker: { state: "checking" },
  view: null,            // { kind: "lesson", topic } | { kind: "problem", name } | { kind: "scratch" } | { kind: "example", id }
  problem: null,         // details of the open problem
  openTopic: null,       // the one topic expanded in the sidebar
  showExamples: false,   // "Under the hood" list expanded
  running: false, loading: false, saveTimer: null, errorLine: null,
};

// ── small utilities ─────────────────────────────────────────────────────────

function h(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value == null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : value);
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

async function api(path, body) {
  const options = body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {};
  const res = await fetch(path, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

const store = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* private mode */ } },
};

const capital = (s) => s.charAt(0).toUpperCase() + s.slice(1);

// A few drawn icons, one stroke weight, instead of unicode glyphs.
const ICONS = {
  check: "M3.5 8.5l3 3 6-7",
  cross: "M4.5 4.5l7 7M11.5 4.5l-7 7",
  chevron: "M6 3.5l4.5 4.5L6 12.5",
  dash: "M4.5 8h7",
};
function icon(name, cls = "") {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 16 16");
  svg.setAttribute("class", `icon ${cls}`.trim());
  svg.setAttribute("aria-hidden", "true");
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", ICONS[name]);
  svg.append(path);
  return svg;
}
const escapeHtml = (s) => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// ── course helpers ──────────────────────────────────────────────────────────

const topicOrder = () => state.stages.flatMap((s) => s.topics);
const problemStatus = (name) => {
  const p = state.progress.problems[name];
  return !p ? "new" : p.solved ? "solved" : "trying";
};
const solvedCount = () => Object.keys(state.problems).filter((n) => problemStatus(n) === "solved").length;
const topicSolved = (t) => t.problems.filter((n) => problemStatus(n) === "solved").length;

// The next thing to study: an unread lesson, else the first unsolved problem, in course order.
function nextStep(after = null) {
  let started = after === null;
  for (const id of topicOrder()) {
    const topic = state.topics[id];
    const items = [];
    if (topic.has_lesson) items.push({ kind: "lesson", topic: id, done: !!state.progress.lessons[id] });
    for (const name of topic.problems) items.push({ kind: "problem", name, done: problemStatus(name) === "solved" });
    for (const item of items) {
      if (!started) {
        if (sameView(item, after)) started = true;
        continue;
      }
      if (!item.done) return item;
    }
  }
  return null;
}

function viewLabel(view) {
  if (view.kind === "lesson") {
    const t = state.topics[view.topic];
    return `Lesson ${t.number}: ${t.title}`;
  }
  if (view.kind === "problem") return state.problems[view.name].title;
  return "";
}

// ── editor (CodeMirror, or a plain textarea if the CDN is unreachable) ─────

function createEditor(host) {
  if (window.CodeMirror) {
    return CodeMirror(host, {
      mode: "python", lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
      matchBrackets: true, autoCloseBrackets: true, styleActiveLine: true,
      extraKeys: {
        Tab: (cm) => cm.somethingSelected() ? cm.indentSelection("add") : cm.replaceSelection("    "),
        "Shift-Tab": (cm) => cm.indentSelection("subtract"),
        "Ctrl-/": "toggleComment", "Cmd-/": "toggleComment",
        "Ctrl-Enter": () => run(), "Cmd-Enter": () => run(),
      },
    });
  }
  const area = h("textarea", { spellcheck: "false", "aria-label": "Code editor" });
  host.append(area);
  const handlers = [];
  area.addEventListener("input", () => handlers.forEach((fn) => fn()));
  area.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      e.preventDefault();
      area.setRangeText("    ", area.selectionStart, area.selectionEnd, "end");
      handlers.forEach((fn) => fn());
    }
  });
  return {
    getValue: () => area.value, setValue: (v) => { area.value = v; }, focus: () => area.focus(),
    on: (event, fn) => event === "change" && handlers.push(fn),
    clearHistory() {}, refresh() {}, addLineClass() {}, removeLineClass() {}, lineCount: () => 0,
  };
}

const editor = createEditor(els.editor);

editor.on("change", () => {
  if (state.loading) return;
  clearErrorLine();
  scheduleSave();
});

function clearErrorLine() {
  if (state.errorLine != null) {
    editor.removeLineClass(state.errorLine, "background", "cm-error-line");
    state.errorLine = null;
  }
}

function markErrorLine(traceback, filename) {
  const matches = [...(traceback || "").matchAll(new RegExp(`File "${filename}", line (\\d+)`, "g"))];
  if (!matches.length) return;
  const line = Number(matches[matches.length - 1][1]) - 1;
  if (line >= 0 && line < editor.lineCount()) {
    clearErrorLine();
    editor.addLineClass(line, "background", "cm-error-line");
    state.errorLine = line;
  }
}

// ── saving ──────────────────────────────────────────────────────────────────

const saveable = () => state.view && (state.view.kind === "problem" || state.view.kind === "scratch");

function scheduleSave() {
  if (!saveable()) return;
  els.saveState.textContent = "Editing…";
  clearTimeout(state.saveTimer);
  state.saveTimer = setTimeout(saveNow, 700);
}

async function saveNow() {
  clearTimeout(state.saveTimer);
  state.saveTimer = null;
  if (!saveable()) return;
  const { kind, name } = state.view;
  try {
    await api("/api/save", { kind, name, code: editor.getValue() });
    els.saveState.textContent = "Saved";
  } catch (err) {
    els.saveState.textContent = "Not saved";
    els.saveState.title = err.message;
  }
}

// ── sidebar ─────────────────────────────────────────────────────────────────

function sameView(a, b) {
  return !!a && !!b && a.kind === b.kind && a.name === b.name && a.id === b.id && a.topic === b.topic;
}

function currentTopic() {
  const v = state.view;
  if (!v) return null;
  if (v.kind === "lesson") return v.topic;
  if (v.kind === "problem") return state.problems[v.name]?.topic_id;
  return null;
}

function navItem(view, label, dotClass, title) {
  return h("button", {
    class: "item", "aria-current": String(sameView(view, state.view)), title, onclick: () => open(view),
  }, h("span", { class: `dot ${dotClass}`, "aria-hidden": "true" }), h("span", { class: "label" }, label));
}

function problemItem(name) {
  const p = state.problems[name];
  const status = problemStatus(name);
  const note = { solved: "solved", trying: "not all tests pass yet", new: "not started" }[status];
  return navItem({ kind: "problem", name }, p.title, status === "new" ? "" : status, `${p.title} (${p.difficulty}, ${note})`);
}

function renderNav() {
  const blocks = [];

  for (const stage of state.stages) {
    const block = h("section", { class: "stage" }, h("h3", {}, stage.title));
    for (const id of stage.topics) {
      const topic = state.topics[id];
      const solved = topicSolved(topic);
      const total = topic.problems.length;
      const done = total > 0 && solved === total;
      const open = state.openTopic === id;
      // Progress only appears once there is some: a column of "0/3" is noise.
      const status = done ? icon("check") : solved ? `${solved}/${total}` : "";
      block.append(h("button", {
        class: `row${done ? " done" : ""}`, "aria-expanded": String(open),
        title: `${topic.title}: ${solved} of ${total} solved`, onclick: () => toggleTopic(id),
      }, h("span", { class: "num" }, topic.number), h("span", {}, topic.title), h("span", { class: "status" }, status)));
      if (open) {
        const read = !!state.progress.lessons[id];
        block.append(h("div", { class: "topic-body" },
          topic.has_lesson ? navItem({ kind: "lesson", topic: id }, "Lesson", read ? "read" : "", "Lesson and cheat sheet") : null,
          topic.problems.map(problemItem)));
      }
    }
    blocks.push(block);
  }

  const more = h("section", { class: "stage more" },
    navItem({ kind: "scratch" }, "Scratchpad", "none", "Run any Python you like"));
  if (state.examples.length) {
    more.append(h("button", {
      class: "row", "aria-expanded": String(state.showExamples),
      onclick: () => { state.showExamples = !state.showExamples; renderNav(); },
    }, h("span", {}, "Under the hood"), h("span", { class: "status" }, icon("chevron", "chevron"))));
    if (state.showExamples) {
      more.append(h("div", { class: "topic-body" }, state.examples.map((e) =>
        navItem({ kind: "example", id: e.id }, capital(e.title), "none", `${e.id}.py: a full implementation`))));
    }
  }
  blocks.push(more);
  els.nav.replaceChildren(...blocks);
  renderContinue();
}

function toggleTopic(id) {
  if (state.openTopic === id) {
    state.openTopic = null;
  } else {
    state.openTopic = id;
    // Opening a topic you're not in jumps to its lesson, the natural first step.
    if (currentTopic() !== id && state.topics[id].has_lesson) return open({ kind: "lesson", topic: id });
  }
  renderNav();
}

function renderContinue() {
  const step = nextStep();
  els.continueBtn.hidden = !step || sameView(step, state.view);
  if (step) {
    els.continueBtn.replaceChildren(h("small", {}, "Continue"), h("span", {}, viewLabel(step)));
    els.continueBtn.onclick = () => open(step);
  }
}

// Solved problems as chalk tally marks: four strokes and a slash per five.
function renderTally(animateIndex = -1) {
  const total = Object.keys(state.problems).length;
  const solved = solvedCount();
  const perRow = 6, groupW = 37, rowH = 24;
  const rows = Math.max(1, Math.ceil(total / 5 / perRow));
  els.tally.setAttribute("viewBox", `0 0 ${perRow * groupW} ${rows * rowH}`);
  els.tally.style.height = `${rows * rowH}px`;
  const wobble = (i, k) => { const x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return (x - Math.floor(x)) - 0.5; };

  const paths = [];
  for (let i = 0; i < total; i++) {
    const g = Math.floor(i / 5), k = i % 5;
    const gx = (g % perRow) * groupW, gy = Math.floor(g / perRow) * rowH;
    let d;
    if (k < 4) {
      const x = gx + 5 + k * 6.5 + wobble(i, 1) * 1.4;
      const top = gy + 3 + wobble(i, 2) * 1.6, bottom = gy + 20 + wobble(i, 3) * 1.6;
      d = `M${x.toFixed(1)} ${top.toFixed(1)} Q${(x + wobble(i, 4) * 2.4).toFixed(1)} ${((top + bottom) / 2).toFixed(1)} ${(x + wobble(i, 5) * 1.2).toFixed(1)} ${bottom.toFixed(1)}`;
    } else {
      d = `M${gx + 1} ${gy + 17 + wobble(i, 6) * 1.6} Q${gx + 15} ${gy + 12 + wobble(i, 7) * 2} ${gx + 30} ${gy + 6 + wobble(i, 8) * 1.6}`;
    }
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", d);
    path.setAttribute("class", i < solved ? "on" : "off");
    paths.push(path);
  }
  els.tally.replaceChildren(...paths);
  els.tally.setAttribute("aria-label", `${solved} of ${total} problems solved`);
  els.tallyCaption.textContent = solved === total && total
    ? `All ${total} solved. Try them again from memory.`
    : `${solved} of ${total} problems solved`;

  const fresh = paths[animateIndex];
  if (fresh && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const length = fresh.getTotalLength();
    fresh.style.strokeDasharray = length;
    fresh.style.strokeDashoffset = length;
    fresh.getBoundingClientRect();
    fresh.style.transition = "stroke-dashoffset 600ms cubic-bezier(.3,.7,.4,1)";
    fresh.style.strokeDashoffset = "0";
  }
}

// ── Docker status ───────────────────────────────────────────────────────────

function renderDocker() {
  const d = state.docker || {};
  const messages = {
    checking: ["Checking for Docker…", false],
    building: ["Setting up the Python container. The first time downloads about 50 MB; after that every Run starts in a second or two.", false],
    stopped: ["Docker Desktop isn't running. Start it, and this page will notice by itself.", true],
    missing: ["Docker isn't installed. Install Docker Desktop, then restart server.py.", true],
    broken: ["The container image didn't build:\n" + (d.detail || ""), true],
  };
  const message = messages[d.state];
  els.banner.hidden = !message;
  if (message) {
    els.banner.textContent = message[0];
    els.banner.classList.toggle("bad", message[1]);
  }
}

async function refreshState({ full = false } = {}) {
  const data = await api("/api/state");
  state.docker = data.docker;
  renderDocker();
  if (full) {
    state.stages = data.stages;
    state.topics = data.topics;
    state.problems = data.problems;
    state.examples = data.examples;
    state.progress = data.progress;
  }
  if (state.docker.state !== "ready") setTimeout(() => refreshState().catch(() => {}), 3000);
}

// ── lesson notes: a tiny markdown renderer ──────────────────────────────────

function inline(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function renderMarkdown(md) {
  const html = [];
  let para = [], list = null, code = null;
  const flushPara = () => { if (para.length) html.push(`<p>${inline(para.join(" "))}</p>`); para = []; };
  const flushList = () => { if (list) html.push(`<${list.tag}>${list.items.map((i) => `<li>${inline(i)}</li>`).join("")}</${list.tag}>`); list = null; };

  for (const raw of md.split("\n")) {
    if (code) {
      if (raw.trim().startsWith("```")) { html.push(code.join("\n")); code = null; html.push(""); continue; }
      code.push(raw);
      continue;
    }
    const line = raw.trimEnd();
    if (line.trim().startsWith("```")) { flushPara(); flushList(); code = []; html.push(" code"); continue; }
    if (line.startsWith("# ")) continue;                       // the title is shown in the header
    if (line.startsWith("## ")) { flushPara(); flushList(); html.push(`<h3>${inline(line.slice(3))}</h3>`); continue; }
    const bullet = line.match(/^- (.*)/), numbered = line.match(/^\d+\. (.*)/);
    if (bullet || numbered) {
      flushPara();
      const tag = bullet ? "ul" : "ol";
      if (!list || list.tag !== tag) { flushList(); list = { tag, items: [] }; }
      list.items.push((bullet || numbered)[1]);
      continue;
    }
    if (list && /^\s{2,}\S/.test(line)) { list.items[list.items.length - 1] += " " + line.trim(); continue; }
    if (!line.trim()) { flushPara(); flushList(); continue; }
    flushList();
    para.push(line.trim());
  }
  flushPara();
  flushList();

  // Swap code placeholders for highlighted <pre> blocks.
  const container = document.createElement("div");
  const flat = document.createElement("div");
  const parts = [];
  for (let i = 0; i < html.length; i++) {
    if (html[i] === " code") {
      parts.push({ code: html[i + 1] });
      i += 2;
    } else {
      parts.push({ html: html[i] });
    }
  }
  for (const part of parts) {
    if (part.code != null) {
      const pre = document.createElement("pre");
      if (window.CodeMirror?.runMode) CodeMirror.runMode(part.code, "python", pre);
      else pre.textContent = part.code;
      flat.append(pre);
    } else if (part.html) {
      flat.insertAdjacentHTML("beforeend", part.html);
    }
  }

  // Each "## heading" becomes a collapsible section; only the first two start open,
  // so a lesson reads as a short intro plus a list of things to open.
  let section = null, sections = 0;
  for (const node of [...flat.childNodes]) {
    if (node.nodeName === "P" && /^Press Run\b/.test(node.textContent)) continue;   // the editor already says this
    if (node.nodeName === "H3") {
      section = h("details", sections < 2 ? { open: true } : {},
        h("summary", {}, icon("chevron", "chevron"), node.textContent));
      sections += 1;
      container.append(section);
    } else if (section) {
      section.append(node);
    } else {
      container.append(node);
    }
  }
  return container.childNodes;
}

// ── opening a view ──────────────────────────────────────────────────────────

async function open(view, { focus = true } = {}) {
  if (state.saveTimer) await saveNow();
  state.view = view;
  const topicId = currentTopic();
  if (topicId) state.openTopic = topicId;
  if (view.kind === "example") state.showExamples = true;
  location.hash = view.kind === "problem" ? `problem/${view.name}`
    : view.kind === "lesson" ? `lesson/${view.topic}`
    : view.kind === "example" ? `example/${view.id}` : "scratch";
  store.set("dsa:view", location.hash);
  renderNav();
  clearErrorLine();
  els.results.replaceChildren();
  els.saveState.textContent = "";
  els.custom.value = "";

  const isProblem = view.kind === "problem";
  const hasBrief = isProblem || view.kind === "lesson";
  document.body.classList.toggle("wide", !hasBrief);
  els.customToggle.hidden = !isProblem;
  setCustomOpen(false);
  els.runBtn.textContent = isProblem ? "Run tests" : "Run";
  els.lessonPanel.hidden = view.kind !== "lesson";
  els.problemPanel.hidden = !isProblem;

  let code = "";
  if (isProblem) {
    const p = await api(`/api/problem?name=${encodeURIComponent(view.name)}`);
    state.problem = p;
    code = p.code;
    renderProblemBrief(p);
    els.editorTitle.textContent = "";
    els.resetBtn.textContent = "Reset code";
    els.results.append(h("p", { class: "empty" }, "Write your solution, then press Run tests (Ctrl+Enter)."));
  } else if (view.kind === "lesson") {
    const lesson = await api(`/api/lesson?topic=${encodeURIComponent(view.topic)}`);
    code = lesson.code;
    renderLessonBrief(lesson);
    els.editorTitle.textContent = "Examples to run and change. Edits aren't saved.";
    els.resetBtn.textContent = "Restore original";
    els.results.append(h("p", { class: "empty" }, "Press Run to see what the examples print."));
    if (!state.progress.lessons[view.topic]) {
      api("/api/visit", { topic: view.topic }).then((r) => { state.progress = r.progress; renderNav(); }).catch(() => {});
    }
  } else if (view.kind === "scratch") {
    code = (await api("/api/scratch")).code;
    document.title = "Scratchpad · DSA Playground";
    els.editorTitle.textContent = "Scratchpad. Any Python, saved as you type.";
    els.resetBtn.textContent = "Reset scratchpad";
    els.results.append(h("p", { class: "empty" }, "Press Run to execute your code."));
  } else {
    const ex = await api(`/api/example?id=${encodeURIComponent(view.id)}`);
    code = ex.code;
    document.title = `${capital(ex.title)} · DSA Playground`;
    els.editorTitle.textContent = `${ex.id}.py. Edits aren't saved.`;
    els.resetBtn.textContent = "Restore original";
    els.results.append(h("p", { class: "empty" }, "Press Run to see the demo at the bottom of the file."));
  }

  state.loading = true;
  editor.setValue(code);
  editor.clearHistory();
  state.loading = false;
  editor.refresh();
  if (focus && isProblem) editor.focus();
}

function renderLessonBrief(lesson) {
  const topic = state.topics[lesson.topic_id];
  document.title = `${lesson.title} · DSA Playground`;
  els.title.textContent = lesson.title;
  els.meta.replaceChildren(`${lesson.stage}, lesson ${lesson.number} of ${topicOrder().length}`);
  els.notes.replaceChildren(...renderMarkdown(lesson.notes));
  els.lessonPanel.scrollTop = 0;

  // The topic's problems are already listed in the sidebar; one clear next action is enough here.
  const next = topic.problems.find((n) => problemStatus(n) !== "solved");
  if (topic.problems.length) {
    els.practiceBtn.hidden = false;
    els.practiceBtn.textContent = next ? `Practise: ${state.problems[next].title}` : "Review the problems";
    els.practiceBtn.onclick = () => open({ kind: "problem", name: next || topic.problems[0] });
  } else {
    els.practiceBtn.hidden = true;
  }
}

// Statements are hard-wrapped at ~80 columns. Join prose lines into paragraphs so
// they wrap to the panel, but keep indented lines (examples, diagrams) exactly as written.
function reflow(text) {
  const out = [];
  let labelled = false;                  // inside an "Aim for:" / "Hint:" block
  for (const line of text.split("\n")) {
    const prev = out[out.length - 1];
    const isLabel = /^[A-Z][A-Za-z ]*:/.test(line);
    if (!line.trim()) { out.push(""); labelled = false; continue; }
    if (isLabel) { out.push(line.replace(/:\s+/, ": ")); labelled = /^(Aim for|Hint):/.test(line); continue; }
    const continuesLabel = labelled && /^ {6,}\S/.test(line);
    const continuesProse = /^\S/.test(line) && prev && /^\S/.test(prev) && !prev.endsWith(":");
    if (continuesLabel || continuesProse) out[out.length - 1] = `${prev} ${line.trim()}`;
    else out.push(line);
  }
  return out.join("\n");
}

function renderProblemBrief(p) {
  document.title = `${p.title} · DSA Playground`;
  const topic = state.topics[p.topic_id];
  els.title.textContent = p.title;
  els.meta.replaceChildren(
    p.difficulty ? h("span", { class: `chip ${p.difficulty}` }, p.difficulty) : null,
    h("span", {},
      topic.has_lesson ? h("button", { class: "link", onclick: () => open({ kind: "lesson", topic: topic.id }), title: "Open the lesson" }, topic.title) : topic.title,
      `, problem ${p.index + 1} of ${p.of}`),
  );

  // Hide the hint behind a button: trying without it is the point.
  const lines = p.statement.split("\n");
  const hintAt = lines.findIndex((l) => /^Hint:/.test(l));
  const body = hintAt >= 0 ? lines.slice(0, hintAt) : lines;
  const hint = hintAt >= 0 ? lines.slice(hintAt).join("\n").replace(/^Hint:\s*/, "") : "";
  els.statement.textContent = reflow(body.join("\n").trimEnd());
  els.hintBtn.hidden = !hint;
  els.hint.textContent = reflow(hint.split("\n").map((l) => l.replace(/^ {10}/, "")).join("\n"));
  setRevealed(els.hintBtn, els.hint, false, "hint");
  els.solutionBtn.hidden = !p.has_solution;
  els.solution.replaceChildren();
  setRevealed(els.solutionBtn, els.solution, false, "solution");

  const siblings = topic.problems;
  const prev = siblings[p.index - 1], next = siblings[p.index + 1];
  els.prevBtn.hidden = !prev;
  els.nextBtn.hidden = !next;
  if (prev) { els.prevBtn.textContent = "Previous problem"; els.prevBtn.title = state.problems[prev].title; els.prevBtn.onclick = () => open({ kind: "problem", name: prev }); }
  if (next) { els.nextBtn.textContent = `Next: ${state.problems[next].title}`; els.nextBtn.onclick = () => open({ kind: "problem", name: next }); }

  const example = p.statement.split("\n").map((l) => l.trim()).find((l) => l.startsWith(p.name + "(") && l.includes("->"));
  const sample = example ? example.split("->")[0].trim()
    : p.starter.includes("build_list") ? `${p.name}(build_list([1, 2, 3]))`
    : p.starter.includes("build_tree") ? `${p.name}(build_tree([2, 1, 3]))`
    : `${p.name}(...)`;
  els.custom.placeholder = `e.g. ${sample}`;
  els.problemPanel.scrollTop = 0;
}

// Hint and solution stay folded until asked for: trying without them is the point.
function setRevealed(button, panel, show, noun) {
  panel.hidden = !show;
  button.textContent = `${show ? "Hide" : "Show"} ${noun}`;
  button.setAttribute("aria-expanded", String(show));
}

els.hintBtn.addEventListener("click", () => setRevealed(els.hintBtn, els.hint, els.hint.hidden, "hint"));

async function toggleSolution(show = els.solution.hidden) {
  setRevealed(els.solutionBtn, els.solution, show, "solution");   // visible first: CodeMirror can't measure a hidden box
  if (!show) return;
  if (!els.solution.childElementCount) {
    const { code } = await api(`/api/solution?name=${encodeURIComponent(state.problem.name)}`);
    if (window.CodeMirror) {
      CodeMirror(els.solution, { value: code.trimEnd(), mode: "python", readOnly: true, lineNumbers: false, viewportMargin: Infinity });
    } else {
      els.solution.append(h("pre", { class: "printed" }, code));
    }
  }
  els.solution.querySelector(".CodeMirror")?.CodeMirror.refresh();
  els.solution.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

els.solutionBtn.addEventListener("click", () => toggleSolution());

function setCustomOpen(open) {
  els.customWrap.hidden = !open;
  els.customToggle.setAttribute("aria-expanded", String(open));
  if (!open) els.custom.value = "";
}

els.customToggle.addEventListener("click", () => {
  const open = els.customWrap.hidden;
  setCustomOpen(open);
  if (open) els.custom.focus();
});

// ── running ─────────────────────────────────────────────────────────────────

async function run() {
  if (state.running || !state.view) return;
  state.running = true;
  els.runBtn.disabled = true;
  clearTimeout(state.saveTimer);
  state.saveTimer = null;
  els.results.replaceChildren(h("p", { class: "running" }, "Starting a fresh container…"));
  const { kind, name, id } = state.view;
  const before = solvedCount();
  try {
    const reply = await api("/api/run", { kind, name, id, code: editor.getValue(), custom: els.custom.value });
    if (reply.docker_error) {
      state.docker = reply.docker;
      renderDocker();
      if (state.docker.state !== "ready") refreshState().catch(() => {});
      els.results.replaceChildren(h("p", { class: "note" }, reply.docker_error));
    } else if (kind === "problem") {
      els.saveState.textContent = "Saved";
      state.progress = reply.progress || state.progress;
      renderProblemResult(reply);
      renderNav();
      const after = solvedCount();
      renderTally(after > before ? after - 1 : -1);
    } else {
      if (kind === "scratch") els.saveState.textContent = "Saved";
      renderScriptResult(reply);
    }
  } catch (err) {
    els.results.replaceChildren(h("p", { class: "note" },
      `Couldn't reach the playground server (${err.message}). Is server.py still running?`));
  } finally {
    state.running = false;
    els.runBtn.disabled = false;
  }
}

function containerNote(reply) {
  return h("span", { class: "container-note", title: `Container ${reply.container}` }, `Fresh container, ${reply.seconds}s`);
}

function renderProblemResult(reply) {
  const out = [];
  if (reply.crash) {
    out.push(h("div", { class: "summary" }, h("strong", { class: "some" }, "The container stopped before finishing"), containerNote(reply)));
    out.push(h("pre", { class: "trace" }, reply.crash));
    return els.results.replaceChildren(...out);
  }
  const r = reply.report;
  if (r.load_error) {
    out.push(h("div", { class: "summary" }, h("strong", { class: "some" }, "Your code didn't run"), containerNote(reply)));
    out.push(h("pre", { class: "trace" }, r.load_error));
    if (r.load_output) out.push(h("pre", { class: "printed" }, r.load_output));
    markErrorLine(r.load_error, "solution.py");
    return els.results.replaceChildren(...out);
  }

  const tests = r.tests;
  const passed = tests.filter((t) => t.status === "pass").length;
  const allTodo = tests.length && tests.every((t) => t.status === "todo");
  let headline;
  if (allTodo) headline = h("strong", { class: "todo" }, "Not started yet");
  else if (passed === tests.length) headline = h("strong", { class: "all" }, `All ${tests.length} tests passed`);
  else headline = h("strong", { class: "some" }, `${passed} of ${tests.length} tests passed`);
  out.push(h("div", { class: "summary" }, headline, containerNote(reply)));

  if (r.custom) {
    const c = r.custom;
    out.push(h("div", { class: "custom-result" },
      c.expr, h("span", { class: "arrow" }, "  returned  "),
      c.error ? h("span", { style: "color: var(--rose)" }, "an error") : c.value,
      c.error ? h("pre", { class: "trace" }, c.error) : null,
      c.output ? h("pre", { class: "printed" }, c.output) : null));
    if (c.error) markErrorLine(c.error, "solution.py");
  }

  if (r.load_output) out.push(h("pre", { class: "printed" }, r.load_output));

  if (allTodo) {
    out.push(h("p", { class: "note" }, "Your function still raises ", h("code", {}, "NotImplementedError"),
      ". Replace that line with your solution and run again."));
    return els.results.replaceChildren(...out);
  }

  const marks = { pass: "check", fail: "cross", error: "cross", timeout: "cross", todo: "dash", skipped: "dash" };
  const labels = { pass: "passed", fail: "failed", error: "error", timeout: "timed out", todo: "not started", skipped: "skipped" };
  const failing = [], passing = [];
  for (const t of tests) {
    const block = h("div", { class: `test ${t.status}` },
      h("div", { class: "test-line" },
        icon(marks[t.status] || "dash"),
        h("span", { class: "sr-only" }, labels[t.status]),
        h("span", { class: "call" }, t.call)));
    if (t.status === "fail") {
      block.append(h("dl", { class: "detail" },
        h("dt", {}, "expected"), h("dd", {}, t.expected),
        h("dt", {}, "got"), h("dd", { class: "bad" }, t.got)));
    } else if (t.status === "error" || t.status === "timeout") {
      block.append(h("pre", { class: "trace" }, t.error));
      markErrorLine(t.error, "solution.py");
    } else if (t.status === "todo") {
      block.append(h("pre", { class: "printed" }, "raised NotImplementedError"));
    } else if (t.status === "skipped") {
      block.append(h("pre", { class: "printed" }, "Skipped: two tests already timed out."));
    }
    if (t.output) block.append(h("pre", { class: "printed" }, t.output));
    (t.status === "pass" && !t.output ? passing : failing).push(block);
  }

  // Problems first, in full. Tests that passed quietly fold into one line.
  out.push(h("div", {}, failing));
  if (passing.length) {
    const label = passed === tests.length ? `Show all ${passing.length} tests` : `${passing.length} passed`;
    out.push(h("details", { class: "passed-group" }, h("summary", {}, icon("chevron", "chevron"), label), h("div", {}, passing)));
  }

  if (passed === tests.length) {
    const step = nextStep(state.view) || nextStep();
    out.push(h("div", { class: "next-step" },
      step ? h("button", { class: "btn primary", onclick: () => open(step) }, `Next: ${viewLabel(step)}`) : null,
      state.problem?.has_solution ? h("button", { class: "btn ghost", onclick: () => toggleSolution(true) }, "Compare with the solution") : null));
  }
  els.results.replaceChildren(...out);
}

function renderScriptResult(reply) {
  const ok = reply.exit_code === 0 && !reply.killed;
  const headline = reply.killed ? "Stopped" : ok ? "Finished" : "Finished with an error";
  const out = [h("div", { class: "summary" }, h("strong", { class: ok ? "all" : "some" }, headline), containerNote(reply))];
  if (reply.killed) out.push(h("pre", { class: "trace" }, reply.killed));
  out.push(h("pre", { class: "terminal" }, reply.output || "(nothing printed)"));
  if (!ok) markErrorLine(reply.output, "main.py");
  if (state.view.kind === "lesson") {
    const topic = state.topics[state.view.topic];
    const first = topic.problems.find((n) => problemStatus(n) !== "solved") || topic.problems[0];
    if (first) {
      out.push(h("div", { class: "next-step" },
        h("button", { class: "btn primary", onclick: () => open({ kind: "problem", name: first }) }, `Practise: ${state.problems[first].title}`)));
    }
  }
  els.results.replaceChildren(...out);
}

// ── reset ───────────────────────────────────────────────────────────────────

const resetLabels = { problem: "Reset code", scratch: "Reset scratchpad", example: "Restore original", lesson: "Restore original" };
let resetArmed = null;
els.resetBtn.addEventListener("click", async () => {
  if (!resetArmed) {
    els.resetBtn.textContent = "Click again to confirm";
    resetArmed = setTimeout(() => { els.resetBtn.textContent = resetLabels[state.view.kind]; resetArmed = null; }, 3000);
    return;
  }
  clearTimeout(resetArmed);
  resetArmed = null;
  const { kind, name, id, topic } = state.view;
  clearTimeout(state.saveTimer);
  state.saveTimer = null;
  let code;
  if (kind === "example") code = (await api(`/api/example?id=${encodeURIComponent(id)}`)).code;
  else if (kind === "lesson") code = (await api(`/api/lesson?topic=${encodeURIComponent(topic)}`)).code;
  else code = (await api("/api/reset", { kind, name })).code;
  state.loading = true;
  editor.setValue(code);
  state.loading = false;
  clearErrorLine();
  els.resetBtn.textContent = resetLabels[kind];
  els.saveState.textContent = saveable() ? "Reset" : "";
  editor.focus();
});

// ── controls, shortcuts, splitter ───────────────────────────────────────────

els.runBtn.addEventListener("click", run);
els.custom.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); run(); } });
document.addEventListener("keydown", (e) => {
  const mod = e.ctrlKey || e.metaKey;
  if (mod && e.key === "Enter") { e.preventDefault(); run(); }
  if (mod && e.key.toLowerCase() === "s") { e.preventDefault(); saveNow(); }
});

(function splitter() {
  const saved = Number(store.get("dsa:results-h"));
  if (saved > 40) document.documentElement.style.setProperty("--results-h", `${saved}px`);
  const setHeight = (px) => {
    const max = els.bench.getBoundingClientRect().height - 180;
    const value = Math.max(60, Math.min(max, px));
    document.documentElement.style.setProperty("--results-h", `${value}px`);
    store.set("dsa:results-h", String(Math.round(value)));
    editor.refresh();
  };
  els.splitter.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    els.splitter.setPointerCapture(e.pointerId);
    els.splitter.classList.add("dragging");
    const move = (ev) => setHeight(els.bench.getBoundingClientRect().bottom - ev.clientY);
    const up = () => {
      els.splitter.classList.remove("dragging");
      els.splitter.removeEventListener("pointermove", move);
      els.splitter.removeEventListener("pointerup", up);
    };
    els.splitter.addEventListener("pointermove", move);
    els.splitter.addEventListener("pointerup", up);
  });
  els.splitter.addEventListener("keydown", (e) => {
    const current = els.results.getBoundingClientRect().height;
    if (e.key === "ArrowUp") { e.preventDefault(); setHeight(current + 24); }
    if (e.key === "ArrowDown") { e.preventDefault(); setHeight(current - 24); }
  });
})();

window.addEventListener("beforeunload", () => {
  if (state.saveTimer && saveable()) {
    const { kind, name } = state.view;
    navigator.sendBeacon("/api/save", new Blob([JSON.stringify({ kind, name, code: editor.getValue() })], { type: "application/json" }));
  }
});

window.addEventListener("hashchange", () => {
  const view = viewFromHash(location.hash);
  if (view && !sameView(view, state.view)) open(view);
});

// ── start ───────────────────────────────────────────────────────────────────

function viewFromHash(hash) {
  const [kind, ...rest] = hash.replace(/^#/, "").split("/");
  const value = rest.join("/");
  if (kind === "problem" && state.problems[value]) return { kind, name: value };
  if (kind === "lesson" && state.topics[value]) return { kind, topic: value };
  if (kind === "example" && state.examples.some((e) => e.id === value)) return { kind, id: value };
  if (kind === "scratch") return { kind };
  return null;
}

(async function start() {
  try {
    await refreshState({ full: true });
  } catch {
    els.results.replaceChildren(h("p", { class: "note" }, "Couldn't reach the playground server. Start it with: python server.py"));
    return;
  }
  renderTally();
  const view = viewFromHash(location.hash) || viewFromHash(store.get("dsa:view") || "")
    || nextStep() || { kind: "scratch" };
  await open(view, { focus: false });
})();
