# VoWiFi Ruleset

![Last sync](https://img.shields.io/badge/last%20sync-2026--10--02-2ea44f)

Wi-Fi Calling (VoWiFi) rule sets for [sing-box](https://sing-box.sagernet.org/), converted from [HenryChiao/the_clash_ruleset](https://github.com/HenryChiao/the_clash_ruleset/tree/main/The_Location_rule-set/Wi-Fi_Calling_rule-set).

The source-format JSON files use rule-set version 2. Binary SRS files are compiled with the official sing-box executable. `VoW-ALL` combines all regional lists and removes duplicate rules.

## Rule sets

| Region | Basename | JSON | SRS |
| --- | --- | --- | --- |
| Americas | `VoW-AM` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-AM.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-AM.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-AM.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-AM.srs) |
| Asia | `VoW-AS` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-AS.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-AS.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-AS.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-AS.srs) |
| Germany | `VoW-DE` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-DE.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-DE.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-DE.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-DE.srs) |
| Europe | `VoW-EU` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-EU.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-EU.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-EU.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-EU.srs) |
| Hong Kong | `VoW-HK` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-HK.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-HK.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-HK.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-HK.srs) |
| Oceania | `VoW-OC` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-OC.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-OC.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-OC.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-OC.srs) |
| United Kingdom | `VoW-UK` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-UK.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-UK.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-UK.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-UK.srs) |
| United States | `VoW-US` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-US.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-US.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-US.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-US.srs) |
| All regions | `VoW-ALL` | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/json/VoW-ALL.json) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/json/VoW-ALL.json) | [Original](https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-ALL.srs) · [CDN](https://cdn.jsdelivr.net/gh/Leovikii/VoWiFi-ruleset@main/rulesets/srs/VoW-ALL.srs) |

Files are published under `rulesets/json/` and `rulesets/srs/` with matching basenames.

`Original` links point directly to GitHub Raw. `CDN` links use the third-party jsDelivr mirror, which may provide better access from mainland China but can serve a cached version briefly after an update. Open a link and copy its URL into your client configuration.

## Usage

Use the binary `VoW-ALL.srs` rule set for all regions:

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "vowifi",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/Leovikii/VoWiFi-ruleset/main/rulesets/srs/VoW-ALL.srs",
        "download_detour": "proxy"
      }
    ],
    "rules": [
      {
        "rule_set": "vowifi",
        "outbound": "proxy"
      }
    ]
  }
}
```

To use source JSON instead, set `format` to `source` and use the corresponding JSON link in the table above.

## Updates

GitHub Actions checks the upstream lists once a month, at 19:23 UTC on the first day of each month (03:23 Hong Kong time on the second day), and can also be started manually. A successful sync updates the badge above, rebuilds every JSON/SRS pair, verifies the output, and commits changed files with `github-actions[bot]`.

Pull requests are built and verified without modifying the branch. Their generated files are available as the `VoWiFi-rule-sets` workflow artifact.

Published JSON and SRS files are generated and committed by GitHub Actions. When updating rules or the converter, commit the source lists and code; local build outputs are for verification and should not be included in your commit.

## Development and troubleshooting

Python 3.10+ is required. The workflow uses sing-box **1.13.16**; use the same version locally to keep binary output reproducible. With `sing-box` on your `PATH`, run from the repository root:

```sh
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/build.py --check
```

To refresh the upstream lists first, run `python scripts/sync_upstream.py`. This also updates the last-sync badge. For JSON-only development without sing-box, use `python scripts/build.py --json-only` and `python scripts/build.py --json-only --check`. To select another executable path, pass `--sing-box /path/to/sing-box`.

Source lists are saved as UTF-8 with one final newline. Git keeps lists and generated JSON files with LF line endings on every platform so Windows checkouts can pass the byte-for-byte output check.

The converter supports `DOMAIN`, `DOMAIN-SUFFIX`, `DOMAIN-KEYWORD`, `IP-CIDR`, and `IP-CIDR6`. Clash's `no-resolve` option is omitted because DNS resolution behavior is not stored in sing-box source rule-sets; configure it in your client's routing configuration as needed. The upstream KPN/SIMYO IP rule currently spells this option `re-resolve`. The converter accepts that spelling on IP rules with a warning and preserves the CIDR; it does not implement a new DNS behavior. Other unknown options, unsupported rule types, and invalid CIDRs still fail with a filename and line number.

All source lists are parsed before existing generated files are replaced or stale files are removed. Regression tests run before upstream synchronization and compilation in Actions. If an upstream change introduces another unsupported rule, inspect the reported line and update the converter deliberately before rerunning **Build rule-sets** from the Actions tab. Automatic commits require repository Actions write permissions and branch rules that allow `github-actions[bot]` to push to the default branch.

## License

Source rules remain subject to the upstream project's license. Repository code is released under the [MIT License](LICENSE).
