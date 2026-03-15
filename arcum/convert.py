"""Dispatch layer — routes a file to the correct extractor."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from rich.console import Console

from arcum.display import print_status, print_error
from arcum.output import ConversionResult


def convert_file(
    file: Path,
    console: Console,
    quiet: bool = False,
) -> Optional[ConversionResult]:
    """Route file to the correct extractor and return a ConversionResult."""
    suffix = file.suffix.lower()

    def status(msg: str) -> None:
        if not quiet:
            print_status(console, suffix.lstrip("."), msg)

    if not quiet:
        size_mb = file.stat().st_size / 1_048_576
        console.print(f"\n  [bold]Arcum MD[/bold] — converting [cyan]{file.name}[/cyan]")
        console.print(f"  {'─' * 40}")

    try:
        if suffix == ".pdf":
            from arcum.extractors.pdf import extract
        elif suffix == ".pptx":
            from arcum.extractors.pptx import extract
        elif suffix == ".m4a":
            from arcum.extractors.audio import extract
        else:
            print_error(console, f"Unsupported file type: {suffix}")
            return None

        result = extract(file, status_fn=status)

    except ImportError as exc:
        print_error(
            console,
            f"Missing dependency for {suffix} extraction: {exc}\n"
            f"  Run: pip install arcum-md",
        )
        return None
    except Exception as exc:  # noqa: BLE001
        print_error(console, f"Extraction failed: {exc}")
        return None

    if not result or not result.body.strip():
        print_error(console, "Extraction returned no content. The file may be empty or unsupported.")
        return None

    if not quiet:
        console.print(f"  [dim]Done. {result.word_count:,} words extracted.[/dim]")
        from arcum.display import print_preview
        print_preview(console, result.markdown, result.word_count)

    return result
