---
name: slide-deck-pro
description: >
  Turn a real, working flow in the user's app (onboarding, checkout, an admin
  workflow, any multi-screen process) into a print-ready 16:9 slide deck: a
  self-contained HTML file with a cover, section dividers, and one slide per
  step, each backed by a real screenshot captured by actually driving the
  app. Exports cleanly to PDF via the browser's print dialog. Use when the
  user asks for a "slide deck", "presentation", "walkthrough deck",
  "PowerPoint", or "deck" documenting how something in their product works —
  not for content-free marketing decks with nothing to screenshot.
---

# Process → Slide Deck

You're building one self-contained `.html` file: 16:9 slides (cover, agenda,
one or more part-dividers each followed by content slides, an optional
reference/glossary slide, closing), every content slide backed by a real
screenshot of the actual app. Fonts, logo, and screenshots are all embedded
as base64 so the file works offline and travels as a single artifact.
Printing it (`Cmd/Ctrl+P` → Save as PDF) produces one PDF page per slide at
the exact 16:9 size.

Start from `assets/deck-template.html` in this skill folder — it's a working
9-slide skeleton demonstrating every layout pattern you'll need (cover,
agenda, divider, content-split, content-frame-only, content-two-frame,
reference table, closing), with `[bracketed placeholders]` for content and
`__TOKEN__` placeholders for embedded assets. Copy it into the target
project rather than building from scratch.

**Neither the slide count/structure nor the visual design is fixed.** The
template is one worked example, not a mold. The real flow you're
documenting decides how many parts and steps there are — could be 6 slides,
could be 40; some flows have one divider, some have none. The target
project's own brand — colors, fonts, logo, cover treatment — decides what
it looks like, not the template's default green-on-navy palette. Every deck
built with this skill should look and be shaped differently, because every
app and every flow is different. Add, remove, and reorder slide blocks
freely; swap every color token; the only parts worth keeping intact by
default are the print/sizing/footer CSS mechanics in Step 4, because those
are the parts that are easy to get subtly wrong.

## Before you build — ask, don't assume

1. **Which flow, exactly.** Get the ordered list of screens/steps in the
   user's own words and read it back before building anything. Don't infer
   the flow purely from route names in the codebase — confirm it.
2. **Who's the audience.** Technical teammates or non-technical
   stakeholders? This changes the language register later (see Step 5) and
   whether raw filenames/technical references belong anywhere in the deck.
3. **Real screenshots or illustrative only.** Strongly prefer real — ask
   whether a running/staging instance and test credentials exist. If part of
   the flow needs a human on the other end (approving a signup, reading a
   one-time code), say so up front and ask the user to handle that step when
   you get there.
4. **Deliverable scope.** Deck only, or also a written companion guide
   (markdown + a scrolling HTML version)? Keep this skill's output focused on
   the slide deck unless a companion guide is explicitly requested too.

## Step 1 — Understand the real flow

Explore the codebase for the actual routes/pages/components involved before
assuming a structure. Screen order, field names, and branching (e.g. a form
that reveals extra fields based on a choice) should come from the real app,
not a guess — note anything that surprises you relative to what the user
described, and flag it back to them.

## Step 2 — Capture real screenshots

Drive the app in an actual browser end to end — reuse whichever
browser-automation tool or skill is available in this environment rather
than describing screens from memory or fabricating them.

- For steps that need a human (approving a registration, reading an OTP or
  a confirmation email, clicking a link sent externally), pause and ask the
  user to do that part, then continue once they confirm.
- Strip dev-only chrome from screenshots. Most frameworks show a dev-mode
  badge or overlay — hide it (inject a small stylesheet or a
  `MutationObserver`) before capturing, and make sure the hide survives
  client-side navigation, not just the first page load.
- Save originals, then optimize before embedding (convert to WebP, cap max
  width around 1200px) — screenshots are almost always the majority of the
  final file's size, and un-optimized PNGs bloat it fast.

## Step 3 — Build from the template, not by hand

- Copy `assets/deck-template.html` into the target project as your source
  of truth. Duplicate its example slide blocks to match however many steps
  the real flow needs — the five content patterns it demonstrates (split,
  frame-only, two-frame, reference-table, plus cover/divider/closing) cover
  almost every layout a walkthrough needs.
- Write a small manifest (`{token: file path}`) mapping every `__TOKEN__`
  placeholder in your copy of the template to a real font/logo/screenshot
  file, then run `scripts/build_deck.py --template your-deck.html --manifest
  manifest.json --out slides.html` to produce the final self-contained file.
  The script fails loudly if a token is missing from the manifest or a
  placeholder is left unresolved — fix those before moving on.
- Keep editing the small template + manifest, never the large generated
  output file. See Gotchas below for what goes wrong if you don't.

## Step 4 — Slide mechanics already handled by the template

The template has these worked out; keep them intact when you adapt it:

- **Exact 16:9 sizing**: `--sw`/`--sh` CSS vars (1280×720 by default) matched
  by `@page { size: 1280px 720px; margin: 0; }` inside `@media print`. Change
  both together if you need a different pixel size.
- **Backgrounds that survive print**: `print-color-adjust: exact` (+
  `-webkit-` prefix, + unprefixed `color-adjust`) on `*` inside
  `@media print`. Without this, dark or colored slide backgrounds silently
  turn white in the exported PDF no matter what the browser's print dialog
  options say.
