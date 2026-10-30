# AGENTS.md

## What this repo is

A **Quarto book** of worked examples teaching non-computational biologists to use LLMs for microscopy image analysis *reproducibly* (ask the LLM for a script; don't upload images to a chat). The site is still being built.

**`quarto-guide-build-plan.md` is the authoritative spec.** Read it before doing anything. It defines the target structure, page contents, the example template, acceptance criteria and open questions. This file only covers what the plan doesn't make obvious.

## Current state (as of writing)

- Tracked: `pixi.toml`, `.gitattributes`, `.gitignore`. Untracked: `pixi.lock`, `quarto-guide-build-plan.md`, `AGENTS.md`, `_extensions/`, `.idea/`. Nothing has been committed since the initial commit.
- Plan step 1 (repo setup) is done: plan ignores added to `.gitignore`, `*.py -text` added to `.gitattributes`, and `include-code-files` 1.0.0 installed in `_extensions/quarto-ext/include-code-files/`. No `_quarto.yml` or `.qmd` content exists yet. Single branch `master`, no remote.
- `AI_For_Image_Analysis.pdf` (repo root) is the **source article** ("AI for image analysis – reproducibility is key"), which plan section 3 lists as input #1. It is deliberately **gitignored**. Read it, but never commit it.

## Gotchas / mismatches between the plan and the repo

- **Quarto 1.10.20 is on PATH** (`quarto` works), installed at `H:\Users\davej\AppData\Local\Programs\Quarto\bin` (note the `H:` drive, not `C:`). If `quarto` is ever "not found", the shell probably started before the install updated PATH; call the full path `H:/Users/davej/AppData/Local/Programs/Quarto/bin/quarto.exe` instead. `quarto check` passes: Pandoc 3.10, Typst present, no TinyTeX (fine, since PDF output is out of scope), no R/Jupyter (fine, since execution is disabled).
- The agent shell is a minimal POSIX emulator: `grep`, `tr`, `tail`, `which` etc. are **not available** in bash, and `printf '---...'` silently writes the wrong content. Use the dedicated grep/glob/view/write tools instead. `python` (miniconda, 3.13) is on PATH for quick checks; open files with `encoding='utf8'` because the console is cp1252.
- **The repo already exists.** The plan's step 2 (`git init`, root folder named `llm-bioimage-examples/`) is out of date. Build the structure in the **current repo root** and don't re-init.
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

`--no-prompt` is there because `quarto add` otherwise asks for interactive confirmation. `check`, `--version` and `add` have been run. The filter was tested with a throwaway render: ` ```{.python include="file.py"} ` followed by an empty closing fence embeds the file. `render`/`preview` of the book itself haven't been run yet because there's no `_quarto.yml`.

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
- Licensing: CC-BY 4.0 for text, MIT for code, **pending user confirmation** (BSD-3 is the alternative).

## Open questions to raise with the user

See plan section 11 (title/authors, code licence, script date and Python/Cellpose versions, dataset hosting and redistribution, whether to keep all five stubs, repo URL). The final report must list every remaining `TODO`, grouped into "needs user input" and "needs verification".
