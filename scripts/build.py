#!/usr/bin/env python3
"""Convert Clash classical rule lists to sing-box source and binary rule-sets."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT / "rulesets" / "source"
DEFAULT_JSON_DIR = ROOT / "rulesets" / "json"
DEFAULT_SRS_DIR = ROOT / "rulesets" / "srs"

TYPE_TO_FIELD = {
    "DOMAIN": "domain",
    "DOMAIN-SUFFIX": "domain_suffix",
    "DOMAIN-KEYWORD": "domain_keyword",
    "IP-CIDR": "ip_cidr",
    "IP-CIDR6": "ip_cidr",
}
FIELD_ORDER = ("domain", "domain_suffix", "domain_keyword", "ip_cidr")
OUTPUT_NAMES = {
    "wificalling-americas": "VoW-AM",
    "wificalling-asia": "VoW-AS",
    "wificalling-de": "VoW-DE",
    "wificalling-europe": "VoW-EU",
    "wificalling-hk": "VoW-HK",
    "wificalling-oceania": "VoW-OC",
    "wificalling-uk": "VoW-UK",
    "wificalling-us": "VoW-US",
}
ALL_OUTPUT_NAME = "VoW-ALL"


class RuleError(ValueError):
    pass


def parse_list(path: Path) -> dict[str, list[str]]:
    rules = {field: [] for field in FIELD_ORDER}
    seen = {field: set() for field in FIELD_ORDER}

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue

        parts = [part.strip() for part in line.split(",")]
        rule_type = parts[0].upper()
        if rule_type not in TYPE_TO_FIELD:
            raise RuleError(f"{path}:{line_number}: unsupported rule type {rule_type!r}")
        if len(parts) < 2 or not parts[1]:
            raise RuleError(f"{path}:{line_number}: missing rule value")
        options = {option.lower() for option in parts[2:] if option}
        allowed_options = {"no-resolve"}
        # Upstream uses this misspelling on the KPN/SIMYO IP rule.
        if rule_type in ("IP-CIDR", "IP-CIDR6"):
            allowed_options.add("re-resolve")
        if options - allowed_options:
            raise RuleError(f"{path}:{line_number}: unsupported option(s): {parts[2:]}")
        if "re-resolve" in options:
            print(
                f"warning: {path}:{line_number}: ignoring upstream 're-resolve' option; "
                "DNS resolution options are not stored in sing-box rule-sets",
                file=sys.stderr,
            )

        field = TYPE_TO_FIELD[rule_type]
        value = parts[1]
        if field == "ip_cidr":
            try:
                ipaddress.ip_network(value, strict=False)
            except ValueError as exc:
                raise RuleError(f"{path}:{line_number}: invalid CIDR {value!r}") from exc
        else:
            value = value.lower().rstrip(".")

        if value not in seen[field]:
            seen[field].add(value)
            rules[field].append(value)

    return {field: values for field, values in rules.items() if values}


def merge_rules(rule_sets: list[dict[str, list[str]]]) -> dict[str, list[str]]:
    merged = {field: [] for field in FIELD_ORDER}
    seen = {field: set() for field in FIELD_ORDER}
    for rules in rule_sets:
        for field in FIELD_ORDER:
            for value in rules.get(field, []):
                if value not in seen[field]:
                    seen[field].add(value)
                    merged[field].append(value)
    return {field: values for field, values in merged.items() if values}


def source_document(rules: dict[str, list[str]]) -> dict[str, object]:
    return {"version": 2, "rules": [rules]}


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def compile_srs(sing_box: str, json_dir: Path, srs_dir: Path) -> None:
    srs_dir.mkdir(parents=True, exist_ok=True)
    for json_path in sorted(json_dir.glob("*.json")):
        output_path = srs_dir / f"{json_path.stem}.srs"
        subprocess.run(
            [sing_box, "rule-set", "compile", "--output", str(output_path), str(json_path)],
            check=True,
        )


def remove_stale_outputs(directory: Path, suffix: str, expected_stems: set[str]) -> None:
    if not directory.exists():
        return
    for path in directory.glob(f"*{suffix}"):
        if path.stem not in expected_stems:
            path.unlink()


def generate(source_dir: Path, json_dir: Path, srs_dir: Path | None, sing_box: str | None) -> int:
    source_paths = sorted(source_dir.glob("*.list"))
    if not source_paths:
        raise RuleError(f"no .list files found in {source_dir}")

    unknown_stems = sorted(path.stem for path in source_paths if path.stem not in OUTPUT_NAMES)
    if unknown_stems:
        raise RuleError(f"missing output name mapping for: {', '.join(unknown_stems)}")

    # Validate every source before replacing or removing any existing output.
    parsed = [parse_list(path) for path in source_paths]
    expected_stems = {OUTPUT_NAMES[path.stem] for path in source_paths} | {ALL_OUTPUT_NAME}
    remove_stale_outputs(json_dir, ".json", expected_stems)
    if sing_box and srs_dir:
        remove_stale_outputs(srs_dir, ".srs", expected_stems)

    for source_path, rules in zip(source_paths, parsed):
        write_json(json_dir / f"{OUTPUT_NAMES[source_path.stem]}.json", source_document(rules))

    write_json(json_dir / f"{ALL_OUTPUT_NAME}.json", source_document(merge_rules(parsed)))
    if sing_box and srs_dir:
        compile_srs(sing_box, json_dir, srs_dir)
    return len(source_paths)


def compare_directories(expected: Path, actual: Path, pattern: str) -> list[str]:
    expected_files = {path.name: path for path in expected.glob(pattern)}
    actual_files = {path.name: path for path in actual.glob(pattern)}
    differences: list[str] = []
    for name in sorted(expected_files.keys() | actual_files.keys()):
        if name not in expected_files:
            differences.append(f"unexpected generated file: {actual_files[name]}")
        elif name not in actual_files:
            differences.append(f"missing generated file: {expected_files[name]}")
        elif expected_files[name].read_bytes() != actual_files[name].read_bytes():
            differences.append(f"outdated generated file: {expected_files[name]}")
    return differences


def resolve_executable(value: str | None) -> str | None:
    if not value:
        return None
    resolved = shutil.which(value)
    if not resolved:
        raise RuleError(f"sing-box executable not found: {value}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--json-dir", type=Path, default=DEFAULT_JSON_DIR)
    parser.add_argument("--srs-dir", type=Path, default=DEFAULT_SRS_DIR)
    parser.add_argument("--sing-box", default=os.environ.get("SING_BOX", "sing-box"))
    parser.add_argument("--json-only", action="store_true", help="skip SRS compilation")
    parser.add_argument("--check", action="store_true", help="verify committed outputs are current")
    args = parser.parse_args()

    try:
        sing_box = None if args.json_only else resolve_executable(args.sing_box)
        if args.check:
            with tempfile.TemporaryDirectory(prefix="vowifi-ruleset-") as temp_name:
                temp = Path(temp_name)
                generated_json = temp / "json"
                generated_srs = temp / "srs"
                count = generate(args.source_dir, generated_json, generated_srs, sing_box)
                differences = compare_directories(args.json_dir, generated_json, "*.json")
                if sing_box:
                    differences += compare_directories(args.srs_dir, generated_srs, "*.srs")
                if differences:
                    print("\n".join(differences), file=sys.stderr)
                    return 1
        else:
            count = generate(args.source_dir, args.json_dir, args.srs_dir, sing_box)
    except (RuleError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    mode = "verified" if args.check else "generated"
    print(f"{mode} {count} individual rule-sets plus all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
