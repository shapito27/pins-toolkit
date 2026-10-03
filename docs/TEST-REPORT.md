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
