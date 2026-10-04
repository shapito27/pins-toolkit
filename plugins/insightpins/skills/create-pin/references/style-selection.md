# Palette and font selection

Always call `list_styles` first; palettes and font pairings can change. Use this guide to choose.

## Rules, in order

1. **Every piece of text must be readable.** The headline needs strong contrast, and so do the
   subtitle, site name and button text. They are small, and many templates draw them lighter than
   the headline. Check the palette against the contrast table below before rendering.
2. **Separate the text area from the photo by lightness, not only by hue.** A dark panel next to a
   bright photo (snow, beach, white kitchen) or a light panel next to a dark, moody photo stands out.
   Two mid-tones side by side (a bright blue panel above a blue sky) blur together at thumbnail size.
3. **Fit the topic's mood.** Color says something before the words are read. Red, coral and orange
   say energy, appetite, fun or urgency: good for food, deals, kids and fitness, wrong for calm
   topics (winter, wellness, luxury, spirituality). A color that echoes one in the photo (the green of
   a salad, the blue of a lake) looks designed; one that fights the photo's mood looks like an ad.
4. **Brand consistency.** If the user has a brand color or used a palette on earlier pins, reuse it,
   as long as it passes rule 1. Recognizable pins across a feed build trust. If the user asks for a
   palette by name and it fails rule 1 on the template you planned, keep their palette and switch to
   a template where it passes (a light-background one), or tell them in one line and offer a
   readable alternative. Don't swap their choice silently.
5. **One mood per pin.** Font pairing and palette should say the same thing (elegant, playful,
   bold, calm).

Rule 1 wins over everything else, then rule 2, then rule 3 and the mood table below.

## Contrast table (measured 2026-10-04)

Templates use the palette in two ways:
- **Color panel or band** (tested: `split-horizontal`, `diagonal-cut`): white text on the palette's
  primary color. The subtitle and site name are drawn lighter, so the panel color must be dark.
- **Light background** (tested: `minimal-clean`, `number-badge`, `quote-with-image`,
  `vine-corners`): the palette's dark text color on its pale background. Every palette passes for
  the headline. Buttons are white bold text on the primary color; bold button labels need 3 or more
  in the table below, so sunset-glow, sage, electric and (just) cool-mint make them hard to read.

| Palette | White on primary (panels, buttons) | Use on panel templates |
| - | - | - |
| minimalist | 16.1 | Strong: all text reads, including site name |
| berry-blush | 7.0 | Strong |
| midnight | 6.9 | Strong |
| dusty-rose | 5.9 | Good: headline and subtitle; site name faint |
| lavender | 5.2 | Good |
| warm-earth | 4.6 | Good, keep `description_size` 110-115 |
| terracotta | 4.4 | Good, keep `description_size` 110-115 |
| rose-gold | 3.8 | Headline only: hide the subtitle or choose another palette |
| ocean-breeze | 3.7 | Headline only |
| forest-calm | 3.3 | Headline only |
| coral-reef | 3.2 | Headline only |
| cool-mint | 3.0 | Avoid on panels (just under 3) |
| sunset-glow | 2.7 | Avoid on panels |
| sage | 2.5 | Avoid on panels |
| electric | 2.3 | Avoid on panels |

Numbers are WCAG contrast ratios. Body-size text needs 4.5 or more; large or bold text (the
headline, button labels) needs at least 3. On a pin, the subtitle and site name are small, so treat
them as body text.

**If `list_styles` returns different colors**, recompute: contrast = (L1 + 0.05) / (L2 + 0.05),
where L is the relative luminance of the lighter (L1) and darker (L2) color. White has L = 1.
A quick check without math: if the panel color is about as light as a medium gray or lighter
(bright blue, orange, coral, lime, turquoise), white small text on it will be hard to read.

**Known template issue:** `number-badge` draws its subtitle and site name in the palette's light
secondary color, which fails on every palette (about 1.5-2.9) except minimalist (4.4). On that
template, leave the subtitle out (`show_description: false`) and put that line in the Pinterest
description instead. The site name stays faint there; that's acceptable for a small brand line, or
use minimalist. Check other templates' small text in the preview the same way.

## Palette by mood and topic

| Mood / topic | On panel templates | On light templates |
| - | - | - |
| Food, cooking, baking, autumn | terracotta, warm-earth, berry-blush (desserts) | terracotta, warm-earth, coral-reef |
| Home decor, interiors, wedding, beauty | dusty-rose, warm-earth, berry-blush | rose-gold, dusty-rose, warm-earth |
| Health, wellness, gardening, nature | warm-earth, midnight, lavender | forest-calm, warm-earth |
| Travel, outdoors, water, winter | midnight, minimalist | ocean-breeze, midnight |
| Finance, business, career, tech | midnight, minimalist | midnight, minimalist |
| Kids, crafts, parties, fun | berry-blush, dusty-rose | coral-reef, berry-blush |
| Fashion, luxury, minimal aesthetic | minimalist, berry-blush | minimalist, rose-gold |
| Spirituality, self-care, quotes | lavender, midnight | lavender, dusty-rose |
| Sales, deals, urgent or bold | terracotta, berry-blush | coral-reef, terracotta |

These are starting points: check the photo against rule 2 and switch to another listed palette
when the panel color and the photo blend together. sunset-glow, sage, electric and cool-mint are
left out because their button text (white on the primary color) is hard to read; on light
templates, use them only with `show_cta: false`.

## Font pairing by mood

| Mood | Font pairings |
| - | - |
| Bold, attention-grabbing, listicles, fitness, deals | bold-impact, modern-sans |
| Clean, modern, how-to, business, tech | modern-sans, minimalist, tech-modern, professional |
| Elegant, home, wedding, beauty, luxury | classic-serif, editorial |
| Warm, family, food, lifestyle | friendly, classic-serif |
| Fun, kids, casual | playful, friendly |
| Artistic, fashion, creative | creative, editorial |

Thin or decorative display fonts (`editorial`, `creative`) are harder to read at thumbnail size;
avoid them for long headlines and quotes, or raise `title_size` and keep the headline short.
