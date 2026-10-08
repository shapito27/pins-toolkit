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

## Submitting to OpenAI

There is one submission, not two: the plugin goes in as a ZIP with its MCP server, and OpenAI's
review covers the server (as the ChatGPT app) and the skills together. Don't submit a skills-only
version first: OpenAI can't add an MCP server to a plugin that was submitted without one.

### Before you open the form

1. **Server changes** (pin-generator-tool), needed before OpenAI scans the tools:
   - Every tool must set `readOnlyHint`, `openWorldHint` **and** `destructiveHint`; a missing hint
     blocks the submission. Today the six read-only tools (`extract_url`, `list_templates`,
     `preview_templates`, `list_styles`, `get_quota`, `get_upload`) have no `destructiveHint`: add
     `destructiveHint: false` to each.
   - Domain check: OpenAI shows a token in the form; serve it as plain text at
     `https://app.insightpins.com/.well-known/openai-apps-challenge`.
   - Optional: no tool declares an `outputSchema`. OpenAI warns about it but doesn't block.
2. **Account**: a verified OpenAI platform organization, and the Apps Management role with write
   access. The developer name in the form must match the verified identity.
3. **Reviewer sign-in**: the server signs in with Google. The form asks for test credentials; make
   a separate Google account for the reviewers (not your own), or say in the form that any Google
   account works.
4. **The ZIP**: the contents of `plugins/insightpins/`, with `.codex-plugin/plugin.json` at the
   top level of the ZIP.

### In the form

- Choose a plugin **with MCP** and give `https://app.insightpins.com/api/mcp`. The host can't
  change later without a new submission.
- Import [`chatgpt-app-submission.json`](chatgpt-app-submission.json): it fills in the app info,
  a one-sentence reason for each tool's three hints, 5 test prompts and 3 prompts that shouldn't
  use the app. Its hints match the server once the `destructiveHint` change above is live. Run
  every test prompt in ChatGPT yourself before submitting.
- Listing: name, short description, icon, screenshots, privacy policy and terms URLs (the same
  as the Claude listing).

### Hint choices to be ready to defend

OpenAI reads `openWorldHint` as "changes something public or outside the app". Two tools set it
to `true`, which matches the MCP meaning the Claude directory uses:

- `extract_url` reads a public web page. It's read-only, so the hint doesn't add a confirmation.
- `render_pin` hosts the pin at an unlisted link anyone with the link can open for 7 days. It
  never posts to Pinterest. ChatGPT may ask the user to confirm each render because of it. If
  reviewers ask for `false`, change it on the server; the Claude listing doesn't depend on it.

The submission file gives the reason for each. After approval, if OpenAI gives the plugin an app
ID, add it as `.app.json` (`{"apps": {"insightpins": {"id": "asdk_app_..."}}}`) and
`"apps": "./.app.json"` in `.codex-plugin/plugin.json`.

Until then, anyone can install the plugin in Codex from this repo with the commands in the
[README](../README.md#try-it).
