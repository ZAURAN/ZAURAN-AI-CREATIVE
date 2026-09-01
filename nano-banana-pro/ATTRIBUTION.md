# Attribution — vendored `awesome-nanobanana-pro`

## Source

- Repository: https://github.com/ZeroLu/awesome-nanobanana-pro
- Owner: ZeroLu
- Licence: MIT — full text in `LICENSE`, kept unchanged.
- Vendored into `zauran-ai-creative` on 2026-09-01.

## What is here

- `AWESOME-NBP.md` — the upstream `README.md`, copied verbatim. 70 community prompt recipes across 10 categories, each with a title, a one-line description, sample images, the prompt body, and a link to the original creator.
- `recipes.json` — a derived index built by parsing `AWESOME-NBP.md`. One record per recipe: `id`, `category`, `title`, `description`, `promptFormat` (`json` or `text`), the verbatim `prompt`, `source` (creator label plus URL), and `images`. Nothing is rewritten or summarised — the index exists so the 102 KB Markdown file never has to be loaded into context.
- Read it through `scripts/search-nbp-recipes.mjs`; routing and usage rules are in `../references/nano-banana-pro.md`.

## What was not copied

- `assets/*.webp` and `assets/*.png` — sponsor banners (Cyberbara, Doloffer). They are advertising, not knowledge, so the two relative `./assets/...` image links inside `AWESOME-NBP.md` do not resolve. Deliberate.
- `.github/workflows/update-readme-timestamp.yml` — upstream CI.

## Sponsored content warning

`AWESOME-NBP.md` opens with paid sponsor blocks (APIMart, Cyberbara, Doloffer) and closes with a Star History widget. These are advertisements carried by the upstream repository, not vetted recommendations. Never surface them to the user as advice.

## Standing inside `zauran-ai-creative`

This is a **prompt-donor library, not a platform contract.** It carries no parameters, size limits, pricing, or API facts, and it cannot override the Nano Banana Pro model contract (the Obsidian note `02 · Nano Banana Pro (Gemini 3 Pro Image).md`), the approved `BRIEF LOCK`, or the skill's own rules on reference roles, on-image text and QA. Its wording is verified on Nano Banana Pro only — it does not transfer to GPT Image or Seedream 5.0, which keep their own platform files.

Every recipe keeps its creator credit in `source`. Carry that credit when a recipe is reused in a noticeable way.
