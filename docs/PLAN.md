# InsightPins plugin for Claude - plan

Goal: publish a Claude plugin in Anthropic's directory that (1) connects Claude to the
InsightPins MCP server (`https://app.insightpins.com/mcp`) and (2) ships skills that teach
Claude how to make a good Pinterest pin, not just a rendered one. Later, (3) add a Pinterest
keywords MCP server so titles and descriptions are built on real search data.

Sources: [Plugin structure](https://claude.com/docs/plugins/build),
[Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist),
[Submit / withdraw / delist](https://claude.com/docs/plugins/submit).

---

## 1. Key decisions

| Decision | Recommendation | Why |
| - | - | - |
| One plugin or two (pins + keywords) | **One plugin**, add the keywords server to `.mcp.json` in a later version | Pin copy and keyword research are one workflow. Skills can use keyword tools when they exist and fall back gracefully when they don't. One listing, one install. |
| Plugin `name` | `insightpins` (permanent, never change) | Must be your own brand. Putting "pinterest" in `name`/`displayName` risks a **"Name matches a known brand"** reviewer hold. Mention Pinterest only descriptively in `description`/README. |
| `displayName` | `InsightPins` | Can be changed later. |
| Repo layout | Plugin in `plugins/insightpins/`, repo root holds `docs/`, `evals/` and a `marketplace.json` | Users install only the plugin folder, so plan docs, eval fixtures (a shell script and a JPEG) don't ship and can't trigger reviewer holds. The marketplace lets teams install from GitHub before the listing is live. (Changed in Phase 3; was repo root.) |
| Components | `.mcp.json` + skills + 1-2 commands. **No** hooks, agents, scripts, `bin/` | Skills, commands and remote MCP load on all surfaces (chat, Cowork, Claude Code). `bin/` would block claude.ai/Cowork install entirely. No executable code = no "Scripts the validator couldn't follow" holds and an easy security scan. |
| License | MIT (or your choice) via `LICENSE` + `license` field | Required to publish. |
| Connector | **Also submit the MCP server as an MCP connector** listing | Docs recommend submitting your own remote server separately. Use the exact same URL in `.mcp.json` so users with both see one set of tools. |

## 2. What the MCP server gives us (current tool surface)

| Tool | Notes for skills |
| - | - |
| `extract_url` | Title, description, site name, up to 10 images from a page |
| `list_templates` | 30 templates in 6 categories: blog, product, list, quote, recipe, creative. Each says `supports_subtitle` and `custom_fields` (price, cookTime, servings, listNumber, listPrefix, categoryLabel) |
| `list_styles` | 15 palettes (5 color families) + 10 font pairings |
| `render_pin` | 1000x1500 JPEG; title <= 200, description <= 500, CTA <= 30 chars; `text_size` 70-250 plus per-element sizes; up to 2 extra images; returns preview, 7-day link and `edit_url` |
| `get_quota` | Daily render limit, resets 00:00 UTC |

Implication: the skills must never hardcode the template/palette list as truth (it will change).
They should call `list_templates` / `list_styles` and use our references as *selection guidance*
keyed by category and mood, so new templates still work.

## 3. Repository layout

```
pins-toolkit/
├── .claude-plugin/
│   └── marketplace.json        # install from GitHub: /plugin marketplace add shapito27/pins-toolkit
├── plugins/
│   └── insightpins/            # the plugin = the folder submitted to the directory
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json
│       ├── skills/
│       │   ├── create-pin/      (SKILL.md, references/template-selection.md, style-selection.md)
│       │   ├── pin-design/      (SKILL.md, references/design-checklist.md)
│       │   ├── pin-copy/        (SKILL.md, references/title-formulas.md, description-and-seo.md)
│       │   ├── review-pin/      (SKILL.md, references/scoring-rubric.md)
│       │   ├── optimize-pin/    (SKILL.md)
│       │   └── remake-pin/      (SKILL.md)
│       ├── commands/
│       │   ├── pin.md              # /insightpins:pin <url>
│       │   └── pin-variations.md   # /insightpins:pin-variations <url> [n]
│       ├── README.md
│       └── LICENSE
├── evals/                      # claude plugin eval suite, mocked MCP (not shipped)
├── docs/
│   ├── PLAN.md
│   └── TEST-REPORT.md
├── README.md
└── LICENSE
```

`.mcp.json`:

```json
{
  "mcpServers": {
    "insightpins": {
      "type": "http",
      "url": "https://app.insightpins.com/mcp"
    }
  }
}
```

No API keys in any file. Auth must be the server's OAuth flow (users connect from the plugin's
**Connectors** tab). If the server ever needs a key instead, use `userConfig` with
`sensitive: true` and `${user_config.KEY}` - never a literal key, never `$ENV_VAR`.

`plugin.json`:

```json
{
  "name": "insightpins",
  "displayName": "InsightPins",
  "version": "0.1.0",
  "description": "Design and render Pinterest pins from any article, product or recipe URL, with built-in best practices for layout, readable text and search-friendly titles and descriptions.",
  "author": { "name": "InsightPins", "url": "https://insightpins.com" },
  "homepage": "https://insightpins.com",
  "license": "MIT"
}
```

## 4. Skills design

Principle: the MCP server's own instructions already cover the *mechanics* (extract, list, render,
report). Skills add the *judgement*: what makes a pin perform, which template fits which content,
how to write copy, when to re-render, how to save quota. Each `SKILL.md` stays short; detail lives in
`references/` and is loaded only when needed.

