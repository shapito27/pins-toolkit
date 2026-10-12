# Mockups: when the page has no image that works on a pin

Some pages give you nothing a pin can use as its photo.

- A page about an app, a tool or a browser extension has screenshots. A screenshot is wide, and its
  text is sized for a desktop screen. In a pin's photo panel it shrinks to a thin strip, or it is
  cropped and loses half its columns. A pin is about 230 px wide in the feed, so text that is 14 px
  tall on a 1900 px screenshot ends up under 2 px.
- Other pages have only a logo, an author photo or a banner, or no image at all.

For these pages, draw the image. A **mockup** is a simple picture made for the pin's photo panel:
a few large elements, and only real content.

## Three kinds of mockup

| Kind | Use it when | What it shows |
| - | - | - |
| **App screen** | There is a screenshot of the product, on this page or on the product's other public pages | A zoomed-in, cleaned-up copy of one part of the real screen |
| **Feature** | The page is about one thing the product does, and there is a real screen to copy | That one feature at work: what goes in and what comes out, as the product shows it |
| **Concept** | There is no screen to copy, but the page's point can be drawn from its text | A plain card: a short list, steps, a small table, a comparison or one key number |

Use the first kind the page supports. An app-screen or feature mockup needs a real screen to copy.
Without one it would be an invented interface, which is misleading: draw a concept card instead.

## When this applies

- The page is about software (an app, a SaaS tool, a browser extension, a dashboard, a plugin) and
  the images that show the subject are screenshots of its interface. An image's `alt` or file name
  often says so: "screenshot", "dashboard", "interface", "UI", "table", "settings", "report",
  "extension popup". An image may also carry `hint: "screenshot"` (a server may add it; treat it
  as this case, not as a junk image).
- The user gives you a screenshot as the photo for the pin.
- The page has no proper image: none at all, only images with a `hint` (logo, author, banner,
  promo), only `low_resolution` ones, or none that shows what the page is about. And the page's
  point can be drawn from its text: a tool, a feature, a workflow, a comparison, key numbers.
- You rendered a pin and the preview shows a screenshot whose text can't be read. Crop settings
  (`image_focus`, `image_zoom`, `image_fit`) won't fix it: don't re-render with them.

It does not apply to:

- **Photo-led content**: recipes and food, home decor, fashion, travel, and products people buy for
  how they look. Never draw a dish, a room, a place or a physical product: that passes off a drawing as the
  real thing. With no usable photo there, ask the user for one or use a text-only template.
- A page that isn't about software but has a stray screenshot among real photos: skip the
  screenshot like any other text image.
- A page that could not be read (blocked, or a bot check): there is nothing to draw from.
- A photo of a phone or a laptop with an app on it: that is a photo.

## Look for a real screen first

Only when you can build a mockup (see "Can you build it?" below); otherwise skip this. When a
product page has no usable image, look at the product's other public pages before settling
for a concept card: read its home page and its features page with `extract_url` (the same site
only, two extra reads at most) and look for a screenshot or a drawing of the interface. Sites often
show a simplified version of their own screen there, which is the best thing to copy.

## Recommend the mockup, then build it

Don't put an unreadable screenshot on the pin, and don't drop it silently either.

**If you can build a mockup** (see "Can you build it?" below): tell the user in one line why the
page's images won't work on a pin and that you are making a mockup instead, say what it will show
(for example "the keyword list with its search volumes, five rows"), and build it
without waiting for an answer. Stop and ask first only when you don't have real labels and numbers
for it. The user can still ask for the screenshot or their own photo afterwards.

**If you can't build one:** say a mockup would work best, then offer what can be done and wait
for the answer:

1. **An image from the user**: a closer screenshot (one part of the screen, zoomed in so a few big
   words or numbers fill it, portrait or square) or a photo of their own. They upload it as in
   `user-photos.md`.
2. **The screenshot as it is**, if the page has one, cropped to its most readable part. Say plainly
   that the text will be small.
3. **No mockup**: another photo from the page if one fits, or a text-only template
   (`uses_photo: false`).

If the user already said what they want ("use the screenshot", "no mockup", "no image"), do that
without asking again and without building a mockup.

## Can you build it?

