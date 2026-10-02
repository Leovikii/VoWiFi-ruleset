"""Offline regression checks for upstream conversion and output validation."""

from contextlib import redirect_stderr
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from scripts.build import RuleError, compare_directories, generate, parse_list


class BuildTests(unittest.TestCase):
    def test_upstream_options_preserve_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wificalling-europe.list"
            path.write_text(
                "\ufeff# KPN SIMYO\n"
                "DOMAIN-SUFFIX,EPDG.EPC.MNC008.MCC204.PUB.3GPPNETWORK.ORG.\n"
                "IP-CIDR,62.133.64.0/18,re-resolve\n"
                "IP-CIDR,62.133.64.0/18,no-resolve\n"
                "IP-CIDR6,2001:db8::/32,RE-RESOLVE\n",
                encoding="utf-8",
            )
            warning = StringIO()
            with redirect_stderr(warning):
                rules = parse_list(path)
            self.assertEqual(rules, {
                "domain_suffix": ["epdg.epc.mnc008.mcc204.pub.3gppnetwork.org"],
                "ip_cidr": ["62.133.64.0/18", "2001:db8::/32"],
            })
            self.assertIn("ignoring upstream 're-resolve'", warning.getvalue())

    def test_invalid_rules_still_fail_with_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.list"
            for rule in (
                "IP-CIDR,62.133.64.0/18,unexpected",
                "IP-CIDR,62.133.64.0/18,re-resolve,unexpected",
                "DOMAIN,example.com,re-resolve",
                "IP-CIDR,invalid,no-resolve",
                "DOMAIN,",
                "MATCH,proxy",
            ):
                with self.subTest(rule=rule):
                    path.write_text("# comment\n" + rule, encoding="utf-8")
                    with self.assertRaisesRegex(RuleError, r"invalid\.list:2:"):
                        parse_list(path)

    def test_invalid_source_leaves_existing_outputs_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            output = root / "json"
            source.mkdir()
            output.mkdir()
            (source / "wificalling-americas.list").write_text("DOMAIN,example.com")
            (source / "wificalling-europe.list").write_text("IP-CIDR,invalid")
            (output / "VoW-AM.json").write_bytes(b"existing regional output")
            (output / "stale.json").write_bytes(b"existing stale output")
            before = {path.name: path.read_bytes() for path in output.iterdir()}
            with self.assertRaises(RuleError):
                generate(source, output, None, None)
            self.assertEqual(before, {path.name: path.read_bytes() for path in output.iterdir()})

    def test_generation_merges_and_detects_outdated_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            for name in ("wificalling-americas", "wificalling-europe"):
                (source / f"{name}.list").write_text("DOMAIN,example.com\n")
            output = root / "json"
            output.mkdir()
            (output / "stale.json").write_text("stale")
            self.assertEqual(generate(source, output, None, None), 2)
            self.assertFalse((output / "stale.json").exists())
            self.assertEqual(json.loads((output / "VoW-ALL.json").read_text()), {
                "version": 2, "rules": [{"domain": ["example.com"]}],
            })
            expected = root / "expected"
            generate(source, expected, None, None)
            self.assertEqual(compare_directories(expected, output, "*.json"), [])
            (output / "VoW-ALL.json").write_text("outdated")
            self.assertIn("outdated generated file", compare_directories(expected, output, "*.json")[0])


if __name__ == "__main__":
    unittest.main()
