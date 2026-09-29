"""Resolve the optional ESG document corpus without coupling it to Git."""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_esg_corpus_root(path: str | Path | None = None) -> Path:
    """Return the configured corpus path, preferring an existing local corpus."""
    raw = path or os.getenv("ESG_CORPUS_ROOT")
    if raw:
        candidate = Path(raw).expanduser()
        return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate

    candidates = (
        PROJECT_ROOT / "esg_reports",
        PROJECT_ROOT.parent / "量化平台数据" / "esg_reports",
        PROJECT_ROOT / "ESG报告",
    )
    return next((candidate for candidate in candidates if candidate.exists()), candidates[0])
