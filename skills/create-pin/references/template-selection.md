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
| Recipe | `recipe-card`, `bold-title`, `image-focus` | Fill `cookTime` and `servings` from the recipe if known; food photo carries the pin |
| Quote / mindset / saying | `centered-quote`, `quote-with-image` | Keep the quote under ~20 words; attribute it in the subtitle if the template has one |
| Travel / destination | `destination-card`, `travel-overlay`, `arch-window` | Big scenic photo; headline names the place |
| Lifestyle / home / fashion inspiration | `lifestyle-collage`, `collage-style`, `arch-window`, `modern-minimal`, `story-card` | Collages need 2-3 photos that match in tone |
| Bold, trend or "stop the scroll" content | `diagonal-cut`, `starburst-badge`, `corner-badge`, `framed-bold`, `gradient-wave` | Good for variations and A/B tests |

## By photo

- **Busy photo** (lots of detail behind where text would go): choose a template that puts text on a
  solid band or panel (`split-horizontal`, `image-focus`, `minimal-clean`, `story-card`,
  `text-focus`), not a full-bleed overlay.
- **Calm photo with empty space**: full-bleed overlays work (`bold-title`, `gradient-wave`, `corner-badge`).
- **Weak or small photo**: use a typography-led template (`text-focus`, `split-horizontal`) so the photo is small.
- **No photo at all**: `centered-quote` or `text-focus`; ask the user for an image before using a photo template.

## Custom fields

- Fill custom fields only with real values from the content.
- If a template shows a field you have no value for (a price, a list number), choose another
  template instead of showing the default placeholder. `number-badge` and `side-panels` always show
  a number, so use them only for content that has one.
- `categoryLabel` is a short topic tag ("Home Decor", "Budget Travel"), not the site name.
- `listPrefix` is a short word before the number ("TOP", "BEST"); leave it off if it reads oddly.

## Variations

For several pins of the same page, pick templates from different rows above (for example one
listicle template, one bold/creative and one split layout), so the pins look clearly different in
the feed.
