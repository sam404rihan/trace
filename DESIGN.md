---
name: Trace
description: Learn data structures and algorithms one drawn step at a time; offline, calm, stage-coloured.
colors:
  ground: "#ffffff"
  panel: "#f8f8fb"
  sunk: "#f2f2f6"
  line: "#e8e8ef"
  line-strong: "#d6d6e0"
  ink: "#17161f"
  ink-muted: "#4f4d5c"
  ink-faint: "#6f6c7d"
  fill: "#f4f4f8"
  fill-strong: "#e9e9f0"
  ok: "#13803f"
  on-ok: "#ffffff"
  ok-soft: "#e4f6ea"
  bad: "#c4410c"
  bad-soft: "#fdeee7"
  warn: "#9a5b00"
  mark: "#ffd23f"
  mark-ink: "#2b2300"
  mark-soft: "#fff4c7"
  st1: "#3d5afe"
  st1-ink: "#2a3fc4"
  st1-soft: "#e8ecff"
  on-st1: "#ffffff"
  st1-text: "#2f47d6"
  st2: "#ffc22e"
  st2-ink: "#d99a00"
  st2-soft: "#fff4d6"
  on-st2: "#2a1f00"
  st2-text: "#8a5a00"
  st3: "#1fbf8f"
  st3-ink: "#12916b"
  st3-soft: "#dcf7ee"
  on-st3: "#03261b"
  st3-text: "#0b7353"
  st4: "#ff6a45"
  st4-ink: "#d9482a"
  st4-soft: "#ffe9e2"
  on-st4: "#2b0b02"
  st4-text: "#b8391b"
  st5: "#7c4dff"
  st5-ink: "#5a2fd6"
  st5-soft: "#efe8ff"
  on-st5: "#ffffff"
  st5-text: "#6a3fd6"
  st6: "#f0508a"
  st6-ink: "#cc2f68"
  st6-soft: "#ffe5ef"
  on-st6: "#2b0414"
  st6-text: "#b8245a"
  on-text: "#ffffff"
typography:
  display:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(34px, 4.6vw, 56px)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "40px"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "16.5px"
    fontWeight: 400
    lineHeight: 1.6
  body-ui:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Schibsted Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.4
  code:
    fontFamily: "IBM Plex Mono, Cascadia Mono, Consolas, monospace"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  code: "4px"
  nav: "8px"
  button-sm: "10px"
  button: "12px"
  stop: "14px"
  surface: "16px"
  hero: "28px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "12px"
  md: "16px"
  lg: "24px"
  xl: "28px"
  section: "48px"
components:
  button-primary:
    backgroundColor: "{colors.st1}"
    textColor: "{colors.on-st1}"
    rounded: "{rounded.button}"
    padding: "0 18px"
    height: "38px"
  button-default:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    padding: "0 18px"
    height: "38px"
  button-default-hover:
    backgroundColor: "{colors.fill-strong}"
  button-ghost:
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.button}"
    padding: "0 18px"
    height: "38px"
  button-small:
    rounded: "{rounded.button-sm}"
    padding: "0 13px"
    height: "32px"
  button-hero:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "0 26px"
    height: "54px"
  hero-card:
    backgroundColor: "{colors.st1}"
    textColor: "{colors.on-st1}"
    rounded: "{rounded.hero}"
    padding: "44px 44px 44px 52px"
  list-row:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "12px 16px"
  road-stop:
    backgroundColor: "{colors.fill}"
    textColor: "{colors.ink}"
    rounded: "{rounded.stop}"
    padding: "10px 14px 10px 10px"
  road-stop-here:
    backgroundColor: "{colors.st1}"
    textColor: "{colors.on-st1}"
  road-marker:
    backgroundColor: "{colors.st1}"
    textColor: "{colors.on-st1}"
    rounded: "{rounded.pill}"
    size: "52px"
  nav-link:
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.nav}"
    padding: "6px 10px"
  nav-link-current:
    backgroundColor: "{colors.st1-soft}"
    textColor: "{colors.st1-text}"
  badge:
    backgroundColor: "{colors.fill-strong}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.pill}"
    padding: "0 9px"
    height: "22px"
