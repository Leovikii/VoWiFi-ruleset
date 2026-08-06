# VoWiFi Ruleset

![Last sync](https://img.shields.io/badge/last%20sync-2026--08--06-2ea44f)

Wi-Fi Calling (VoWiFi) rule sets for [sing-box](https://sing-box.sagernet.org/), converted from [HenryChiao/the_clash_ruleset](https://github.com/HenryChiao/the_clash_ruleset/tree/main/The_Location_rule-set/Wi-Fi_Calling_rule-set).

The source-format JSON files use rule-set version 2. Binary SRS files are compiled with the official sing-box executable. `VoW-ALL` combines all regional lists and removes duplicate rules.

## Rule sets

| Region | JSON / SRS basename |
| --- | --- |
| Americas | `VoW-AM` |
| Asia | `VoW-AS` |
| Germany | `VoW-DE` |
| Europe | `VoW-EU` |
| Hong Kong | `VoW-HK` |
| Oceania | `VoW-OC` |
| United Kingdom | `VoW-UK` |
| United States | `VoW-US` |
| All regions | `VoW-ALL` |

Files are published under `rulesets/json/` and `rulesets/srs/` with matching basenames.

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
        "url": "https://raw.githubusercontent.com/<owner>/VoWiFi-ruleset/main/rulesets/srs/VoW-ALL.srs",
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

Replace `<owner>` with the GitHub account or organization hosting this repository. To use source JSON instead, set `format` to `source` and point the URL to `rulesets/json/VoW-ALL.json`.

## Updates

GitHub Actions checks the upstream lists once a month, at 19:23 UTC on the first day of each month (03:23 Hong Kong time on the second day), and can also be started manually. A successful sync updates the badge above, rebuilds every JSON/SRS pair, verifies the output, and commits changed files with `github-actions[bot]`.

Pull requests are built and verified without modifying the branch. Their generated files are available as the `VoWiFi-rule-sets` workflow artifact.

## License

Source rules remain subject to the upstream project's license. Repository code is released under the [MIT License](LICENSE).
