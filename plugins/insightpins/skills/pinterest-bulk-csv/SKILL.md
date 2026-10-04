---
name: pinterest-bulk-csv
description: Builds, checks and fixes the CSV file for Pinterest's free bulk upload. Validates every row (title and description length, direct media links, board, dates in UTC, unquoted commas, semicolons, duplicate links, 200-pin limit), spreads pins across days in the user's time zone, converts dates to UTC and splits big batches. Use when the user wants to validate or fix a Pinterest bulk upload CSV, asks why a bulk upload failed, wants to schedule pins in bulk, or wants to schedule pins made with InsightPins.
---

# Pinterest bulk upload CSV

You prepare the file that Pinterest's own bulk upload reads. Pinterest
publishes and schedules the pins. You never publish anything.

## Ground rules

- Never log in to Pinterest, click around the user's account, or automate it
  in a browser: Pinterest does not allow automation it has not approved. The
  user uploads the finished file.
- Never ask for the user's Pinterest password.
- Never invent image URLs, board names, links or facts in descriptions. Ask.
- Count characters, convert dates and quote fields with the scripts, not by
  eye. If you cannot run code, follow `reference.md` by hand and tell the user
  the lengths and dates were checked manually.
- The scripts are in this skill's `scripts/` folder (`${CLAUDE_SKILL_DIR}/scripts/`).
  They use only Python's standard library, read and write local files only, and
  make no network requests.

## Just checking a file?

When the user brings a CSV and wants it checked or fixed, skip to step 4: run
the checker, then explain each finding with its row and fix, most serious first.
Fix only what is mechanical (spaces, line breaks in descriptions, quoting, date
format once the user confirms the time zone and day/month order). Never shorten
a title or description, or pick a different image, without asking.

## Workflow

### 1. Collect the inputs

Ask for anything missing. Do not guess a time zone.

- **The pins.** For each: image or video URL, destination link, board, and
  either a title and description or the post to write them from. Optional:
  keywords, a fixed publish time.
- **Time zone**, as an IANA name (America/New_York, Europe/London).
- **Which days** (start and end date) and a **time window** (default 09:00-21:00).
- **Pinterest's own sample CSV**, if the user has downloaded it from the bulk
  upload screen. Its header row wins over the one in `reference.md`.

If a pin's image is not online yet, stop and say so: Pinterest fetches each
file from its URL, so images must be uploaded somewhere public first (the
user's blog media library is the usual place).

### 2. Write the copy, if asked

Follow the limits in `reference.md`: title 100 characters or fewer, keyword
first when there is one; description 500 or fewer, plain sentences about what
the reader gets. Say nothing the post does not say.

### 3. Build the CSV

Write the pins to `pins.json` (format in `reference.md`), then run:

```bash
python3 -B ${CLAUDE_SKILL_DIR}/scripts/build_csv.py pins.json --tz America/New_York \
  --start 2026-10-05 --end 2026-10-11 --window 09:00-21:00 \
  --out pinterest-bulk-upload.csv
```

The script spreads the pins evenly across the days and the window, keeps two
pins with the same link off the same day when it can, converts each time to
UTC with that date's own offset, sorts by date, and writes one file per 200
pins (`-part1.csv`, `-part2.csv`, ...). Pinterest refuses a link used twice in
one file, so pins that share a link go into separate files; tell the user to
upload every file. Pins with their own `publish_at` keep
it. It refuses dates in the past and warns about any closer than
`--min-lead` hours (default 2), since the user still has to upload the file.

### 4. Check it

The build script runs the checker on every file it writes. Run it yourself on
any CSV the user brings or edits:

```bash
python3 -B ${CLAUDE_SKILL_DIR}/scripts/check_csv.py pinterest-bulk-upload.csv
```

Add `--json` for machine-readable findings.

Fix every ERROR and re-run until there are none. Explain each WARN to the
user in one sentence. The checker catches the usual reasons a row does not
publish: titles over 100 characters, share pages instead of file links, video
without a thumbnail, dates in the past or rewritten by a spreadsheet app,
unquoted commas, semicolon-separated files, a repeated header row, and files
over 200 pins.

The same rules run in a page the user can open without you, in their browser,
with the file staying on their computer:
https://insightpins.com/tools/pinterest-csv-checker.html . Mention it when they
want to check a file they edit by hand later.

### Pins made with InsightPins

When the pins come from the `create-pin` skill in this conversation:

- Use each render's `image_url` as the Media URL, its title and description as
  Title and Description, and the source page as Link.
- **Rendered image links expire after 7 days.** Pinterest fetches the image when
  it creates the pin, about 2 hours after upload, and keeps its own copy, so a
  file uploaded within the 7 days works even for pins dated later. Tell the user
  to upload it soon, or to put the images on their own site and use those links.
- Variations of one page share a Link. Pinterest refuses a Link repeated in one
  file, so `build_csv.py` puts them in separate files; say that each file must be uploaded.

### 5. Hand over

Give the user the file(s) and a short summary: number of pins, first and last
publish time **in their time zone**, pins per day, boards used. Then tell them:

1. **Upload it as it is.** Opening and re-saving the CSV in Excel can rewrite
   the dates into a format Pinterest rejects. To edit, use Google Sheets or a
   text editor, or re-run the scripts.
2. **First time scheduling by CSV? Test small.** Pinterest's help pages state
   200 pins per file but no other cap. One test account scheduled 21 CSV pins
   at once, so the 10-pin queue did not apply, but upload a few rows first and
   check that every pin shows under Scheduled Pins before sending a big batch.
   Pins take about 2 hours to appear, and problems arrive by email.
3. **Spread big batches over several days.** Pinterest can temporarily block
   an account that repeats the same action many times in a short period.
4. Upload with Pinterest's bulk upload from a business account:
   https://help.pinterest.com/en/business/article/bulk-upload-video-pins
