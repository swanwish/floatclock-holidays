#!/usr/bin/env python3
"""Regenerate manifest.json from the regions/ tree.

Run after adding/updating any .fch file. Computes SHA-256 and rebuilds
the top-level index that FloatClock fetches on launch.

Usage:
    python3 scripts/update-manifest.py
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = "swanwish/floatclock-holidays"
BRANCH = "main"

# Add new regions here. The folder name under regions/ must match the id.
REGIONS_META: dict[str, dict[str, str]] = {
    "cn-statutory": {
        "displayName": "中国大陆 · 法定节假日",
        "locale": "zh-CN",
        "category": "statutory",
    },
    # Examples for future regions:
    # "cn-gis-school": {
    #     "displayName": "GIS 国际学校 · 校历",
    #     "locale": "zh-CN",
    #     "category": "school",
    # },
    # "us-federal": {
    #     "displayName": "United States · Federal holidays",
    #     "locale": "en-US",
    #     "category": "statutory",
    # },
}


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    regions_dir = repo_root / "regions"
    base_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

    regions_out: list[dict] = []
    for region_dir in sorted(p for p in regions_dir.iterdir() if p.is_dir()):
        meta = REGIONS_META.get(region_dir.name)
        if meta is None:
            print(f"WARN: no entry in REGIONS_META for {region_dir.name}; skipping")
            continue

        files = []
        for fch in sorted(region_dir.glob("holidays-*.fch")):
            m = re.match(r"holidays-(\d{4})\.fch$", fch.name)
            if not m:
                continue
            sha256 = hashlib.sha256(fch.read_bytes()).hexdigest()
            rel = fch.relative_to(repo_root).as_posix()
            files.append({
                "year": int(m.group(1)),
                "url": f"{base_url}/{rel}",
                "sha256": sha256,
            })

        regions_out.append({
            "id": region_dir.name,
            **meta,
            "files": files,
        })

    manifest = {
        "schema": "floatclock.holidays.manifest/v1",
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regions": regions_out,
    }

    out = repo_root / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(repo_root)} ({len(regions_out)} regions)")


if __name__ == "__main__":
    main()
