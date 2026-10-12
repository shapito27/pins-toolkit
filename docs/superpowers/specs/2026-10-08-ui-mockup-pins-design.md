# UI mockups instead of software screenshots: design

Date: 2026-10-08. Status: draft for review. Plan: [../plans/2026-10-08-ui-mockup-pins.md](../plans/2026-10-08-ui-mockup-pins.md).

## The request

The owner, after making pins for their own software pages with the plugin:

> what i noticed pin generation when I provide UI screenshot is awful. instead of putting UI
> screenshot, can it do realistic UI mockup?

and, after seeing one mockup pin:

> mockup is look much better. Now i'm thinking can I enhance plugin (skills, mcp ...) for Pinterest
> based on our conversation. Ask user rather to generate mockup instead of using screenshot.

and on 2026-10-12, widening the scope:

> based on our communication create/update skill - some websites if they don't have a proper
> image/images, need to create mockup of the app UI, important feature or concept.

## Scope widened on 2026-10-12 (implemented in the working tree)

The rule now covers any page with no image that works on a pin, not only software screenshots.
The text of record is `plugins/insightpins/skills/create-pin/references/ui-mockups.md` on branch
`claude/ui-mockup-pins`; where it differs from sections A1-A7 below, the file wins.

- **Three kinds of mockup:** app screen (a zoomed-in copy of one part of the real screen), feature
  (one feature at work, copied from a real screen), concept (a plain card drawn from the page's
  text: a list, steps, a small table, a comparison, one key number).
- **New trigger:** the page has no proper image (none, only hinted or low-resolution ones, or none
  that shows what the page is about) and its point can be drawn from its text.
- **An app-screen or feature mockup needs a real screen to copy.** Without one it would be an
  invented interface. The agent first looks at the product's home and features pages (two extra
  `extract_url` reads at most); if there is still nothing, it draws a concept card with no window
  bar and nothing styled as an app.
- **Never for photo-led content:** food, rooms, fashion, places, products bought for their look.
  A drawing there passes itself off as the real thing; the existing path (ask for a photo, or a
  text-only template) stays. Blocked pages also stay on their existing path.
- **Existing rules changed:** `create-pin` step 6 ("if only hinted images are left, ask for a
  photo...") and `template-selection.md` ("No photo at all") now mention the mockup for software,
  tool and feature pages. `optimize-pin` and `remake-pin` point to the reference.
- **Second eval case:** `no-photo-feature` (a SaaS feature page with only a hinted logo and author
  photo).

## What happened (evidence)

Pin for `https://insightpins.com/blog/best-pinterest-keyword-research-tools.html`, template
`checklist`, palette `deep-navy`, font `modern-sans`, six list items. All files are in
[`2026-10-08-ui-mockup-pins/`](2026-10-08-ui-mockup-pins/); the live links expire on 2026-10-15.

| Attempt | Image in the panel | Result |
| - | - | - |
| 1 | The article's table screenshot (`source-screenshot.webp`, 1923x899), `image_fit: "contain"` | A thin strip in an empty panel; no text readable. |
| 2 | The same screenshot, cropped to its left part (`image_focus` `{x: 0, y: 0.5}`) | `pin-before-screenshot.jpg`. Fills the panel, but the right-hand columns are cut off and the text is still about 14 px on a 1000 px pin, so under 4 px in the feed. |
| 3 | A mockup drawn for the panel (`keyword-explorer-mockup.html` -> `.png`, 1808x1488) | `pin-after-mockup.jpg`. Five rows, readable in the 200x300 preview, no render warnings. The owner: "much better". |

A second pin was made the same way the same day (`best-pinterest-analytics-tools.html`, `checklist`,
`berry-blush`, four items): `pin-stats-overlay-mockup.html` at 1808x1736 for a 904x868 panel,
result `pin6-after-mockup.jpg`, no warnings. It replaces a screenshot of Pinterest results full of
other people's pins with two plain colour cards carrying the extension's numbers.

After the owner's feedback the second pin was redone (`pin-stats-overlay-mockup-v2.png`, result
`pin6-after-mockup-v2.jpg`): no added captions, the overlay's icons redrawn by eye from an
enlarged crop of the public screenshot (`pin-stats-overlay-mockup-v2-icons.py`, written without
using the extension's source), the same two tiles, and a browser bar with `pinterest.com` and its
favicon. The first version (`pin6-after-mockup.jpg`) had invented text labels, one of them wrong
("Likes" for what the product calls reactions): a reason for the "drawn precisely" rule below.

How attempt 3 was made, by hand, in Claude Code:

1. Looked at the product's own pages to see the real interface (the site already draws a
   simplified Keyword Explorer panel on `keyword-explorer.html`).
