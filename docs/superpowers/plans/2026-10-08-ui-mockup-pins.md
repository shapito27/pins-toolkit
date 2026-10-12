# UI Mockups Instead of Software Screenshots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When a pin's subject is software and the available image is a screenshot of its interface, the plugin doesn't put the screenshot on the pin: where the agent can build an image it says so in one line and makes a simplified mockup without waiting, by rules that keep it honest and readable; where it can't, it explains and offers choices.

**Architecture:** Skill text only. One new reference file (`create-pin/references/ui-mockups.md`) holds the whole procedure; `create-pin`, `pin-design` and `review-pin` get short pointers to it. One new eval case and unit tests pin the behaviour. Server-side ideas are recorded in `docs/MCP-IMPROVEMENTS.md` and not built here.

**Tech Stack:** Markdown skills, Python 3 `unittest` (standard library only), `claude plugin validate`, `claude plugin eval` with mocked MCP tools.

**Spec:** [`docs/superpowers/specs/2026-10-08-ui-mockup-pins-design.md`](../specs/2026-10-08-ui-mockup-pins-design.md). Read it first: it has the evidence, the rules (A1-A5) and the open questions for the owner (question 1 is answered). The owner chose "recommend the mockup in one line and build it without waiting" (2026-10-08); a product that runs on another website gets a browser bar with that site's domain and favicon (open question 2, answered the same day).

## Status on 2026-10-12