---

# Design System: Trace

## Overview

**Creative North Star: "The Drawn Next Step"**

Trace is a clean, bright study room with one coloured thing in it at a time. The ground is plain white (near-black in the dark rendition), the chrome is quiet greys, and colour arrives in whole regions: the home hero is a single slab of the current stage's colour holding a drawing of the topic's actual data structure and one Continue button. Everything else (the roadmap, the problem list, the study plans) is a calm step away, never on the same screen as the next step.

The course has six stages, and each stage owns one saturated colour. The page you are on takes its stage's colour (the router sets it on the body), so the accent, the primary button, the "you are here" stop and the current sidebar link all speak in that colour and change as you move through the course. The drawings are built in code from rounded, toy-like tiles with a darker under-edge, laid on the stage colour with a partner stage colour marking the part the eye should land on. Buttons share that tactile material: they sit on a darker edge and sink into it when pressed.

Density is low on home and the roadmap, comfortable on reading pages, and working-tool dense only in the problem workspace (editor, console, tests). The product is fully offline, so every face is vendored and nothing is fetched.

**Key Characteristics:**
- White (or near-black) ground; colour paints whole regions, not trims.
- Six stage colours, each a five-token family; the page wears its stage.
- Data structures drawn in code-built SVG, never raster illustrations.
- Generous rounding (12px buttons, 16px surfaces, 28px hero).
- A pressed bottom edge on pressables and on drawing tiles; flat everywhere else.
- One authored motion: the home drawing builds itself in.

## Colors

A neutral, slightly violet-cool grey system carries the interface; six saturated stage colours do all the talking, one at a time.

### Primary (the six stage colours)
Each stage owns a five-token family. `--stN` is the fill that paints regions (hero card, primary button, current roadmap stop and markers). `--stN-ink` is the darker pressed edge under that fill. `--stN-soft` is the tint for quiet "current" states (sidebar current link, soft badges, ahead-stage markers). `--on-stN` is text placed on the fill. `--stN-text` is the stage colour used as text or outline on the page ground.
- **Ultramarine** (st1): stage 1 (Foundations); also the default when a page has no stage. White text on the fill.
- **Sunflower** (st2): stage 2 (Core patterns). Dark text on the fill.
- **Mint** (st3): stage 3. Dark text on the fill.
- **Coral** (st4): stage 4. Dark text on the fill.
- **Electric Violet** (st5): stage 5. White text on the fill.
- **Bubblegum Pink** (st6): stage 6; also the colour of the "course finished" hero. Dark text on the fill.

Stage names come from the course data, not the stylesheet; the colour is bound to the stage's position (1 to 6).

### Secondary (state colours)
- **Pass Green** (ok): passing tests, solved items, done markers, the topic progress meter. Text on it uses on-ok.
- **Rust Fail** (bad): failing tests, wrong answers, error notices; always on bad-soft or as text.
- **Amber Caution** (warn): medium difficulty and reported-problem badges, the sandbox "busy" dot.

### Tertiary
- **Highlighter Yellow** (mark / mark-ink / mark-soft): the decision being made on a drill board (hot cells, picked nodes). It belongs to the drill boards, not to page chrome; the brand mark's underline is its only other use.

### Neutral
- **Paper White** (ground): page background, button face on the hero, drawing tile face.
- **Sidebar Mist** (panel): sidebar and console background.
- **Well** (sunk): inline code chips on boards, icon-button hover.
- **Hairline** (line) and **Firm Hairline** (line-strong): the only borders; top bar, sidebar edge, dividers, unfilled markers.
- **Ink** (ink), **Ink Muted** (ink-muted), **Ink Faint** (ink-faint): primary text, secondary text, captions and labels. Ink Faint still clears 4.5:1 on ground and panel.
- **Fill** and **Fill Strong** (fill, fill-strong): the resting and hover faces of rows, cards, chips and default buttons.

### Dark rendition
Every token has a dark value (in `web/app.css` under `prefers-color-scheme: dark` and `[data-theme="dark"]`; also recorded in the sidecar). Stage fills are deepened in dark, never lighter than their light-theme fill; `--stN-text` lifts to a pale tint so it reads on the near-black ground; `--on-text` flips to near-black.

