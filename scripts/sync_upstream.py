#!/usr/bin/env python3
"""Synchronize Wi-Fi Calling Clash lists from the referenced upstream repository."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESTINATION = ROOT / "rulesets" / "source"
DEFAULT_README = ROOT / "README.md"
API_URL = (
    "https://api.github.com/repos/HenryChiao/the_clash_ruleset/contents/"
    "The_Location_rule-set/Wi-Fi_Calling_rule-set"
)
LAST_SYNC_BADGE_PATTERN = re.compile(
    r"(https://img\.shields\.io/badge/last%20sync-)\d{4}--\d{2}--\d{2}(-2ea44f)"
)
HONG_KONG_TIMEZONE = timezone(timedelta(hours=8))


def request(url: str) -> bytes:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "VoWiFi-ruleset-sync"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        return response.read()


def update_last_sync_badge(readme_path: Path) -> None:
    readme = readme_path.read_text(encoding="utf-8")
    date = datetime.now(HONG_KONG_TIMEZONE).strftime("%Y--%m--%d")
    updated, replacements = LAST_SYNC_BADGE_PATTERN.subn(rf"\g<1>{date}\g<2>", readme)
    if replacements != 1:
        raise RuntimeError(f"expected exactly one last-sync badge in {readme_path}")
    readme_path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    args = parser.parse_args()

    try:
        entries = json.loads(request(API_URL))
        files = sorted(
            (entry["name"], entry["download_url"])
            for entry in entries
            if entry.get("type") == "file" and entry["name"].endswith(".list")
        )
        if not files:
            raise RuntimeError("upstream contains no .list files")

        args.destination.mkdir(parents=True, exist_ok=True)
        upstream_names = {name for name, _ in files}
        for name, download_url in files:
            content = request(download_url)
            text = content.decode("utf-8-sig").rstrip() + "\n"
            (args.destination / name).write_text(text, encoding="utf-8", newline="\n")
        for stale_path in args.destination.glob("*.list"):
            if stale_path.name not in upstream_names:
                stale_path.unlink()
        update_last_sync_badge(args.readme)
    except (
        AttributeError,
        KeyError,
        OSError,
        RuntimeError,
        TypeError,
        UnicodeError,
        urllib.error.URLError,
    ) as exc:
        print(f"error: unable to synchronize upstream: {exc}", file=sys.stderr)
        return 1

    print(f"synchronized {len(files)} source lists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