2. Wrote one HTML file with inline CSS: a window bar, the seed keyword with its monthly searches,
   five related keywords with a bar and a number each. The numbers are the sample result shown on
   the site's free keyword tool page, not invented.
3. Captured it with headless Chrome at a 1808x1488 window, read the PNG to check it, fixed one
   overlap, captured again.
4. Uploaded the PNG with `create_upload_link` and rendered with `render_pin` (one upload, one render).

The panel size was measured from the first pin: about 904x744 px on the 1000x1500 pin for
`checklist` with six items. `list_templates` does not give it (`best_photo` only says "square").

## Why screenshots fail

A pin is shown about 230 px wide in the feed. A desktop screenshot is 1300-1900 px wide with 13-16 px
text. Scaled into a panel that is at most 900 px of a 1000 px pin, that text is 7 px on the pin and
under 2 px in the feed. Cropping instead of scaling keeps the text at 14 px on the pin (3 px in the
feed) and loses most of the screen. No setting of `image_focus`, `image_zoom` or `image_fit` fixes
both. The skills today say to skip images whose `alt` or file name says "screenshot"
(`create-pin` step 6), which on a software page leaves no image at all.

## Goal

When the subject of a pin is software and the available image is a screenshot of its interface,
the plugin should not put the screenshot on the pin. When the agent can build an image, it says
so in one line and makes a simplified mockup without waiting, by rules that keep the mockup honest
and readable. When it can't, it explains and offers choices.

Not goals: a general illustration generator; mockups for non-software content; changing how
photos are chosen.

## Scope

Two parts with different owners.

**A. Plugin (this repo, version 1.0.7).** Skill text, one new reference file, one eval case,
tests. Covered by the plan.

**B. Server (`pin-generator-tool`, not in this repo).** Recorded as new items in
[`docs/MCP-IMPROVEMENTS.md`](../../MCP-IMPROVEMENTS.md). Not in the plan. The plugin part must work
without them and get better when they arrive.

## A. Plugin behaviour

### A1. When the rule fires

Any of:

- the page is about software (app, SaaS tool, browser extension, dashboard, plugin) and the images
  that show the subject are screenshots of its interface;
- an image's `alt` or file name says "screenshot", "dashboard", "interface", "UI", "table",
  "settings", "report" or "extension popup";
- an image has `hint: "screenshot"` (planned on the server, see B1);
- the user hands over a screenshot as the pin photo;
- a rendered preview shows a screenshot whose text can't be read.

It does not fire for photos, product shots, or a photo of a phone or laptop with an app on it.