### Named Rules
**The Stage Owns the Page Rule.** A page wears exactly one stage colour, the stage of the thing being viewed, set as `data-stage` on the body (or on a component such as the hero). `--accent` is that stage's `--stN-text`; never hard-code a stage hex in a component. Partner colours appear only inside drawings.

**The 4.5 Floor Rule.** Every text pair in the stage families clears 4.5:1 in both themes: on-stN on stN, stN-text on ground, stN-text on stN-soft, and on-text on stN-text. A new stage colour or new pairing is not added until it passes all four.

**The Deepen, Never Lighten Rule.** In dark, a stage fill is a darker, slightly less luminous version of its light self; contrast is gained by lightening the `-text` tint, never by brightening the fill.

## Typography

**Display Font:** Schibsted Grotesk (with Segoe UI, system-ui)
**Body Font:** Schibsted Grotesk (same family)
**Label/Mono Font:** IBM Plex Mono (with Cascadia Mono, Consolas), for code, numbers and indices only

**Character:** One friendly, slightly condensed grotesk carries everything from the 56px hero title to 11.5px sidebar group names, with weight doing the hierarchy work; Plex Mono marks anything that is data (code, topic numbers, progress fractions, drawing labels).

### Hierarchy
- **Display** (700, clamp(34px, 4.6vw, 56px), 1.02, -0.035em, balanced wrap): the topic name in the home hero only.
- **Headline** (700, 40px, 1.1, -0.03em): page titles (roadmap, topic). Drill 28px, walkthrough 32px, statement 23px are the same role scaled to the surface.
- **Title** (700, 22px, -0.02em): roadmap stage names. Rung titles use 600 at 17px. Size, not a heavier weight, separates the display from the headline and title.
- **Body** (400, 16.5px, 1.6): reading pages; long prose is 17px/1.65 capped at 72ch; ledes are 18.5px in ink-muted capped at 62ch. App chrome runs at 15px/1.55.
- **Label** (600, 14px, ink-faint, sentence case): section titles such as "The ladder"; 12.5px for fact headings and figure captions; 11.5px for sidebar groups. Never uppercase, never tracked out.
- **Code** (Plex Mono 13.5px/1.6 in the editor; 13 to 14px in blocks; 500 weight for numbers and indices).

### Named Rules
**The Vendored Faces Rule.** Only the two families in `web/vendor/fonts` may appear. Trace runs offline; a face that is not vendored is a face that falls back to Segoe UI.

**The Weight Ceiling Rule.** Ask only for weights a vendored face has: the grotesk 400 to 700, Plex Mono 400 to 600. The hero title, the hero button and roadmap stage names are 700; drawing labels and other mono data top out at 600. `strong` is pinned to 700 so `bolder` never asks for 900. Heavier type needs a vendored face declared at that weight, not a bigger number.

**The Mono Is Data Rule.** Plex Mono is for code and for numbers that are data (topic numbers, `2/12`, indices, drawing values). Prose and headings never set in mono.

## Layout

A fixed two-column shell: a 252px sidebar (panel, hairline right edge) and a content column with a 44px top bar holding the sidebar toggle and breadcrumbs. Under 900px the sidebar becomes a 280px overlay drawer.

Content is centred in a single measure per surface: home 1080px, reading pages 880px, roadmap 820px, walkthrough and starting check 760px, drills 1040px. The problem workspace is the exception: a resizable split (statement left, editor and console right) that stacks under 900px.

Home is one hero card, one line beneath it (topic progress meter left, "See the roadmap" right) and at most one quiet text link. The hero is a two-column grid (text 0.9fr, drawing 1.2fr); under 760px it stacks with the drawing first and the Continue button full-width.

Rhythm is loose and mostly multiples of 6 and 8 inside components (6px row gaps, 12 to 16px padding) and 24 to 48px between blocks (48px above section titles, 28px under the hero).

## Elevation & Depth

