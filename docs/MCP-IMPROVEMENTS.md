# InsightPins MCP: issues and improvement ideas

Feedback on `https://app.insightpins.com/api/mcp` from building and testing the Claude plugin
(10 live renders and 11 page reads on 2026-10-03, see [TEST-REPORT.md](TEST-REPORT.md)).
Each item notes whether it was **observed** in testing or is **inferred** from the tool surface.
Effort is a rough estimate without seeing the server code.

## Short answer

- **Nothing here blocks submitting the plugin.** The skills already work around the worst problems.
  The one thing to do now is a quick security check of URL fetching (item 1).
- **The biggest quality problem is images, not templates.** Pins went wrong because of photo
  choice and cropping, not layout. `extract_url` returns images with no information about them, and
  `render_pin` has no control over how a photo is cropped.
- **Templates are decent** (30 layouts, good category coverage). The weak spots are around them:
  default text that's too small, list templates that can't show list items, only light backgrounds,
  and preset colors only, with no brand colors.
- **Missing functions**, in order of value: image upload, template previews, a brand kit, stock
  photo search, pin history, then publishing to Pinterest.

## What already works well

Keep these as they are:
- The tool descriptions and server instructions are clear. Claude followed the intended flow
  without extra prompting.
- `edit_url` is a great handoff to the website, and `renders_remaining_today` in every result saves a call.
- The ~200x300 preview is about the size of a pin in a phone feed, which makes it a good readability check.
- Failed renders don't count against the limit. Renders took a few seconds each.

## Priority list

