# Template selection

Always call `list_templates` first: templates are added and changed over time. Use this guide to
choose among what the list returns. Each template says whether it shows a subtitle
(`supports_subtitle`), whether it uses a photo (`uses_photo`), whether it takes extra photos
(`uses_extra_images`) and which `custom_fields` it takes. Templates marked (new) were added in
October 2026 and chosen here from their descriptions, not yet tested.

## By content type

| Content | Good first choices | Notes |
| - | - | - |
| How-to / blog post / guide | `bold-title`, `minimal-clean`, `split-horizontal`, `magazine-cover`, `text-focus` | Headline does the work; pick a template with a subtitle if the benefit needs explaining |
| Listicle ("17 ideas", "10 tips") | `number-badge`, `travel-overlay`, `side-panels`, `fitness-grid`, `blog-card` | Put the real number in `listNumber`; the number is the hook |
| Step-by-step / checklist | `numbered-steps`, `checklist` | Short subtitle listing what's covered |
| Product | `product-spotlight`, `price-tag`, `side-rail` (new) | Use `price-tag` only with a real price (`structured.price`); clean product photo on a plain background works best. A square product photo sits small in `product-spotlight`: `image_zoom` 130-160 enlarges it |
| Recipe | `recipe-card`, `split-horizontal`, `photo-stack` (new; only with 4 different matching photos: the main one plus 3 in `additional_image_urls`. With fewer it repeats them, and one photo fills all four slots), `bold-title` (portrait photo only) | Fill `cookTime` and `servings` from `structured`; food photo carries the pin |
| Quote / mindset / saying | `vine-corners` (new), `tulip-frame` (new), `centered-quote`, `quote-with-image` | Keep the quote under ~20 words. `vine-corners` and `tulip-frame` are text-only with a subtitle for the attribution; `centered-quote` has no subtitle, so put the attribution at the end of the title ("... - Thoreau"). Use a heavy font (`classic-serif`, `bold-impact`, `professional`); thin fonts fade on light backgrounds |
| Travel / destination | `destination-card`, `travel-overlay`, `arch-window` | Big scenic photo; headline names the place |
| Lifestyle / home / fashion inspiration | `lifestyle-collage`, `overlap-collage` (new, 3 photos), `photo-quad` (new, 4 photos), `collage-style`, `arch-window`, `modern-minimal`, `story-card` | Collages need photos that match in tone. `photo-quad` shows two short script labels (`photoLabelTop`, `photoLabelBottom`): set them from the content or leave them out |
| Bold, trend or "stop the scroll" content | `diagonal-cut`, `starburst-badge`, `corner-badge`, `framed-bold`, `gradient-wave`, `grid-lines` (new), `vertical-title` (new) | Good for variations and A/B tests. `grid-lines` has two round badges (`badgeTop`, `badgeBottom`, defaults "NEW ON THE BLOG", "SAVE FOR LATER"); pass only text that's true. `vertical-title` needs a portrait photo (full height) |

## By photo

- **Photo shape matters most.** Full-bleed templates (`bold-title`, `gradient-wave`, `corner-badge`,
  `travel-overlay`, `destination-card`, `framed-bold`, `starburst-badge`, `vertical-title`) crop the
  photo to fill a tall frame, so they suit portrait photos. Landscape or square photos usually go in
  a wide panel: `split-horizontal`, `recipe-card`, `product-spotlight` (tested) or `minimal-clean`
  (see the last bullet for the exception).

- **Busy photo** (lots of detail behind where text would go): choose a template that puts text on a
  solid band or panel (`split-horizontal`, `image-focus`, `minimal-clean`, `story-card`,
  `text-focus`), not a full-bleed overlay.
- **Calm vertical photo with empty space**: full-bleed overlays work (`bold-title`, `gradient-wave`, `corner-badge`).
- **Weak or small photo**: use a typography-led template (`text-focus`, `split-horizontal`) so the photo is small.
- **No photo at all**: use a template with `uses_photo: false` (`centered-quote`, `vine-corners`,
  `tulip-frame`). Every other template needs a photo, so ask the user for an image URL first.
- **A full-bleed template with a landscape photo**: if it must be full-bleed, set `image_focus` on
  the subject (for example `left` or `top`), or `image_fit: "contain"` to show the whole photo with
  bars. A panel template is usually better.

## Custom fields

- Fill custom fields only with real values from the content. Never invent a price, cook time,
  servings or count.
- Fields you don't pass are left off the pin, so just omit what you don't know.
- Exception: `number-badge` and `side-panels` always show a number, so use them only for content that has one.
- `categoryLabel` is a short topic tag ("Home Decor", "Budget Travel"), not the site name.
- `listPrefix` is a short word before the number ("TOP", "BEST"); leave it off if it reads oddly.

## Variations

For several pins of the same page, pick templates from different rows above (for example one
listicle template, one bold/creative and one split layout), so the pins look clearly different in
the feed.
