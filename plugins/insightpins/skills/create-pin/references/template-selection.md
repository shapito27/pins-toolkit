# Template selection

Always call `list_templates` first: templates are added and changed over time. Use this guide to
choose among what the list returns. Each template says whether it shows a subtitle
(`supports_subtitle`) and which `custom_fields` it takes.

## By content type

| Content | Good first choices | Notes |
| - | - | - |
| How-to / blog post / guide | `bold-title`, `minimal-clean`, `split-horizontal`, `magazine-cover`, `text-focus` | Headline does the work; pick a template with a subtitle if the benefit needs explaining |
| Listicle ("17 ideas", "10 tips") | `number-badge`, `travel-overlay`, `side-panels`, `fitness-grid`, `blog-card` | Put the real number in `listNumber`; the number is the hook |
| Step-by-step / checklist | `numbered-steps`, `checklist` | Short subtitle listing what's covered |
| Product | `product-spotlight`, `price-tag` | Use `price-tag` only with a real price; clean product photo on a plain background works best |
| Recipe | `recipe-card`, `split-horizontal`, `bold-title` (vertical photo only) | Fill `cookTime` and `servings` from the recipe if known; food photo carries the pin |
| Quote / mindset / saying | `centered-quote`, `quote-with-image` | Keep the quote under ~20 words. `centered-quote` has no subtitle, so put the attribution at the end of the title ("... - Thoreau"). Use a heavy font (`classic-serif`, `bold-impact`, `professional`) and `text_size` 140-150; thin fonts fade on its light background |
| Travel / destination | `destination-card`, `travel-overlay`, `arch-window` | Big scenic photo; headline names the place |
| Lifestyle / home / fashion inspiration | `lifestyle-collage`, `collage-style`, `arch-window`, `modern-minimal`, `story-card` | Collages need 2-3 photos that match in tone |
| Bold, trend or "stop the scroll" content | `diagonal-cut`, `starburst-badge`, `corner-badge`, `framed-bold`, `gradient-wave` | Good for variations and A/B tests |

## By photo

- **Photo shape matters most.** Full-bleed templates (`bold-title`, `gradient-wave`, `corner-badge`,
  `travel-overlay`, `destination-card`, `framed-bold`, `starburst-badge`) crop the photo to fill
  2:3, so use them only with vertical photos. Horizontal, square or unknown-shape photos go in a wide
  panel: `split-horizontal`, `recipe-card`, `product-spotlight` (tested) or `minimal-clean`.

- **Busy photo** (lots of detail behind where text would go): choose a template that puts text on a
  solid band or panel (`split-horizontal`, `image-focus`, `minimal-clean`, `story-card`,
  `text-focus`), not a full-bleed overlay.
- **Calm vertical photo with empty space**: full-bleed overlays work (`bold-title`, `gradient-wave`, `corner-badge`).
- **Weak or small photo**: use a typography-led template (`text-focus`, `split-horizontal`) so the photo is small.
- **No photo at all**: `centered-quote` works without an image. Most other templates are built around
  a photo, so ask the user for an image URL before using one.

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
