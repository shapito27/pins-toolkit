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
- [ ] **Confirm the connector URL is exactly `https://app.insightpins.com/api/mcp`** (the MCP server,
      also the OAuth token audience). `https://app.insightpins.com/mcp` is only the human docs page;
      a client pointed there can't connect. It must be the same as in
      `plugins/insightpins/.mcp.json`, so users with both see one set of tools.
- [x] **Privacy policy and terms cover the Claude connector** (both updated 03.10.2026; the
      plugin README matches the privacy policy).
- [x] **Security item** in [MCP-IMPROVEMENTS.md](MCP-IMPROVEMENTS.md): fix deployed 2026-10-03;
      internal addresses refused from outside. Cover redirects and `render_pin` image URLs in server tests.
- [ ] **Free tier works for a new account**, so a reviewer can sign in and render a pin.
- [ ] **Optional: test on claude.ai.** Zip `plugins/insightpins`, then go to **Customize > Plugins >
      Add > Upload plugin**, connect InsightPins and make one pin.
- [ ] **GitHub account connected** on claude.ai in the organization you submit from. On Team or
      Enterprise plans, an Owner must submit.
- [ ] **Repository visibility:** it can stay private while validating and in review (the Claude
      GitHub App is installed). It **must be public before publishing**.

## Privacy policy and terms: what's missing

Checked on 2026-10-03: [privacy.html](https://insightpins.com/privacy.html) (updated 29.09.2026)
and [terms-of-use.html](https://insightpins.com/terms-of-use.html) (updated 09.08.2026).

- The privacy policy covers the extension, the website and the Pin Generator web app, but **not the
  MCP connector used by Claude**. Reviewers compare the policy with what the connector does.
- The terms list the extension, the Keyword Explorer, the free keyword tool and the website. They
  **don't cover the Pin Generator or the connector**.

Suggested privacy policy section. The account data matches what you told me the sign-in collects;
check the two bracketed parts against what your server really does before publishing:

> **The InsightPins connector for Claude (app.insightpins.com/api/mcp)**
> When you connect InsightPins to Claude, you sign in with your Google account. This creates an
> InsightPins account with: your email address, your Google account ID (which identifies you), your
> name (which can be empty), the date the account was created and, if you close it, the date it was
> closed. We use this to identify you and count your daily renders. We don't receive your Google
> password or access to your Google data beyond these details.
> [When you close your account, we delete your email address, name and Google account ID and keep
> only the creation and closing dates.]
> When Claude makes a pin for you, it sends us the page URL you asked about, the pin text (headline,
> subtitle, button text and site name), the image URLs and your design choices. We fetch the page to
> read its title, description and images, and do not keep the extracted content after responding.
> Rendered pin images are stored for 7 days so you can download them, then deleted. We keep
> [a count of renders per account per day] for limits and abuse prevention.
> We do not receive your Claude conversation, files you upload to Claude, or anything other than what
> the connector's tools send.

Suggested addition to the terms: name the Pin Generator and the Claude connector in the list of
Services in section 1, with their daily render limits.

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
   | Does the plugin read or store personal data? | **Yes** | The plugin files store nothing, but signing in to the connector creates an InsightPins account with the user's email, Google account ID, name and account dates. Answering Yes and describing this is safer than a No that a reviewer could see contradicted by the sign-in screen and privacy policy. Pin content sent (page URLs, pin text, image URLs) isn't personal data. |
   | Does it send data to services other than its declared connectors? | **No** | Only `app.insightpins.com` (declared in `.mcp.json`). |
   | How long is data kept? | Account data (email, Google account ID, name) and render records (time, design choices, headline) as long as the account exists; rendered images 7 days; unused connections expire after 30 days; extracted page content is not kept. | Matches the README and the privacy policy updated 03.10.2026. |
   | Intended for people under 18? | **No** | |

5. **Compliance:** contact email `ruslan@insightpins.com`, and select all four acknowledgements.
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
