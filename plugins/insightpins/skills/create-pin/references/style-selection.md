# Palette and font selection

Always call `list_styles` first; palettes and font pairings can change. Use this guide to choose.

## Rules, in order

1. **Every piece of text must be readable.** The headline needs strong contrast, and so do the
   subtitle, site name and button text. They are small, and many templates draw them lighter than
   the headline. Pick from the template's `readable_palettes` in `list_templates` (on an older
   server without that field, from its list in [template-colors.md](template-colors.md)) before
   rendering, and check the table below for the small text.
2. **Separate the text area from the photo by lightness, not only by hue.** A dark panel next to a
   bright photo (snow, beach, white kitchen) or a light panel next to a dark, moody photo stands out.
   Two mid-tones side by side (a bright blue panel above a blue sky) blur together at thumbnail size.
3. **Fit the topic's mood.** Color says something before the words are read. Red, coral and orange
   say energy, appetite, fun or urgency: good for food, deals, kids and fitness, wrong for calm
   topics (winter, wellness, luxury, spirituality). A color that echoes one in the photo (the green of
   a salad, the blue of a lake) looks designed; one that fights the photo's mood looks like an ad.
4. **Brand consistency.** If the user has a brand color or used a palette on earlier pins, reuse it,
   as long as it passes rule 1. Recognizable pins across a feed build trust. If the user asks for a
   palette by name and it fails rule 1 on the template you planned, keep their palette and pick a
   template whose `readable_palettes` has it, hiding the button if needed (the "Also without a
   button" column in template-colors.md), or tell them in one line and offer a readable
   alternative. Don't swap their choice silently.
5. **One mood per pin.** Font pairing and palette should say the same thing (elegant, playful,
   bold, calm).

Rule 1 wins over everything else, then rule 2, then rule 3 and the mood table below.

## Contrast: which palettes keep text readable

Since October 5, 2026 every palette keeps the title, subtitle and button readable on every
template: `list_templates` lists all 15 in each template's `readable_palettes`. Most templates draw
some text in the palette's light `background` colour on its `primary` colour (the button on almost
every template, and the title and subtitle on colour-panel templates such as `split-horizontal`,
`diagonal-cut` and `bold-title`), and that pair now reaches 3:1 on every palette:

| Palette | Light text on primary | Rating |
| - | - | - |
| minimalist | 15.4 | Strong: all text reads, including small text |
| berry-blush | 5.8 | Strong |
| midnight | 5.7 | Strong |
| dusty-rose | 4.9 | Strong |
| lavender | 4.3 | Good: title, subtitle and button read; small text on the panel is faint |
| terracotta | 4.0 | Good |
| warm-earth | 3.9 | Good |
| rose-gold | 3.5 | Good |
| ocean-breeze | 3.2 | Good |
| forest-calm | 3.2 | Good |
| sage | 3.2 | Good |
| electric | 3.2 | Good |
| sunset-glow | 3.2 | Good |
| coral-reef | 3.2 | Good |
| cool-mint | 3.2 | Good |

Numbers are WCAG contrast ratios. Text of 24px and up (titles, subtitles, buttons at default size)
needs 3 or more; small text (site names, labels) needs 4.5, which only the "Strong" palettes give
on a colour panel.

**Check the template too.** `list_templates` gives each template's `readable_palettes`: the
palettes on which its title, subtitle and button all reach 3:1, so a render with one of them never
warns `LOW_CONTRAST`. Pick from it even though it lists every palette today: palettes and templates
change. [template-colors.md](template-colors.md) is generated from the same colour map and adds
what that list doesn't judge: where the site name is faint, labels drawn in a light colour, and
text that sits on the photo. When the site name matters (a brand that wants its domain seen), pick
a palette its notes name as fully readable.

**If `list_styles` returns different colours**, recompute: contrast = (L1 + 0.05) / (L2 + 0.05),
where L is the relative luminance of the lighter (L1) and darker (L2) colour, here the palette's
`background` and `primary`.

## Palette by mood and topic

Every palette keeps the pin readable, so choose by the topic's mood and by the photo (rule 2).

| Mood / topic | Palettes |
| - | - |
| Food, cooking, baking, autumn | terracotta, warm-earth, sunset-glow, berry-blush (desserts) |
| Home decor, interiors, wedding, beauty | dusty-rose, rose-gold, warm-earth, berry-blush |
| Health, wellness, gardening, nature | forest-calm, sage, cool-mint, warm-earth, lavender |
| Travel, outdoors, water, winter | ocean-breeze, midnight, electric, cool-mint, minimalist |
| Finance, business, career, tech | midnight, minimalist, electric |
| Kids, crafts, parties, fun | coral-reef, sunset-glow, berry-blush, electric |
| Fashion, luxury, minimal aesthetic | minimalist, berry-blush, rose-gold |
| Spirituality, self-care, quotes | lavender, midnight, dusty-rose |
| Sales, deals, urgent or bold | coral-reef, sunset-glow, terracotta, berry-blush |

These are starting points: check the photo against rule 2 and switch to another palette from the
row when the panel colour and the photo blend together (a blue panel above a blue sky, a green
panel next to a salad). Red, coral and orange palettes (coral-reef, sunset-glow, terracotta) still
say energy and urgency, so keep them off calm topics such as winter, wellness and luxury.

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
