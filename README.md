# slide-deck-pro

An [Agent Skill](https://agentskills.io) that turns a real, working flow in
your app — onboarding, checkout, an admin workflow, any multi-screen process
— into a print-ready 16:9 slide deck: a self-contained HTML file with a
cover, section dividers, and one slide per step, each backed by a real
screenshot captured by actually driving your app. Exports cleanly to PDF via
the browser's print dialog.

Works in Claude Code, Cursor, Codex, and any other agent that supports the
Agent Skills spec.

## Install

    npx skills add Kuameh/slide-deck-pro --skill slide-deck-pro

## Use

Ask your agent for a "slide deck" or "walkthrough deck" of a flow in your
product. The skill will:

1. Ask what flow to document, who it's for, and whether to use real screenshots.
2. Explore your codebase for the real routes/screens involved.
3. Drive your app in a browser and capture real screenshots.
4. Build a self-contained 16:9 HTML deck from the included template.
5. Verify the PDF export actually works before calling it done.

Neither the slide count nor the visual design is fixed to what's in
`assets/deck-template.html` — that's a worked example to adapt, not a mold.
Your actual flow decides the structure; your actual brand decides the look.

See [SKILL.md](./SKILL.md) for the full process, plus the included
`assets/deck-template.html` (a working 9-slide skeleton) and
`scripts/build_deck.py` (the asset-embedding build script) you can also use
directly.

[![skills.sh](https://skills.sh/b/Kuameh/slide-deck-pro)](https://skills.sh/Kuameh/slide-deck-pro)
