# pins-toolkit

Source for the **InsightPins** plugin for Claude: create, review and optimize Pinterest pins with the
[InsightPins](https://insightpins.com) pin generator and built-in pin design and copywriting best practices.

| Path | What it is |
| - | - |
| [`plugins/insightpins/`](plugins/insightpins/) | The plugin itself (manifest, MCP connector, skills, commands). This is the folder submitted to the Claude directory. See its [README](plugins/insightpins/README.md). |
| [`evals/`](evals/) | `claude plugin eval` suite with mocked InsightPins tools (no real renders) |
| [`docs/PLAN.md`](docs/PLAN.md) | Roadmap and design decisions |
| [`docs/SUBMISSION.md`](docs/SUBMISSION.md) | Directory submission checklist and portal answers |
| [`docs/TEST-REPORT.md`](docs/TEST-REPORT.md), [`docs/MCP-IMPROVEMENTS.md`](docs/MCP-IMPROVEMENTS.md) | Test results and ranked server improvement ideas |
| `.claude-plugin/marketplace.json` | Lets you install the plugin straight from this repo |

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
claude plugin eval . --no-publish --scaffold
```

`--scaffold` lets the review case copy its fixture image into the run's workspace.

## License

MIT
