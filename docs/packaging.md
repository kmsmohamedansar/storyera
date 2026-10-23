# Packaging boundaries

Distribute the complete `skills/storyera/` folder: instructions, bundled MIT license, references, and optional Codex metadata. Copying only `SKILL.md` breaks its reference links.

This repository has no MCP server, model API integration, persistent canon database, hosted UI, marketplace listing or background task. A plugin manifest is omitted until a specific host's packaging workflow is implemented and verified.

Run `python3 scripts/build_skill.py --output /tmp/storyera.zip` for a deterministic folder ZIP rooted at `storyera/`. It excludes novel excerpts, answer keys, general docs and development tools. This archive is not a promise that every host accepts ZIP uploads.

`scripts/render_docs.py` regenerates original SVG and PNG diagrams using Pillow and local fonts. These are explanatory illustrations, not screenshots or an invented app. Rendering is optional, not a skill or grader dependency.

For future plugin distribution, consult the then-current [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins). Do not advertise a marketplace installation before submission and acceptance.