Tasks 1 to 3 and the README and version parts of Task 4 are done in the working tree of branch
`claude/ui-mockup-pins`, **uncommitted**, with the scope widened to any page that has no image
that works on a pin (see the spec's "Scope widened" section). The skill text in the working tree
is the text of record; the text blocks quoted in Tasks 1 to 3 below are the earlier, narrower
draft. `python3 -m unittest discover -s tests` passes (67 tests) and both `claude plugin validate`
commands pass.

Still to do:

- Run the two new eval cases and the regression cases (they need a terminal, to trust the plugin
  directory once): `claude plugin eval . --case screenshot-image --runs 3 --no-publish --judge-model sonnet`,
  the same for `no-photo-feature`, `recipe-from-url`, `hinted-photos`, `crop-warning` and `blocked-page`.
- Task 4 steps 1 and 2 (server items 22 to 25 in `docs/MCP-IMPROVEMENTS.md`, the link in `docs/PLAN.md`).
- Task 5 (live check), then commit and open the pull request.

## Global Constraints

- Work on a branch named `claude/ui-mockup-pins`; this repo merges to `main` through pull requests. Never commit to `main`.
- No scripts, hooks, agents or `bin/` in `plugins/insightpins/` (decision in `docs/PLAN.md`). The mockup procedure is described in words.
- Plugin files (`plugins/insightpins/**`) must contain no em dash or en dash, none of `curl`, `-F file=`, `/api/uploads`, `multipart`, and no `assets/` path outside `README.md` (existing tests enforce these).
- `ui-mockups.md` must contain no `<script`, no `http://` or `https://` URL, and no browser command line (`--headless`, `google-chrome`, `chromium`).
- Keep the exact phrase ``Never use an image with a `hint` `` in `create-pin/SKILL.md` (an existing test asserts it).
- A mockup shows only labels and numbers from the page, the screenshot or the user. Never invented.
- Nothing in the plugin may depend on a server feature that isn't live (`hint: "screenshot"` is handled if present, not required).
- Plugin version after this work: `1.0.7`.
- Baseline before starting: `python3 -m unittest discover -s tests` prints `Ran 60 tests` and `OK (skipped=1)`.

## Review Focus

Inputs the spec implies that the mocked eval doesn't exercise. Each is pinned by a text assertion in Task 1 and checked live in Task 5.

1. An agent that can run a browser builds a mockup and fills it with plausible invented numbers. Expected: only real values, or it asks for three to five rows. Pinned by the needles `Only real content` and `Never invent` (Task 1), live check 5.3.
2. A page that isn't about software has one stray screenshot among real photos. Expected: the screenshot is skipped silently and no question is asked. Pinned by the needle `isn't about software` (Task 1) and the regression cases in step 4.6.
3. The user says "use the screenshot anyway". Expected: one render with the screenshot, a plain warning, no mockup and no question. Pinned by the needle `without asking again` (Task 1), live check 5.4.
4. A future server returns `hint: "screenshot"`. Expected: the mockup choice, not "ask for a photo". Pinned by the eval mock (one screenshot carries the hint) and the needle ``except `screenshot` `` (Tasks 1 and 3).
5. The user has one render or no uploads left. Expected: the agent says a mockup costs one upload and one render before starting. Pinned by the needle `one upload` (Task 1).

---

### Task 0: Branch and commit the design documents

**Files:**
- Already on disk, untracked: `docs/superpowers/specs/2026-10-08-ui-mockup-pins-design.md`, `docs/superpowers/specs/2026-10-08-ui-mockup-pins/` (5 files), `docs/superpowers/plans/2026-10-08-ui-mockup-pins.md`

- [ ] **Step 1: Create the branch**

```bash
git checkout -b claude/ui-mockup-pins
```

- [ ] **Step 2: Confirm the baseline**

Run: `python3 -m unittest discover -s tests`
Expected: `Ran 60 tests` and `OK (skipped=1)`

- [ ] **Step 3: Commit the documents**

```bash
git add docs/superpowers
git commit -m "Spec and plan: UI mockups instead of software screenshots"
```

---

### Task 1: The mockup reference and the `create-pin` branch

**Files:**
- Create: `plugins/insightpins/skills/create-pin/references/ui-mockups.md`
- Modify: `plugins/insightpins/skills/create-pin/SKILL.md` (steps 2, 6, 9, 10)
- Modify: `plugins/insightpins/skills/create-pin/references/template-selection.md` (one table row)
- Test: `tests/test_plugin.py` (new class `UiMockupsTest`, placed after `UserPhotosTest`)

**Interfaces:**
- Produces: the file `references/ui-mockups.md` with the section titles `Recommend the mockup, then build it`, `Can you build it?`, `What goes in a mockup`, `Size and rendering`, `Report`. Tasks 2 and 3 refer to it by the path `references/ui-mockups.md` and by the phrase "simplified mockup".

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_plugin.py`, directly after the `UserPhotosTest` class:

```python
class UiMockupsTest(unittest.TestCase):
    """Software screenshots: ask before rendering, offer a simplified mockup, keep it honest."""

    GUIDE = os.path.join(SKILLS, "create-pin", "references", "ui-mockups.md")

    def test_guide_covers_the_rules(self):
        text = read(self.GUIDE)
        for needle in ("Recommend the mockup, then build it", "without waiting for an answer",
                       "Can you build it?", "Only real content",
                       "Never invent", "No fake controls", "No other people's content",
                       "drawn precisely", "Zoom in instead of shrinking", "browser bar",
                       'hint: "screenshot"', "isn't about software", "without asking again",
                       "user-photos.md", "create_upload_link", "904x744", "one upload", "7 days"):
            self.assertIn(needle, text)

    def test_guide_has_nothing_the_scan_could_hold(self):
        text = read(self.GUIDE)
        for pattern in (r"<script", r"https?://", r"--headless", r"\bgoogle-chrome\b", r"\bchromium\b"):
            self.assertIsNone(re.search(pattern, text, re.I), pattern)

    def test_create_pin_sends_screenshots_to_the_guide(self):
        create = read(os.path.join(SKILLS, "create-pin", "SKILL.md"))
        self.assertIn("references/ui-mockups.md", create)
        self.assertIn("Software screenshots are their own case", create)
        self.assertIn("except `screenshot`", create)
        self.assertIn("software or tool", create)
        skip = create.split("Skip photos whose `alt` or file name", 1)[1].split("\n   - ", 1)[0]
        self.assertNotIn('"screenshot"', skip)

    def test_template_guide_has_a_software_row(self):
        guide = read(os.path.join(SKILLS, "create-pin", "references", "template-selection.md"))
        row = next(line for line in guide.splitlines() if line.startswith("| Software, app or tool page |"))
        self.assertIn("ui-mockups.md", row)
        fields = {e["id"]: e["photo_area"] for e in list_templates_mock()}
        for tid in re.findall(r"`([a-z-]+)`", row.split("|")[2]):
            self.assertEqual(fields[tid], "panel", tid)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest tests.test_plugin.UiMockupsTest -v`
Expected: 4 tests, all fail or error (`FileNotFoundError` for `ui-mockups.md`, `AssertionError` for the others)

- [ ] **Step 3: Create `plugins/insightpins/skills/create-pin/references/ui-mockups.md`**

Exactly this content:

```markdown
# Software screenshots and UI mockups

A screenshot of an app, dashboard, table or browser extension almost never works as the pin photo.
It is wide, and its text is sized for a desktop screen. In a pin's photo panel it either shrinks to a
thin strip with unreadable text, or it is cropped and loses half its columns. A pin is shown about
230 px wide in the feed, so text that is 14 px tall on a 1900 px screenshot ends up under 2 px.

A **UI mockup** is a simplified picture of the same screen, drawn for the pin: four to six rows
instead of thirty, large type, the product's real labels and real numbers.

## When this applies

- The page is about software (an app, a SaaS tool, a browser extension, a dashboard, a plugin) and
  the images that show the subject are screenshots of its interface.
- An image's `alt` or file name says so: "screenshot", "dashboard", "interface", "UI", "table",
  "settings", "report", "extension popup".
- An image has `hint: "screenshot"` (a server may add it; treat it as this case, not as a junk image).
- The user gives you a screenshot as the photo for the pin.
- You rendered a pin and the preview shows a screenshot whose text can't be read. Don't try to
  rescue it with `image_focus`, `image_zoom` or `image_fit` more than once; go to the choice below.

It does not apply to photos, product shots, a phone or laptop photographed with an app on it, or a
page that isn't about software: skip a stray screenshot there like any other text image.

## Recommend the mockup, then build it

Don't put the screenshot on the pin, and don't drop it silently either.

**If you can build a mockup** (see "Can you build it?" below): tell the user in one line that the
screenshot won't read at pin size and that you are making a simplified mockup of that screen
instead, say what it will show (for example "the keyword list with its search volumes, five
rows"), and build it without waiting for an answer. Stop and ask first only when you don't have
real labels and numbers for it. The user can still ask for the screenshot afterwards.

**If you can't build one:** say a mockup would work best, then offer what can be done and wait
for the answer:

1. **A closer screenshot from the user**: one part of the screen, zoomed in so a few big words or
   numbers fill it, portrait or square. They upload it as in `user-photos.md`.
2. **The screenshot as it is**, cropped to its most readable part. Say plainly that the text will
   be small.
3. **No screenshot**: another photo from the page that fits, or a text-only template
   (`uses_photo: false`).

If the user already said what they want ("use the screenshot", "no mockup", "no image"), do that
without asking again and without building a mockup.

## Can you build it?

You can build a mockup only when you can write a file, run a headless browser to turn an HTML page
into a PNG, and read the PNG to check it (Claude Code and Cowork usually can; a chat without code
tools can't). If you can't, don't promise one: say a mockup would work best and offer the three
choices above. Never say a mockup was made when it wasn't, and never describe one
as if it were on the pin.

## What goes in a mockup

- **Only real content.** Every label, column name and number comes from the page (`extract_url`
  text, `structured`), from the screenshot itself if you can read it, or from the user. If you
  don't have real values, ask for three to five rows of them. Never invent a metric, a count or a
  result, and never show numbers better than the product gives.
- **The product's real elements, drawn precisely.** A mockup is a zoomed-in, cleaned-up copy of
  the real screen, not a new design. Enlarge the screenshot and look at the part you will show,
  then redraw each element as it is: the same icons (their shapes and colours, redrawn as simple
  vector shapes), the same order, the same panel shape and transparency, a similar font. If the
  real screen shows icons with no text labels, the mockup shows icons with no text labels; don't
  add captions the product doesn't have. Leave out menus, filters, pagination and side columns.
- **Zoom in instead of shrinking.** Show a small part of the screen large: two tiles of a grid, or
  one panel, or five rows of a table. Two tiles with every element readable beat eight tiles
  nobody can read.
- **Few, large elements.** One screen area, four to six rows, at most three columns. Row text at
  least 3% of the image width tall (about 60 px on an 1800 px wide image), larger for the one
  number that matters.
- **No fake controls.** No play buttons, cursors or "click here" arrows, and no buttons the
  product doesn't have. Controls the real screen shows (its own small action icons) may be drawn
  as they are.
- **A browser bar for things that run on a website.** When the product is a browser extension or
  works inside another site, frame the mockup with a plain browser bar showing that site's domain
  and its favicon (for example the address of the site the extension adds its numbers to). It tells
  the viewer where the product works. Show only the domain and the favicon: no other part of that
  site's interface, and nothing that suggests the site made or endorses the product.
- **No other people's content.** Use plain colour blocks where the screenshot shows other people's
  photos, pins, avatars or names.

## Size and rendering

- Use a `panel` template (`photo_area: "panel"`) and match the panel's shape so nothing is cropped:
  draw the image at twice the panel's size. Measured on the 1000x1500 pin: the `checklist` panel
  with six items is about 904x744 (an 1808x1488 image) and with four items about 904x868 (an
  1808x1736 image); fewer list items leave a taller panel. For another template, look at its sample
  in `preview_templates` and estimate the panel's width and height, or go by `best_photo` (square,
  or 3:2 for landscape).
- Keep everything important at least 4% in from each edge: the panel has rounded corners and its
  shape can change a little with the amount of text.
- Use white or the product's own background colour.
- Write one self-contained HTML file with inline CSS: no scripts, and fonts that are already on the
  machine. Set the page to the exact image size and capture it with a headless browser at that
  window size. Open the PNG and check it before uploading: no text cut off, nothing overlapping,
  every number as given.
- Upload the PNG as in `user-photos.md` (`create_upload_link`) and pass the returned `image_url` to
  `render_pin` with the default `image_fit`. A mockup costs one upload and the pin one render: say
  so first if the user is low on either (`get_quota`).
- Check the pin preview like any other. If the mockup's text is still small, enlarge the type and
  cut a row; don't add more.

## Report

In addition to the usual report: say the image is a simplified mockup made for the pin, name where
its labels and numbers came from, and say that the uploaded mockup is kept for 7 days (the
`edit_url` stops showing it after that). If you kept the HTML file, say where it is.
```

- [ ] **Step 4: Edit `create-pin/SKILL.md`, step 2**

Replace:

```
2. **Classify the content**: how-to/blog post, listicle (has a number), product, recipe, quote,
   travel/destination, or lifestyle/inspiration. Pull out facts the templates can show: the list
```

with:

```
2. **Classify the content**: how-to/blog post, listicle (has a number), product, recipe, quote,
   travel/destination, lifestyle/inspiration, or software or tool (an app, extension or dashboard;
   its images are often screenshots, see step 6). Pull out facts the templates can show: the list
```

- [ ] **Step 5: Edit `create-pin/SKILL.md`, step 6**

Replace:

```
   - **Never use an image with a `hint`** (such as `author`, `logo`, `promo`, `banner` or
     `infographic`; the list can grow): the server marks images that are probably not a photo for
```

with:

```
   - **Never use an image with a `hint`** (such as `author`, `logo`, `promo`, `banner` or
     `infographic`; the list can grow; except `screenshot`, see below): the server marks images that are probably not a photo for
```

Then, in the same bullet, replace:

```
     a pin photo. If only hinted images are left (even `primary_image`), ask the user for a photo or
     use a template with `uses_photo: false`.
```

with:

```
     a pin photo. If only hinted images are left (even `primary_image`), ask the user for a photo or
     use a template with `uses_photo: false`; a `screenshot` hint goes to the screenshot case below instead.
```

Then replace:

```
   - Skip photos whose `alt` or file name points to text or a person rather than the subject:
     "infographic", "chart", "before and after", "screenshot", "quote", author headshots and logos
     (the server doesn't catch them all).
```

with:

```
   - Skip photos whose `alt` or file name points to text or a person rather than the subject:
     "infographic", "chart", "before and after", "quote", author headshots and logos
     (the server doesn't catch them all).
   - **Software screenshots are their own case.** When the page is about an app, tool, extension or
     dashboard and the image is a screenshot of its interface (its `alt` or file name says
     "screenshot", "dashboard", "interface" or "table", it has `hint: "screenshot"`, or the user
     hands you one), don't put it on the pin as it is and don't drop it silently: follow
     [references/ui-mockups.md](references/ui-mockups.md). In short: if you can build an image,
     say in one line that a screenshot won't read at pin size and that you are making a simplified
     mockup with the page's real labels and numbers, and build it without waiting. If you can't,
     say a mockup would work best, offer a closer screenshot from the user, the screenshot as it
     is, or no screenshot, and wait for the answer before rendering. On a page that isn't about
     software, skip a stray screenshot like any other text image.
```

- [ ] **Step 6: Edit `create-pin/SKILL.md`, steps 9 and 10**

In step 9, replace:

```
   lost, a wrong photo, or a field showing a value that isn't true. `LOW_CONTRAST` means the title,
```

with:

```
   lost, a wrong photo, or a field showing a value that isn't true. A software screenshot whose text
   can't be read in the preview is also a real defect, but crop settings won't fix it: stop and
   follow `references/ui-mockups.md`. `LOW_CONTRAST` means the title,
```

In step 10, replace:

```
      that it is kept for 7 days, so the `edit_url` stops showing it after that;
```

with:

```
      that it is kept for 7 days, so the `edit_url` stops showing it after that;
    - for a mockup: that the image is a simplified mockup made for the pin, and where its labels
      and numbers came from;
```

- [ ] **Step 7: Add the row to `references/template-selection.md`**

Insert this line directly after the row that starts with `| Step-by-step / checklist |`:

```
| Software, app or tool page | `checklist`, `numbered-steps`, `split-horizontal`, `minimal-clean`, `text-focus` | A `panel` template, never `full-bleed`. A screenshot of the interface won't read at pin size: follow `ui-mockups.md` before using one. On `checklist` and `numbered-steps` the list carries the content, so the image only has to show what the product looks like |
```

- [ ] **Step 8: Run the tests**

Run: `python3 -m unittest tests.test_plugin.UiMockupsTest -v`
Expected: 4 tests, `OK`

Run: `python3 -m unittest discover -s tests`
Expected: `Ran 64 tests`, `OK (skipped=1)`. If `test_no_em_or_en_dashes_in_authored_text` or `test_no_upload_commands_in_plugin_files` fails, the new text broke a Global Constraint: fix the text, not the test.

- [ ] **Step 9: Commit**

```bash
git add plugins/insightpins/skills/create-pin tests/test_plugin.py
git commit -m "create-pin: ask before putting a software screenshot on a pin, offer a mockup"
```

---

### Task 2: `pin-design` and `review-pin` know the defect

**Files:**
- Modify: `plugins/insightpins/skills/pin-design/SKILL.md` ("Common defects to catch in a preview", "What not to do")
- Modify: `plugins/insightpins/skills/pin-design/references/design-checklist.md` ("Photo" section)
- Modify: `plugins/insightpins/skills/review-pin/references/scoring-rubric.md` (row 3, one new paragraph)
- Test: `tests/test_plugin.py` (one more method in `UiMockupsTest`)

**Interfaces:**
- Consumes: the path `references/ui-mockups.md` in the `create-pin` skill (Task 1) and the phrase "simplified mockup".

- [ ] **Step 1: Write the failing test**

Add this method to `UiMockupsTest`:

```python
    def test_design_and_review_know_the_defect(self):
        design = read(os.path.join(SKILLS, "pin-design", "SKILL.md"))
        self.assertIn("A software screenshot as the photo", design)
        self.assertIn("references/ui-mockups.md", design)
        self.assertIn("nothing that looks pressable", design)
        checklist = read(os.path.join(SKILLS, "pin-design", "references", "design-checklist.md"))
        self.assertIn("Not a full software screenshot", checklist)
        self.assertIn("simplified mockup", checklist)
        rubric = read(os.path.join(SKILLS, "review-pin", "references", "scoring-rubric.md"))
        self.assertIn("a full software screenshot whose text can't be read", rubric)
        self.assertIn("**Software pins:**", rubric)
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m unittest tests.test_plugin.UiMockupsTest.test_design_and_review_know_the_defect -v`
Expected: FAIL with `'A software screenshot as the photo' not found`

- [ ] **Step 3: Edit `pin-design/SKILL.md`**

Replace:

```
- Text baked into the photo (captions in GIFs or screenshots) showing through or cut off by the crop.
```

with:

```
- Text baked into the photo (captions in GIFs or screenshots) showing through or cut off by the crop.
- A software screenshot as the photo: its text is far too small at thumbnail size, or the crop cuts
  off half the screen. Crop and zoom settings don't fix it; a simplified mockup does (see the
  `create-pin` skill's `references/ui-mockups.md`).
```

Replace:

```
- No fake play icons, fake app controls or "click here" gimmicks. A small button-style label that
  names what the click gives ("Get the Recipe", "Read the Guide") is fine.
```

with:

```
- No fake play icons, fake app controls or "click here" gimmicks. A small button-style label that
  names what the click gives ("Get the Recipe", "Read the Guide") is fine. So is a simplified
  mockup of a product's real screen, with its real labels and numbers and nothing that looks
  pressable. An invented screen or invented numbers are misleading.
```

- [ ] **Step 4: Edit `pin-design/references/design-checklist.md`**

Replace:

```
- [ ] No text, watermark or logo baked into the photo (other than a product's own label).
```

with:

```
- [ ] No text, watermark or logo baked into the photo (other than a product's own label).
- [ ] Not a full software screenshot: interface text is unreadable at thumbnail size. A simplified
      mockup with the product's real labels and numbers works instead.
```

- [ ] **Step 5: Edit `review-pin/references/scoring-rubric.md`**

Replace:

```
| 3 | Photo quality and relevance | 15% | Sharp, bright, shows the result/benefit, matches the headline | Blurry, dark, generic, unrelated, watermarked |
```

with:

```
| 3 | Photo quality and relevance | 15% | Sharp, bright, shows the result/benefit, matches the headline | Blurry, dark, generic, unrelated, watermarked; a full software screenshot whose text can't be read |
```

Then insert this paragraph, with a blank line before and after, directly above the line that starts with `Weighted overall =`:

```
**Software pins:** a full screenshot of an app or dashboard is a 3-4 on criterion 3 and usually
pulls criterion 1 down too. The fix to suggest is a simplified mockup of that screen: four to six
rows, large type, the product's real labels and numbers.
```

- [ ] **Step 6: Run the tests**

Run: `python3 -m unittest discover -s tests`
Expected: `Ran 65 tests`, `OK (skipped=1)`

- [ ] **Step 7: Commit**

```bash
git add plugins/insightpins/skills/pin-design plugins/insightpins/skills/review-pin tests/test_plugin.py
git commit -m "pin-design, review-pin: a software screenshot is a defect, a simplified mockup is allowed"
```

---

### Task 3: Eval case `screenshot-image`

**Files:**
- Create: `evals/screenshot-image/prompt.md`
- Create: `evals/screenshot-image/mocks/insightpins/extract_url.md`
- Create: `evals/screenshot-image/graders/skill-fired.md`, `no-screenshot-on-pin.md`, `renders.md`, `report.md`
- Modify: `evals/README.md` (one row in the "Cases" table)
- Test: `tests/test_plugin.py` (one method in `EvalSuiteTest`)

**Interfaces:**
- Consumes: the skill behaviour from Task 1. The shared mocks in `evals/mocks/insightpins/` answer every tool this case doesn't mock itself.
- Produces: the grader file name `no-screenshot-on-pin` and the three image URLs below, which the unit test reads.

- [ ] **Step 1: Write the failing test**

Add this method to `EvalSuiteTest` in `tests/test_plugin.py`, directly after `test_hinted_photo_graders`:

```python
    def test_screenshot_graders(self):
        _, shot, _ = grader("screenshot-image", "no-screenshot-on-pin")
        _, body = strip_frontmatter(read(os.path.join(EVALS, "screenshot-image", "mocks", "insightpins",
                                                      "extract_url.md")))
        page = json.loads(body)
        details = page["image_details"]
        self.assertEqual([d.get("hint") for d in details], [None, "screenshot", "logo"])
        # the first screenshot can only be recognised by its alt text and file name
        self.assertRegex(details[0]["alt"] + details[0]["url"], r"(?i)screenshot|dashboard")
        self.assertEqual(page["primary_image"], details[0]["url"])
        self.assertNotIn("structured", page)
        for d in details:
            self.assertTrue(re.search(shot, render_input(image_url=d["url"])), d["url"])
            self.assertTrue(re.search(shot, render_input(image_url="https://x.example/a.jpg",
                                                         additional_image_urls=[d["url"]])), d["url"])
        self.assertFalse(re.search(shot, render_input(template_id="centered-quote", title="5 Reports")))
        self.assertFalse(re.search(shot, render_input(
            image_url="https://pins.insightpins.com/mcp/uploads/2026-10-08/abc.jpg")))
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m unittest tests.test_plugin.EvalSuiteTest.test_screenshot_graders -v`
Expected: ERROR with `FileNotFoundError` for `evals/screenshot-image/graders/no-screenshot-on-pin.md`

- [ ] **Step 3: Create `evals/screenshot-image/prompt.md`**

```markdown
---
plugins: ["../../plugins/insightpins"]
description: A software blog post whose only images are wide dashboard screenshots (one recognisable by its alt text, one with hint "screenshot") and a logo, with no tools to build an image; tests that the skill puts no screenshot on the pin, explains why, says a simplified mockup would work best and offers choices it can carry out, without inventing numbers or claiming a mockup exists
tags: [mcp, create, photo]
max_turns: 25
allowed_tools: [Skill]
---

Make a Pinterest pin for my post: https://tallyhours.example/blog/time-tracking-reports/
```

- [ ] **Step 4: Create `evals/screenshot-image/mocks/insightpins/extract_url.md`**

The JSON is one line:

```markdown
---
type: fixed
---

{"title": "5 Time Tracking Reports Every Freelancer Should Check Weekly", "description": "The five reports in Tally Hours that show where your week went: hours by project, billable share, overtime, idle time and unbilled work.", "images": ["https://tallyhours.example/img/weekly-report-dashboard-1920x1080.png", "https://tallyhours.example/img/projects-table-1880x940.png", "https://tallyhours.example/img/tally-mark-512x512.png"], "siteName": "Tally Hours", "url": "https://tallyhours.example/blog/time-tracking-reports/", "image_details": [{"url": "https://tallyhours.example/img/weekly-report-dashboard-1920x1080.png", "width": 1920, "height": 1080, "orientation": "landscape", "animated": false, "alt": "Screenshot of the Tally Hours weekly report dashboard", "source": "og", "low_resolution": false}, {"url": "https://tallyhours.example/img/projects-table-1880x940.png", "width": 1880, "height": 940, "orientation": "landscape", "animated": false, "alt": "Projects table with hours and billable amount columns", "source": "content", "low_resolution": false, "hint": "screenshot"}, {"url": "https://tallyhours.example/img/tally-mark-512x512.png", "width": 512, "height": 512, "orientation": "square", "animated": false, "alt": null, "source": "json-ld", "low_resolution": false, "hint": "logo"}], "primary_image": "https://tallyhours.example/img/weekly-report-dashboard-1920x1080.png"}
```

- [ ] **Step 5: Create the graders**

`evals/screenshot-image/graders/skill-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?create-pin"'
---
```

`evals/screenshot-image/graders/no-screenshot-on-pin.md`:

```markdown
---
type: tool_used
tool: mcp__plugin_insightpins_insightpins__render_pin
input_match: 'weekly-report-dashboard-1920x1080\.png|projects-table-1880x940\.png|tally-mark-512x512\.png'
min: 0
max: 0
weight: 3
---
```

`evals/screenshot-image/graders/renders.md` (the skill asks and waits, so nothing is rendered in this one-message case):

```markdown
---
type: tool_used
tool: mcp__plugin_insightpins_insightpins__render_pin
min: 0
max: 0
---
```

`evals/screenshot-image/graders/report.md`:

```markdown
---
type: llm
---

PASS if the final reply does all of these: (1) tells the user the page's images are screenshots of the app that won't be readable on a pin (too wide, or the text too small); (2) says a simplified mockup of the screen would work better; (3) offers at least one choice that can be carried out without building an image in this chat (the user sends a closer or zoomed screenshot, use the screenshot anyway with small text, or make the pin with no screenshot); (4) leaves the choice to the user.
FAIL if it says a mockup was made, generated or is on the pin; if it says it used a screenshot on a pin; or if it states hours, amounts, percentages or other figures for Tally Hours that the page text doesn't give.
```

- [ ] **Step 6: Add the row to `evals/README.md`**

Insert directly after the row that starts with `| `hinted-photos` |`:

```
| `screenshot-image` | A software blog post whose only images are two wide dashboard screenshots (one known only by its `alt`, one with `hint: "screenshot"`) and a logo; no tools to build an image | never renders a screenshot or the logo, renders nothing before the user chooses, explains why a screenshot won't read, says a simplified mockup would work best, offers a choice it can carry out, claims no mockup and invents no figures |
```

- [ ] **Step 7: Run the unit tests**

Run: `python3 -m unittest discover -s tests`
Expected: `Ran 66 tests`, `OK (skipped=1)`

- [ ] **Step 8: Run the eval case**

Run: `claude plugin eval . --case screenshot-image --runs 3 --no-publish --judge-model sonnet`
Expected: with the plugin, every grader passes in all 3 runs (score 1.00).

If `report` fails because the reply offers to build the mockup itself, the skill's "Can you build it?" section was not followed: reread the transcript in `results/`, and tighten that section's wording in `ui-mockups.md` (not the grader). If `no-screenshot-on-pin` fails, tighten the step 6 bullet in `create-pin/SKILL.md`. Re-run until 3 of 3 pass.

- [ ] **Step 9: Commit**

```bash
git add evals/screenshot-image evals/README.md tests/test_plugin.py
git commit -m "evals: screenshot-image, a software page with only interface screenshots"
```

---

### Task 4: Docs, server items, version 1.0.7, regression run

**Files:**
- Modify: `docs/MCP-IMPROVEMENTS.md` (four rows in the priority table, one new section at the end)
- Modify: `docs/PLAN.md` (one item under "Phase 7 - maintenance")
- Modify: `plugins/insightpins/README.md` (the `create-pin` row of the Skills table)
- Modify: `plugins/insightpins/.claude-plugin/plugin.json` (`version`)

- [ ] **Step 1: Add the server items to `docs/MCP-IMPROVEMENTS.md`**

Append these rows to the priority table, directly after the row that starts with `| 21 |`:

```
| 22 | A mockup tool (`render_mockup`): fixed layouts drawn from rows of data, returning an `image_url` | Functions | Observed (2026-10-08) | High for software and SaaS pages | M | Next |
| 23 | `extract_url`: `hint: "screenshot"` for interface screenshots (finishes `likely_text` from item 3) | Images | Observed (2026-10-08) | Medium-High | S-M | Next, not before plugin 1.0.7 is published |
| 24 | `list_templates`: the photo panel's size on the pin (`photo_box: {width, height}`) | Templates | Observed (2026-10-08) | Medium | S | Next |
| 25 | `render_pin`: an `IMAGE_TEXT_SMALL` warning for a photo full of small text | Images | Inferred | Medium | M | Later |
```

Append this section at the end of the file:

```markdown
## Software screenshots and mockups (2026-10-08)

Found while making pins for insightpins.com's own software pages. Design and evidence:
[superpowers/specs/2026-10-08-ui-mockup-pins-design.md](superpowers/specs/2026-10-08-ui-mockup-pins-design.md).
The plugin (1.0.7) handles this without the server: it asks before putting a screenshot on a pin
and, where it can run a browser, draws a simplified mockup in HTML, captures it and uploads it.

**Observed:** a 1923x899 table screenshot in the `checklist` panel was a thin strip with
`image_fit: "contain"` and lost its right-hand columns when cropped. A 1808x1488 mockup drawn for
the panel (five rows, large type, real numbers) rendered with no warnings and read at preview size.

### 22. A mockup tool

`render_mockup` with a few fixed layouts, taking rows of data and returning an `image_url`:

- `keyword-list`: a heading with one big number, then up to six rows of label, bar and number;
- `table`: up to three columns and six rows;
- `big-number`: one number with a label and a short line under it.

Inputs: `layout`, `title`, `rows`, optional `window_label`, optional brand colours, and the target
template (so the image matches that template's panel). It should not count as a render; counting
it as an upload is fine. This is the only way mockups can work in claude.ai chat, where the plugin
can't run a browser, and it keeps mockups in one style. The data must still come from the page or
the user: say so in the tool description.

### 23. `hint: "screenshot"`

Mark images that look like interface screenshots: landscape, large flat-colour areas, many small
text runs, often PNG. Plugin 1.0.7 sends such an image to the mockup choice. Older plugin versions
treat every `hint` as "never use" and would ask the user for a photo, so release this after 1.0.7
is published.

### 24. The photo panel's size

`best_photo` says "square" for `checklist`, but the panel is about 904x744 with six list items. An
image drawn to fit needs the real shape. Return it per template; if it depends on the amount of
text, return the smallest and largest, or return the size used in each `render_pin` result.

### 25. A small-text warning

When the photo, after scaling into its frame, is mostly text under about 12 px tall on the pin,
return `IMAGE_TEXT_SMALL`. It is a backstop for screenshots that carry no telling `alt` text. When
it ships, add the code to `create-pin/references/render-warnings.md` (a test checks that every
code named in the `render_pin` description is documented there).
```

- [ ] **Step 2: Add the link to `docs/PLAN.md`**

Under `### Phase 7 - maintenance`, add as the last item of that list:

```
- [ ] Software pages: ask before using an interface screenshot, offer a simplified mockup (1.0.7). Design: [superpowers/specs/2026-10-08-ui-mockup-pins-design.md](superpowers/specs/2026-10-08-ui-mockup-pins-design.md); plan: [superpowers/plans/2026-10-08-ui-mockup-pins.md](superpowers/plans/2026-10-08-ui-mockup-pins.md). Server follow-ups: MCP-IMPROVEMENTS items 22-25.
```

- [ ] **Step 3: Update the plugin README**

In `plugins/insightpins/README.md`, replace:

```
| `create-pin` | The full workflow from a URL to a finished pin: reads the page, picks the photo (or uploads your own), template and style, renders, checks the result and writes the copy. Also makes sets of variations. |
```

with:

```
| `create-pin` | The full workflow from a URL to a finished pin: reads the page, picks the photo (or uploads your own), template and style, renders, checks the result and writes the copy. Also makes sets of variations. For software pages it asks before using an interface screenshot, which is unreadable at pin size, and offers a simplified mockup instead. |
```

- [ ] **Step 4: Bump the version**

In `plugins/insightpins/.claude-plugin/plugin.json`, change `"version": "1.0.6"` to `"version": "1.0.7"`.

- [ ] **Step 5: Validate and run all tests**

Run: `claude plugin validate ./plugins/insightpins && claude plugin validate .`
Expected: both report no blocking findings.

Run: `python3 -m unittest discover -s tests`
Expected: `Ran 66 tests`, `OK (skipped=1)`

- [ ] **Step 6: Run the regression cases**

These cases choose photos and must behave as before (no new question, same scores):

Run: `claude plugin eval . --case recipe-from-url --runs 3 --no-publish --judge-model sonnet`
Run: `claude plugin eval . --case hinted-photos --runs 3 --no-publish --judge-model sonnet`
Run: `claude plugin eval . --case crop-warning --runs 3 --no-publish --judge-model sonnet`
Expected: 1.00 with the plugin for each. If a run now stops to ask about screenshots on one of these pages, the "When this applies" list in `ui-mockups.md` or the step 6 bullet is too broad: narrow the wording and re-run.

- [ ] **Step 7: Commit**

```bash
git add docs plugins/insightpins/README.md plugins/insightpins/.claude-plugin/plugin.json
git commit -m "Plugin 1.0.7: software screenshots and mockups; server items 22-25"
```

---

### Task 5: Live check, then pull request

These steps use the real server (uploads and renders count against the daily limits), so the owner runs them or approves them first. Check `get_quota` before starting: the four checks use up to 3 renders and 1 upload.

- [ ] **Step 1: Start Claude Code with the plugin from the branch**

Run, from the repo root: `claude --plugin-dir ./plugins/insightpins`

- [ ] **Step 2: Recommend and build**

Prompt: `Make a Pinterest pin for https://insightpins.com/blog/pinterest-pin-stats-competitor-analysis.html`
Expected: one line saying the page's screenshots won't read at pin size and that it is making a simplified mockup instead, then it goes on without waiting.

- [ ] **Step 3: The mockup (Review Focus 1)**

In the same run. Expected: the agent takes its labels and numbers from the page, or stops to ask for them if the page gives none; it builds an image, reads it, uploads it (with the 7-day notice) and renders once. Open the pin and compare every label and number in the mockup with the page. Any value that isn't on the page is a failure: fix the "Only real content" rule's wording and repeat.

- [ ] **Step 4: The override (Review Focus 3)**

In a new session, prompt: `Make a pin for https://insightpins.com/blog/best-pinterest-analytics-tools.html and use the screenshot from the article, I want the real UI on it.`
Expected: one render with the screenshot, a plain note that its text will be small, no question about mockups.

- [ ] **Step 5: A page that isn't about software (Review Focus 2)**

In a new session, ask for a pin for a page that has nothing to do with software and sits on another site: a recipe or home decor post of the owner's choice. (Don't use an insightpins.com blog post here: those pages show the extension's screenshots, so a question about them would be correct.)
Expected: the usual flow with no question about screenshots.

- [ ] **Step 6: Record the results**

Add a short dated section to `docs/TEST-REPORT.md` with the four prompts, what happened, and the renders and uploads used. Commit:

```bash
git add docs/TEST-REPORT.md
git commit -m "Test report: live check of the screenshot and mockup flow"
```

- [ ] **Step 7: Open the pull request**

```bash
git push -u origin claude/ui-mockup-pins
gh pr create --title "Plugin 1.0.7: UI mockups instead of software screenshots" --body "Design: docs/superpowers/specs/2026-10-08-ui-mockup-pins-design.md. Asks before putting an interface screenshot on a pin and offers a simplified mockup; new reference ui-mockups.md, eval case screenshot-image, server items 22-25 in MCP-IMPROVEMENTS."
```

Before merging, the owner answers the spec's remaining open questions (3 and 4).
