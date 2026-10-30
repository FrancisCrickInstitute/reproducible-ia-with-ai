# LLM-Assisted Bioimage Analysis: Worked Examples

An open guide of worked examples showing biologists how to use large language models (LLMs) for microscopy image analysis *reproducibly*. The core message: don't upload your images to a chat assistant and ask it to "analyse" them. Ask it to write a script instead, inspect the script, and run it yourself.

Built with [Quarto](https://quarto.org). The site is still under construction.

## Repository contents

- `index.qmd`, `principles.qmd`, `getting-started.qmd`, `resources.qmd`, `glossary.qmd`, `contributing.qmd` — the guide's supporting pages.
- `examples/` — one folder per worked example, each following the same template (`examples/_template.qmd`). Example 1 (`01-nuclear-cytoplasmic-ratio`) is fully written; examples 02–06 are stubs.
- `_quarto.yml` — the book configuration.

## Building locally

Requires a recent Quarto (the project was developed with 1.10.20). No code runs at build time, so no Python environment is needed to render the site.

```
quarto render      # outputs to _book/
quarto preview     # local preview in the browser
```

## Contributing

See `contributing.qmd` (or `CONTRIBUTING.md`) for how to propose and write a new example.

## Licence

- Text: CC-BY 4.0 (`LICENSE-CONTENT`). TODO: confirm with user.
- Code: MIT (`LICENSE`). TODO: confirm code licence with user (BSD-3 is the alternative).
