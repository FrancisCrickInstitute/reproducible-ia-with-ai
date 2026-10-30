# Build plan: worked-examples guide to LLM-assisted bioimage analysis (Quarto)

This document is a handover for an agent that will build the project locally. It assumes no knowledge of the conversation that produced it, so all relevant context is included below.

---

## 1. Context

### What this is

An open, freely available online guide of **worked examples** showing biologists how to use LLMs (ChatGPT, Claude, etc.) for microscopy image analysis **reproducibly**. The guide does not try to be a textbook. Each example shows a concrete task done the tempting way and the better way, and links out to existing resources for depth.

### Audience

Biologists who are **not very computationally literate**. They may never have run a Python script. Write plainly, gloss jargon on first use, and never assume familiarity with the command line, conda or Git.

### The core message (applies to every example)

1. Don't upload images to a chat assistant and ask it to "analyse" them. Results vary between runs, the method is hidden, and data protection is a concern.
2. Instead, ask the LLM to **write a script**, describing the images rather than uploading them. The script can be inspected, saved, shared and rerun by anyone, without an LLM.
3. **Reproducible is not the same as correct.** Always validate: look at the segmentation overlay first, then spot-check measurements (for example by hand in Fiji).
4. **Domain knowledge still matters.** Specific prompts need you to know what to ask for. Vague prompts let the LLM make key methodological decisions for you.

### Existing resources (link to them; don't duplicate them)

- *AI in Microscopy: A BioImaging Guide* (HHMI Janelia), https://bioimagingai.janelia.org/. Built with Quarto, source at https://github.com/aicjanelia/BioImagingAI. Still under construction. Its planned "Practical guide: getting started with LLMs for microscopy" section overlaps with this project, so content may later be contributed there. **Keeping our format Quarto-compatible is a deliberate choice for that reason.**
- *The Turing Way*, https://book.the-turing-way.org/, for general reproducible research practice.
- Pete Bankhead, *Analyzing Fluorescence Microscopy Images with ImageJ* (online textbook), for image analysis fundamentals.
- Robert Haase's material on LLMs for bioimage analysis: bia-bob (https://github.com/haesleinhuepf/bia-bob), the prompt engineering chapter of his Bio-image Analysis Notebooks, and his talks on Zenodo.
- Alan Turing Institute, "Using generative AI to write code: a guide for researchers" (Chalstrey & Grishina, 2024).
- Aalto University, *Generative AI in Research Work* (Glerean & Silva, draft), https://aaltodataagents.github.io/gen-ai-and-research-work/.
- The image.sc forum, https://forum.image.sc/, for help with specific problems.

**Verify every URL before including it.** Where a URL can't be confirmed, leave a `TODO: verify link` marker rather than guessing.

---

## 2. Decisions already made