Trace is flat by default and conveys structure through tonal fills (fill on ground, panel for the sidebar) and hairlines. Depth appears in exactly two forms: the tactile pressed edge, and the floating overlays (command palette, mobile drawer) that genuinely sit above the page.

### Shadow Vocabulary
- **Pressed edge, default** (`box-shadow: 0 3px 0 var(--fill-2)`): default buttons.
- **Pressed edge, stage** (`box-shadow: 0 4px 0 var(--stage-ink)`): primary and run buttons; the current roadmap stop (a link).
- **Pressed edge, hero** (`box-shadow: 0 5px 0 var(--stage-ink)`): the hero Continue button.
- **Tile edge** (`filter: drop-shadow(0 3px 0 var(--stage-ink))`): every cell and node in a topic drawing.
- **Palette float** (`box-shadow: 0 24px 60px -20px rgba(0,0,0,0.35)`): the Ctrl K palette over a 28% dark scrim.
- **Drawer float** (`box-shadow: 8px 0 30px -12px rgba(0,0,0,0.3)`): the sidebar as a mobile overlay.

### Named Rules
**The Pressed Edge Rule.** The solid, unblurred bottom edge belongs to things you press (buttons, the current roadmap stop) and to the tiles of a drawing, which are the world's toy-block material. It never goes on containers: the hero card, fact panels, list rows, sheets, roadmap markers and badges stay flat. On press the element translates down by the edge height and the edge collapses to 0 (disabled under reduced motion).

## Shapes

Generously rounded, soft-cornered and toy-like, with no sharp corners in the chrome. Buttons 12px (10px small), the hero Continue 16px, surfaces and rows 16px, roadmap stops 14px with 11px number tiles, the hero 28px. Pills (999px) for badges, chips, the search field and drill tabs. Circles for roadmap stage markers (52px), rung dots and state dots. Inline code 4px. Drawing tiles round to min(9px, a quarter of the width). Borders are rare: hairlines separate regions; 1.5px rings mark selected or current states (`inset 0 0 0 1.5px var(--accent)`).

## Components

### Buttons
Chunky and tactile: a solid face on a darker under-edge that sinks when pressed.
- **Shape:** gently rounded (12px), 38px tall, 18px side padding, 600 weight 14px (700 for primary).
- **Primary:** stage fill with on-stage text over a 4px stage-ink edge. Hover brightens 5%; active drops 4px and the edge disappears.
- **Default:** fill face over a 3px fill-strong edge; hover moves to fill-strong.
- **Ghost:** no face, no edge, ink-muted text; hover gains a fill face.
- **Small:** 32px tall, 10px radius, 13px text.
- **Hero Continue:** the inversion on the stage slab: ground face with ink text, 54px tall, 16px radius, 18px/700, 5px stage-ink edge, 20px arrow icon; focus ring is a 3px on-stage outline offset 4px. Full width on narrow screens.
- **Focus:** every control shows a 2px accent outline offset 2px.

### Badges and Chips
- **Badge:** 22px pill, 12px/500. Difficulty uses state pairs (ok on ok-soft, warn on a 12% warn tint, bad on bad-soft); rung kinds use accent on accent-soft.
- **Chips:** pill links on fill (drill chips with progress pips), technique chips on fill-strong turning ok/ok-soft once known.

### Cards / Containers
- **Corner Style:** 16px.
- **Background:** fill on ground; ground inside a fill sheet. Never shadowed.
- **Border:** none; a 1.5px inset accent ring marks the current step.
- **Internal Padding:** 12 to 22px.

### Inputs / Fields
- **Search ("Go to anything"):** a 34px pill on ground with a 1px inset hairline, faint placeholder and a `Ctrl K` kbd; hover firms the hairline.
- **Custom test input:** 32px pill, line-strong border, mono 13px.

### Navigation
- **Sidebar:** panel background, brand at top, search pill, then Home and Roadmap with 16px stroke icons, then collapsible groups (11.5px/600 faint names) of 13.5px links with mono topic numbers and mono progress fractions. Links are 8px-rounded; hover fill-strong; current is accent on accent-soft at 500 weight.
- **Top bar:** 44px, hairline bottom, sidebar toggle and breadcrumbs (ink-muted links, 13px drawn chevron separators in ink-faint, ink current crumb).
- **Mobile:** the sidebar becomes a fixed overlay drawer.

