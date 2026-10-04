---
name: create-pin
description: Create a Pinterest pin image with the InsightPins connector. Use when the user wants a pin, pin image, pin graphic or Pinterest image for a URL, blog post, article, product, recipe, listicle or quote, says "make a pin", "pin this" or "turn this into a pin", or asks for several pin variations of one page.
---

# Create a Pinterest pin

You make finished 1000x1500 pins with the InsightPins connector (`extract_url`, `list_templates`,
`list_styles`, `render_pin`, `get_quota`). This skill adds the judgement: which template, which
photo, which words. Apply the `pin-design` and `pin-copy` skills while you work.

If the InsightPins tools are not available, tell the user to connect **InsightPins** on the
plugin's Connectors tab (or run `/mcp` in Claude Code), then continue once it's connected. You can
still draft the copy without it.

## Workflow

1. **Get the source.**
   - URL given: call `extract_url`. Note the title, description, site name, the images with their
     `image_details`, `primary_image`, and `structured` data when the page has it.
   - **Check that the page really loaded.** Many large sites block automated requests. Errors start
     with a code:
     - `[BOT_CHALLENGE]`: the site blocks automated readers. Tell the user, and ask for the page
       title (or a short summary) and a direct image URL, then continue.
     - `[NOT_FOUND]`: the page doesn't exist. Ask the user to check the link.
     - `[FETCH_FAILED]` or anything else: the page couldn't be read. Ask the user to check the link,
       or to give the title and an image URL instead.
     As a fallback, also treat a result as blocked when its title looks like a bot check ("Client
     Challenge", "Just a moment...", "One moment, please", "Access denied", "Verify you are human")
     and it has no images. Never build a pin from such a page.
   - The page's description is often a chatty intro, not a summary. Write your own copy from what the
     page is about.
   - No URL: ask for the topic, the headline idea, an image URL and the site name. Don't invent a site name.
   - An image uploaded into the chat cannot be used as the pin photo (the tool needs a URL). Ask for a URL for it, or use a page image.

2. **Classify the content**: how-to/blog post, listicle (has a number), product, recipe, quote,
   travel/destination, or lifestyle/inspiration. Pull out facts the templates can show: the list
   number, price, cook time, servings, category. `structured` gives them directly when the page
   publishes them:
   - `Recipe`: `cook_time` for `cookTime`; if there is only a `total_time`, write it with "total"
     ("1 h 15 min total") so it isn't passed off as cook time, or leave the field out.
     `servings` for `servings` (write "4 servings").
   - `Product`: `price` for `price`, exactly as given; it already carries the symbol or currency
     code ("$100", "€49.90", "1299 CAD"). If `structured` has no price, the server couldn't read it
     reliably: ask the user, or don't use `price-tag`.
   These values come from the page itself.

3. **Write the copy** using the `pin-copy` skill: a short on-image headline (3-8 words, ideally),
   an optional subtitle, and separately the Pinterest title, description and alt text.
   Use only facts the page states: don't add selling points like "one-pan", "ready in 20 minutes"
   or "kid-friendly", or results like "that made it stick", unless the page says so.

4. **Pick the template.** Call `list_templates` (the list changes over time) and choose with
   [references/template-selection.md](references/template-selection.md). Fill `custom_fields` from
   real content only, for example `listNumber: "17"` for "17 Easy Dinners". Fields you don't pass are
   left off the pin, so omit any you don't have a real value for (never invent a price, cook time or
   count). Exception: `number-badge` and `side-panels` always show a number, so use them only when the
   content has one.

5. **Pick the style.** Call `list_styles` and choose a palette and font pairing with
   [references/style-selection.md](references/style-selection.md): first a palette whose text stays
   readable on the chosen template ([references/template-colors.md](references/template-colors.md)
   lists the readable palettes for each template), then one that stands apart from the photo
   by lightness and fits the topic's mood. If the user or their site has colors already used on
   earlier pins, keep them for brand consistency unless the template's list rules them out.
   **When the user names a palette** (a brand palette) that isn't in the template's "Readable with"
   list, keep their palette: choose a template where it is listed, or one where it is under "Also
   without a button" and send `show_cta: false`. Six palettes (forest-calm, cool-mint, sage,
   electric, coral-reef, sunset-glow) make almost every button hard to read, so with them hide the
   button unless you use `collage-style`. Tell the user in one line why the button is off.

