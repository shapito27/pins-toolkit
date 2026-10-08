# The plugin on OpenAI (Codex and ChatGPT)

The folder `plugins/insightpins/` is one plugin for both Claude and OpenAI. The skills, commands,
`.mcp.json` and README are shared; each side has its own manifest:

| File | Read by |
| - | - |
| `.claude-plugin/plugin.json` (plugin) and `.claude-plugin/marketplace.json` (repo root) | Claude |
| `.codex-plugin/plugin.json` (plugin) and `.agents/plugins/marketplace.json` (repo root) | Codex and ChatGPT |
| `skills/*/agents/openai.yaml` | Codex and ChatGPT: each skill's display name and starter prompt |
| `assets/logo.png` | The OpenAI listing's logo (a copy of `.claude-plugin/icon.png`) |

Neither side reads the other's files. The layout follows OpenAI's examples in
[openai/plugins](https://github.com/openai/plugins).

## Keeping the two in step

- Bump `version` in **both** manifests. `tests/test_plugin.py` (`OpenAIManifestTest`) fails when
  the name, version, description, author, links or keywords differ.
- Write skills for any agent. Where a skill needs something only one app has, name both:
  `create-pin` tells the user where to connect the server in either app, and `pinterest-bulk-csv`
  says what to use when `${CLAUDE_SKILL_DIR}` is empty (Codex leaves it empty).
- A merge to `main` still goes to Claude directory review through the webhook, even when only the
  OpenAI files changed.

## Checked on 2026-10-08 with Codex CLI 0.161.0

```bash
codex plugin marketplace add /path/to/pins-toolkit
codex plugin add insightpins@insightpins      # installed, enabled, version 1.0.7
codex mcp list                                 # insightpins, https://app.insightpins.com/api/mcp
codex mcp login insightpins                    # opens the InsightPins Google sign-in
codex debug prompt-input "hi"                  # lists all 7 skills as insightpins:<skill>
```

Not checked yet: a full pin run in Codex. It needs a Codex login and the InsightPins sign-in in a
browser. The evals (`claude plugin eval`) only run in Claude.

## Next steps

1. **Get the server approved as a ChatGPT app.** Public plugins go into one directory shared by
   ChatGPT and Codex, and a plugin with live tools needs its MCP server approved as an app first.
   Expect OpenAI's own review of the privacy policy, the tools (read-only and write hints on each
   tool help) and the sign-in.
2. **Add `.app.json`** with the app ID from that approval, and `"apps": "./.app.json"` in
   `.codex-plugin/plugin.json`:

   ```json
   { "apps": { "insightpins": { "id": "asdk_app_..." } } }
   ```
3. **Submit the plugin** to OpenAI's plugin directory.

Until then, anyone can install it in Codex from this repo with the commands in the
[README](../README.md#try-it).
