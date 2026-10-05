# pins-toolkit

Source for the **InsightPins** plugin for Claude: turn any blog post, product page or recipe into a
finished Pinterest pin in one message, with the [InsightPins](https://insightpins.com) pin generator
and built-in pin design and copywriting best practices. It also reviews and improves pins you
already have, and builds or checks Pinterest bulk upload CSV files.

![Four pins made with the InsightPins plugin](plugins/insightpins/assets/example-pins.jpg)

- **Create** a pin from a link, or several variations to test, with ready-to-paste title,
  description, alt text and board
- **Review** an uploaded pin: a score on 8 criteria and the fixes that matter most
- **Optimize** a pin into improved versions, or **remake** one you like in your own style
- **Check and build** Pinterest bulk upload CSV files before Pinterest rejects them

7 skills, 2 commands and the InsightPins connector (8 tools). Full list, examples and data handling
in the [plugin README](plugins/insightpins/README.md).

| Path | What it is |
| - | - |
| [`plugins/insightpins/`](plugins/insightpins/) | The plugin itself (manifest, MCP connector, skills, commands). This is the folder submitted to the Claude directory. See its [README](plugins/insightpins/README.md). |
| [`evals/`](evals/) | `claude plugin eval` suite with mocked InsightPins tools (no real renders) |
| [`tests/`](tests/) | Unit tests: directory requirements, contrast table, CSV scripts, eval graders |
| [`docs/PLAN.md`](docs/PLAN.md) | Roadmap and design decisions |
| [`docs/SUBMISSION.md`](docs/SUBMISSION.md) | Directory submission checklist and portal answers |
| [`docs/TEST-REPORT.md`](docs/TEST-REPORT.md), [`docs/MCP-IMPROVEMENTS.md`](docs/MCP-IMPROVEMENTS.md) | Test results and ranked server improvement ideas |
| `.claude-plugin/marketplace.json` | Lets you install the plugin straight from this repo |
| [`scripts/check-bulk-csv-sync.py`](scripts/check-bulk-csv-sync.py) | Checks the plugin's CSV checker against the insightpins.com fixtures |
| [`scripts/build-template-colors.py`](scripts/build-template-colors.py) | Builds the per-template palette guide from the pin generator's `docs/TEMPLATE_COLOR_ROLES.md` |

## Try it

Claude Code:

```bash
claude --plugin-dir ./plugins/insightpins
```

Or add this repo as a marketplace (`/plugin marketplace add shapito27/pins-toolkit`) and install
`insightpins` from it. On claude.ai, add the repo under **Customize > Plugins > Add > Add marketplace**.

## Validate and test

```bash
claude plugin validate ./plugins/insightpins
claude plugin validate .
python3 -m unittest discover -s tests          # directory checks, contrast table, CSV scripts, graders
claude plugin eval . --no-publish --scaffold --allow-tools Bash
```

`tests/test_plugin.py` checks what the directory's validator checks (manifest, icon, privacy URL,
file sizes, README images), that the contrast table in `style-selection.md` matches the palette
colors, that the CSV scripts work and carry nothing the security scan reads as "uses the
environment", and that the eval graders match what they should.

`--scaffold` lets two cases copy their fixture into the run's workspace; `--allow-tools Bash` lets the
bulk CSV case run the checker script.

## The bulk CSV skill has a source of truth elsewhere

`plugins/insightpins/skills/pinterest-bulk-csv/` is a copy of `downloads-src/pinterest-bulk-csv/` in the
`insightpins.com` repo, whose `check_csv.py` also defines the rules of the
[web CSV checker](https://insightpins.com/tools/pinterest-csv-checker.html). The plugin copy adds
script paths (`${CLAUDE_SKILL_DIR}`), a "just checking a file?" path and notes for pins made with
InsightPins. `reference.md` is unchanged. The scripts differ in two places, both for the Claude
directory's security scan, which held the plugin for "reads the environment" because of the word
`env` next to the share-link host names in `check_csv.py`:

- no `#!/usr/bin/env python3` first line (the skill runs them with `python3 -B`);
- `check_csv.py`'s semicolon message says "a regional Excel format" instead of "export".

Making the same two changes in `insightpins.com` keeps the copies identical. When the rules change
there, copy the scripts and `reference.md` again, re-apply the two changes if they aren't upstream
yet, and run the fixtures and the plugin tests (all 41 fixtures matched on 2026-10-04):

```bash
cp ../insightpins.com/downloads-src/pinterest-bulk-csv/reference.md plugins/insightpins/skills/pinterest-bulk-csv/
cp ../insightpins.com/downloads-src/pinterest-bulk-csv/scripts/*.py plugins/insightpins/skills/pinterest-bulk-csv/scripts/
sed -i '1{/^#!/d}' plugins/insightpins/skills/pinterest-bulk-csv/scripts/*.py
sed -i 's/"export); Pinterest expects commas/"format); Pinterest expects commas/' \
  plugins/insightpins/skills/pinterest-bulk-csv/scripts/check_csv.py
python3 scripts/check-bulk-csv-sync.py ../insightpins.com   # must print "0 mismatches"
python3 -m unittest discover -s tests                     # must pass
```

## The palette guide comes from the pin generator

`plugins/insightpins/skills/create-pin/references/template-colors.md` is generated from
`docs/TEMPLATE_COLOR_ROLES.md` in the `pin-generator-tool` repo, which is itself generated from the
templates' colour map. When templates or palettes change there, regenerate it and run the tests
(they check it against that doc when the repo is checked out next to this one):

```bash
python3 scripts/build-template-colors.py ../pin-generator-tool
python3 -m unittest discover -s tests
```

## License

MIT
