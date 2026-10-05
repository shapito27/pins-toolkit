# Phase 3 test report (2026-10-03)

Two kinds of testing:

1. **Live run**: the skills followed by hand against the real InsightPins MCP with public pages,
   10 renders.
2. **Eval suite**: `claude plugin eval` with mocked tools, with and without the plugin. See
   [evals/README.md](../evals/README.md).

## Live run

Page reads (`extract_url`, free): allrecipes.com, budgetbytes.com, apartmenttherapy.com and
becomingminimalist.com returned "Access denied"; wikihow.com and nomadicmatt.com returned a
bot-check page ("Client Challenge", "One moment, please...") **as a successful result** with no
images. Usable: minimalistbaker.com, allbirds.com, nerdfitness.com, zenhabits.net.

Image links expire on 2026-10-10.

| # | Test | Page | Template / palette / font | Result |
| - | - | - | - | - |
| 1 | create-pin | Minimalist Baker recipe | recipe-card / terracotta / friendly | Headline too small at thumbnail size, top panel half empty. [image](https://pins.insightpins.com/mcp/2026-10-03/519e3678-c279-4f69-90b6-f150d08b29c4.jpg) |
| 2 | fix of #1 | same | same + `text_size` 160 | Fixed: readable at thumbnail. [image](https://pins.insightpins.com/mcp/2026-10-03/f5455079-b4be-4885-9140-fcc60e60d7c8.jpg) |
| 3 | create-pin | Allbirds product | product-spotlight / sage / modern-sans | Clean and readable; product small in frame (typical of plain product shots). [image](https://pins.insightpins.com/mcp/2026-10-03/ba56e700-e356-42c3-9683-5945b5c5414b.jpg) |
| 4 | create-pin | Nerd Fitness how-to | split-horizontal / coral-reef / bold-impact | Good: strong contrast, subtitle works. Skipped tracking GIF, headshot, infographic. [image](https://pins.insightpins.com/mcp/2026-10-03/1a538b35-cad7-4eaf-af25-b24727c7fdec.jpg) |
| 5 | create-pin, weak images | Zen Habits essay | centered-quote / lavender / editorial | Weak: thin pale text, empty lower half. Review score 5.3/10. [image](https://pins.insightpins.com/mcp/2026-10-03/52b16ab0-0130-42ac-b793-b3e2dcb6d730.jpg) |
| 6 | optimize-pin V1 (readability) | same | centered-quote / midnight / classic-serif, `text_size` 150 | Clearly more readable (~7/10). [image](https://pins.insightpins.com/mcp/2026-10-03/8395ca0d-699c-4e69-b9ad-90eeb5303101.jpg) |
| 7 | optimize-pin V2 (color/boldness) | same | centered-quote / berry-blush / bold-impact, `text_size` 140 | Bolder, readable (~7/10). [image](https://pins.insightpins.com/mcp/2026-10-03/708f0c54-d86d-4eda-bb1c-97436ad7836e.jpg) |
| 8 | remake-pin (style of #4) | Minimalist Baker recipe | split-horizontal / sunset-glow / bold-impact | Strong: orange panel pops against navy photo. [image](https://pins.insightpins.com/mcp/2026-10-03/2fe664e8-e0f0-49d7-aaf0-ccffa4104b8d.jpg) |
| 9 | pin-variations | Nerd Fitness | bold-title / electric / bold-impact, GIF photo | Defect: GIF had a baked-in caption, cropped to "NEE PUSH-U". [image](https://pins.insightpins.com/mcp/2026-10-03/386f86bf-abbe-428b-ada4-44f7fae71d51.jpg) |
| 10 | fix of #9 | same | same, push-up photo | Defect: horizontal photo in full-bleed template, head cropped off. [image](https://pins.insightpins.com/mcp/2026-10-03/f8e8ba05-a06c-4170-b0ed-73e252dd5923.jpg) |

### What changed in the skills

| Finding | Change |
| - | - |
| Bot-check pages come back as success | `create-pin`: treat titles like "Just a moment...", "Client Challenge", "Access denied" with no images as a failed read; ask the user for title and image URL |
| Template default text size too small for short headlines (#1) | `create-pin`: set `text_size` on the first render (130-160 for headlines up to ~7 words); `pin-design`: listed as the most common defect |
| Preview is ~200x300 | `create-pin`: use the preview as the thumbnail test |
| GIFs with baked-in captions (#9) | `create-pin`: skip animated GIFs and images whose names suggest text (infographic, pin, collage, chart, before-after, screenshot) |
| Horizontal photo in full-bleed template (#10) | `create-pin`, `template-selection`: full-bleed templates only with vertical photos; others go in panel templates; file-name sizes hint at orientation |
| Omitted custom fields are hidden, not shown as placeholders | `create-pin`, `template-selection`: omit unknown fields; never invent price/cook time/count |
| Thin fonts fade on quote cards (#5) | `template-selection`, `style-selection`: heavy fonts and `text_size` 140-150 for quotes; attribution at the end of the title |
| Rubric assumed a photo | `scoring-rubric`: guidance for text-only pins |
| Copy added claims the source didn't make (eval) | `pin-copy`: "facts only from the source" rule |

## Requests for the InsightPins server

Full, ranked version with proposals: [MCP-IMPROVEMENTS.md](MCP-IMPROVEMENTS.md).

1. **Flag bot-check pages in `extract_url`.** Return an error (or a `blocked: true` flag) when the
   fetched page is a challenge page, instead of a "successful" result titled "Client Challenge".
2. **Return image metadata from `extract_url`**: width, height (or orientation) and whether it's
   animated, so photo choice doesn't rely on file names. Filtering out tracking pixels (`ee.gif?`),
   favicons and tiny images server-side would help too.
3. **Improve fetching for big sites.** 4 of 10 popular sites returned "Access denied". Falling back
   to Open Graph tags or a different fetch strategy would raise the success rate.
4. **Image upload.** An `upload_image` tool (or base64 input) so users can use a photo they upload
   in chat; needed for `remake-pin` and `optimize-pin` without a URL.
5. **Dark or high-contrast option for quote templates.** All `centered-quote` palettes have light
   backgrounds, which limits scroll-stopping quote pins.
6. **Quota and plans.** For paid plans: `get_quota` with plan name and limits for renders and
   keyword lookups; limit errors with `resets_at` and an `upgrade_url`.
7. **Smart default text size.** Templates' default text size is often too small for short
   headlines; auto-fitting the headline to its area would help every client, not just Claude.

## Re-test after the October 4 server deploy

4 renders on 2026-10-04 (links expire 2026-10-11). Details and follow-ups:
[MCP-IMPROVEMENTS.md, "Check of the October 4 deploy"](MCP-IMPROVEMENTS.md#check-of-the-october-4-deploy).

| # | Test | Result |
| - | - | - |
| 11 | Repeat of #10 (wide photo in `bold-title`) | Warnings `IMAGE_CROPPED` (47% visible) and `IMAGE_UPSCALED` (3.1x). [image](https://pins.insightpins.com/mcp/2026-10-04/b194d561-d6ea-43f7-a726-1762244cdf81.jpg) |
| 12 | #11 with `image_focus: "left"` | Head back in view; `IMAGE_CROPPED` still reported (the crop itself is unchanged). [image](https://pins.insightpins.com/mcp/2026-10-04/5d4cb418-c4cb-4f37-9d9c-20d7e0df237f.jpg) |
| 13 | Repeat of #1 with cook time and servings from `structured` | Fields shown; title still small at default size, and no `TITLE_SMALL` warning. [image](https://pins.insightpins.com/mcp/2026-10-04/e2124f2f-48b5-49fb-a59f-ad7cc8c2ac2c.jpg) |
| 14 | #13 with `text_size: "auto"` | Title fills its area; no warnings. [image](https://pins.insightpins.com/mcp/2026-10-04/ae000eba-db78-4ed0-82e3-19d457aee953.jpg) |

Skill changes from this round: `create-pin` uses `image_details`, `primary_image` and `structured`,
`text_size: "auto"` by default, the photo controls, and the new `references/render-warnings.md`
(what each warning means, when to re-render, and not to loop on `IMAGE_CROPPED`); the template guide
covers the 8 new templates and `uses_photo` / `uses_extra_images`.


## Contrast and color check (2026-10-04)

Prompted by the README's "optimize" example: its "after" pin used `coral-reef` on `diagonal-cut`, and
the subtitle and site name were hard to read. Measured on the full-size renders (WCAG contrast):

| Pin | Title | Subtitle | Site name | Button |
| - | - | - | - | - |
| `diagonal-cut` / `coral-reef` (old README "after") | 3.2 | 2.7 | 2.0 | |
| `split-horizontal` / `ocean-breeze` (old gallery) | 3.6 | 3.3 | 2.6 | |
| `number-badge` / `sunset-glow` (old gallery) | 7.0 | 1.8 | 1.8 | 2.5 |
| `number-badge` / `terracotta` | 17.0 | 2.6 | 2.5 | 4.4 |
| `diagonal-cut` / `midnight` (new variant B) | 6.7 | 5.9 | 4.1 | |
| `split-horizontal` / `minimalist` (new gallery) | 16.1 | 13.9 | 9.4 | |
| `vine-corners` / `forest-calm` (new gallery) | 11.2 | 6.4 | 6.2 | 3.2 |

Small text needs about 4.5:1. The coral "after" pin was also a mood mismatch: a hot sales color on
a calm winter scene. Changes:
- `style-selection.md`: rules in order (all text readable, separate from the photo by lightness,
  fit the mood), a contrast table for all 15 palettes, which templates use white-on-primary panels,
  the `number-badge` subtitle issue, and a mood table split by panel and light templates.
- `pin-design` and its checklist: contrast for the subtitle, site name and button; color that fits
  the topic and photo; faded small text as a common defect; a button label is fine, fake controls aren't.
- `optimize-pin`: diagnosis by where people drop off (not seen, not saved, not clicked), a
  hypothesis per variant, fair comparisons (B and C reuse A's headline, C reuses B's template),
  a check that every variant beats the original without new defects, and a rate-based test plan.
- `create-pin`: palette chosen by the contrast table, small text checked in the preview.
- New evals `winter-palette` and `optimize-variants`; server proposal in
  [MCP-IMPROVEMENTS.md, item 21](MCP-IMPROVEMENTS.md#21-readable-small-text-contrast-check-next-first-round).
- README examples re-rendered with readable palettes, and the optimize example now shows the
  original plus two variants that each change one thing.

### Update: the pin generator's colour map

`pin-generator-tool` #85 added an exact map of which palette colour each template draws each text
in (`docs/TEMPLATE_COLOR_ROLES.md`). The measurements above assumed white text on panels and
buttons; the templates use the palette's lighter `background` colour, so contrast is a little lower
(forest-calm's button is 2.9:1, not 3.2). The plugin's palette table now uses that pair, a generated
`template-colors.md` lists the readable palettes per template, and the gallery's text-only pin moved
from `forest-calm` to `dusty-rose` (4.9:1 button).

## Re-test after the October 5 server deploy (uploads, auto focus, overlay strength)

2 renders and 2 uploads on 2026-10-05; details in
[MCP-IMPROVEMENTS.md, "Check of the October 5 deploy"](MCP-IMPROVEMENTS.md#check-of-the-october-5-deploy-86-87-88).

| Test | Result |
| - | - |
| Upload a 1000x740 JPEG through `create_upload_link` (file posted from the command line), then `get_upload` | `ready`, `image_url` returned; a second post to the same link refused (`LINK_USED`) |
| `upload_image` with an 80x60 JPEG as base64 | Stored and returned an `image_url` |
| `bold-title` with the uploaded photo, `image_focus: "auto"`, `overlay_strength: 60` | Focus chosen at x 0.69, y 0.28 (cliffs and waterfall); `image_focus_used` returned; only `IMAGE_UPSCALED` (small photo) |
| `magazine-cover`, `image_focus: "auto"`, `overlay_strength: 30` | `OVERLAY_LOW_CONTRAST` raised as documented, with `IMAGE_CROPPED` and `TITLE_SMALL` |

Skill changes from this round: `create-pin/references/user-photos.md` (when and how to upload the
user's own photo, never a shared or reference pin, the 7-day notice, limits and errors), `"auto"`
focus and `overlay_strength` in `create-pin` step 8, the overlay warnings in `render-warnings.md`,
and `remake-pin`, `optimize-pin` and `review-pin` updated to match.

## Re-test after the second October 5 deploy (readable palettes, contrast warning, image hints)

- `list_templates` returns `readable_palettes` for every template; after #93 and #95 it is all 15
  palettes everywhere, and `template-colors.md` (regenerated from the new colour map) agrees with it
  for all 38 templates (unit test `test_matches_readable_palettes_from_list_templates`).
- One render on `dashed-accent` with `ocean-breeze`, made before #93 and #95 reached production,
  returned `LOW_CONTRAST` for the subtitle (1.9:1) and suggested Minimalist; `image_focus: "auto"`
  returned its point with `"source": "auto"`.
- `extract_url` on an insightpins.com article marked the site logo with `hint: "logo"` and listed it
  last.
- Skills: palette choice now starts from `readable_palettes`; the "six weak palettes" and "hide the
  subtitle on six templates" rules are gone; `LOW_CONTRAST` has a row in `render-warnings.md`; an
  image with a `hint` is never the pin photo, even when it is the only portrait.
- Evals: new case `hinted-photos`; graders that encoded the old weak palettes were removed
  (`no-faded-panel`, `no-weak-palette`, `no-faded-badge-subtitle`, `no-faded-button`), the winter case
  now checks the mood (`calm-palette`) and the brand case checks the button stays (`keeps-button`).

## Re-test after the October 5 evening deploy (template photo fields, promo hints, lower limits)

- `list_templates` returns `photo_area`, `best_photo` and `preview_url`; the mock is rebuilt from the
  server's generated catalog, and the skills now match photos to `best_photo` instead of a
  hand-written list of full-bleed templates (that list had `bold-title` and `gradient-wave`, which
  now put the photo in a panel).
- `extract_url` on a BBC Good Food recipe now marks the presenter headshot `author` and three promos
  `promo`, and ranks the pancake photo first.
- Limits are 20 renders and 10 uploads a day in the terms; the plugin, its mocks and the docs follow.
- Template guide: the leftover advice to hide the subtitle on `number-badge` and `side-panels` (drawn
  in a readable colour since #91) is gone.
- Graders: `crop-warning` accepts any panel template whose `best_photo` is `landscape` or `square`;
  `recipe-from-url` also accepts the wide food photo in a panel template whose `best_photo` is
  `landscape`. Unit tests build both lists from the template mock.
