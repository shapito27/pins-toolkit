# Palette and font selection

Always call `list_styles` first; palettes and font pairings can change. Use this guide to choose.

## Rules, in order

1. **Every piece of text must be readable.** The headline needs strong contrast, and so do the
   subtitle, site name and button text. They are small, and many templates draw them lighter than
   the headline. Check the palette against the table below and the template's list in
   [template-colors.md](template-colors.md) before rendering.
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
   template where it passes, hiding the button if needed (the "Also without a button" column in
   template-colors.md), or tell them in one line and offer a readable alternative. Don't swap their
   choice silently.
5. **One mood per pin.** Font pairing and palette should say the same thing (elegant, playful,
   bold, calm).

Rule 1 wins over everything else, then rule 2, then rule 3 and the mood table below.

## Contrast: which palettes keep text readable

Most templates draw some text in the palette's light `background` colour on its `primary` colour:
the title and subtitle on colour-panel templates (`split-horizontal`, `diagonal-cut`, `bold-title`
and others) and the button on almost every template. How readable that is depends only on the
palette:

| Palette | Light text on primary | Rating |
| - | - | - |
| minimalist | 15.4 | Strong: all text reads, including small text |
| berry-blush | 5.8 | Strong |
| midnight | 5.7 | Strong |
| dusty-rose | 4.9 | Strong |
| lavender | 4.3 | Good: title, subtitle and button read; small text is faint |
| terracotta | 4.0 | Good |
| warm-earth | 3.9 | Good |
| rose-gold | 3.5 | Good |
| ocean-breeze | 3.2 | Good, but not on `split-horizontal` or `diagonal-cut`, where the subtitle is faded |
| forest-calm | 2.9 | Fails: the button and any panel text are hard to read |
| coral-reef | 2.8 | Fails |
| cool-mint | 2.6 | Fails |
| sunset-glow | 2.3 | Fails |
| sage | 2.3 | Fails |
| electric | 2.1 | Fails |

Numbers are WCAG contrast ratios. Text of 24px and up (titles, subtitles, buttons at default size)
needs 3 or more; small text (site names, labels) needs 4.5.

**Check the template too.** [template-colors.md](template-colors.md) lists, for each of the 38
templates, the palettes that keep its title, subtitle and button readable, the extra palettes that
work when you hide the button (`show_cta: false`), and its known problems. Six templates draw the
subtitle in the light secondary colour, which is never readable (`number-badge`, `dashed-accent`,
`starburst-badge`, `arch-window`, `side-panels`, `lifestyle-collage`): leave the subtitle out there
(`show_description: false`) and put that line in the Pinterest description. `gradient-wave` is
readable only with minimalist.

**A "Fails" palette is still usable** on a template whose text is dark on a light background, if
you hide the button (`show_cta: false`): the template list names those combinations. Use this when
the user asks for that palette or the topic needs its colour (greens for gardening).

**If `list_styles` returns different colours**, recompute: contrast = (L1 + 0.05) / (L2 + 0.05),
where L is the relative luminance of the lighter (L1) and darker (L2) colour, here the palette's
`background` and `primary`.

## Palette by mood and topic

Every palette here passes for the button. On a colour-panel template, also check that it is in the
template's "Readable with" list in [template-colors.md](template-colors.md).

| Mood / topic | On colour-panel templates | On light templates |
| - | - | - |
| Food, cooking, baking, autumn | terracotta, warm-earth, berry-blush (desserts) | terracotta, warm-earth, berry-blush |
| Home decor, interiors, wedding, beauty | dusty-rose, warm-earth, berry-blush | rose-gold, dusty-rose, warm-earth |
| Health, wellness, gardening, nature | warm-earth, midnight, lavender | lavender, warm-earth |
| Travel, outdoors, water, winter | midnight, minimalist | ocean-breeze, midnight |
| Finance, business, career, tech | midnight, minimalist | midnight, minimalist |
| Kids, crafts, parties, fun | berry-blush, dusty-rose | berry-blush, dusty-rose |
| Fashion, luxury, minimal aesthetic | minimalist, berry-blush | minimalist, rose-gold |
| Spirituality, self-care, quotes | lavender, midnight | lavender, dusty-rose |
| Sales, deals, urgent or bold | terracotta, berry-blush | terracotta, berry-blush |

These are starting points: check the photo against rule 2 and switch to another listed palette
when the panel colour and the photo blend together. The green, coral and bright palettes
(forest-calm, cool-mint, sage, electric, coral-reef, sunset-glow) are left out because their button
text is hard to read; use them on a light template with `show_cta: false` when the colour matters
more than the button.

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