### 4.1 `create-pin` (orchestrator)

**description (trigger):** Use when the user wants a Pinterest pin, pin image or pin graphic for a
URL, blog post, product, recipe, list or quote, or asks to "make a pin" / "pin this".

Workflow:
1. Get the source: URL -> `extract_url`; no URL -> ask for title, image and site name.
2. Classify content: blog / how-to, listicle, product, recipe, quote, travel/lifestyle.
3. Write copy using `pin-copy` rules (on-image title is short; Pinterest title/description are separate, longer, keyword-rich).
4. Choose template via `references/template-selection.md` (content type -> 2-3 candidate templates, filled custom fields such as `listNumber` taken from the content, e.g. "17 easy dinners" -> 17).
5. Choose palette + font via `references/style-selection.md` (niche/mood -> palette family, and pick a palette that contrasts with the photo's dominant colors).
6. Pick the image: vertical or crop-safe, subject not in the text area, no text already baked in, highest resolution from `extract_url`.
7. `get_quota` before batch work; render once.
8. Inspect the preview against `pin-design` checklist; re-render only for real defects (unreadable text, wrong photo, cut-off title), adjusting `text_size`/`title_size` rather than switching everything.
9. Report: image link, `edit_url`, template/palette/font used, link expires in 7 days, photo source + licensing note, plus ready-to-paste **Pinterest title, description, alt text and suggested board**.

### 4.2 `pin-design` (visual best practices)

**description:** Use when choosing or judging how a Pinterest pin looks: layout, text overlay,
readability, colors, fonts, image choice, or when reviewing a pin before publishing.

Content (checklist in `references/design-checklist.md`):
- 2:3 vertical (1000x1500) - already the render default; never suggest other ratios.
- Thumbnail test: most viewers see the pin at ~200-250 px wide on mobile. On-image title readable at that size -> roughly 3-8 words, large weight, high contrast.
- One focal point; text in a calm area or on a solid band; avoid busy backgrounds behind text.
- Max 2 fonts (the font pairings already enforce this); bold sans or serif for headline.
- Brand consistency: same site name, consistent palette per site; `site_name` on every pin.
- Lifestyle/real-context photos beat plain product shots for most niches; faces optional.
- Avoid: tiny text, more than ~2 lines of subtitle, low-res or watermarked photos, clickbait claims, misleading imagery.
- Multiple pins per URL are fine and encouraged (fresh pins), but vary image + template + headline, not just color.

### 4.3 `pin-copy` (titles, descriptions, SEO)

**description:** Use when writing a Pinterest pin title, on-image headline, pin description, alt text,
or choosing keywords and boards for a pin.

Content:
- Three different texts: on-image headline (short, benefit-led), Pinterest pin title (up to 100 chars, keyword first), pin description (up to 500 chars, first ~50 chars carry the keyword, natural sentences, 2-4 related keywords, soft CTA).
- Headline formulas in `references/title-formulas.md`: number + outcome ("15 Cozy Fall Dinners Under 30 Minutes"), how-to, mistake-avoidance, before/after, "for [audience]".
- Alt text: literal description of the image for accessibility.
- No hashtag stuffing; no keyword lists; no promises the page doesn't deliver.
- Board suggestion: keyword-named board, not "My stuff".
- **Keywords hook (v2):** "If a keyword research tool is connected (InsightPins keywords), call it with the topic first and use the top relevant terms; otherwise derive keywords from the page title and description." This lets v1 ship now and v2 light up without rewriting skills.

### 4.4 `review-pin` (uploaded pin -> scored review)

**description:** Use when the user uploads or links a pin image and asks for feedback, a review, a
score, or "what's wrong with this pin" / "is this pin good".

- Claude reads the image itself (vision); no MCP call needed, no render quota used.
- Scores 1-10 on a fixed rubric (`references/scoring-rubric.md`): thumbnail readability, contrast,
  headline strength, focal point/layout, image quality and relevance, branding (site name, consistency),
  clarity of promise/CTA, Pinterest-fit (vertical 2:3, not an ad-looking banner).
- Output: overall score, top 3 fixes ranked by expected impact, what to keep, and a rewritten headline.
- Also reviews pin copy (title/description) if the user pastes it.

### 4.5 `optimize-pin` (review -> improved versions)

**description:** Use when the user wants to improve a pin's performance: more clicks, saves,
impressions, conversion, or to make it more noticeable / eye-catching.

- Runs the `review-pin` rubric first, then rebuilds: stronger headline (2-3 angles), better template
  for the content type, higher-contrast palette, larger `text_size`, better photo if a source URL is given.
- Renders 2-3 improved variants (quota-checked) designed as an A/B test: each variant changes one main
  lever (headline angle / layout / color) so the user learns what works.
- Also outputs optimized Pinterest title, description, alt text, and posting tips (fresh pins,
  seasonality, keyword boards).

### 4.6 `remake-pin` (uploaded pin -> similar but better)

**description:** Use when the user uploads a pin and wants one like it, a better version of it, or a
pin in the same style for their own content.

- Claude analyzes the uploaded pin: layout type, text hierarchy, color mood, font style, content type.
- Maps it to the closest InsightPins template + palette + font (from the live lists).
- **Image problem:** `render_pin` needs an image URL, and an image uploaded into chat has no URL. So the
  new pin's photo comes from: the user's own page (`extract_url`), an image URL the user gives, or the
  user's own pin if they confirm it's theirs and give its URL. Never reuse the uploaded pin as the
  background (it has text baked in).
- If it's someone else's pin: use it only as style inspiration, write original copy, don't copy their
  photo or wording.
- Then applies `pin-design` + `pin-copy` improvements, renders, and explains what was improved vs the original.
- **Server feature request:** an `upload_image` tool (or accepting base64 images) on the MCP would let
  users render with a photo they upload in chat. Worth adding to the server.

### 4.7 Commands

- `/insightpins:pin <url>` - runs `create-pin` end to end for one pin.
- `/insightpins:pin-variations <url> [n=3]` - checks quota, then makes n distinct pins (different template category, image, headline angle), and returns a comparison table.
- Skills are invocable as slash commands too (`/insightpins:review-pin`, `/insightpins:optimize-pin`,
  `/insightpins:remake-pin`), so they get no separate command files (same names would clash).

Possible later skills (not MVP): `seasonal-planning` (Pinterest seasonality - pin 30-45+ days ahead of holidays/seasons),
`brand-kit` (remember a site's preferred palette/font across pins).

## 5. Phases

### Phase 0 - decisions and prerequisites (done)
- [x] Plugin name `insightpins`; you own the InsightPins product and website.
- [x] License MIT; author "InsightPins", https://insightpins.com.
- [x] MCP server uses OAuth.
- [x] MCP connector already created.
- [ ] Make sure insightpins.com has a public privacy policy (the README points to it).
- [ ] Paid Claude plan; on Team/Enterprise an Owner must submit. GitHub connected on claude.ai for that org.

### Phase 1 - scaffold (v0.1.0) (done)
- [x] `plugin.json`, `.mcp.json`, `README.md` (>= 40 words outside code blocks), `LICENSE`.
- [x] README sections: what it does, how to use, components, **data handling** (what is sent to app.insightpins.com: page URLs, text, image URLs; rendered images hosted for 7 days; nothing else sent anywhere), photo licensing note.
- [x] `claude plugin validate ./plugins/insightpins` passes.

### Phase 2 - skills and commands (done)
- [x] Write `create-pin`, `pin-design`, `pin-copy` + references.
- [x] Write `review-pin` (+ rubric), `optimize-pin`, `remake-pin`.
- [x] Write the two commands (`pin`, `pin-variations`).
- [x] Keep every file < 256 KiB, text only, valid YAML frontmatter, `description` a single string.

### Phase 3 - evaluate (done, see [TEST-REPORT.md](TEST-REPORT.md))
- [x] Claude Code loads all 8 skills/commands (`claude -p --plugin-dir`).
- [x] Live run against the real MCP: 10 renders on 4 public pages (create, fix loop, review, optimize, remake, variations). 9 findings fed back into the skills; 7 requests for the server.
- [x] Eval suite (`evals/`, 6 cases, mocked MCP): all cases 1.00 with the plugin.
- [ ] claude.ai/Cowork: zip `plugins/insightpins`, **Customize > Plugins > Upload**, connect connector, try a few real prompts (needs you, in the browser).
- [ ] More eval cases later: no-URL request, "text is too small" follow-up, remake, optimize with numbers.

### Phase 4 - connector submission (if not already listed)
- [ ] Developer portal -> **Submit new -> MCP connector** for `https://app.insightpins.com/mcp`.

### Phase 5 - plugin submission
Full checklist and portal answers: [SUBMISSION.md](SUBMISSION.md). Local checks all pass; version 1.0.0.
- [ ] Portal: **Submit new -> Plugin bundle**, repository `shapito27/pins-toolkit`, plugin path `plugins/insightpins`, tracked branch `main`.
- [ ] **Validate**, fix Blocking findings, re-validate.
- [ ] Data handling answers: personal data - no (URLs and marketing copy only); sends data only to declared connector; retention - rendered images 7 days; under-18 - no.
- [ ] Compliance step, keep **GitHub push webhook**, submit.
- [ ] Repo can stay private during review (requires Claude GitHub App + source upload consent), must be **public before publishing**.
- [ ] After pass: **Publish**.

### Phase 6 - keywords MCP (v0.2.0 / v1.x)
- [ ] Keywords will live on the insightpins.com domain. Best option: add keyword tools to the **same**
  `app.insightpins.com/mcp` server - one OAuth sign-in, one connector, no `.mcp.json` change, no new
  destination for the security scan. If it must be a separate endpoint, add a second `.mcp.json` entry
  (e.g. `"insightpins-keywords": { "type": "http", "url": "https://app.insightpins.com/keywords/mcp" }`)
  and register it as a connector too.
- [ ] Update `pin-copy` with explicit tool names and flow: topic -> keywords -> pick primary + 2-4 secondary -> title/description/board.
- [ ] Possibly new skill `pin-keyword-research` (find keywords, trends, seasonality for a niche).
- [ ] Update README data-handling section; bump `version`; add evals. Submit the keywords server as a connector too.
- [ ] Note: a new remote destination may be looked at closely by the security scan - it must be declared in `.mcp.json` and the README.

### Phase 7 - maintenance
- [ ] Bump `version` on every release; merging to `main` triggers scan and publish per auto-publish setting.
- [ ] Track installs/errors on the portal **Usage** tab.
- [ ] If template/style IDs change on the server, skills keep working because they read the live lists.
- [ ] Withdraw (before publish) or **Delist plugin** (after publish) from the portal page; relist is a request.

## 6. Paid plans (pins and keyword explorer)

Planned: paid plans with higher limits for renders and keyword lookups. How this fits the plugin:

- Billing lives entirely on insightpins.com, never inside the plugin or the chat. The plugin stays free
  and MIT; it only gets more useful with a paid account.
- The server should return clear, structured errors when a limit is hit, e.g. `quota_exceeded` with
  `resets_at` and an `upgrade_url`. Skills will say: limit reached, resets at X UTC, higher limits are
  available at the upgrade link. One mention, no pushy upselling (directory policy and user trust).
- `get_quota` should report plan name and limits for both renders and keyword lookups, so skills can plan
  batches (variations, optimize) within what's left.
- Keep a usable free tier so reviewers and new users can test the plugin end to end. Consider giving
  Anthropic reviewers a test account if the free tier is very small.
- README "Usage limits" section must be updated when plans launch (mention paid plans and link to
  pricing). Any change that sends data somewhere new must be declared in README + `.mcp.json`.
- `review-pin` uses no quota (vision only) - a good free hook into the product.

## 7. Risks and mitigations

| Risk | Mitigation |
| - | - |
| Brand hold for "Pinterest" naming | Keep "Pinterest" out of `name`/`displayName`/`author.name` |
| Skills duplicate server instructions or conflict with them | Skills reference the server flow and add judgement only; same reporting rules (links, edit_url, 7-day expiry, photo source) |
| Quota burn from re-renders/variations | `get_quota` before batches; re-render only on defects; prefer `text_size` tweaks |
| Photo copyright | Always say where the image came from; recommend own images or licensed stock |
| Hardcoded template lists drift | Reference files give guidance by category; always call `list_templates`/`list_styles` |
| Skills don't trigger | Descriptions written as user situations ("make a pin", "pin this", "Pinterest graphic"); verify in evals |
| Pinterest best practices change | Keep them in `references/` so updates are a doc change + version bump |
| Name review: "InsightPins" is your product name but not a registered trademark | Fine for the directory; reviewers check it doesn't impersonate others. README includes a "not affiliated with Pinterest" disclaimer |
| Remaking someone else's pin = copying | `remake-pin` treats others' pins as style inspiration only; original copy and photos |

## 8. Open questions

1. Any brand voice or niche focus (food, home, travel, e-commerce) to bias defaults?
2. Can the server add an `upload_image` tool so users can use photos they upload in chat?
3. Can `get_quota` / limit errors return plan info and an upgrade URL (for paid plans)?