6. **Pick the photo.** You can't see the images before rendering, so use `image_details`: each entry
   has `width`, `height`, `orientation` (portrait, landscape, square), `animated`, `alt` text,
   `source` (og, content, json-ld) and `low_resolution`.
   - Choose a photo whose `alt` matches the headline, prefer `portrait`, and skip `animated` and
     `low_resolution` ones.
   - `primary_image` is the page's share image. It is a good default, but not always the best photo:
     check its `alt` and shape like any other.
   - Skip photos whose `alt` or file name points to text or a person rather than the subject:
     "infographic", "chart", "before and after", "screenshot", "quote", author headshots and logos.
   - If a page gives no `image_details` (older responses), judge by file name: a size like
     `689x1024` hints at orientation, and `.gif`, `pixel`, `logo` or `200x200` mean skip.
   **Match the photo to the template:** full-bleed templates (photo fills the whole pin, such as
   `bold-title`, `gradient-wave`, `corner-badge`, `travel-overlay`, `destination-card`) need a
   portrait photo, or heads and products get cut off. For a landscape or square photo, use a template
   that puts the photo in a wide panel: `split-horizontal`, `recipe-card` or `product-spotlight`
   (tested), or `minimal-clean`. If a full-bleed template is still the right choice, set
   `image_focus` to the subject (see step 8).
   `list_templates` marks templates with no photo (`uses_photo: false`) and collage templates that
   take extra photos (`uses_extra_images: true`, up to 3 in `additional_image_urls`). Use extra
   photos only with those templates, and only photos that clearly belong together.

7. **Check quota before more than one render.** Call `get_quota` when making variations or when a
   render failed for limits. Tell the user how many renders a plan will use if they're running low.

8. **Render** with `render_pin`: template, palette, font, headline as `title`, subtitle as
   `description` (only on templates that support it, and not where `template-colors.md` says the
   subtitle is never readable, such as `number-badge`: send `show_description: false` there), `site_name`, `image_url`, and a CTA that fits
   the content ("Get the Recipe", "Read the Guide", "Shop Now", "See the List"; 30 characters max).
   **Set the text size on the first render**; the template default (100) is usually too small at
   thumbnail size. Use `text_size: "auto"`: it fits the title to its area (never smaller than
   normal) and keeps the other text at its size. It can't be combined with `title_size`. Use a number
   instead only when the user asks for all the text to be bigger or smaller, or when the subtitle and
   button need to grow too: 130-160 for short headlines, 120-140 for 8-12 words, 100-110 for very
   long text (or shorten it). On templates with a subtitle, keep `description_size` at 100-115.
   **Photo controls**, for single-photo templates: `image_focus` keeps a part in view when the photo
   is cropped (`top`, `bottom`, `left`, `right`, `center`, or `{ "x": 0.3, "y": 0.2 }`, 0 to 1 from
   left/top); `image_zoom` 100-200 enlarges a small product in a big frame (it softens a small
   photo); `image_fit: "contain"` shows the whole photo with bars in the palette's secondary color.
   Set `image_focus` up front when you already know where the subject is, for example `top` for a
   person in a wide photo.
   **If the tool refuses these options** (an app that still has the older tool definitions only
   allows a number for `text_size` and has no photo controls), use `text_size` 130-160 instead of
   "auto", and pick a template whose frame matches the photo's shape instead of `image_focus`.

9. **Check the preview and the warnings.** The preview image is about 200x300, roughly how the pin
   looks in a phone feed, so use it as the thumbnail test against the `pin-design` checklist. Then
   read the result's `warnings` (see [references/render-warnings.md](references/render-warnings.md)
   for what each code means and what to do). Re-render only for a real defect:
   unreadable or cut-off text (`TITLE_CLAMPED`, `DESCRIPTION_CUT`), a photo cropped so the subject is
   lost, a wrong photo, or a field showing a value that isn't true. Check the small text too: if the
   subtitle, site name or button text looks faded against its background, switch to a palette
   from the template's "Readable with" list, or hide the subtitle (`show_description: false`). Some warnings describe the pin
   rather than a defect: `IMAGE_CROPPED` stays after you've set `image_focus` well, because the crop
   itself doesn't change. Judge by the preview, and never re-render twice for the same warning.
   Fix the one thing that's wrong and keep the rest. Don't re-render for taste alone unless the user asks.

10. **Report** (keep it short):
    - the image link from the latest render and its `edit_url` (opens the pin on insightpins.com
      for editing without using a render);
    - template, palette and font used;
    - the link expires in 7 days, so download the image;
    - where the photo came from, and that they need the right to publish it;
    - ready to paste: **Pinterest title**, **description**, **alt text**, **suggested board**,
      and the destination link (the source URL).

## Variations

When asked for several pins for one page (or via `/insightpins:pin-variations`), make each pin
different in a way that matters: a different photo, a different template category and a different
headline angle (see `pin-copy` angles). If the page has only one usable photo, reuse it and vary the
template and angle, and say so. Changing only the color is not a variation. Present a short
table: pin, angle, template, link. Suggest posting them over several days or weeks, not all at once.
To schedule several pins in one go, offer the `pinterest-bulk-csv` skill to put them in a Pinterest
bulk upload CSV (the image links expire after 7 days, so the file should be uploaded soon).

## When a limit is hit

If a render fails because the daily limit is reached, say so once: how many renders were used,
when the limit resets (00:00 UTC) and, if the tool's response gives an upgrade or plans link, share
it. Then offer what doesn't need a render: finished copy, the chosen settings so they can render
later, or the `edit_url` of an earlier pin.
