"""File-hash result cache — avoids re-processing unchanged files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "arcum-md"


def _file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def get(path: Path) -> dict | None:
    """Return cached result dict for path, or None on miss."""
    cache_file = CACHE_DIR / f"{_file_hash(path)}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def put(path: Path, data: dict) -> None:
    """Store result dict for path in cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{_file_hash(path)}.json"
    cache_file.write_text(json.dumps(data), encoding="utf-8")
