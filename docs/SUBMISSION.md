# Submitting the InsightPins plugin

Step-by-step for the developer portal at [claude.ai/directory/manage](https://claude.ai/directory/manage),
with the answer for every field. Based on Anthropic's
[submit guide](https://claude.com/docs/plugins/submit) and
[pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).

## Your first validation (2026-10-04) and what changed

The portal validated `main` at the time (25 files, 341.7 kB) with these results:

| Portal check | Result | What it means | Status |
| - | - | - | - |
| Repository fetched; size limits; `plugin.json` valid | Passed | | |
| 7 skills, 2 commands, 1 MCP server (`insightpins`) | Passed | The portal sees exactly what we ship | |
| Name and publisher checks | Passed | | |
| Directory lints | Passed with warnings | The warnings are the icon and privacy URL rows below | Fixed |
| **Uses a credential from the user's machine** (`MCP_FORWARDS_CREDENTIAL_ENV`) | **Policy hold**, 2 findings | A pattern match, not a real credential read. `check_csv.py` started with `#!/usr/bin/env python3` (the scanner reads `env` as "prints the environment") and contains host names (`drive.google.com`, `dropbox.com`...) in its list of share links it rejects. Together that looked like "reads the environment and sends it to a host"; the second finding repeats it at plugin level because the plugin also has a remote MCP server. The scripts never read environment variables and make no network calls. | Fixed: both scripts lost the shebang (the skill runs them with `python3 -B`), and "Excel export" became "Excel format" in one message. A unit test now fails if either comes back |
| No icon (`ICON_MISSING`) | Warning | | Fixed: `.claude-plugin/icon.png`, your site's 512x512 logo |
| No privacy policy URL (`PRIVACY_URL_MISSING`) | Info | It found the URL in the README anyway | Fixed: `privacyPolicyUrl` in `plugin.json` |
| Images and fonts passed without a code check (`ASSETS_PASSED_UNREAD`) | Info | The two README example images were accepted as images | Nothing to do |

## Local checks (v1.0.0, after the fixes)

| Check | Result |
| - | - |
| `claude plugin validate ./plugins/insightpins` and `claude plugin validate .` | Passed |
| `python3 -m unittest discover -s tests` (38 tests: manifest, icon, privacy URL, file limits, README images, scanner triggers in scripts, contrast table, CSV scripts, graders) | Passed |
| Plugin files | 26: 23 text files (largest ~16 KB), 2 JPEG example images (122 KB, 166 KB), 1 PNG icon (35 KB) |
| Name, `description`, `author`, `version`, `license`, LICENSE file, README >= 40 words | Yes |
| `.mcp.json`: one remote `type: http` server, `https://app.insightpins.com/api/mcp`, no secrets | Yes |
| No hooks, local MCP servers, `bin/`, symlinks, junk files or package launchers | None |
| Scripts | 2 Python scripts in `pinterest-bulk-csv`, standard library only, no network, no environment reads; disclosed in the README |
| Repository < 50 MiB, < 10,000 files | ~0.6 MB, 141 files |
| Eval suite | All 14 cases 1.00 with the plugin (2026-10-04) |

## Step by step from here

1. **Merge the pull request with these fixes into `main`.** The portal reads the tracked branch.
2. **Decide on the icon before anything else is saved.** The portal takes the icon from
   `.claude-plugin/icon.png` only the first time the plugin is saved or submitted, and changing it
   later doesn't change the listing. The current file is your site's 512x512 magnifying-glass logo
   (`insightpins.com/assets/images/android-chrome-512x512.png`). To use a different one, replace
   that file (square PNG, 512-2048 px, under 2 MB) and merge before step 3.
3. **Re-validate** the submission in the portal (**Check for new commits** or **Re-validate** on
   the Versions tab, branch `main`). Expect:
   - the policy hold gone, or still listed but now explainable (see the note below);
   - no icon or privacy URL warnings;
   - only the info row about the two images.
   If your draft was already saved before the icon existed and the listing preview still shows no
   icon, withdraw that draft and start a new submission (allowed while it isn't published), or
   ask Anthropic support to pick it up.
4. **If the credential finding is still there,** it isn't blocking: a reviewer confirms it. Where
   the portal asks for a note to the reviewer, paste:
   > The flagged file `skills/pinterest-bulk-csv/scripts/check_csv.py` reads no environment
   > variables or credentials and makes no network requests (standard library only: argparse,
   > csv, io, json, re, sys, collections, datetime, and urllib.parse to parse URLs). The host names in it
   > (drive.google.com, dropbox.com...) are a deny list: the checker reports Pinterest bulk-upload
   > rows whose image link points to a share page instead of an image file. The plugin's only
   > network access is the declared InsightPins connector at app.insightpins.com.
5. **Listing details:** check the name, description and icon preview (they come from `plugin.json`
   and the README).
6. **Data handling, compliance and submit:** answers are in "Portal steps and answers" below
   (personal data **Yes**, contact `ruslan@insightpins.com`, all four acknowledgements). Keep
   **GitHub push webhook** for updates and leave auto-publish at the default.
7. **Before you select Publish:** make the repository public, and make sure a brand-new
   InsightPins account can sign in and render a pin (a reviewer will try).
8. **After publishing:** for every update, merge to `main` and raise `version` in `plugin.json`.

## Before you open the portal

- [x] **Plugin on `main`** (PRs #1-#5 merged; merge the PR with the validation fixes too).
- [x] **Connector URL is exactly `https://app.insightpins.com/api/mcp`** (the MCP server, also the
      OAuth token audience). `https://app.insightpins.com/mcp` is only the human docs page.
- [x] **Privacy policy and terms cover the Claude connector** (both updated 03.10.2026; the
      plugin README and `privacyPolicyUrl` point to the privacy policy).
- [x] **Security item** in [MCP-IMPROVEMENTS.md](MCP-IMPROVEMENTS.md): fix deployed 2026-10-03;
      internal addresses refused from outside. Cover redirects and `render_pin` image URLs in server tests.
- [ ] **Free tier works for a new account**, so a reviewer can sign in and render a pin.
- [ ] **Optional: test on claude.ai.** Zip `plugins/insightpins`, then go to **Customize > Plugins >
      Add > Upload plugin**, connect InsightPins and make one pin.
- [x] **GitHub account connected** on claude.ai (you've validated already). On Team or Enterprise
      plans, an Owner must submit.
- [ ] **Repository visibility:** it can stay private while validating and in review. It **must be
      public before publishing**.

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
     Blocking or held (tell me the finding), push, then **Re-validate**. The first run's findings
     and fixes are in the table at the top.
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
  If the CSV rules changed on the website (`insightpins.com/downloads-src/pinterest-bulk-csv`), first
  copy its scripts and `reference.md` into `plugins/insightpins/skills/pinterest-bulk-csv/` and run
  `python3 scripts/check-bulk-csv-sync.py ../insightpins.com` (must print "0 mismatches").
- **Withdraw or delist:** **Withdraw submission** while in review; **Delist plugin** from the page
  menu once live. **Relist plugin** brings it back (as a request).

## Listing copy (for reference)

**Name:** InsightPins

**Short description:** Create, review and optimize Pinterest pins from any article, product or
recipe URL. Renders 1000x1500 pins from InsightPins templates and applies pin design and
copywriting best practices.

**What users get:** 7 skills (create-pin, pin-design, pin-copy, review-pin, optimize-pin,
remake-pin, pinterest-bulk-csv) and 2 commands (`/insightpins:pin`, `/insightpins:pin-variations`), plus the
InsightPins connector.
