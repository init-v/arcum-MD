"""PPTX extractor — wraps Docling for slide-to-Markdown conversion."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from arcum.output import ConversionResult


def extract(
    file: Path,
    status_fn: Optional[Callable[[str], None]] = None,
) -> ConversionResult:
    """
    Convert a PPTX to Markdown using Docling.

    Produces structured Markdown from slide decks:
    - Slide titles become headings
    - Bullet points become lists
    - Tables preserved where possible
    """
    from docling.document_converter import DocumentConverter

    def status(msg: str) -> None:
        if status_fn:
            status_fn(msg)

    size_mb = file.stat().st_size / 1_048_576
    status(f"Detected: {file.name} ({size_mb:.1f} MB)")
    status("Extracting with Docling...")

    converter = DocumentConverter()
    result = converter.convert(str(file))
    markdown = result.document.export_to_markdown()

    slide_count: int = _count_slides(file)
    metadata = {"slides": slide_count}

    status(f"Extracted {len(markdown.split()):,} words from {slide_count} slides.")

    return ConversionResult(
        source_path=file,
        file_type="pptx",
        body=markdown,
        metadata=metadata,
    )


def _count_slides(file: Path) -> int:
    try:
        from pptx import Presentation
        prs = Presentation(str(file))
        return len(prs.slides)
    except Exception:
        return 0