You can build a mockup only when you can write a file, run a headless browser to turn an HTML page
into a PNG, and read the PNG to check it (Claude Code and Cowork usually can; a chat without code
tools can't). If you can't, don't promise one: say a mockup would work best and offer the three
choices above. Never say a mockup was made when it wasn't, and never describe one as if it were on
the pin.

If a step fails after you said you were making one (writing the file is refused, there is no
browser, the upload fails), stop: say the mockup could not be made and why, and offer the three
choices above. Don't render a pin in the meantime.

## What goes in a mockup

Rules for every kind:

- **Only real content.** Every label, column name and number comes from the page (`extract_url`
  text, `structured`), from the screenshot itself if you can read it, or from the user. If you
  don't have real values, ask for three to five rows of them. Never invent a metric, a count or a
  result, and never show numbers better than the product gives. Never name a number from a guess
  at what its icon means: leave the label off, or find the name on the product's pages.
- **Not from a promo banner.** A figure that appears only on the page's share banner or another
  promo graphic (a sample score, a "before and after" pair, example names) is an illustration, not
  a fact: leave it out unless the page's text or the product's real screen shows it too.
- **Live counts are dated.** A counter copied from a live screen (results found, products listed,
  visitors this month) was true when you read the page. Use it as shown, and say in the report
  that it is that day's figure and will change.
- **Zoom in instead of shrinking.** Show a small part large: two tiles of a grid, one panel, five
  rows of a table, three steps. Two tiles with every element readable beat eight tiles nobody can
  read.
- **Few, large elements.** One area, four to six rows, at most three columns. Row text at least 3%
  of the image width tall (about 60 px on an 1800 px wide image), larger for the one number that
  matters.
- **No fake controls.** No play buttons, cursors or "click here" arrows, and no buttons the product
  doesn't have.
- **No other people's content.** Use plain colour blocks where a screenshot shows other people's
  photos, pins, avatars or names.

For an **app screen** or a **feature**:

- **The product's real elements, drawn precisely.** The mockup is a cleaned-up copy of the real
  screen, not a new design. Enlarge the screenshot and look at the part you will show, then redraw
  each element as it is: the same icons (their shapes and colours, redrawn as simple vector
  shapes), the same order, the same panel shape and transparency, a similar font. If the real
  screen shows icons with no text labels, the mockup shows icons with no text labels: don't add
  captions the product doesn't have. Controls the real screen shows (its own small action icons)
  may be drawn as they are. Leave out menus, filters, pagination and side columns.
- **Icons you can't redraw.** If you stand in a stock symbol or an emoji for one of the product's
  own icons, pick the closest in shape and colour and say in the report which icons are
  stand-ins. Don't swap an icon for one with another meaning.
- **Work from what is public.** The screenshot and the product's public pages are your references.
  Don't assume you can read the product's source code.
- **A browser bar for things that run on a website.** When the product is a browser extension or
  works inside another site, frame the mockup with a plain browser bar showing that site's domain
  and its favicon. It tells the viewer where the product works. The favicon must look like the
  real one: use the site's actual favicon file when you can fetch it, otherwise redraw it closely
  (the same shape, colour and letter). A neutral dot or a made-up icon is wrong. Show only the
  domain and the favicon: no other part of that site's interface, and nothing that suggests the
  site made or endorses the product.

For a **concept** card:

- **A plain card, not a pretend app.** No window bar, no browser bar, no menus, and nothing styled
  to look like the product's or any other company's interface. It is a diagram of the idea.
- **Drawn from the page's own words.** The steps the page lists, the items it compares, the number
  it reports. Shorten them; don't add any.
- **One idea.** A list of three to five lines, three steps with arrows, a two-column comparison, or
  one big number with its label. Use the site's colours if you know them, otherwise the pin
  palette's.

## Which templates a mockup fits

A mockup is text, so it can't be cropped, repeated or shrunk the way a photo can. No mockup fits
every template.

- **Use a single-photo `panel` template** (`photo_area: "panel"`) whose panel is large:
  `split-horizontal`, `checklist`, `numbered-steps`, `minimal-clean`, `image-focus`, `bold-title`
  (`split-horizontal` and `checklist` are tested with mockups; the others are chosen from their
  layouts).
- **Never** a `full-bleed` template (the mockup is blown up until only parts of words show, with
  the title on top of it), a `multi` template (the same mockup is repeated in every photo box),
  `text-focus` (the image is a small accent), `arch-window` (the arch cuts the corners) or
  `vertical-title` (a tall, narrow slice).
- The user can open the pin in the editor and try other templates there. Many of them will crop
  or repeat the mockup: say so in the report.

## Size and rendering

- **Made to measure.** Match the panel's shape so nothing is cropped, and draw the image at twice
  the panel's size. Measured on the 1000x1500 pin: the `split-horizontal` panel is 4:3, about
  1000x750 (a 2000x1500 image fills it uncropped); the `checklist` panel with six items is about 904x744 (an
  1808x1488 image) and with four items about 904x868 (an 1808x1736 image); fewer list items leave
  a taller panel. For another template, look at its sample in `preview_templates` and estimate the
  panel's width and height, or go by `best_photo` (square, or 3:2 for landscape).
- **Or a safe zone**, when you don't know the panel's shape or the user will try several
  templates: draw a square image with one flat background colour and keep every element inside
  the central 70% of its width and height. A square or landscape panel then trims only
  background. The elements come out smaller than in a made-to-measure image, so use fewer rows.
- Keep everything important at least 4% in from each edge: the panel has rounded corners and its
  shape can change a little with the amount of text.
- Use white or the product's own background colour, one flat colour to the edges.
- **Choose the background and the palette together.** The mockup must stand apart from the pin's
  text panel by lightness: a dark mockup under a dark panel reads as one black block. With a dark
  mockup pick a palette whose panel is light or coloured; with a light mockup, a dark or coloured
  one.
- Write one self-contained HTML file with inline CSS: no scripts, and fonts that are already on the
  machine. Set the page to the exact image size and capture it with a headless browser at that
  window size. Open the PNG and check it before uploading: no text cut off, nothing overlapping,
  every number as given.
- Upload the PNG as in `user-photos.md` (`create_upload_link`) and pass the returned `image_url` to
  `render_pin` with the default `image_fit`. A mockup costs one upload and the pin one render: say
  so first if the user is low on either (`get_quota`).
- Check the pin preview like any other. If the mockup's text is still small, enlarge the type and
  cut a row; don't add more.

## Report

In addition to the usual report: say the image is a mockup made for the pin and which kind (a
simplified copy of the product's screen, or a concept card drawn from the page's text), name where
its labels and numbers came from, list anything you could not verify (and any icons that are
stand-ins), name the figures that are live counts and will change, say that the mockup was made
for this template and other templates in the editor may crop or repeat it, and say that the uploaded
mockup is kept for 7 days (the `edit_url` stops showing it after that). If you kept the HTML file,
say where it is.
