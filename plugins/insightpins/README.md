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

## Commands

| Command | What it does |
| - | - |
| `/insightpins:pin <url>` | Create one pin for a page |
| `/insightpins:pin-variations <url> [count]` | Create several different pins for one page |
| `/insightpins:review-pin` | Review and score an uploaded pin (uses no renders) |
| `/insightpins:optimize-pin` | Review a pin and render improved versions to A/B test |
| `/insightpins:remake-pin` | Make a new pin in the style of an uploaded one, but better |

In claude.ai chat and Cowork you don't need commands: just describe what you want and Claude uses
the right skill.

## Skills

- **create-pin** - the full workflow from a URL to a finished pin and ready-to-paste copy
- **pin-design** - visual best practices: readability at phone size, layout, photo, color, branding
- **pin-copy** - headlines, Pinterest titles, descriptions, alt text, boards and keywords
- **review-pin** - scores a pin on an 8-point rubric and ranks the fixes
- **optimize-pin** - turns a review into 2-3 improved variants, each testing one change
- **remake-pin** - recreates a pin's style for your content, with original photo and copy

## Setup

1. Install the plugin from the Claude directory.
2. Open the plugin's **Connectors** tab and connect **InsightPins**. You sign in with your Google account (OAuth). No API key is needed.
3. Ask Claude to make a pin.

In Claude Code the connector loads with the plugin; run `/mcp` to sign in.

## Usage limits

Each rendered pin counts against your InsightPins daily render limit, which resets at 00:00 UTC.
Claude checks your remaining renders before making several pins and only re-renders when you ask
for a change or the preview has a real defect. Plans with higher limits may be offered on
insightpins.com; see the website for current plans.

## Data handling

This plugin contains only instructions (skills and commands) and a connector reference. It runs no
code on your computer.

When you use it, Claude sends the following to the InsightPins server at `app.insightpins.com`
through the connector:

- the page URLs you ask it to turn into pins (the server fetches the page to read its title, description and images)
- the pin text (headline, subtitle, button text, site name) and the image URLs chosen for the pin
- your template, palette, font and text size choices

Signing in with Google creates an InsightPins account with your email address, Google account ID,
name (if your Google account has one), the date the account was created and, if you close it, the
date it was closed. InsightPins
uses it to identify you and count your daily renders. It doesn't get your Google password or any
other Google data.

Rendered pin images are hosted by InsightPins and the image links expire after 7 days. Pins you
upload for review or remakes are read by Claude in the conversation and are not sent to InsightPins.
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
