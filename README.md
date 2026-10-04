# pins-toolkit

Source for the **InsightPins** plugin for Claude: create, review and optimize Pinterest pins with the
[InsightPins](https://insightpins.com) pin generator and built-in pin design and copywriting best practices,
and build or check Pinterest bulk upload CSV files.

| Path | What it is |
| - | - |
| [`plugins/insightpins/`](plugins/insightpins/) | The plugin itself (manifest, MCP connector, skills, commands). This is the folder submitted to the Claude directory. See its [README](plugins/insightpins/README.md). |
| [`evals/`](evals/) | `claude plugin eval` suite with mocked InsightPins tools (no real renders) |
| [`docs/PLAN.md`](docs/PLAN.md) | Roadmap and design decisions |
| [`docs/SUBMISSION.md`](docs/SUBMISSION.md) | Directory submission checklist and portal answers |
| [`docs/TEST-REPORT.md`](docs/TEST-REPORT.md), [`docs/MCP-IMPROVEMENTS.md`](docs/MCP-IMPROVEMENTS.md) | Test results and ranked server improvement ideas |
| `.claude-plugin/marketplace.json` | Lets you install the plugin straight from this repo |
| [`scripts/check-bulk-csv-sync.py`](scripts/check-bulk-csv-sync.py) | Checks the plugin's CSV checker against the insightpins.com fixtures |

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
claude plugin eval . --no-publish --scaffold --allow-tools Bash
```

`--scaffold` lets two cases copy their fixture into the run's workspace; `--allow-tools Bash` lets the
bulk CSV case run the checker script.

## The bulk CSV skill has a source of truth elsewhere

`plugins/insightpins/skills/pinterest-bulk-csv/` is a copy of `downloads-src/pinterest-bulk-csv/` in the
`insightpins.com` repo, whose `check_csv.py` also defines the rules of the
[web CSV checker](https://insightpins.com/tools/pinterest-csv-checker.html). The plugin copy adds
script paths (`${CLAUDE_SKILL_DIR}`), a "just checking a file?" path and notes for pins made with
InsightPins; the scripts and `reference.md` are unchanged. When the rules change there, copy the
scripts and `reference.md` again and re-run that repo's fixtures against the copy (all 41 matched
on 2026-10-04):

```bash
cp ../insightpins.com/downloads-src/pinterest-bulk-csv/reference.md plugins/insightpins/skills/pinterest-bulk-csv/
cp ../insightpins.com/downloads-src/pinterest-bulk-csv/scripts/*.py plugins/insightpins/skills/pinterest-bulk-csv/scripts/
python3 scripts/check-bulk-csv-sync.py ../insightpins.com   # must print "0 mismatches"
```

## License

MIT
