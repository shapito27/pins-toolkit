# Pinterest bulk upload: reference

Sources: Pinterest's help pages, checked October 1, 2026. Pinterest changes
these; when the user has Pinterest's own sample CSV, its header row wins.

## Columns

```
Title,Media URL,Pinterest board,Thumbnail,Description,Link,Publish date,Keywords
```

| Column | Rule | Source |
|---|---|---|
| Title | Required. 100 characters or fewer. | Pinterest help |
| Media URL | Required. A public link to the image or video file itself, usually ending in .jpg, .jpeg, .png or .mp4. It must open without logging in. Share pages (Google Drive, Dropbox, iCloud, OneDrive, Google Photos) are not file links. | Pinterest help |
| Pinterest board | The board name exactly as on the user's profile. Treated as required here. | Column name from Pinterest's sample file; confirm against it |
| Thumbnail | Video only, and then required: a timestamp (mm:ss), a number of seconds, or a public image URL with the video's aspect ratio. Empty for images. | Pinterest help |
| Description | 500 characters or fewer. | Pinterest help |
| Link | The destination URL, starting with https:// (http:// works but is flagged). **Use each link once per file**: Pinterest refused a row whose Link repeated an earlier row of the same file ("Duplicate Pin link"), on any day. Any change to the text, such as a `?utm_content=` tag or a missing trailing slash, made it a new link, and a link from an earlier upload was accepted (our uploads, October 2026). | Pinterest help; duplicate rule observed |
| Publish date | `yyyy-mm-dd` or `yyyy-mm-ddThh:mm:ss` (Pinterest's example: `2023-12-17T08:00:00`), in **UTC**. `yyyy-mm-dd hh:mm:ss`, with a space, and `yyyy-mm-ddThh:mm:ssZ`, with a trailing Z, also worked in our upload tests (October 2026); `build_csv.py` writes the space form. A future date schedules the pin; empty publishes on upload; a date without a time publishes at the time of day the file is uploaded; a wrong format makes the row fail. | Pinterest help |
| Keywords | Optional. A few comma-separated keywords. | Column name from Pinterest's sample file; confirm against it |

Column names matter. Users on Pinterest's community forum report errors when
the second column was named "Media file URL" (an older help page wording) and
success after renaming it "Media URL".

## Limits

- 200 pins per file. Pinterest states no cap on the number of files, and says
  there is no limit to how many pins an account creates.
- Pinterest's one-at-a-time scheduler holds 10 pins up to 30 days ahead.
  Pinterest's help does not say whether that applies to CSV pins. Tested on one
  business account on 2026-10-01 (observed, not stated by Pinterest): 21 CSV
  pins from three files showed in Scheduled Pins at once, with up to 3 on a
  day, and a row dated 35 days ahead was accepted. The scripts still warn about
  dates more than 30 days out, because the limit is undocumented.
- After upload Pinterest says pins take about 2 hours to be created and reports
  problems by email. The pins then show under Scheduled Pins on the profile.
  Same test: a pin still published after its image file was deleted from the
  host, so Pinterest keeps its own copy once the pin has been created.
- Repeating the same action many times in a short period can trigger a
  temporary rate-limit block.
- Community reports (not Pinterest's help pages): a broken or login-only Media
  URL can fail without an error message, and rows that share one Media URL can
  fail after the first. Give every pin its own public file.

## File format

- UTF-8, comma-separated, one header row, one pin per row.
- Fields containing a comma, a double quote or a line break go in double
  quotes, with inner quotes doubled (`""`). The scripts handle this.
- Keep descriptions on one line.
- Excel can rewrite dates on save (`2026-10-07 22:00:00` becomes
  `10/7/2026 22:00`), and some regional Excel versions save with semicolons.
  Both make rows fail.

## pins.json

A list of objects. Only `title`, `media_url`, `board` and `link` are needed.

```json
[
  {
    "title": "One Pot Pasta in 20 Minutes (Easy Weeknight Dinner)",
    "media_url": "https://www.example.com/wp-content/uploads/one-pot-pasta-pin.jpg",
    "board": "Easy Dinner Recipes",
    "description": "One pot pasta that cooks in 20 minutes with pantry staples.",
    "link": "https://www.example.com/one-pot-pasta/",
    "keywords": "one pot pasta, easy weeknight dinner",
    "thumbnail": "",
    "publish_at": "2026-10-07 18:00"
  }
]
```

`publish_at` is optional and in the user's local time; without it the build
script picks the slot.
