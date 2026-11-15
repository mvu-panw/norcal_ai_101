# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A 30-minute "AI 101" talk on how a prompt travels from a laptop (Claude Code) to an AI factory (NVIDIA GB300 NVL72) and back. It holds a static companion site plus local reference material from NVIDIA's *AI Infrastructure and Operations Fundamentals* course.

**Public repo:** `github.com/mvu-panw/norcal_ai_101` (branch `main`). `.github/workflows/pages.yml` publishes only `site/` to GitHub Pages. One-time manual step: Settings → Pages → Source = "GitHub Actions". `.gitignore` keeps all reference folders (`NVIDIA Datasheets/`, `NVIDIA Stencils/`, `nvidia_course_content/`, `palo_docs/`, `reference_text/`) out of git: they are NVIDIA/PANW material that isn't ours to republish. Never commit them.

```bash
python3 -m http.server 8600 --directory site    # preview; no build step
python3 -I tools/scrape.py URL [URL ...]        # save an NVIDIA page as text to reference_text/nvidia_pages/ (skips existing files)
pdftotext -layout "NVIDIA Datasheets/X.pdf" reference_text/datasheets/X.txt
```

`reference_text/` holds greppable text of every datasheet plus scraped nvidia.com, developer.nvidia.com and docs.nvidia.com pages. Grep it before searching the web. `scrape.py` fetches with `curl` because the python.org Python on this Mac has no CA bundle.

## Site (`site/`)

- 6 pages: `index` (prompt-flow video, summary, demo prompt, AI basics), `basics` (AI ⊃ ML ⊃ DL ⊃ generative AI rings diagram, quick definitions, how a neural network learns, waves-of-AI timeline, Claude Code as generative + agentic mapped to NVIDIA's agent traits; content from `nvidia_course_content/notes` Units 2–3), `journey` (laptop → API → serving cluster, the tool-use agent loop, prompt caching), `nvl72` (four networks, path into the rack, rack diagram, prefill vs. decode), `glossary` (Key Terms: ~50 infrastructure terms in 7 sections, GPU and NVLink comparison tables, inline search script), `resources` (Anthropic + NVIDIA doc links).
- Glossary specs must come from `reference_text/`. Label sparse vs. dense FLOPS, and mark Rubin numbers as projections.
- **UI is copied from `~/lambda/site`** (itself from `~/ai_sec_by_design`): cyan/purple gradient, Inter font. `site/assets/css/styles.css` is the base template, then the lambda site's content classes (`.prose`, `.two-col`, `.link-card`…), then a block marked "AI 101 additions" (`.flow`, `.steps`, `pre.code`, `.stat-grid`, `.rack`, `.tokens`).
- No templating: nav and footer are copy-pasted into all 6 pages. Each page's `.nav-links` lists the *other* pages. Bump `styles.css?v=N` (currently 5) on every page after CSS edits.
- The NVL72 rack diagram in `nvl72.html` is 27 `.tray` divs (10 compute, 9 NVLink switch, 8 compute), simplified.
- **Accuracy rule:** Anthropic serves Claude on Google TPUs, AWS Trainium and NVIDIA GPUs, and which hardware serves a request isn't public. Always frame the NVL72 content as "how a prompt like this is processed on an NVL72", never "where your prompt went". Hardware numbers come from the GB300 and Vera Rubin NVL72 datasheets in `NVIDIA Datasheets/`.

## Reference layout

- `nvidia_course_content/transcripts/`: raw course video transcripts. Each file is one long paragraph of text (with stray zero-width characters). `Module_1/` covers Units 2–5, `Module_2/` covers Units 6–12, and the Unit 13 and 14 transcripts sit loose at the top level. File names don't always match the note names (`nvidia_networking_porfolio.md` is misspelled, and some end in `_transcript`).
- `nvidia_course_content/notes/`: cleaned study notes, one per transcript, in kebab-case. These are the main thing you edit.
- `NVIDIA Datasheets/`: product PDFs (H100/H200, B200, Blackwell, GH200, Grace, L4, L40S, DGX BasePOD/SuperPOD, ConnectX-7, Quantum-X800, Vera Rubin). Use these to check specs.
- `NVIDIA Stencils/`: Visio stencils (`.vss`/`.vssx`) for NVIDIA switches, used for network diagrams. They are binary, so don't edit them.

## Note format

Every note follows the same template. Keep it when you write or revise one:

```
# Unit N: <Title>

**Exam mapping:** Topic 1, *Essential AI Knowledge* | Topic 2, *AI Infrastructure* | Topic 3, *AI Operations*
**Source:** AI Infrastructure and Operations Fundamentals course, unit transcript (part X of Unit N[, sub-unit N.M])

---
## What you should be able to do after this unit   (optional)
## 1. ... numbered content sections, with tables for comparisons and **bold** key facts
## Key Terms
## Exam Tips
---
## NVIDIA Documentation
Official NVIDIA pages for this lesson's main concepts (links checked <Month D, YYYY>).
- [Page title](official nvidia.com / docs.nvidia.com URL): one-line purpose.
```

Conventions:
- A unit split across several transcripts gets one note per part, each labeled with "part X of Unit N" in its Source line (see Units 7, 8 and 12).
- Notes summarize the transcript. Don't add facts the transcript doesn't support, except in the NVIDIA Documentation links. When you add or change links, check that they work and update the "links checked" date.

## Coverage gaps

- `transcripts/Module_2/nvidia_solutions_in_the_cloud.md` has no matching note yet.
- There is no Unit 1 transcript or note.