- **One slide per PDF page**: `.slide { page-break-after: always; }`, with
  `.slide:last-child` reset to `auto` so there's no trailing blank page.
- **Responsive on-screen scaling** via `zoom`, not `transform: scale()` —
  `zoom` shrinks the layout box itself so slides stack without extra
  whitespace; `transform` only scales visually and leaves the full-size box
  in the layout. `zoom` resets to `1` on `beforeprint` and recomputes on
  `afterprint`, since print always needs true size regardless of viewport.
- **Footer/pagination row**: every footer item has an explicit
  `grid-column`, because some slides (dividers) only show two of the three
  items. Keep this explicit on any new footer variant you add — see
  Gotchas for what breaks if you don't.

## Step 5 — Make it look like the product, not a generic deck

- Use the target project's real logo and brand colors if a design-system
  doc or existing brand assets exist — check before inventing a palette.
  Swap the template's `--ink`/`--accent`/`--alt` tokens for the real ones.
- A generic decorative icon (a circle, a crosshair, an abstract mark) reads
  as filler. If the cover wants a background watermark, use a large, faded
  rendering of the actual logo instead (the template's commented-out
  `.cover-crest` does this) — it reads as intentional rather than generic.
- When layering a background color under an element that already has a
  `background-image` (e.g. a light/dark variant of the logo mark), set
  `background-color`, not the `background` shorthand — the shorthand resets
  `background-image` to `none` on anything it touches, silently deleting
  the logo.
- If the same asset (logo, a font) is referenced in more than one CSS rule,
  hoist it into one custom property (`--logo-brand: url(data:...)`) and
  reference the variable everywhere, rather than repeating the base64
  string — repeating it multiplies file size by however many times it's used.

## Step 6 — Write like a person explaining it, not a system describing itself

This is the single most common round of feedback you'll get on a first
draft. Concretely:

- Prefer full sentences with an imperative verb ("Go to Settings, then
  click Edit Profile") over breadcrumb notation ("Settings → Edit Profile").
  The arrow shorthand reads like a flowchart, not like someone talking to you.
- Don't narrate the software's own behavior in the abstract ("no fixed
  turnaround is shown in-app") — say what the reader should do or expect
  ("there's no fixed timeline for this — if it's taking a while, reach out
  directly rather than resubmitting").
- Don't expose environment/deployment details the reader doesn't need.
  "In production, that's X" tells a reader that dev/staging/prod exist as a
  concept, which is true but irrelevant to them — just state the fact plainly.
- Don't leave placeholder-shaped text in shipped copy — a literal
  `{Variable}` or a bare `N` reads as an unfinished template. Swap in a
  natural example value instead.
- Only name a companion document if it will actually reach this audience.
  If it won't, describe it in plain words ("the full guide") instead of
  pointing at a filename that won't exist for them — and match the whole
  deck's register to the audience from the clarifying questions: no raw
  filenames or code-styled text for a non-technical audience.
- Do one dedicated read-through at the end just for tone, separate from a
  content-accuracy pass — it catches a different class of problem.

## Step 7 — Verify before calling it done

Never report "done" without proving it:

- Load the actual file in a browser and screenshot a handful of
  representative slides (a divider, a content slide, the closing slide).
- Export a real PDF (e.g. Playwright: `page.pdf({ printBackground: true,
  preferCSSPageSize: true })`) and confirm: page count matches slide count,
  page size matches (CSS px ÷ 96 × 72 = PDF points — 1280×720px → 960×540pt,
  i.e. 13.333"×7.5", the standard PowerPoint 16:9 size), and any dark or
  colored backgrounds actually survived into the PDF.
- Clean up afterward: kill any local preview server you started, delete
  scratch screenshots and browser-automation output folders, and leave the
  repo's `git status` no messier than you found it.

## Gotchas

- **Never rebuild from the template without checking for direct edits
  first.** If the user (or their editor) has touched the generated output
  file directly since your last build, regenerating from the template will
  silently discard those edits. `git diff`/`git status` the output file
  before every rebuild; if it's dirty in a way the template doesn't explain,
  fold that drift into the template before regenerating.
- **IDE auto-formatters can reformat the big file's whitespace** between
  your edits, which breaks exact-string find/replace against it. Prefer
  always regenerating the full file from the small template over patching
  the large generated file directly.
- **CSS grid auto-placement is not "skip the empty slot."** A shared layout
  row with an optional middle item (like the footer) needs every item's
  `grid-column` set explicitly, or content shifts on exactly the slides
  where the middle item is missing — which is easy to miss because most
  slides look fine and only a few are subtly off.
- **`background: <color>` is a shorthand that resets `background-image`**
  on anything it's applied to with equal-or-higher specificity — use
  `background-color` if the intent is only to tint on top of an existing
  image.
- **Real screenshots beat mockups every time.** Reality routinely
  contradicts assumptions made from reading code alone — a "manual" step
  turns out to be automatic, a notification goes out by SMS as well as
  email, an empty state shows different copy than expected. Run the actual
  flow and correct the deck against what you see, not the other way around.
- **Don't let scratch verification artifacts (screenshots, PDFs, temp
  servers) leak into the target repo.** Use a scratchpad/temp directory for
  anything you generate purely to check your own work.
