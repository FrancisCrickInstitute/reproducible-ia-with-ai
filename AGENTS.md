# AGENTS.md

## What this repo is

A **Quarto book** of worked examples teaching non-computational biologists to use LLMs for microscopy image analysis *reproducibly* (ask the LLM for a script; don't upload images to a chat). The site is still being built.

**`quarto-guide-build-plan.md` is the authoritative spec.** Read it before doing anything. It defines the target structure, page contents, the example template, acceptance criteria and open questions. This file only covers what the plan doesn't make obvious.

## Current state (as of writing)

- The book skeleton and all pages are written: `_quarto.yml`, the four supporting pages, `examples/_template.qmd`, Example 1 (full), and stubs 02–06. `quarto render` produces `_book/` with **no errors or warnings**.
- Example 1's script `examples/01-nuclear-cytoplasmic-ratio/nuc_cyto_ratio.py` is byte-identical to the gist (LF only, sha256 `e03bf977331ca91e440d16b2583e3655e8b396f1568ea76391bc33c0662f3286`). Regenerate it only with `python` (see below), never hand-edit.
- The article text was extracted from `AI_For_Image_Analysis.pdf` with `pypdf` to pull exact numbers/wording. The PDF is gitignored; don't commit it or its extracts.
- Example 1 images live in `images/` (user-provided): `003003-10.tif` (gitignored) plus `Overlay1.png`/`Overlay2.png`, copied into `examples/01-nuclear-cytoplasmic-ratio/outputs/` as `chat_run1_overlay.png`/`chat_run2_overlay.png`. `Overlay1` = chat run 1, `Overlay2` = chat run 2 (assumed in order). `Overlay3` (the script's overlay, i.e. `script_overlay.png`) and the composite image are still missing; `script_overlay.png` there is a **4px placeholder** and `results.csv` doesn't exist yet. The `images/` folder is not referenced by the build; the authoritative copies are the `.png` files under `examples/01-nuclear-cytoplasmic-ratio/outputs/`.
- The plan's Example 1 "tempting approach" prompt differs from the article: the article says "the **yellow protein**", but the user corrected it to "the protein in **channel 4**". Use the corrected wording in Example 1.
- Nothing new has been committed since the initial commit. Branch `main` (renamed from `master`), remote `origin` → `github.com/FrancisCrickInstitute/reproducible-ia-with-ai`.
- `AI_For_Image_Analysis.pdf` (repo root) is the **source article** ("AI for image analysis – reproducibility is key"), which plan section 3 lists as input #1. It is deliberately **gitignored**. Read it, but never commit it.

## Gotchas / mismatches between the plan and the repo

- **Quarto 1.10.20 is on PATH** (`quarto` works), installed at `H:\Users\davej\AppData\Local\Programs\Quarto\bin` (note the `H:` drive, not `C:`). If `quarto` is ever "not found", the shell probably started before the install updated PATH; call the full path `H:/Users/davej/AppData/Local/Programs/Quarto/bin/quarto.exe` instead. `quarto check` passes: Pandoc 3.10, Typst present, no TinyTeX (fine, since PDF output is out of scope), no R/Jupyter (fine, since execution is disabled).
- The agent shell is a minimal POSIX emulator: `grep`, `tr`, `tail`, `which` etc. are **not available** in bash, and `printf '---...'` silently writes the wrong content. Use the dedicated grep/glob/view/write tools instead. `python` (miniconda, 3.13) is on PATH for quick checks; open files with `encoding='utf8'` because the console is cp1252.
- The repo already has a **remote** (`origin` → `github.com/FrancisCrickInstitute/reproducible-ia-with-ai`) and the default branch is **`main`** (renamed from `master`). The plan says "never push"; still, the `master`-vs-`main` trigger mismatch bit once, so keep the workflow trigger as `main`.
- **Environment tooling conflict.** The repo uses **pixi** (`pixi.toml`, `win-64` only, conda-forge, Python `>=3.15.2,<3.16`, env name `reproducible`, no tasks defined yet). The plan, though, asks for a per-example conda `environment.yml` and Miniforge instructions for readers. Treat pixi as the *authoring* environment and `environment.yml` as the *reader-facing* artefact. Don't swap one for the other without asking.
- `pixi.lock` is marked `merge=binary -diff` in `.gitattributes`. Don't hand-edit it; regenerate it with `pixi install`/`pixi add`.
- Image ignores are lowercase patterns. They also catch `.TIF` etc. here only because Windows git is case-insensitive; on Linux/CI they wouldn't.
- `core.autocrlf=true` is set system-wide. The `*.py -text` rule in `.gitattributes` stops git converting line endings in scripts, which Example 1 needs (it must stay **byte-identical** to the gist). Still verify with a hash after saving it, because editor tools may write CRLF.

## Commands

| Purpose | Command |
|---|---|
| Install/refresh pixi env | `pixi install` |
| Run inside env | `pixi run <cmd>` / `pixi shell` |
| Check Quarto install | `quarto check` |
| Add Quarto extension (plan) | `quarto add quarto-ext/include-code-files --no-prompt` |
| Build site | `quarto render` (output to `_book/`) |
| Local preview | `quarto preview` (long-running; run it in the background) |

`--no-prompt` is there because `quarto add` otherwise asks for interactive confirmation. `check`, `--version`, `add` and `render` have all been run and the book builds cleanly.

- Download example 1's script verbatim (LF-only, no CRLF) with `python -c "import urllib.request;open('examples/01-nuclear-cytoplasmic-ratio/nuc_cyto_ratio.py','wb').write(urllib.request.urlopen('https://gist.githubusercontent.com/djpbarry/0ceaeb94a30aa955bdf23922311623cf/raw').read())"`, then verify sha256 == `e03bf977…2f3286`. Editing tools may rewrite line endings; re-check the hash after touching it.
- Extract text from the gitignored article PDF with `pypdf` (`from pypdf import PdfReader`), which is already installed in the miniconda Python on PATH.

## Hard rules (from the plan; these are the most common ways to fail)

- **No invented content.** No made-up results, citations, URLs, versions, dates or Fiji measurements. Every unknown becomes a visible `TODO` (`TODO: verify link`, `TODO: citation`, `TODO: user to perform`).
- **Verify every URL** before adding it.
- Example 1's script comes **verbatim** from the gist `djpbarry/0ceaeb94a30aa955bdf23922311623cf`. Never reformat or "improve" it. Its numbers and figures must match the article exactly.
- When describing what a script does, read the actual code. If something is unclear, flag it as a question rather than guessing.
- **No code runs at build time** (`execute: enabled: false`). Outputs (PNG overlays, CSVs) are pre-computed and committed. **Never commit raw image data.**
- Show scripts with the `include-code-files` filter, not pasted copies.
- **British English** throughout (analyse, colour, labelled, localisation).
- Audience has little or no programming experience. Explain jargon the first time it appears and don't assume CLI, conda or Git knowledge.
- Every example uses exactly the template sections in plan section 6, in that order. Stubs (02–06) fill in only "At a glance" and "The question", add the "Work in progress" callout, and leave `TODO` under every other heading.
- Prepare `.github/workflows/publish.yml`, but **never push, add a remote or enable Pages**.
- The publish workflow uses the **official GitHub Pages OIDC flow** (`actions/upload-pages-artifact` + `actions/deploy-pages`, uploading `_book/`), *not* `quarto publish gh-pages`. The latter fails in CI with "the remote origin does not have a branch named gh-pages" and needs `contents: write`; the OIDC flow needs no `gh-pages` branch and Pages must be set to source **"GitHub Actions"**. The default branch is **`main`** (renamed from `master`).
- Licensing: **CC BY-SA 4.0 for the whole repo** (text and code together, single licence). This replaces the plan's split; see plan section 2. Confirmed by the user 2026-10-30.

## Open questions to raise with the user

See plan section 11 (title/authors, script date and Python/Cellpose versions, dataset hosting and redistribution, whether to keep all five stubs, repo URL). The code-licence question is resolved: CC BY-SA 4.0 for the whole repo. The final report must list every remaining `TODO`, grouped into "needs user input" and "needs verification".