Detection before rendering is by text only (the agent can't see page images before a render), so it
will miss screenshots with no telling `alt` or file name. The last trigger (the preview) is the
backstop. B1 makes detection reliable.

### A2. Recommend the mockup, then build it

Decided by the owner on 2026-10-08: "recommend the mockup in one line and build it without waiting".

**The agent can build a mockup (A3):** it says in one line that the screenshot won't read at pin
size and that it is making a simplified mockup of that screen instead, says what it will show, and
builds it without waiting. It stops to ask first only when it has no real labels and numbers. The
user can still ask for the screenshot afterwards.

**The agent can't build one:** it says a mockup would work best, offers what can be done, and waits:

1. **A closer screenshot from the user**: one part of the screen, zoomed so a few big words or
   numbers fill it, portrait or square, uploaded as in `user-photos.md`.
2. **The screenshot as it is**, cropped to its most readable part, with a plain warning that the
   text will be small.
3. **No screenshot**: another fitting photo from the page, or a text-only template.

If the user already said what they want ("use the screenshot", "no mockup"), it does that, with no
mockup and no question.

### A3. Building a mockup, and when the agent can't

The agent can build a mockup only if it can write a file, run a headless browser to turn an HTML
page into a PNG, and read the PNG back (Claude Code, Cowork). In a chat without code tools it
can't. Then it must not promise one: it says a mockup would work best and offers the three choices
in A2. It never claims a mockup exists when it doesn't.

No script ships with the plugin (see "Constraints"). The reference file describes the steps in
words; the agent writes the HTML itself each time.

### A4. Mockup rules

- **Only real content.** Labels, column names and numbers come from the page, from the screenshot
  if the agent can read it, or from the user. No values available: ask for three to five rows.
  Never invent a metric or show better numbers than the product gives.
- **The real elements, drawn precisely.** Owner, 2026-10-08: "when do mockup, UI elements must be
  more precise. I liked that you zoomed and limited by 2 tiles only." A mockup is a zoomed-in,
  cleaned-up copy of the real screen, not a new design. The agent enlarges the screenshot, looks
  at the part it will show, and redraws each element as it is: same icons (redrawn as simple
  vector shapes), same order, same panel shape and transparency, similar font. Icon-only rows
  stay icon-only. The agent normally has no access to the product's source, so the screenshot and
  the product's public pages are the only references.
- **Zoom in instead of shrinking.** A small part of the screen shown large: two tiles of a grid,
  one panel, or five rows of a table.
- **Few, large elements.** One screen area, four to six rows, at most three columns. Row text at
  least 3% of the image width tall (about 60 px on an 1800 px image).
- **No fake controls.** No play buttons, cursors or "click here" arrows, and no buttons the
  product doesn't have. The real screen's own small action icons may be drawn as they are.
- **A browser bar for things that run on a website.** Owner, 2026-10-08: "because we know that
  extension for pinterest and it's opened browser of pinterest website, then can we also render in
  browser header pinterest domain with it favicon." For a browser extension, or anything that
  works inside another site, the mockup is framed by a plain browser bar with that site's domain
  and favicon. Only the domain and the favicon: no other part of that site's interface, nothing
  that suggests the site made or endorses the product.
- **No other people's content.** Plain colour blocks where the screenshot shows other people's
  photos, pins, avatars or names. (Two more pins from the same batch used screenshots full of
  third-party pin images; a mockup removes that exposure.)
- **Sized to the panel.** A `panel` template; image drawn at twice the panel size; important
  content at least 4% in from each edge. Known sizes of the `checklist` panel on the pin: 904x744 with six items, 904x868 with four.
- **Checked before upload.** The agent reads the PNG: no cut-off text, no overlap, every number as
  given.
- **Reported as a mockup.** The report says the image is a simplified mockup, where its content
  came from, and that the upload is kept for 7 days.

### A5. Existing rules this changes

| Rule today | Change |
| - | - |
| `create-pin` step 6: "Never use an image with a `hint`" and, if only hinted images are left, ask for a photo | `hint: "screenshot"` is the exception: it goes to A2, not to "ask for a photo". |
| `create-pin` step 6: skip images whose `alt` or file name says "screenshot" | On a software page, a screenshot of the subject is not skipped silently: it goes to A2. Elsewhere (a recipe post with a stray screenshot) it is still skipped. |
| `pin-design` "What not to do": "No fake play icons, fake app controls or 'click here' gimmicks" | Add the boundary: a simplified, non-interactive picture of the product's real screen with real labels and numbers is allowed; invented screens, invented numbers and pressable-looking controls are not. |
| `pin-design` defects: "Text baked into the photo (captions in GIFs or screenshots) ..." | Add a separate defect: a software screenshot as the photo. |
| `review-pin` rubric, criterion 3 | A full software screenshot with unreadable text scores low; the fix to suggest is a simplified mockup. |

### A6. Files

| File | Change |
| - | - |
| `plugins/insightpins/skills/create-pin/references/ui-mockups.md` | New. A1-A4 in full. |
| `plugins/insightpins/skills/create-pin/SKILL.md` | Step 2 (a "software or tool" content type), step 6 (the screenshot branch and the hint exception), step 9 (preview backstop), step 10 (report). |
| `plugins/insightpins/skills/create-pin/references/template-selection.md` | A "Software, app or tool page" row. |
| `plugins/insightpins/skills/pin-design/SKILL.md`, `references/design-checklist.md` | The defect, the boundary, a checklist item. |
| `plugins/insightpins/skills/review-pin/references/scoring-rubric.md` | Criterion 3 wording and the fix. |
| `evals/screenshot-image/` | New case (below). |
| `tests/test_plugin.py` | Text and grader checks. |
| `evals/README.md`, `plugins/insightpins/README.md`, `docs/PLAN.md`, `docs/MCP-IMPROVEMENTS.md`, `plugin.json` | Case row, one README sentence, links, server items, version 1.0.7. |

### A7. Eval case `screenshot-image`

A fictional time-tracking app's blog post ("5 reports ..."), whose only non-hinted images are two
wide dashboard screenshots with telling `alt` text, plus a hinted logo. Only `Skill` is allowed, so
the agent cannot build a mockup.

Graders: `create-pin` fires; `render_pin` is never called with a screenshot URL; the reply explains
why the screenshot won't read, says a simplified mockup would work best, offers at least one
choice it can carry out, does not claim a mockup was made, and invents no numbers.

A case where the agent builds a mockup needs a browser inside the eval sandbox and an upload mock
that accepts a file; left for later.

## B. Server items (for `MCP-IMPROVEMENTS.md`)

| # | Item | Why |
| - | - | - |
| B1 | `extract_url`: `hint: "screenshot"` on images that look like interface screenshots (wide, large flat areas, many small text runs). This finishes the open `likely_text` idea in item 3. | Makes A1 reliable; today detection depends on `alt` text. Must be released together with, or after, plugin 1.0.7: older plugin versions treat every hint as "never use" and would ask for a photo. |
| B2 | `render_pin`: an `IMAGE_TEXT_SMALL` warning when the photo has a lot of small text after scaling. | A backstop the agent can't miss; today it depends on judging a 200x300 preview. |
| B3 | `list_templates`: the photo panel's size on the pin (for example `photo_box: {width, height}`), per template. | The 904x744 panel was measured by hand from a rendered pin. A mockup, or any made-to-fit image, needs the exact shape. |
| B4 | A mockup tool: `render_mockup` with a few fixed layouts (keyword list with bars, table of up to three columns, one big number with a label), taking rows of data and a few brand colours, returning an `image_url`. | Makes mockups work in every app (chat has no browser), keeps them in one style, and removes the hand-written HTML. The honesty rules in A4 still apply to the data passed in. |

Order by value: B4 (the only way claude.ai users get mockups), B1, B3, B2.

## Constraints

- **No scripts in the plugin.** `docs/PLAN.md` decided "No hooks, agents, scripts, `bin/`", and the
  directory's security scan once held the plugin over the word `env` in a CSV script. So no bundled
  HTML-to-PNG or upload script.
- **Existing test guards apply to the new reference file:** no em or en dashes; none of `curl`,
  `-F file=`, `/api/uploads`, `multipart` in plugin files; no `assets/` paths outside the README.
  The reference describes the browser capture and the upload in words and points to `user-photos.md`.
- **No external URLs or `<script>` in any HTML shown in the reference.** Keep any example to a few
  lines of plain HTML and inline CSS, or leave it out; the full example lives in this spec's folder.
- **Limits:** a mockup pin costs one upload (10 a day) and one render. The agent says so when the
  user is low on either.
- **Works on older servers:** nothing in the plugin part needs B1-B4.

## Risks

| Risk | Mitigation |
| - | - |
| The agent invents plausible numbers for the mockup | The "only real content" rule is first in the reference; the eval's LLM grader fails invented numbers; the report must name the source of the content. |
| The rule nags users whose pins are not about software | Triggers are narrow (A1); the eval suite's existing photo cases (`recipe-from-url`, `hinted-photos`, `crop-warning`) must still pass unchanged. |
| A mockup implies a product or a screen that doesn't exist | "The real screen, simplified" rule; the boundary added to `pin-design`; `review-pin` criterion 8 (trust) already covers misleading images. |
| The security scan dislikes the new reference (browser, HTML) | Words only, no commands, no script tags, no URLs; run `claude plugin validate` before release. If it is held anyway, shorten the "Size and rendering" section to the size rules. |
| Hand-written mockups look different every time | Acceptable for 1.0.7; B4 fixes it. |
| The panel size differs by template and list length | The reference gives one measured size, tells the agent to estimate from `preview_templates` otherwise, and requires a 4% safe margin. B3 fixes it. |

## Open questions for the owner

1. **Ask, or recommend and proceed?** Answered 2026-10-08: recommend in one line and build without
   waiting (A2).
2. **What may the window bar say?** Answered 2026-10-08: for a product that runs on another site, the
   site's domain and favicon (A4). Note for the README and the directory review: the plugin already
   says it is not affiliated with Pinterest; a favicon in a browser bar is descriptive use, but it
   is another company's mark, so keep it to the bar.
3. **Should the two published-style examples go in the plugin README?** A before/after pair would
   show the feature, but the README's assets are checked by a test and both images are of the
   owner's own product.
4. **B1 timing.** If the server adds `hint: "screenshot"` before most users have 1.0.7, their
   plugin will refuse the image and ask for a photo. Acceptable, or hold B1 until 1.0.7 is published?
