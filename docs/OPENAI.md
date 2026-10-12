# The plugin on OpenAI (Codex and ChatGPT)

The folder `plugins/insightpins/` is one plugin for both Claude and OpenAI. The skills, commands,
`.mcp.json` and README are shared; each side has its own manifest:

| File | Read by |
| - | - |
| `.claude-plugin/plugin.json` (plugin) and `.claude-plugin/marketplace.json` (repo root) | Claude |
| `.codex-plugin/plugin.json` (plugin) and `.agents/plugins/marketplace.json` (repo root) | Codex and ChatGPT |
| `skills/*/agents/openai.yaml` | Codex and ChatGPT: each skill's display name and starter prompt |
| `assets/logo.png` | The OpenAI listing's logo (a copy of `.claude-plugin/icon.png`) |

Claude doesn't read the OpenAI files. This uses OpenAI's Codex layout (`.codex-plugin/plugin.json`
plus `.mcp.json`), which their docs list as supported and which the examples in
[openai/plugins](https://github.com/openai/plugins) use. Their newer "portable" layout (a root
`plugin.json` with an `extensions.com.openai` block and a root `mcp.json` with
`"type": "streamable-http"`) is recommended for new packages but not required; move to it only if
the submission portal asks.

## Keeping the two in step

- Bump `version` in **both** manifests. `tests/test_plugin.py` (`OpenAIManifestTest`) fails when
  the name, version, description, author, links or keywords differ.
- Write skills for any agent. Where a skill needs something only one app has, name both:
  `create-pin` tells the user where to connect the server in either app, and `pinterest-bulk-csv`
  says what to use when `${CLAUDE_SKILL_DIR}` is empty (Codex leaves it empty).
- A merge to `main` still goes to Claude directory review through the webhook, even when only the
  OpenAI files changed.

## Checked on 2026-10-08 with Codex CLI 0.161.0 (1.0.7, and 1.0.8 installed again)

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

From OpenAI's [submission guide](https://developers.openai.com/plugins/deploy/submission), read on
2026-10-08. One ZIP holds the skills and the MCP server, and review covers both. Don't submit a
skills-only version first: OpenAI can't add an MCP server to a plugin submitted without one.

### Before you open the portal

1. **Server** (pin-generator-tool):
   - Every tool sets `readOnlyHint`, `destructiveHint` and `openWorldHint` (done: pin-generator-tool
     #127).
   - Domain check: the portal shows a token. Serve it exactly, as plain text (not JSON), at
     `https://app.insightpins.com/.well-known/openai-apps-challenge` (the MCP host, or a parent
     domain OpenAI accepts).
   - Optional: no tool declares an `outputSchema`. OpenAI warns about it but doesn't block.
2. **Account**: the organization owner, or a member with Apps Management write access, and a
   completed individual or business verification. The developer name must match it.
3. **Reviewer sign-in**: a dedicated test account with some sample data (a few pins made). It must
   work **without MFA, email or SMS codes, or magic links**. The server signs in only with Google,
   and Google often asks a new account for a phone or email code on a new device: sign in to the
   test account from several browsers first, turn off 2-Step Verification, and check it still signs
   in without a code. If it can't, reviewers can't get in, which is the most common rejection.
4. **Review material**: a video walkthrough URL reviewers can open (a pin made from a link, from
   the user's own photo, and the daily limit), and release notes.
5. **The ZIP**: `python3 scripts/build-openai-zip.py` writes `insightpins-openai-<version>.zip`
   with `.codex-plugin/plugin.json` at the top and without the Claude manifest. It must not contain
   `.app.json`, an `apps` entry or hooks: OpenAI can't take those yet (the tests check).

### In the portal

1. **Plugins > Upload new or existing plugin**, choose your verified developer identity, upload
   the ZIP. Fix any metadata or skill-scan findings and upload again (bump the version for each
   ZIP).
2. **MCP**: connect the server from the ZIP's `.mcp.json`, pass the domain check, wait for the tool
   scan and fix its findings (Rescan after a deploy). One MCP server per plugin; changing its URL
   later needs OpenAI support.
3. **Review details**: the five test cases and three negative ones, the reviewer account, the
   video URL and the release notes. [`chatgpt-app-submission.json`](chatgpt-app-submission.json)
   has the test cases, app info and a one-sentence reason for each tool's hints. Import it if the
   form offers it, or copy from it. Run every test prompt in ChatGPT yourself first.
4. **Submit for review**, complete the attestations. Feedback comes by email; after approval,
   select **Publish plugin**.

Listing limits (tested in `OpenAIManifestTest`): display name and short description 30 characters
each, long description 4000, up to 3 starter prompts of 128 characters. The website, support,
privacy and terms URLs must be HTTPS.

### After it's live

- A change to skills, metadata or images needs a new ZIP and a new review. Merging to main here
  also sends the Claude version to review, so bump both manifests.
- Server changes are scanned daily (or Rescan). Changed tools that pass go live on their own; a
  flagged tool keeps its last approved definition until it's approved.

### Hint choices to be ready to defend

OpenAI reads `openWorldHint` as "changes something public or outside the app". Two tools set it
to `true`, which matches the MCP meaning the Claude directory uses:

- `extract_url` reads a public web page. It's read-only, so the hint doesn't add a confirmation.
- `render_pin` hosts the pin at an unlisted link anyone with the link can open for 7 days. It
  never posts to Pinterest. ChatGPT may ask the user to confirm each render because of it. If
  reviewers ask for `false`, change it on the server; the Claude listing doesn't depend on it.

Until it's approved, anyone can install the plugin in Codex from this repo with the commands in
the [README](../README.md#try-it).
