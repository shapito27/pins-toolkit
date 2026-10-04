# InsightPins for Claude

Make Pinterest pins that get noticed and clicked, right from a conversation with Claude.

Give Claude a link to your blog post, product page or recipe and it turns it into a finished
1000x1500 pin: it reads the page, writes a short headline, picks a matching InsightPins template,
color palette and font pairing, renders the image, and checks the result. You also get a
ready-to-paste Pinterest title, description, alt text and board suggestion.

The plugin connects Claude to the [InsightPins](https://insightpins.com) pin generator and adds
skills that teach Claude what makes a good pin: readable text at phone size, one clear focal
point, a strong headline and search-friendly copy.

## What you can do

- **Create a pin from a URL** - "Make a pin for https://myblog.com/fall-soups"
- **Make several variations** - different templates, photos and headline angles for the same page, so you can post fresh pins and see which performs best
- **Remake a pin, better** - upload a pin you like (yours or one for inspiration) and Claude builds a new, original pin with a similar style and stronger design and copy
- **Review a pin** - upload a pin and get a scored review: readability, contrast, layout, headline, branding and copy, with concrete fixes
- **Optimize a pin** - get a review plus improved versions aimed at more saves and clicks
- **Check a bulk upload CSV** - find every row Pinterest would reject (long titles, Drive or Dropbox
  links instead of image files, dates a spreadsheet rewrote, missing boards, unquoted commas, repeated
  links, files over 200 pins) with the fix for each
- **Schedule pins in bulk** - turn a list of pins into a ready-to-upload CSV, spread across days in
  your time zone and converted to UTC, split into files of up to 200 pins

## Commands

| Command | What it does |
| - | - |
| `/insightpins:pin <url>` | Create one pin for a page |
| `/insightpins:pin-variations <url> [count]` | Create several different pins for one page |
| `/insightpins:review-pin` | Review and score an uploaded pin (uses no renders) |
| `/insightpins:optimize-pin` | Review a pin and render improved versions to A/B test |
| `/insightpins:remake-pin` | Make a new pin in the style of an uploaded one, but better |
| `/insightpins:pinterest-bulk-csv` | Build or check a Pinterest bulk upload CSV |

In claude.ai chat and Cowork you don't need commands: just describe what you want and Claude uses
the right skill.

## Skills

- **create-pin** - the full workflow from a URL to a finished pin and ready-to-paste copy
- **pin-design** - visual best practices: readability at phone size, layout, photo, color, branding
- **pin-copy** - headlines, Pinterest titles, descriptions, alt text, boards and keywords
- **review-pin** - scores a pin on an 8-point rubric and ranks the fixes
- **optimize-pin** - turns a review into 2-3 improved variants, each testing one change
- **remake-pin** - recreates a pin's style for your content, with original photo and copy
- **pinterest-bulk-csv** - builds and checks Pinterest bulk upload CSV files, with two small Python
  scripts for exact character counts, UTC dates and CSV quoting. The same rules run in the free
  [Pinterest CSV checker](https://insightpins.com/tools/pinterest-csv-checker.html)

## Setup

1. Install the plugin from the Claude directory.
2. Open the plugin's **Connectors** tab and connect **InsightPins**. You sign in with your Google account (OAuth). No API key is needed.
3. Ask Claude to make a pin.

In Claude Code the connector loads with the plugin; run `/mcp` to sign in.

The connector's server is `https://app.insightpins.com/api/mcp`. Its tools and limits are documented at
[app.insightpins.com/mcp](https://app.insightpins.com/mcp).

## Usage limits

Each rendered pin counts against your InsightPins daily render limit (currently 50 free renders per
account per day), which resets at 00:00 UTC.
Claude checks your remaining renders before making several pins and only re-renders when you ask
for a change or the preview has a real defect. Plans with higher limits may be offered on
insightpins.com; see the website for current plans.

## Data handling

This plugin contains instructions (skills and commands), a connector reference, and two Python
scripts in the `pinterest-bulk-csv` skill (`build_csv.py`, `check_csv.py`). Claude runs those scripts
only when you ask it to build or check a bulk upload CSV. They use only Python's standard library,
read and write the CSV and JSON files you work with, and make no network requests: your CSV is not
sent to InsightPins or anywhere else. Nothing else in the plugin runs code.

When you use it, Claude sends the following to the InsightPins server at `app.insightpins.com`
through the connector:

- the page URLs you ask it to turn into pins (the server fetches the page to read its title, description and images)
- the pin text (headline, subtitle, button text, site name) and the image URLs chosen for the pin
- your template, palette, font and text size choices, and template fields such as a price or cook time

The server fetches the page and the images to draw the pin, and doesn't keep the page content.
It never receives your conversation or files you upload to Claude: pins you upload for review or
remakes are read by Claude in the conversation only.

What InsightPins keeps:

- **Your account.** Signing in with Google gives InsightPins your email address, name and Google
  account ID, which identify you. It never sees your Google password and doesn't store your
  profile picture.
- **The connection.** Which app is connected, when, and a hashed copy of its access token. Claude
  never gets your Google sign-in. Unused connections expire after 30 days.
- **Render records.** For each pin: the time, template, colors, font, image format and size, and the
  headline. They count your daily limit and list your recent pins, and stay as long as your account.
- **Rendered images**, for 7 days. Anyone with an image's link can open it, so share links with care.
- **Server logs**, including failed page fetches or renders with your account ID and the URL involved.
The plugin sends no data to any other service. See the InsightPins
[privacy policy](https://insightpins.com/privacy.html) and
[terms of service](https://insightpins.com/terms-of-use.html).

## Support

Email [ruslan@insightpins.com](mailto:ruslan@insightpins.com) or see
[insightpins.com/contacts.html](https://insightpins.com/contacts.html).

## Images and copyright

Pins often use photos from the page you link. Claude always tells you where the photo came from.
Make sure you have the right to publish it, or use your own images or licensed stock photos. When
you upload someone else's pin for inspiration, Claude creates an original design and copy rather
than copying their image or text.

## Disclaimer

Pinterest is a trademark of Pinterest, Inc. InsightPins is an independent product and is not
affiliated with, endorsed by or sponsored by Pinterest.

## License

MIT - see [LICENSE](LICENSE).
