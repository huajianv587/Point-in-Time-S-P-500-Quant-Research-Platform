#!/usr/bin/env python3
"""
S&P 500 Universe Import & Validation Script
=============================================

Import S&P 500 constituents from CSV, validate, and generate audit metadata.

Supports:
- Capital IQ exports
- Manual CSV with columns: symbol, company_name, sector, industry, weight
- Point-in-time snapshots with effective dates

Output:
- data/sp500_universe.json with SHA-256, snapshot_date, import_time
- Research-ready flag based on completeness
"""

import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import sys


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of file."""
    sha = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def parse_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """Parse CSV into constituent records."""
    constituents = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        # Normalize headers
        header_map = {
            'ticker': 'symbol',
            'symbol': 'symbol',
            'company': 'company_name',
            'company_name': 'company_name',
            'name': 'company_name',
            'sector': 'sector',
            'gics_sector': 'sector',
            'industry': 'industry',
            'gics_industry': 'industry',
            'weight': 'weight',
            'benchmark_weight': 'weight',
            'market_cap': 'market_cap',
        }

        for row in reader:
            normalized = {}
            for key, value in row.items():
                norm_key = header_map.get(key.lower().strip(), key)
                normalized[norm_key] = value.strip() if value else ''

            if not normalized.get('symbol'):
                continue

            constituent = {
                'symbol': normalized['symbol'].upper(),
                'company_name': normalized.get('company_name', ''),
                'sector': normalized.get('sector', 'Unknown'),
                'industry': normalized.get('industry', 'Unknown'),
            }

            # Optional weight
            if 'weight' in normalized and normalized['weight']:
                try:
                    constituent['weight'] = float(normalized['weight'])
                except ValueError:
                    pass

            constituents.append(constituent)

    return constituents


def validate_universe(constituents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate universe completeness."""
    total = len(constituents)

    # Check required fields
    missing_names = sum(1 for c in constituents if not c.get('company_name'))
    missing_sectors = sum(1 for c in constituents if c.get('sector') == 'Unknown')

    # Expected S&P 500 count
    is_complete = 490 <= total <= 510  # Allow small variance

    validation = {
        'total_constituents': total,
        'is_complete': is_complete,
        'completeness_pct': min(100, (total / 500) * 100),
        'missing_company_names': missing_names,
        'missing_sectors': missing_sectors,
        'sectors': {},
    }

    # Sector distribution
    for c in constituents:
        sector = c.get('sector', 'Unknown')
        validation['sectors'][sector] = validation['sectors'].get(sector, 0) + 1

    return validation


def import_universe(csv_path: str, snapshot_date: str = None, output_path: str = None):
    """Main import function."""
    csv_file = Path(csv_path)

    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"📊 Importing S&P 500 universe from: {csv_file.name}")

    # Parse
    constituents = parse_csv(csv_file)
    print(f"✓ Parsed {len(constituents)} constituents")

    # Validate
    validation = validate_universe(constituents)
    print(f"✓ Validation: {validation['total_constituents']} stocks, "
          f"{validation['completeness_pct']:.1f}% complete")

    if not validation['is_complete']:
        print(f"⚠️  Warning: Expected ~500 constituents, got {validation['total_constituents']}")

    # Metadata
    snapshot_date_iso = snapshot_date or datetime.now(timezone.utc).date().isoformat()

    universe = {
        'name': 'SP500',
        'snapshot_date': snapshot_date_iso,
        'import_time': datetime.now(timezone.utc).isoformat(),
        'source_file': csv_file.name,
        'source_sha256': compute_sha256(csv_file),
        'validation': validation,
        'research_ready': validation['is_complete'] and validation['missing_sectors'] < 10,
        'constituents': constituents,
    }

    # Write
    if output_path is None:
        output_path = Path(__file__).parent.parent / 'data' / 'sp500_universe.json'
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(universe, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to: {output_path}")
    print(f"✓ Research ready: {universe['research_ready']}")
    print(f"\nSector distribution:")
    for sector, count in sorted(validation['sectors'].items(), key=lambda x: -x[1]):
        print(f"  {sector:30s} {count:3d}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Import S&P 500 universe from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/import_sp500_universe.py sp500.csv
  python scripts/import_sp500_universe.py sp500.csv --snapshot-date 2024-12-31
  python scripts/import_sp500_universe.py capital_iq_export.csv --output data/universe_2024.json
        """
    )

    parser.add_argument('csv', help='Path to CSV file')
    parser.add_argument('--snapshot-date', help='Effective date (YYYY-MM-DD)')
    parser.add_argument('--output', help='Output JSON path')

    args = parser.parse_args()

    import_universe(args.csv, args.snapshot_date, args.output)
