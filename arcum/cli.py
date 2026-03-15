"""Arcum MD — CLI entry point."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from arcum import __version__
from arcum.convert import convert_file
from arcum.display import print_logo, print_error

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Structured knowledge for humans now, agents next.",
)
console = Console()

SUPPORTED_TYPES = {".pdf", ".pptx", ".m4a"}


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", is_eager=True, help="Show version and exit."),
) -> None:
    if version:
        console.print(f"arcum-md {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        print_logo(console)
        console.print(ctx.get_help())


@app.command()
def convert(
    file: Path = typer.Argument(..., help="Path to input file (.pdf, .pptx, .m4a)"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Write output to this file (default: <input-name>.md)"
    ),
    preview: bool = typer.Option(
        False, "--preview", "-p", help="Print output to terminal without writing a file."
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress status output."),
) -> None:
    """Convert a file to clean structured Markdown."""
    if not quiet:
        print_logo(console)

    if not file.exists():
        print_error(console, f"File not found: {file}")
        raise typer.Exit(1)

    suffix = file.suffix.lower()
    if suffix not in SUPPORTED_TYPES:
        print_error(
            console,
            f"Unsupported file type: {suffix}  (supported: .pdf, .pptx, .m4a)",
        )
        raise typer.Exit(1)

    result = convert_file(file, console=console, quiet=quiet)

    if result is None:
        raise typer.Exit(1)

    if preview:
        result.render_preview(console)
        return

    out_path = output or file.with_suffix(".md")
    out_path.write_text(result.markdown, encoding="utf-8")

    if not quiet:
        console.print(f"\n  [bold green]✓[/bold green] Written to: [cyan]{out_path}[/cyan]")


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"arcum-md {__version__}")
