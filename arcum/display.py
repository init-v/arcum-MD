"""Terminal display helpers — status lines, preview, logo, errors."""

from __future__ import annotations

from rich.console import Console
from rich.rule import Rule
from rich.text import Text

LOGO = """\
  ___                       __  __ ____
 / _ \\  _ __  ___  _   _ _ |  \\/  |  _ \\
| |_| || '__|/ __|| | | | || |\\/| || | |
|  _  || |  | (__ | |_| | || |  | || |_|
|_| |_||_|   \\___| \\__,_|_||_|  |_||____/
"""

PREVIEW_LINES = 20
PREVIEW_CHARS_PER_LINE = 120


def print_logo(console: Console) -> None:
    console.print(f"[bold cyan]{LOGO}[/bold cyan]")
    console.print("  [dim]Structured knowledge for humans now, agents next.[/dim]\n")


def print_status(console: Console, tag: str, message: str) -> None:
    tag_str = f"[bold white on blue] {tag.upper()} [/bold white on blue]"
    console.print(f"  {tag_str} {message}")


def print_success(console: Console, message: str) -> None:
    console.print(f"  [bold green]✓[/bold green] {message}")


def print_error(console: Console, message: str) -> None:
    console.print(f"\n  [bold red]✗[/bold red] {message}\n")


def print_preview(console: Console, markdown: str, word_count: int) -> None:
    lines = markdown.splitlines()
    preview_lines = lines[:PREVIEW_LINES]
    truncated = len(lines) > PREVIEW_LINES

    console.print()
    console.print(Rule("  Preview  ", style="dim"))

    for line in preview_lines:
        if len(line) > PREVIEW_CHARS_PER_LINE:
            line = line[:PREVIEW_CHARS_PER_LINE] + "…"
        console.print(f"  {line}")

    if truncated:
        console.print(
            f"  [dim]... [{word_count:,} words total — use --preview to see full output][/dim]"
        )

    console.print(Rule(style="dim"))
