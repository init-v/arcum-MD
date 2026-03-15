"""PDF extractor — wraps Marker for high-quality PDF-to-Markdown conversion."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from arcum.output import ConversionResult


def extract(
    file: Path,
    status_fn: Optional[Callable[[str], None]] = None,
) -> ConversionResult:
    """
    Convert a PDF to Markdown using Marker.

    Marker produces high-quality Markdown including:
    - Preserved heading structure
    - Tables rendered as Markdown tables
    - Code blocks detected and fenced
    - Equations in LaTeX where possible
    """
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    def status(msg: str) -> None:
        if status_fn:
            status_fn(msg)

    size_mb = file.stat().st_size / 1_048_576
    status(f"Detected: {file.name} ({size_mb:.1f} MB)")
    status("Extracting with Marker (this may take a moment on first run)...")

    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(str(file))
    markdown, _, images = text_from_rendered(rendered)

    page_count: int = getattr(rendered, "metadata", {}).get("page_count", "?")

    metadata = {"pages": page_count}

    status(f"Extracted {len(markdown.split()):,} words across {page_count} pages.")

    return ConversionResult(
        source_path=file,
        file_type="pdf",
        body=markdown,
        metadata=metadata,
    )
