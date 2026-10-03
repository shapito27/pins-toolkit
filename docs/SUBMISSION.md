# Submitting the InsightPins plugin

Step-by-step for the developer portal at [claude.ai/directory/manage](https://claude.ai/directory/manage),
with the answer for every field. Based on Anthropic's
[submit guide](https://claude.com/docs/plugins/submit) and
[pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).

## Status of the automated checks (checked locally, v1.0.0)

| Check | Result |
| - | - |
| `claude plugin validate ./plugins/insightpins` | Passed |
| `claude plugin validate .` (marketplace) | Passed |
| Folder contains `.claude-plugin/plugin.json` | Yes |
| Name `insightpins`: lowercase, hyphens, not reserved, not a known brand | Yes |
| `description`, `author`, `version`, `license` set | Yes |
| README >= 40 words outside code blocks | 768 words |
| LICENSE file + `license` field | Yes (MIT) |
| No `.DS_Store` / `Thumbs.db` / `__MACOSX`, no symlinks, no LFS, no `.gitattributes` | None |
| Every file < 256 KiB, <= 512 files, text only | 18 text files, largest ~6 KB |
| `.mcp.json` valid, remote server is `type: http` with an `https://` URL | Yes |
| No secrets, no `$ENV` credentials, no package launchers (`npx`, `uvx`...) | None |
| No hooks, scripts, local MCP servers or `bin/` | None (skills, commands and a remote MCP only) |
| Repository < 50 MiB, < 10,000 files | ~0.8 MB, 65 files |
| Eval suite | All 6 cases 1.00 with the plugin |

Expected result in the portal: no Blocking findings. A reviewer may still look at it (first
submissions are published by an Anthropic reviewer by default).

## Before you open the portal

- [ ] **Merge PR #1 into `main`.** The directory follows the tracked branch, so the plugin must be on `main`.
- [ ] **Confirm the connector URL is exactly `https://app.insightpins.com/mcp`**, the same as in
      `plugins/insightpins/.mcp.json`, so users with both see one set of tools.
- [ ] **Privacy policy:** make sure insightpins.com has a public privacy policy page. Send me its
      URL and I'll link it from the plugin README (it currently says "on insightpins.com").
- [ ] **Check the security item** in [MCP-IMPROVEMENTS.md](MCP-IMPROVEMENTS.md) (URL fetching
      can't reach internal addresses). The security scan reads the plugin, but reviewers also use the connector.
- [ ] **Free tier works for a new account**, so a reviewer can sign in and render a pin.
- [ ] **Optional: test on claude.ai.** Zip `plugins/insightpins`, then go to **Customize > Plugins >
      Add > Upload plugin**, connect InsightPins and make one pin.
- [ ] **GitHub account connected** on claude.ai in the organization you submit from. On Team or
      Enterprise plans, an Owner must submit.
- [ ] **Repository visibility:** it can stay private while validating and in review (the Claude
      GitHub App is installed). It **must be public before publishing**.

## Portal steps and answers

1. **Submit new -> Plugin bundle.**
2. **Source**
   - Repository: `shapito27/pins-toolkit`
   - Plugin path: `plugins/insightpins`
   - Branch or tag: `main`
   - Select **Validate**. If the repo is private, confirm the source upload. Fix anything marked
     Blocking (tell me the finding), push, then **Re-validate**.
3. **Listing details:** read from `plugin.json` and the README. To change anything, edit the files
   and re-validate. Name and description: "InsightPins" / "Create, review and optimize Pinterest
   pins from any article, product or recipe URL..."
4. **Data handling** (suggested answers, adjust if your service differs):

   | Question | Answer | Why |
   | - | - | - |
   | Does the plugin read or store personal data? | **No** | The plugin is instructions plus a connector reference. It sends page URLs, pin text and image URLs; it stores nothing. Account data is handled by the InsightPins connector under its own privacy policy. |
   | Does it send data to services other than its declared connectors? | **No** | Only `app.insightpins.com` (declared in `.mcp.json`). |
   | How long is data kept? | The plugin keeps nothing. InsightPins hosts rendered images for 7 days. | Matches the README. |
   | Intended for people under 18? | **No** | |

5. **Compliance:** check the contact email (use an address you read, ideally a support or business
   address), and select all four acknowledgements.
6. **Review and submit**
   - How new versions arrive: keep **GitHub push webhook** (needs admin on the repo). Then select
     **Set up push updates** on the next page.
   - Auto-publish: leave the default. A reviewer publishes the first version.
   - Select **Submit for review**.

## After submitting

- Track it under **Submissions**. The **Versions** tab shows each scanned commit.
- **Passes every check:** select **Publish** (a reviewer publishes it). Make the repo public first.
- **Held for a reviewer:** wait. A hold is not a rejection.
- **Doesn't pass:** send me the findings. I'll fix them and push, then you select **Check for new commits**
  (or **Resubmit for review** if it was rejected).
- **Releasing updates later:** merge to `main` and raise `version` in `plugin.json` each time.
- **Withdraw or delist:** **Withdraw submission** while in review; **Delist plugin** from the page
  menu once live. **Relist plugin** brings it back (as a request).

## Listing copy (for reference)

**Name:** InsightPins

**Short description:** Create, review and optimize Pinterest pins from any article, product or
recipe URL. Renders 1000x1500 pins from InsightPins templates and applies pin design and
copywriting best practices.

**What users get:** 6 skills (create-pin, pin-design, pin-copy, review-pin, optimize-pin,
remake-pin) and 2 commands (`/insightpins:pin`, `/insightpins:pin-variations`), plus the
InsightPins connector.
