

# Arcum MD

**Structured knowledge for humans now, agents next.**

A local-first CLI tool that converts PDFs, slide decks, and audio recordings into clean structured Markdown.

<img width="442" height="132" alt="image" src="https://github.com/user-attachments/assets/98bbf3c0-0a98-4fec-83a0-29e4400dbe8e" />

---

## Install

Requires Python 3.10+. One command installs everything:

```bash
git clone https://github.com/your-org/arcum-md
cd arcum-md
./install.sh
```

That's it. The script checks your Python version, upgrades pip, and installs
Arcum MD along with all extraction libraries (Marker, Docling, faster-whisper).

**On Windows**, use this instead:

```powershell
git clone https://github.com/your-org/arcum-md
cd arcum-md
pip install -e .
```

---

## Usage

```bash
# Convert a PDF
arcum convert lecture.pdf

# Convert a PPTX, specify output path
arcum convert slides.pptx --output notes.md

# Transcribe audio, preview in terminal only
arcum convert interview.m4a --preview

# CI-friendly quiet mode
arcum convert report.pdf --quiet
```

---

## Supported file types

| Type | Extractor | Notes |
|------|-----------|-------|
| `.pdf` | [Marker](https://github.com/VikParuchuri/marker) | Tables, headings, equations |
| `.pptx` | [Docling](https://github.com/DS4SD/docling) | Slide titles → headings |
| `.m4a` | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Timestamped transcript |

---

## Output format

Every conversion produces a Markdown document with a YAML frontmatter block:

```markdown
---
source: lecture.pdf
type: pdf
converted: 2024-01-15T10:30:00Z
pages: 34
---

# Lecture 4: Cellular Respiration

## Overview
...
```

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ARCUM_WHISPER_MODEL` | `base` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) |

---

## Architecture

```
arcum/
├── cli.py           # Typer entry point, commands
├── convert.py       # Dispatch logic
├── display.py       # Terminal output helpers
├── output.py        # Markdown assembly, ConversionResult
└── extractors/
    ├── pdf.py       # Marker wrapper
    ├── pptx.py      # Docling wrapper
    └── audio.py     # faster-whisper wrapper
```

The Python core is designed to be wrapped by a future Tauri desktop app without architectural changes.