### Hero Card (signature)
The whole home screen. A 28px-rounded slab in the stage fill with on-stage text: display-size topic name, then a 15px/600 stage line ("Stage 2 · Core patterns") below the title, the next item's title (19px/700) with its kind, and the Continue button; the topic drawing fills the other column (max 340px tall, 230px on mobile), cropped to its own bounding box.

### Topic Drawing (signature)
Thirty-four drawings, one per topic, composed in `web/art.js` from a small set of atoms (tile, node, line, arrow, curve, frame, wall, note). Tiles are ground-faced with the tile edge; `key` parts use stage-soft with stage-text labels; `hi` parts use a partner stage colour (stage 2 by default; stage 1 on stages 2 and 6; stage 5 on stage 4) with its on-colour label. Labels are Plex Mono 600 15px; notes are the grotesk at 12.5px/600 in on-stage. On home the drawing builds in part by part (0.6s, cubic-bezier(0.16, 1, 0.3, 1), 45ms stagger, 120ms lead-in), switched off under `prefers-reduced-motion`.

### Roadmap (signature)
Six stages as a vertical path: a 52px circular marker (stage fill when current or done, a check icon when done; stage-soft with stage-text when ahead) joined by a 4px rounded rail that takes the stage fill once done. The current stage opens to a list of 14px-rounded stops on fill with 36px number tiles; the "you are here" stop takes the stage fill, the stage-ink pressed edge and a "You're here" pill. Folded stages shrink to a row of numbered tiles so every topic stays one click away. Below the path, study plans, the contest and the review drill are stop-like rows on fill with a 36px ground tile holding a drawn mark and a one-line description.

### Topic and Plan Pages
The home hero at page scale. A lead card in the stage colour (a plan has no stage, so it wears stage 1) with the cropped drawing on one side (a plan draws its next problem's topic) and, on the other, the 40px title, the stage line below it, the next item (17.5px/700 with its kind) and one Continue button; it does not build in. Next on a topic page is where you stopped if that is in the topic, else the topic's next rung; a finished topic points to the next topic. Under the card: the progress meter line, then the idea and facts. The ladder is one summary row per rung (28px dot on a line-strong rail, title, sub, mono `2/5`, chevron) and only the rung holding the next step is open, that step ringed with the 1.5px accent. Techniques and the cheat sheet are fill folds below. Plan sections are hairline-separated rows with a meter; only the section holding the next problem is open. Every fold uses the same 18px chevron, pointing down while shut and up while open.

## Do's and Don'ts

### Do:
- **Do** take colour from the stage tokens (`--stage`, `--stage-ink`, `--stage-soft`, `--on-stage`, `--accent`) and let `data-stage` choose the stage.
- **Do** check any new text pair against 4.5:1 in both themes before shipping it.
- **Do** draw data structures in code-built SVG with the existing atoms, the stage colour as ground and one partner colour for the focal part.
- **Do** quieten drawing notes by weight (500 instead of 600), not by opacity.
- **Do** give anything pressable that carries a pressed edge a matching press-down on `:active`, and drop the transform under reduced motion.
- **Do** keep home to one hero, one progress line and one link; depth lives on the roadmap.
- **Do** use 16px stroked SVG icons (1.8px stroke, round caps) for interface icons.

### Don't:
- **Don't** put the pressed edge on containers: the hero card, rows, fact panels, sheets, roadmap markers or badges.
- **Don't** set opacity on text to make it quieter; it drops pairs below 4.5:1.
- **Don't** lighten a stage fill for dark mode; deepen the fill and lift the `-text` tint.
- **Don't** load fonts, icons or images from a network; everything is vendored for offline use.
- **Don't** place a small coloured label (eyebrow or kicker) above a heading; context such as the stage line goes below the title.
- **Don't** add a second authored animation; hover effects stay to colour and fill changes.
- **Don't** use raster or stock illustration where a drawing of the structure belongs.
