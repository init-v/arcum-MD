"""Markdown assembly — metadata block + body + preview rendering."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax

from arcum.display import print_preview


@dataclass
class ConversionResult:
    source_path: Path
    file_type: str          # pdf | pptx | m4a
    body: str               # extracted markdown body
    metadata: dict          # arbitrary k/v pairs from the extractor
    word_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.word_count = len(self.body.split())

    @property
    def markdown(self) -> str:
        """Full markdown document: metadata block + body."""
        return _build_document(self.source_path, self.file_type, self.metadata, self.body)

    def render_preview(self, console: Console) -> None:
        """Print the full markdown to the terminal with syntax highlighting."""
        syntax = Syntax(
            self.markdown,
            "markdown",
            theme="monokai",
            word_wrap=True,
            background_color="default",
        )
        console.print(syntax)


def _build_document(
    source_path: Path,
    file_type: str,
    metadata: dict,
    body: str,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    meta_lines = [
        "---",
        f"source: {source_path.name}",
        f"type: {file_type}",
        f"converted: {now}",
    ]
    for key, value in metadata.items():
        safe_value = str(value).replace("\n", " ")
        meta_lines.append(f"{key}: {safe_value}")
    meta_lines.append("---")

    header = "\n".join(meta_lines)
    return f"{header}\n\n{body.strip()}\n"
