"""Audio extractor — wraps faster-whisper for M4A-to-Markdown transcription."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from arcum.output import ConversionResult

# Model size → accuracy/speed trade-off.
# "base" is fast and accurate enough for most use cases.
# Users can override via ARCUM_WHISPER_MODEL env var.
DEFAULT_MODEL = "base"


def extract(
    file: Path,
    status_fn: Optional[Callable[[str], None]] = None,
) -> ConversionResult:
    """
    Transcribe an M4A audio file to Markdown using faster-whisper.

    Output format:
    - H2 heading for each detected chapter/segment boundary (every ~5 min)
    - Timestamped paragraphs within each section
    - Speaker diarization is NOT included in v1
    """
    import os
    from faster_whisper import WhisperModel

    def status(msg: str) -> None:
        if status_fn:
            status_fn(msg)

    model_size = os.environ.get("ARCUM_WHISPER_MODEL", DEFAULT_MODEL)
    size_mb = file.stat().st_size / 1_048_576
    status(f"Detected: {file.name} ({size_mb:.1f} MB)")
    status(f"Loading Whisper model '{model_size}' (downloads once on first run)...")

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    status("Transcribing audio...")
    segments, info = model.transcribe(str(file), beam_size=5)

    status(
        f"Detected language: {info.language} "
        f"(confidence: {info.language_probability:.0%})"
    )

    markdown, duration_s = _build_transcript(segments)

    if not markdown.strip():
        raise ValueError("No audio detected. The file may be silent or corrupt.")

    minutes = int(duration_s // 60)
    seconds = int(duration_s % 60)
    metadata = {
        "language": info.language,
        "language_confidence": f"{info.language_probability:.0%}",
        "duration": f"{minutes}m {seconds}s",
        "whisper_model": model_size,
    }

    status(f"Transcribed {minutes}m {seconds}s of audio.")

    return ConversionResult(
        source_path=file,
        file_type="m4a",
        body=markdown,
        metadata=metadata,
    )


def _build_transcript(segments) -> tuple[str, float]:
    """
    Convert Whisper segments into structured Markdown.

    Groups segments into ~5-minute sections with H2 headings.
    Each segment becomes a timestamped paragraph.
    """
    SECTION_INTERVAL = 300  # seconds between section headings

    lines: list[str] = []
    last_section_start: float = -SECTION_INTERVAL
    total_end: float = 0.0

    for segment in segments:
        start: float = segment.start
        end: float = segment.end
        text: str = segment.text.strip()
        total_end = end

        if start - last_section_start >= SECTION_INTERVAL:
            heading = _format_timestamp(start)
            lines.append(f"\n## {heading}\n")
            last_section_start = start

        lines.append(f"[{_format_timestamp(start)}] {text}")

    return "\n".join(lines), total_end


def _format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"