| Decision | Detail |
|---|---|
| Format | **Quarto book** (`project: type: book`), HTML output first. PDF output is optional and not required for this phase. |
| Code execution | **No code runs at build time.** Scripts are standalone `.py` files shown on the page and downloadable. Outputs (overlay PNGs, CSVs) are pre-computed and committed. |
| Displaying scripts | Use the `include-code-files` Quarto extension (`quarto add quarto-ext/include-code-files`) so each page shows the real `.py` file rather than a pasted copy that can drift. |
| Image data | **Not committed to Git.** Sample images are referenced by DOI or stable URL (Zenodo, or the original dataset's repository). |
| Environments | Each example has its own `environment.yml` with **pinned versions**. |
| Provenance | Each example records the verbatim prompt, the model name and the date the script was generated. |
| Licensing | CC-BY 4.0 for text, MIT for code, and the original licence noted for each dataset. **Confirm the code licence with the user** (BSD-3 is the alternative). |
| Language | **British English** spelling throughout (analyse, favourite, colour, labelled). |
| Hosting | GitHub Pages via a GitHub Actions workflow. Prepare the workflow, but **do not push or publish anything**. This phase is local only. |

---

## 3. Inputs required from the user

The agent must not invent any of these. If an input is missing, stop and ask, or leave a clearly marked `TODO`.

1. **The source article** ("AI for image analysis – reproducibility is key"), as PDF or text. It is the basis of Example 1.
2. **The analysis script** from https://gist.github.com/djpbarry/0ceaeb94a30aa955bdf23922311623cf. Use it **verbatim**. Don't edit, "improve" or reformat it. If the gist can't be fetched, ask the user for the file.
3. **The figures from the article:**
   - the composite image of the cells
   - chat run 1 overlay and results table
   - chat run 2 overlay and results table
   - script overlay PNG and CSV output
4. **The sample image** (`003003-10.tif`), from Pascual-Vargas, P., et al. *Sci Data* 4, 170018 (2017). Locate the dataset through the paper's data availability statement, or ask the user. Record its DOI and licence. Don't download from unofficial mirrors.
5. **The versions of Python and Cellpose** the user ran the script with, for pinning the environment. If unknown, leave `TODO` placeholders.

---

## 4. Repository structure

```
llm-bioimage-examples/
├── _quarto.yml
├── index.qmd                     # Introduction
├── principles.qmd                # The four principles, expanded slightly
├── examples/
│   ├── _template.qmd             # Example template (not listed in the book)
│   ├── 01-nuclear-cytoplasmic-ratio/
│   │   ├── index.qmd
│   │   ├── nuc_cyto_ratio.py     # verbatim from gist
│   │   ├── environment.yml
│   │   ├── PROVENANCE.md
│   │   └── outputs/
│   │       ├── composite.png
│   │       ├── chat_run1_overlay.png
│   │       ├── chat_run2_overlay.png
│   │       ├── script_overlay.png
│   │       └── results.csv
│   ├── 02-counting-nuclei-batch/index.qmd
│   ├── 03-colocalisation/index.qmd
│   ├── 04-time-lapse-intensity/index.qmd
│   ├── 05-morphology-and-calibration/index.qmd
│   └── 06-fiji-macro/index.qmd
├── getting-started.qmd           # How to install conda and run a script, for complete beginners
├── resources.qmd                 # Further reading (section 1 list)
├── glossary.qmd
├── contributing.qmd
├── references.bib
├── _extensions/                  # include-code-files
├── .github/workflows/publish.yml # prepared, not triggered
├── .gitignore                    # ignore _book/, *.tif, *.tiff, *.czi, *.nd2, *.lif, .quarto/
├── LICENSE                       # MIT (code)
├── LICENSE-CONTENT               # CC-BY 4.0 (text)
├── CONTRIBUTING.md
└── README.md
```

### `_quarto.yml` sketch

```yaml
project:
  type: book
  output-dir: _book

book:
  title: "TODO: confirm title with user"   # working title: "LLM-Assisted Bioimage Analysis: Worked Examples"
  author: "TODO"
  repo-url: "TODO"
  repo-actions: [edit, issue]
  chapters:
    - index.qmd
    - principles.qmd
    - getting-started.qmd
    - part: "Worked examples"
      chapters:
        - examples/01-nuclear-cytoplasmic-ratio/index.qmd
        - examples/02-counting-nuclei-batch/index.qmd
        - examples/03-colocalisation/index.qmd
        - examples/04-time-lapse-intensity/index.qmd
        - examples/05-morphology-and-calibration/index.qmd
        - examples/06-fiji-macro/index.qmd
    - resources.qmd
  appendices:
    - glossary.qmd
    - contributing.qmd

bibliography: references.bib

filters:
  - include-code-files

format:
  html:
    theme: cosmo
    toc: true
    code-copy: true
    code-overflow: wrap

execute:
  enabled: false
```

---

## 5. Page contents

### 5.1 `index.qmd`: Introduction (keep it short, around 300–400 words)

- What the guide is: a set of worked examples, not a textbook.
- Who it's for: biologists with little or no programming experience.
- The problem: it's tempting to drop images into a chat window. One or two sentences on why that's a problem, linking to Example 1 as the demonstration.
- How the guide is organised: the principles, how to get started, then the examples, each following the same structure.
- How to use an example: read the naive approach, then the better approach, then try running the script yourself.
- Where to go for depth (link to `resources.qmd`).
- An open-source statement and an invitation to contribute.

### 5.2 `principles.qmd`

The four principles from section 1, each with a short paragraph. Reuse wording from the source article where possible. Add a callout noting that the advice applies whichever AI tool is used, and that specific model names in the examples will date quickly while the principles won't.

### 5.3 `getting-started.qmd`

A step-by-step guide for complete beginners:

1. Install Miniforge (conda).
2. Open a terminal (separate short instructions for Windows, macOS and Linux).
3. Create an environment from an example's `environment.yml`.
4. Activate it.
5. Run a script on an image.
6. Find the outputs.

Include a "what to do when it goes wrong" section: paste the error into an LLM, or ask on image.sc. Keep commands copyable. **Don't assume** prior knowledge of paths or directories; explain them briefly.

### 5.4 `glossary.qmd`

Plain-language definitions for: LLM, chat assistant, prompt, script, Python, environment (conda), segmentation, mask, Cellpose, overlay, CSV, mean intensity, nuclear:cytoplasmic ratio, reproducibility, validation, Fiji/ImageJ, macro, pixel size and calibration, bit depth, background subtraction.

### 5.5 `resources.qmd`

The list from section 1, grouped as:
- Fundamentals of image analysis
- Reproducible research
- AI and LLMs in research
- LLMs specifically for bioimage analysis
- Getting help

Give one line for each resource on what it's good for.

### 5.6 `contributing.qmd` and `CONTRIBUTING.md`

- How to propose a new example (open an issue first).
- Copy `_template.qmd`.
- Requirements for a new example: a pinned environment, a verbatim prompt with provenance, a validation section, publicly available sample data with a licence, and no images committed to the repository.
- Spelling and style conventions.

---

## 6. Example template (`examples/_template.qmd`)

Every example uses exactly these sections, in this order:

```markdown
---
title: "TODO: Example title"
---

::: {.callout-note}
## At a glance
- **Biological question:** TODO
- **Data:** TODO (link, DOI, licence)
- **Tools:** TODO (e.g. Python, Cellpose 3)
- **Difficulty:** Beginner / Intermediate
:::

## The question
What a biologist wants to know, in plain language, and why it matters.

## The tempting approach
What happens if you upload the image(s) and ask a vague question.
What varied or went wrong. Show the evidence (outputs, tables).

## Why that's a problem
Link the specific issues back to the principles page.

## A better approach: ask for a script
### The prompt
The verbatim prompt, in a block. Annotate *why* each part is there
(channels described, tool named, outputs specified, comments requested).

### The script
{include the .py file via include-code-files}
Link to download it.

### What the script does, in plain English
A numbered walkthrough of the steps. No code knowledge needed.

## Running it yourself
The environment file, commands, and expected runtime and hardware.
Link to getting-started.qmd.

## Results
The overlay image and results table.

## Checking the results
Overlay inspection, then a manual spot check, then a sanity check
against biological expectation. Note the method choices that
affect the result.

## What domain knowledge helped here
What you needed to know to write the good prompt or spot problems.

## Limitations and variations
What this script doesn't handle, and how you might adapt it.

## Provenance
Model, date, and verbatim prompt (or a link to PROVENANCE.md).

## Further reading
Links to relevant chapters in external resources.
```

---

## 7. Example 1: Nuclear-to-cytoplasmic ratio of YAP/TAZ (full content)

This is the expanded version of the source article. **Use the article's text and figures as the basis, and keep its numbers exactly as published.** Expand it as described below.

### Section-by-section plan

**At a glance.** TNBC LM2 cells. Four channels: Hoechst (nuclei), tubulin, actin (phalloidin), YAP/TAZ. Data from Pascual-Vargas et al. 2017. Python plus Cellpose 3.

**The question.** What fraction of YAP/TAZ is nuclear versus cytoplasmic? Add one or two sentences of biological context explaining why YAP/TAZ localisation is commonly measured (it's a readout of mechanical and Hippo pathway signalling). Keep it brief and add a citation, marking it `TODO: citation` if one can't be verified.

**The tempting approach.** Reproduce the article's demonstration:
- The vague prompt, verbatim: *"Can you tell me how much of the yellow protein in the attached image is in the nuclei relative to the cytoplasm?"*
- Chat run 1: overlay and table (share of signal in nucleus about 50%, concentration ratio about 7.2–7.4×, 13 and 23 cells).
- Chat run 2 (fresh chat, same prompt): overlay and table (47.9% nuclear, 6.4× brightness ratio).

Then add an **expanded discussion that the article lacked**:
- The numbers are close but not identical, and the two runs **chose different metrics**. Run 1 reported per-cell medians and a whole-image total; run 2 reported a whole-image total and a mean-intensity ratio. Run 1 also distinguished cells fully in frame from all cells.
- The segmentations differ visibly. Point to specific regions in the overlays, such as clustered cells at the top.
- The key lesson is that the vague prompt left the methodological decisions to the model, and those decisions changed silently between runs.

**Why that's a problem.** The article's three points (not reproducible, black box, no guarantee of future access to the model), plus data protection. Note that the model probably wrote and ran code in the background, but that code wasn't kept, so it can't be inspected or rerun.

**A better approach.** The specific prompt, verbatim from the article (with Hoechst). Annotate it:
- describing channels replaces uploading images, which also avoids the data protection issue
- naming Cellpose 3 is a methodological decision made by the user, not the model
- specifying output columns fixes the metric
- asking for comments and run instructions makes the script interpretable

Include the script via `include-code-files`.

**What the script does, in plain English.** **Read the actual script and describe what it really does.** Don't describe what it might plausibly do. In particular, document:
- which Cellpose model(s) are used for cells and for nuclei, and with what parameters (diameter, channels)
- how the cytoplasm is defined (for example, the cell mask minus the nuclear mask)
- whether any background subtraction is applied
- whether the ratio is calculated per cell then averaged, or from pooled pixels across the whole image
- how cells touching the image edge are handled

If any of these is unclear from the code, flag it as a question for the user instead of guessing.

**Running it yourself.** `environment.yml` with pinned versions (from the user, or `TODO`), the commands, and a note on GPU vs CPU runtime (`TODO` until measured).

**Results.** The overlay and CSV: nuclear mean 150.9266, cytoplasmic mean 28.31363, ratio 5.330529.

**Checking the results.** New material:
- **Step 1: inspect the overlay.** What to look for: merged cells, missed cells, nuclei outlined accurately. Point out any visible issues in the actual overlay.
- **Step 2: spot check in Fiji.** Give step-by-step instructions for measuring mean YAP/TAZ intensity in a nucleus and a cytoplasmic region for three to five cells. Present the comparison table as `TODO: user to perform` and **don't invent values**.
- **Step 3: why do the three approaches disagree?** Chat runs gave about 6.4–7.4×; the script gave 5.3×. Explain the plausible contributors (segmentation differences, metric definition, background handling, per-cell vs pooled), framed according to what the script analysis above found. Make it clear that disagreement isn't automatically error; it shows why the method must be explicit.
- A short note on background subtraction and why it affects ratios, at a conceptual level.

**What domain knowledge helped here.** Knowing:
- the channel order
- that Cellpose exists and suits this task
- the difference between total signal and concentration (mean intensity)
- that edge cells and background matter

This ties back to the article's closing section on why learning the fundamentals still matters.

**Limitations and variations.**
- A single image, so not a statistical analysis.
- Extending the script to a folder of images (link to Example 2).
- Reporting per-cell values instead of one image-level number.

**Provenance.** Model: Claude Opus 5.5. Date: `TODO` (ask the user). Include the prompt verbatim.

**Further reading.**
- Cellpose documentation (`TODO: verify link`)
- The Janelia book's segmentation chapter
- Bankhead's chapters on measurements and on background

---

## 8. Placeholder examples (stubs)

Create each stub from the template, with **only** the "At a glance" callout and "The question" section filled in. Add a prominent callout to each:

```markdown
::: {.callout-warning}
## Work in progress
This example is planned but not yet written. Contributions welcome. See [Contributing](../../contributing.qmd).
:::
```

Leave the remaining template headings in place, each containing just `TODO`.

| # | Title | Question / focus | Teaching point |
|---|---|---|---|
| 02 | Counting nuclei across many images | Count nuclei per field across a folder of images and summarise per condition. | Batch processing: uploading images one at a time doesn't scale. One script applies an identical method to every image. |
| 03 | Colocalisation of two proteins | Do two labelled proteins colocalise? | Pitfalls that LLMs won't flag unless asked: metric choice (Pearson vs Manders), thresholds, bleed-through, regions of interest. Demonstrates why vague prompts are dangerous here. |
| 04 | Intensity changes in a time-lapse | How does a reporter's intensity change over time in individual cells? | Tracking and photobleaching correction, and describing temporal data in a prompt. |
| 05 | Cell morphology and calibration | Measure cell area and shape in real units. | Pixel size and metadata. LLM-written scripts often silently report pixels instead of µm. Getting calibration from file metadata. |
| 06 | Writing a Fiji macro with an LLM | The same idea for point-and-click users: ask for an ImageJ macro instead of Python. | Reproducibility doesn't require Python. This is a gentler entry point for the target audience. |

The user said four or five placeholders; there are five here. **Ask the user whether to drop any** before finalising.

---

## 9. GitHub Actions workflow (prepare only)

Create `.github/workflows/publish.yml` using the official Quarto actions (`quarto-dev/quarto-actions/setup` and `quarto-dev/quarto-actions/publish` with `target: gh-pages`). Trigger on push to `main` and on `workflow_dispatch`. Since no code runs, no Python setup is needed in CI. **Do not push or enable Pages.**

Optional future phase (out of scope now): a separate workflow that creates each example's environment and runs its script on a small test image, to check scripts still run.

---

## 10. Build steps and acceptance criteria

### Steps

1. Check Quarto is installed (`quarto --version`). If it isn't, tell the user and stop rather than installing system software without asking.
2. Create the repository structure (section 4) and `git init`. Make no remote.
3. Add the `include-code-files` extension.
4. Write `_quarto.yml`, the template, and the supporting pages (sections 5 and 6).
5. Gather the inputs (section 3). Write Example 1 (section 7).
6. Create the stubs (section 8).
7. Write the README, licences, contributing files and `.gitignore`.
8. Prepare the workflow (section 9).
9. Run `quarto render`, then `quarto preview`, and check every page.
10. Report back to the user (see below).

### Acceptance criteria

- [ ] `quarto render` completes with **no errors or warnings**.
- [ ] All pages appear in the sidebar in the specified order.
- [ ] Example 1's script is **byte-identical** to the gist version.
- [ ] Example 1's figures and numbers match the source article exactly.
- [ ] **No invented content:** no fabricated results, citations, URLs, versions or dates. Every unknown is a visible `TODO`.
- [ ] No image data files (`.tif` and similar) are committed. Only PNG figures and small CSVs.
- [ ] All external links resolve, or are marked `TODO: verify link`.
- [ ] British English spelling throughout.
- [ ] The site is readable at phone width (check in the preview).

### Report back to the user with

- A summary of what was built.
- A list of every `TODO` remaining, grouped by "needs user input" and "needs verification".
- Open questions (section 11), plus any raised while reading the script.

---

## 11. Open questions for the user

1. The book's title and author list (individual names or "and contributors")?
2. The code licence: MIT or BSD-3?
3. The date the Example 1 script was generated, and the Python and Cellpose versions used?
4. The sample image: where is the original dataset hosted, and may it be redistributed (for example, a copy on Zenodo)?
5. Keep all five placeholder examples, or drop one?
6. Repository name and GitHub organisation (for `repo-url`, not needed until publishing)?