| # | Improvement | Area | Evidence | Impact | Effort | When |
| - | - | - | - | - | - | - |
| 1 | Verify URL fetching can't reach internal addresses (SSRF) | Security | Inferred | Critical if vulnerable | S | **Done** (deployed 2026-10-03, see below) |
| 2 | `extract_url`: report blocked and bot-check pages as errors | Functions | Observed | High | S | **Done** (deployed 2026-10-03) |
| 3 | `extract_url`: image details and filtering | Images | Observed | High | S-M | **Done** (#56, checked 2026-10-04; author, logo, banner and infographic `hint`s in #92, #94, checked 2026-10-05; `promo` hint and small declared images kept in #97); `likely_text` still open |
| 4 | `render_pin`: crop and focus control for the photo | Images | Observed | High | M | **Done** (#67 controls, #86 `image_focus: "auto"`, #87 `overlay_strength`; checked 2026-10-05) |
| 5 | Auto-fit text size and render warnings | Templates | Observed | High | M | **Done** (#62 warnings, #79 `text_size: "auto"`, checked 2026-10-04); follow-ups below |
| 6 | `upload_image` tool | Functions | Observed (blocked two skills) | High | S-M | **Done** (#88: `upload_image`, `create_upload_link`, `get_upload`; checked 2026-10-05) |
| 7 | `extract_url`: structured data (recipe times, servings, product price) | Functions | Observed | Medium-High | S | **Done** (#56, checked 2026-10-04); description still cut mid-sentence |
| 8 | Template previews in `list_templates` | Templates | Inferred | Medium-High | S | Next |
| 9 | List items for list templates | Templates | Inferred | Medium-High | M | Next |
| 10 | Brand kit: custom colors, logo, saved defaults | Controls | Inferred | High for repeat users | M | Before paid plans |
| 11 | Dark and high-contrast backgrounds | Templates | Observed | Medium | S-M | Next |
| 12 | Quota errors with plan info and an upgrade link | Plans | Inferred | High when billing starts | S | **Before paid plans** |
| 13 | Better page fetching for big sites | Functions | Observed (6 of 10 failed) | Medium | M-L | Later |
| 14 | Stock photo search with license info | Functions | Inferred | High | M | Later |
| 15 | Pin history (`list_my_pins`, `get_pin`) and longer-lived links | Functions | Inferred | Medium | M | Later |
| 16 | More pin elements: badge, overlay strength, text alignment | Controls | Partly observed | Medium | M | Overlay strength **done** (#87); badge and text alignment later |
| 17 | Keyword tools | Functions | Planned | High | L | Planned |
| 18 | Publish and schedule to Pinterest | Functions | Inferred | Very high | L | Later (big project) |
| 19 | Batch rendering of variations | Functions | Inferred | Low-Medium | S | Later |
| 20 | Larger preview on request, carousel pins, background removal | Misc | Inferred | Low-Medium | M | Later |
| 21 | Readable small text: contrast-checked text colors and a `LOW_CONTRAST` warning | Templates | Observed (measured 2026-10-04) | High | S-M | **Done** (#85 colour map; #90 `LOW_CONTRAST` and `readable_palettes`; #91, #95 subtitle colours; #93 darker primaries; checked 2026-10-05). Site name not judged yet |

"Now" means before or alongside directory submission. "Next" means the first improvement round,
the biggest quality wins. "Later" means growth features.

## Check of the October 4 deploy

Checked against the live server on 2026-10-04 (4 renders; `extract_url` on the same pages as the
first test) and the `pin-generator-tool` source at #81.

| Item | Result |
| - | - |
| 3. Image details | `image_details` (size, orientation, animated, alt, source, low_resolution) and `primary_image` returned. Nerd Fitness: tracking GIF, animated demos and thumbnails filtered out. |
| 7. Structured data | Minimalist Baker: Recipe with prep, cook and total time, servings, rating. Allbirds: Product with price, currency, brand. |
| 5. Warnings | Wide photo in `bold-title`: `IMAGE_CROPPED` (47% visible) and `IMAGE_UPSCALED` (3.1x), both accurate. |
| 4. Crop controls | `image_focus: "left"` brought the cut-off head back into view (same pin as test render 10). |
| 5. `text_size: "auto"` | Recipe card title grew to fill its area, about the same as the manual 160% from the first test; no warnings. |
| Templates | 38 live, 8 new (side-rail, vine-corners, tulip-frame, photo-stack, grid-lines, overlap-collage, photo-quad, vertical-title); `list_templates` now has `uses_photo` and `uses_extra_images`. |
| Auth | `/api/mcp` answers 401 with `WWW-Authenticate` pointing at the protected-resource metadata, whose `resource` is `/api/mcp`. `/mcp` is the docs page (405 on POST). |

**Follow-ups found in the check** (none blocks submission):

1. **`TITLE_SMALL` didn't fire where it should.** Recipe Card at the default size with a 6-word title
   left a visibly small title and an empty panel (same as test render 1), and returned no warnings.
   "auto" then made the title much larger. Cause (from the server side): the recipe card is
   box-fitted and reports no fill, so the warning can't fire there; the 0.30 threshold itself was
   calibrated in Chrome across the templates that give the title a size budget, and the 8 newer
   templates haven't been measured yet. Planned fix: the dry-run fill measurement (step 2 of the
   feedback fixes). The skill no longer relies on this warning.
2. **`IMAGE_CROPPED` stays after a good `image_focus`.** It reports the crop (still 47% visible), which
   is true, but a client that re-renders on every warning will loop. Suggest: when `image_focus` or
   `image_fit` was set, say so in the message ("you set image_focus; check the preview") or downgrade it.
3. **`primary_image` can be a weak choice.** On Nerd Fitness it is the og image, a 621x310 before/after
   picture. Ranking by size, orientation and alt relevance would pick better.
4. **Descriptions are still cut mid-sentence** ("...you should totally get"). Prefer `og:description`
   or the meta description, and cut at a sentence end.
5. **Text-heavy images still come through** (an infographic, an author headshot). Their `alt` gives them
   away now; a `likely_text` flag would make it explicit.
6. **The docs page suggests "a quote template and a dark palette"**, but all 15 palettes are still
   light (item 11). Either add dark palettes or change the example.
7. **Clients can keep old tool definitions.** A session that loaded the tools before the deploy
   didn't see `image_focus` or `"auto"` in its schema, even after reconnecting, though the server
   accepted both. This is caching on the client side. The server has no fallback for a client that
   validates locally against a stale integer-only `text_size`; it would refuse "auto". The
   `create-pin` skill falls back to numbers and template choice in that case. Cheap mitigation on the
   server: bump the server version (still 0.1.0) with every tool change, which helps clients that
   compare versions.

## Details

### 1. Security check of URL fetching (done)

**Status, checked from outside on 2026-10-03:** after the deploy, `extract_url` refused the cloud
metadata address, `127.0.0.1` and `10.0.0.1`. Before the deploy it already refused those plus
loopback in decimal, hex and IPv6 forms, `0.0.0.0`, `192.168.1.1` and DNS names that resolve to
loopback; those variants weren't re-run after the deploy. Non-HTTP schemes are refused with "Only
HTTP and HTTPS protocols are allowed". Not checked from outside (cover them in server
tests): redirects from a public URL to an internal one, and internal addresses in `render_pin`
image URLs. Internal addresses return the generic `[FETCH_FAILED]`, so from outside a deliberate block
can't be told apart from a failed connection; a distinct code such as `[URL_NOT_ALLOWED]` would make
this testable without revealing anything useful.


`extract_url` fetches any URL the user gives, and `render_pin` fetches any `image_url`. If the
server doesn't block private and internal addresses, someone could make it request internal
services (server-side request forgery). Examples: `localhost`, `127.0.0.1`, `10.x`, `192.168.x`,
`169.254.169.254` (the cloud metadata endpoint), and redirects or DNS names that resolve to those.
I did **not** test this against your server. Please verify:
- fetching is allowed only over http/https to public IPs, checked after DNS resolution and after every redirect;
- there's a timeout, a size limit and a content-type check (HTML for `extract_url`, images for `render_pin`);
- error messages don't echo internal responses.

Directory reviewers and security scans look at this kind of risk for connectors.

### 2. Report blocked and bot-check pages as errors (done)

**Status after deploy (2026-10-03):** nomadicmatt.com (SiteGround "One moment, please"), wikihow.com
and allrecipes.com now return `[BOT_CHALLENGE] ... This site blocks automated readers ...`; a missing
page returns `[NOT_FOUND]`; normal pages still work. The `create-pin` skill now uses these codes.


**Observed:** wikihow.com came back as a success titled "Client Challenge", and nomadicmatt.com as
"One moment, please...Loader", both with no images. Other sites correctly returned "Access denied".
The skill now detects this, but every other client of your MCP will build pins titled
"Client Challenge".
**Fix:** detect challenge pages (known titles, Cloudflare/Akamai markers, an empty body or no
images) and return an error such as `BOT_CHALLENGE`. Use consistent error codes:
`BLOCKED`, `BOT_CHALLENGE`, `NOT_FOUND`, `TIMEOUT`, `NOT_HTML`.

### 3. Image details and filtering in `extract_url` (next)

**Observed:** Claude has to choose a photo from bare URLs. It received:
- a tracking pixel (`dev.visualwebsiteoptimizer.com/ee.gif?a=`), an author headshot, footer graphics
  and 200x200 thumbnails;
- a photo from a different post (a kabocha soup image on the fried rice page);
- an animated GIF with a baked-in caption, which ruined a pin (render 9);
- a horizontal photo with nothing to show it was horizontal, which got its subject's head cropped
  off in a full-bleed template (render 10).

**Proposal:** return objects instead of strings, and drop the junk server-side.

```json
"images": [
  {"url": "...", "width": 683, "height": 1024, "orientation": "portrait",
   "animated": false, "alt": "Vegan fried rice with crispy tofu in a white bowl",
   "source": "og:image", "likely_text": false}
],
"primary_image": "..."
```

- Filter out images under ~300 px, tracking pixels, icons, logos and favicons.
- Rank the `og:image` / `twitter:image` and the main content images first.
- `alt` text helps Claude pick the photo that matches the headline.
- `likely_text` is optional: a cheap OCR or heuristic flag for infographics and captioned GIFs.
- Keep strings as a fallback field for older clients if needed.

### 4. Crop and focus control for the photo (next)

**Observed:** full-bleed templates center-crop the photo. A horizontal photo lost the person's head
(render 10), and a square product PNG sat small in a big frame (render 3). The full-bleed template
also tinted the whole photo strongly with the palette color (render 10), which made it look washed out.
**Proposal:** new `render_pin` parameters:
- `image_focus`: `center` | `top` | `bottom` | `left` | `right`, or `{ "x": 0.5, "y": 0.3 }`;
- `image_fit`: `cover` | `contain` (contain = blurred or color background behind the whole photo);
- `image_zoom`: 100-200 (for small products in big frames);
- `overlay_strength`: 0-100 (how strongly the color or gradient covers the photo).

Better still, have the server pick the crop automatically with smart cropping (face and saliency
detection) by default, and keep these parameters as overrides.

### 5. Auto-fit text and render warnings (next)

**Observed:** at the default `text_size` (100), a 6-word headline on `recipe-card` was small, with
half the panel empty (render 1). Raising it to 160 fixed it (render 2). Every client would have to
learn this.
**Proposal:**
- `text_size: "auto"` (and make it the default): fit the headline to its area, within min and max sizes.
- Add `warnings` to the render result so Claude can fix problems without seeing details in a
  200x300 preview, for example:
  `["title wraps to 5 lines", "title shrunk to 70% to fit", "image upscaled 2.4x (low resolution)",
  "subtitle hidden: template has no subtitle"]`.

### 6. `upload_image` (next)

**Observed:** an image uploaded into the chat has no URL, so it can't be used. This blocks
"use my photo", `remake-pin` without a URL, and `optimize-pin` when the user has only the image.
**Proposal:** `upload_image({ data: base64, filename })` returns `{ image_url }`, hosted for the same
7 days or tied to the account. Limit size and type (JPEG/PNG/WebP, up to ~10 MB), and scan or
validate the content.

### 7. Structured data from pages (next)

**Observed:**
- `recipe-card` has `cookTime` and `servings` fields, but `extract_url` doesn't return them, so the skill must leave them empty.
- `price-tag` needs a price, but the Allbirds product page price wasn't returned.
- The Minimalist Baker description was the first 150 characters of a chatty intro, cut off mid-sentence.

**Proposal:** parse schema.org JSON-LD, which most recipe and shop sites include:

```json
"structured": {
  "type": "Recipe", "total_time": "30 min", "servings": "4", "rating": 4.8,
  "type": "Product", "price": "98", "currency": "USD", "brand": "Allbirds"
}
```

Prefer `og:description` / meta description over the first paragraph, and don't cut text mid-sentence.

### 8. Template previews (next)

**Inferred:** Claude picks templates from a one-line description ("Organic wavy gradient over full
image") and never sees the template. Add `preview_url` (a small sample image) to `list_templates`.
Add `photo_area` too (`full-bleed`, `panel`, `none`, `multi`) plus the best photo orientation, so
templates can be matched to photos without guessing. The plugin's template guide now does this by
hand, and it will go stale as you add templates.

### 9. List items for list templates (next)

**Inferred from the schema:** `numbered-steps`, `checklist` and `fitness-grid` are list layouts,
but `render_pin` only takes a title and a description. There's no way to pass the actual steps or
items, so a "checklist" pin can't show a checklist.
**Proposal:** `items: string[]` (3-7 short lines) for list templates, with a sensible max length per item.

### 10. Brand kit (before paid plans)

**Inferred:** only 15 preset palettes and 10 font pairings, and no logo. A business can't match its
brand colors, and every pin needs its style set again. This is the feature that turns one-off
users into repeat (paying) users.
**Proposal:**
- `render_pin` accepts custom colors: `colors: { primary, secondary, accent, text, background }` as hex.
- `logo_url` with a small fixed position.
- `save_brand_kit` / `get_brand_kit` on the account (colors, fonts, logo, site name, default CTA).
  `render_pin` uses the brand kit when no style is given.

### 11. Dark and high-contrast backgrounds (next)

**Observed:** all 15 palettes have light pastel backgrounds (`#E3F2FD`, `#FCE4EC`...). Quote pins
can only be light, and the thin-font version scored 5.3/10 (render 5). The palettes are also the
standard Material Design colors, so pins can look generic.
**Proposal:**
- add dark palettes (charcoal, navy, forest, black and gold);
- add a `background_style: light | dark | photo` option on text-led templates;
- add a few more distinctive palettes (muted, earthy and editorial tones).

### 12. Quota errors and plan info (before paid plans)

**Inferred:** `get_quota` returns only limit, used, remaining and reset time.
**Proposal:**
- add `plan` (free/pro...) and separate counters for renders and keyword lookups;
- when a limit is hit, return a structured error with `resets_at` and `upgrade_url`.

The plugin skills already show an upgrade link if the response contains one, and mention it only once.

### 13. Better fetching for big sites (later)

**Observed:** allrecipes.com, budgetbytes.com, apartmenttherapy.com and becomingminimalist.com
returned "Access denied", and wikihow.com and nomadicmatt.com returned bot-check pages: 6 of the 10 existing pages tried failed. Users
pinning their own small blogs will mostly be fine. Options:
- a realistic browser user agent;
- falling back to Open Graph tags from a lighter request;
- a headless-browser fetch for retries;
- respecting robots.txt where required.

### 14. Stock photo search (later)

**Inferred:** many pins use photos taken from other websites, which is a copyright risk for the
user, and blocked or text-less pages leave no photo at all.
**Proposal:** `search_photos({ query, orientation: "portrait" })` via Unsplash or Pexels, returning
the URL, photographer, license and attribution text. This solves the "no usable photo" case and
makes pins safer to publish.

### 15. Pin history and longer-lived links (later)

**Inferred:** links expire after 7 days, and there's no way to find a pin from an earlier
conversation. Proposal:
- `list_my_pins` and `get_pin(id)`;
- permanent storage for account holders (possibly a paid feature);
- `render_pin` accepting `based_on: pin_id`, so a pin can be changed without resending everything.

### 16. More pin elements (later)

- `badge_text`: a small ribbon such as "NEW", "FREE PRINTABLE" or "SAVE THIS". Very common on high-performing pins.
- `overlay_strength` (see item 4) and text-band opacity.
- `text_align` and `text_position` (top/center/bottom) on overlay templates.
- Second image or "before/after" layouts.
- `cta_style` (button, underline, none).

### 17. Keyword tools (planned)

These should go on the same server, so users get one sign-in and one connector. Suggested tools:
- `search_keywords(topic)`: related keywords with volume or popularity and trend;
- `keyword_trends(keyword)`: seasonality, so pins go up 1-3 months early;
- optionally `suggest_boards`.

The `pin-copy` skill already uses a keyword tool when one is connected.

### 18. Publish and schedule to Pinterest (later, big project)

The natural end of the workflow is "make the pin and post it". This means Pinterest API access
(app review, OAuth to the user's Pinterest account) and tools such as:
- `list_boards`
- `publish_pin({ pin_id, board_id, title, description, link, alt_text })`
- `schedule_pin`
- later `get_pin_analytics`, which would let `optimize-pin` work from real impressions, saves and clicks.

High value, but large effort and approval risk. Do it after the image and template basics.

### 19. Batch rendering (later)

`render_variations([...])`: several renders in one call for `pin-variations` and `optimize-pin`.
Mainly a speed and convenience win; quota should count each image.

### 20. Smaller ideas (later)

- `preview_size: "large"` when Claude needs to check details (the default small preview is good for readability checks).
- Carousel pins (2-5 images), a format Pinterest supports.
- Background removal for product photos (clean product on a palette color).

### 21. Readable small text: contrast check (next, first round)

**Observed** (2026-10-04, measured on full-size renders with the WCAG contrast formula):
- On color-panel templates (`split-horizontal`, `diagonal-cut`) the text is white on the palette's
  primary color, and the subtitle and site name are drawn lighter than the headline. On
  `coral-reef`, the title measured 3.2:1, the subtitle 2.7:1 and the site name 2.0:1; on
  `ocean-breeze` 3.6, 3.3 and 2.6. Small text needs 4.5:1.
- White on each palette's primary: minimalist 16.1, berry-blush 7.0, midnight 6.9, dusty-rose 5.9,
  lavender 5.2, warm-earth 4.6, terracotta 4.4, rose-gold 3.8, ocean-breeze 3.7, forest-calm 3.3,
  coral-reef 3.2, cool-mint 3.0, sunset-glow 2.7, sage 2.5, electric 2.3. Half the palettes can't
  carry small white text on a panel, and the same white-on-primary is used for buttons.
- `number-badge` draws the subtitle and site name in the palette's light secondary color on the
  pale background: 1.8:1 on `sunset-glow`, 2.6:1 on `terracotta`. Secondary on background is 1.5-2.9
  for every palette except minimalist (4.4), so this subtitle is never comfortably readable.
- Nothing in `warnings` flags any of this.

**Proposal:**
- Pick text colors by contrast, not by role: for each text element, use white or the palette's
  dark text color, whichever has the higher contrast with what's behind it (4.5:1 target for the
  subtitle, site name and button; 3:1 minimum for a large title). Don't fade small text on panels.
- Draw subtitles and site names in the text color (or text color at most slightly lighter), not
  the secondary color, on light-background templates.
- Add a `LOW_CONTRAST` warning naming the element and the measured ratio, like the other warnings.
- Optionally darken the mid-tone primaries (or add dark variants) so every palette can carry
  white text; this overlaps with item 11.

The plugin works around it for now: `style-selection.md` has the contrast table above, and the
skills check small text in the preview and hide the `number-badge` subtitle.

**Update (pin-generator-tool #85):** `web/src/lib/constants/templateColorPairs.ts` now records which
palette colour every template draws each text in, a test keeps it in line with the templates, and
`docs/TEMPLATE_COLOR_ROLES.md` is generated from it. It corrected one assumption above: panel and
button text is the palette's light `background` colour, not white, so only 9 palettes reach 3:1 and
4 reach 4.5:1 on that pair. The plugin now builds `create-pin/references/template-colors.md` from
that doc (`scripts/build-template-colors.py`), so Claude picks a palette per template.
Still open on the server: choose text colours by contrast (or darken the primaries of the 6
palettes below 3:1), draw subtitles in the `text` colour instead of `secondary` on the 6 templates
that use it, and report `LOW_CONTRAST` in `warnings`. A `readable_palettes` field per template in
`list_templates` would let any client pick well without the plugin's table.

**Update (2026-10-05, #90, #91, #93, #95):** all of that shipped. `render_pin` warns `LOW_CONTRAST`
when the title, subtitle or button is below 3:1 on the chosen palette and names palettes that pass;
`list_templates` gives each template's `readable_palettes`; the six subtitles drawn in `secondary`
now use the `text` colour; the six light palettes have darker primaries (3.2:1 for light text). Every
judged text now reaches 3:1 on all 15 palettes, so every template lists every palette. Still open:
the site name and small labels are not judged and need 4.5:1; on most colour-panel templates the
site name is fully readable only on midnight, berry-blush, dusty-rose and minimalist (see the notes
in `template-colors.md`).

## Suggested order of work

1. ~~**This week:** item 1 (security check) and item 2 (bot-check errors).~~ Done 2026-10-03.
2. **First improvement round:** items 3, 4, 5, 6, 7. These fix every bad pin seen in testing.
   Then 21 (readable small text), 8, 9 and 11 (template side).
3. **Before paid plans:** items 10 and 12 (brand kit, quota and plan errors).
4. **Growth:** 17 (keywords, already planned), 14, 15, 16, then 18 (Pinterest publishing).

When an item ships, the plugin skills can be simplified. For example, once `extract_url` returns
image dimensions, the skill no longer needs to guess orientation from file names. Tell me which
items ship and I'll update the skills and evals.

## Check of the October 5 deploy (#86, #87, #88)

Checked against the live server on 2026-10-05 (2 renders, 2 uploads):

| Item | Result |
| - | - |
| 6. Uploads | `create_upload_link` returned a one-time link (15 minutes, 4.5 MB); a file posted to it was stored (1000x740 JPEG, 7 days) and `get_upload` returned `ready` with its `image_url`. Posting to the same link again returned 409 `LINK_USED`. `upload_image` with a small base64 JPEG worked. Both image URLs rendered. |
| 4. `image_focus: "auto"` | On a wide photo in `bold-title` it chose x 0.69, y 0.28 (the cliffs and waterfall) and returned it as `image_focus_used`; the `edit_url` carries the point. |
| 16. `overlay_strength` | `list_templates` now has `overlay` (`none`, `decor`, `text`). At 30 on `magazine-cover` (text on the overlay) the render added `OVERLAY_LOW_CONTRAST`. |
| Annotations | All 8 tools have `annotations.title` and hints (#84 for the first 5, #88 for the upload tools). |

Follow-ups: the privacy policy said the connector doesn't receive "files you upload to the
assistant"; the text from `docs/POLICY-DRAFTS.md` was published on 05.10.2026. Clients that cached the old
`render_pin` definition still sent `image_focus: "auto"` and `overlay_strength` in this test, but a
stricter client may refuse them; the skills leave them out if refused.

## Check of the second October 5 deploy (#89 to #95)

Checked against the live server on 2026-10-05 (1 render):

| Item | Result |
| - | - |
| 21. `LOW_CONTRAST` | Before #93 and #95 reached production, `dashed-accent` with `ocean-breeze` and a subtitle returned "The subtitle is hard to read on the Ocean Breeze palette (contrast 1.9:1; 3:1 is the minimum). Palettes that work with this template: Minimalist." |
| 21. `readable_palettes` | After the deploy, every one of the 38 templates lists all 15 palettes. `photo-quad` also has `overlay_text_fields` (its two photo labels sit on the overlay). |
| 21. Palettes | `list_styles` returns darker primaries for forest-calm, cool-mint, sage, electric, sunset-glow and coral-reef (3.2:1 for light text), darker accents for electric and sunset-glow, and a darker text colour for coral-reef. |
| 3. Image hints | On `insightpins.com/blog/best-pinterest-analytics-tools.html` the JSON-LD logo (`android-chrome-512x512.png`) now has `hint: "logo"` and is listed last; before #92 it ranked above a real screenshot. |

The plugin (1.0.3) now picks palettes from `readable_palettes`, documents `LOW_CONTRAST`, never uses a
hinted image, and its mocks match this deploy.

## Answers from the server side (2026-10-04)

- **`photo-stack` with fewer than 4 photos** always draws four slots and reuses what it has (1 photo
  fills all four; 2 give a, b, b, a; 3 give a, c, b, a; 0 use palette fallbacks). Tests pin which image
  goes in which slot, but nobody has looked at 1 or 2 distinct photos, and there is no warning for too
  few extra images (a product call). The skill now uses it only with 4 different photos.
- **Prices**: beyond "$100", the extractor handles 98, 98.50, 1,299.00, European 49,90 (becomes
  €49.90), lowPrice, priceSpecification and variant prices, symbols for known codes and "1299 CAD"
  for codes without one. It refuses 1.299,00, prices already carrying a symbol like "$98" and absurd
  values, leaving the price out. Tested on synthetic JSON-LD only. The skill uses the price as given.
- **Cook time vs total time**: the extractor returns `total_time`, `prep_time` and `cook_time`
  separately. The skill now writes a total time with "total" (or leaves it out) instead of putting it
  in the Cook Time field as if it were cook time.
