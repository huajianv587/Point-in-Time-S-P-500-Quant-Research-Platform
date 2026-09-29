from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class UniverseLoadResult:
    members: list[dict[str, Any]]
    source: str
    path: str | None
    as_of_date: str | None
    complete: bool
    warnings: list[str]


def _normalise_symbol(value: Any) -> str:
    return str(value or "").strip().upper().replace("-", ".")


def _first(row: dict[str, Any], *names: str, default: Any = "") -> Any:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value
    return default


def _normalise_row(row: dict[str, Any]) -> dict[str, Any] | None:
    symbol = _normalise_symbol(_first(row, "symbol", "ticker", "Symbol", "Ticker"))
    if not symbol:
        return None
    weight_raw = _first(row, "benchmark_weight", "weight", "Weight", "index_weight", default=0.0)
    try:
        weight = float(str(weight_raw).replace("%", ""))
        if weight > 1.0:
            weight /= 100.0
    except (TypeError, ValueError):
        weight = 0.0
    return {
        "symbol": symbol,
        "company_name": str(_first(row, "company_name", "name", "Security", "Name", default=symbol)).strip(),
        "sector": str(_first(row, "sector", "GICS Sector", "gics_sector", default="Unknown")).strip(),
        "industry": str(_first(row, "industry", "GICS Sub-Industry", "gics_sub_industry", default="Unknown")).strip(),
        "benchmark_weight": max(0.0, weight),
    }


def load_sp500_universe(
    configured_path: str | Path | None,
    fallback_rows: Iterable[dict[str, Any]],
) -> UniverseLoadResult:
    """Load an auditable S&P 500 snapshot, falling back to a small seed catalog."""
    raw_path = configured_path or os.getenv("SP500_CONSTITUENTS_PATH")
    candidate = Path(raw_path).expanduser() if raw_path else Path("storage/quant/universe/sp500_constituents.csv")
    if not candidate.is_absolute():
        candidate = Path(__file__).resolve().parents[2] / candidate

    rows: list[dict[str, Any]] = []
    if candidate.exists():
        try:
            with candidate.open("r", encoding="utf-8-sig", newline="") as handle:
                for raw_row in csv.DictReader(handle):
                    normalised = _normalise_row(raw_row)
                    if normalised:
                        rows.append(normalised)
        except (OSError, UnicodeError) as exc:
            return UniverseLoadResult(
                members=list(fallback_rows),
                source="embedded_seed_catalog",
                path=str(candidate),
                as_of_date=None,
                complete=False,
                warnings=[f"sp500_constituents_read_failed:{type(exc).__name__}"],
            )

    deduplicated = {row["symbol"]: row for row in rows}
    if deduplicated:
        complete = len(deduplicated) >= 450
        warnings = [] if complete else [f"sp500_snapshot_incomplete:{len(deduplicated)}_members"]
        return UniverseLoadResult(
            members=list(deduplicated.values()),
            source="csv_snapshot",
            path=str(candidate),
            as_of_date=None,
            complete=complete,
            warnings=warnings,
        )

    fallback = list(fallback_rows)
    return UniverseLoadResult(
        members=fallback,
        source="embedded_seed_catalog",
        path=str(candidate),
        as_of_date=None,
        complete=False,
        warnings=["sp500_constituents_file_missing", f"using_seed_catalog:{len(fallback)}_members"],
    )
