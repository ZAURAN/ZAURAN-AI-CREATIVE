# Attribution — vendored `seedance-20` package

## Source

- Repository: https://github.com/Emily2040/seedance-2.0
- Release: `6.7.0`
- Commit: `44b514992963a2570beee71aaf2a8720785f7ec2` (2026-08-06)
- Author: Iamemily2050 (@iamemily2050)
- Licence: MIT — full text in `LICENSE`, kept unchanged.
- Vendored into `zauran-ai-creative` on 2026-09-01.

## What was copied

`references/`, `skills/`, `examples/`, `schemas/`, `data/`, `evals/`, the root `SKILL.md` (as `ROOT.md`), `LICENSE`, `CHANGELOG.md`, and `scripts/extract_last_frame.py`.

## What was not copied

- `assets/` (19 MB of README images and fonts) — no reference in any routed Markdown file.
- `docs/` (release notes, frontend redesign notes, quickstart translations) — repository maintenance, not creative routing.
- `.github/`, `.gitattributes`, `.gitignore`, `agents/openai.yaml`, `requirements-*.lock`, `SECURITY.md`, `README.md`.
- All `scripts/*.py` except `extract_last_frame.py` — repository CI and validation tooling that assumes the upstream repo layout.

## Changes made during vendoring

1. Root `SKILL.md` → `ROOT.md`.
2. Every `skills/<name>/SKILL.md` → `skills/<name>/GUIDE.md`, so the host's skill discovery does not register 29 nested skills inside `zauran-ai-creative`.
3. Markdown link targets and path-style link labels updated to match the two renames. Prose mentions of `SKILL.md` that describe the Agent Skills file format (for example in `references/agent-compatibility.md`) were left untouched, because there they are statements about the format, not links.
4. No other content edits. All 361 relative Markdown links in this tree were verified to resolve.

## Precedence inside `zauran-ai-creative`

This package is a conditionally loaded knowledge source. It is subordinate to the skill's own platform contracts (`references/seedance-2.5.md`, `minimax-h3.md`, `gemini-omni-flash.md`, `gpt-image-2.md`, `seedream-5.md`), to `references/cinematic-orchestration.md`, and to the user's approved `BRIEF LOCK`. Its Seedance 2.0 durations, ceilings, resolutions, model IDs, pricing, and surface capabilities apply to the 2.0 line only and must never be restated for another model line. Routing and the exact boundary: `../references/seedance-2.0.md`.
