"""Check a CSV for Pinterest's bulk upload and list every row that would fail.

    python scripts/check_csv.py pinterest-bulk-upload.csv
    python scripts/check_csv.py pinterest-bulk-upload.csv --json   # for tests

ERROR lines are rows Pinterest would reject or publish wrongly; fix them all.
WARN lines are worth a look. Exit code 1 when there is any ERROR.
Standard library only.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

# Python's csv module refuses any field over 128 KB. A huge description should be
# reported as too long, not end the run with a traceback.
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

HEADER = ["Title", "Media URL", "Pinterest board", "Thumbnail",
          "Description", "Link", "Publish date", "Keywords"]
REQUIRED = ["Title", "Media URL", "Pinterest board"]
MAX_ROWS = 200
MAX_TITLE = 100
MAX_DESCRIPTION = 500
HORIZON_DAYS = 30

IMAGE_EXT = (".jpg", ".jpeg", ".png")
VIDEO_EXT = (".mp4", ".mov", ".m4v")
SHARE_HOSTS = ("drive.google.com", "docs.google.com", "photos.google.com",
               "photos.app.goo.gl", "dropbox.com", "www.dropbox.com",
               "icloud.com", "www.icloud.com", "onedrive.live.com", "1drv.ms",
               "canva.com", "www.canva.com")

# re.ASCII: \d means 0-9 only. Without it Python also accepts Arabic-Indic and
# fullwidth digits, which Pinterest will not, and which JavaScript's \d rejects,
# so the page and this script would disagree.
DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
# Pinterest's help shows 2023-12-17T08:00:00. In our uploads (October 2026) a
# space in place of the T worked, and so did a trailing Z after the T form.
DATE_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}:\d{2}|T\d{2}:\d{2}:\d{2}Z?)$", re.ASCII)
EXCEL_DATE = re.compile(r"^\d{1,2}[/.]\d{1,2}[/.]\d{2,4}", re.ASCII)
THUMB_TIME = re.compile(r"^(\d{1,2}:\d{2}|\d+)$", re.ASCII)


class Report:
    """Findings as text lines and as structured records.

    Every finding has a stable `code` (what the web page matches on) and `rows`:
    a list of row numbers, or "file" or "header" when it is not about a row.
    tests/fixtures/csv-checker/expected.json pins both this script and the
    page at /tools/pinterest-csv-checker.html to the same findings."""

    def __init__(self):
        self.lines = []
        self.findings = []
        self.errors = 0
        self.warnings = 0

    def _record(self, severity, code, rows):
        self.findings.append({"severity": severity, "code": code, "rows": rows})

    def error(self, where, msg, code, rows):
        self.errors += 1
        self._record("error", code, rows)
        self.lines.append(f"ERROR {where}: {msg}")

    def warn(self, where, msg, code, rows):
        self.warnings += 1
        self._record("warn", code, rows)
        self.lines.append(f"WARN  {where}: {msg}")

    def note(self, msg, code, rows):
        self._record("note", code, rows)
        self.lines.append(f"NOTE  {msg}")


def is_http_url(value):
    try:
        p = urlparse(value)
    except ValueError:  # e.g. an unbalanced [ or ] in the host: not a web address
        return False
    return p.scheme in ("http", "https") and bool(p.netloc)


def check_text(text, now=None):
    """Check CSV text. Returns (Report, summary dict)."""
    now = now or datetime.now(timezone.utc)
    r = Report()
    summary = {"rows": 0, "scheduled": 0, "immediate": 0, "per_day": Counter()}

    if text.startswith("﻿"):
        r.warn("file", "starts with a byte-order mark (Excel's 'CSV UTF-8'); "
               "save as plain UTF-8 to be safe", "file.bom", "file")
        text = text[1:]
    first_line = re.split(r"[\r\n]", text, maxsplit=1)[0]  # a CR-only file has no \n at all
    if ";" in first_line and "," not in first_line:
        r.error("file", "columns are separated by semicolons (a regional Excel "
                "format); Pinterest expects commas", "file.semicolon", "file")
        return r, summary

    # newline="" keeps \r, \n and \r\n all ending a record (Excel for Mac writes
    # \r alone) and lets a quoted field hold any of them.
    # Row numbers are the numbers a spreadsheet shows: every record counts,
    # blank ones included, and a quoted line break stays inside its record.
    numbered = [(n, row) for n, row in enumerate(csv.reader(io.StringIO(text, newline="")), start=1)
                if any(cell.strip() for cell in row)]
    if not numbered:
        r.error("file", "is empty", "file.empty", "file")
        return r, summary
    rows = [row for _, row in numbered]

    header = [h.strip() for h in rows[0]]
    index = {h.lower(): i for i, h in enumerate(header)}
    for col in REQUIRED:
        if col.lower() not in index:
            r.error("header", f"missing the '{col}' column", "header.missing_required", "header")
    if r.errors:
        return r, summary
    if header != HEADER:
        unknown = [h for h in header if h.lower() not in {c.lower() for c in HEADER}]
        if unknown:
            r.warn("header", f"unexpected column(s) {unknown}; Pinterest may ignore "
                   "or reject them", "header.unexpected", "header")
        missing = [c for c in HEADER if c.lower() not in index]
        if missing:
            r.warn("header", f"no {missing} column(s); fine if empty on purpose",
                   "header.missing_optional", "header")
        if not unknown and not missing:
            r.warn("header", "column names or order differ from Pinterest's sample "
                   f"({','.join(HEADER)}); match the sample file if you have it",
                   "header.differs", "header")

    header_again = [n for n, row in numbered[1:]
                    if [x.strip().lower() for x in row] == [h.lower() for h in header]]
    if header_again:
        r.error(f"row {', '.join(map(str, header_again))}", "repeats the header row "
                "(two files pasted together?); delete it, or upload the files separately",
                "header.repeated", header_again)
    data = [row for n, row in numbered[1:] if n not in header_again]
    numbers = [n for n, _ in numbered[1:] if n not in header_again]
    summary["rows"] = len(data)
    if len(data) > MAX_ROWS:
        r.error("file", f"has {len(data)} pins; Pinterest takes {MAX_ROWS} per file. "
                "Split it (build_csv.py does this automatically)", "file.too_many_rows", "file")

    def get(row, col):
        i = index.get(col.lower())
        return row[i].strip() if i is not None and i < len(row) else ""

    media_seen = defaultdict(list)
    link_seen = defaultdict(list)
    far_rows, now_rows, dateonly_rows = [], [], []

    for n, row in zip(numbers, data):
        where = f"row {n}"
        if len(row) != len(header):
            r.error(where, f"has {len(row)} fields, the header has {len(header)}; "
                    "a comma inside a field is probably not quoted", "row.field_count", [n])
            continue

        title = get(row, "Title")
        if not title:
            r.error(where, "Title is empty", "title.empty", [n])
        elif len(title) > MAX_TITLE:
            r.error(where, f"Title is {len(title)} characters (max {MAX_TITLE})", "title.long", [n])

        media = get(row, "Media URL")
        kind = None
        if not media:
            r.error(where, "Media URL is empty", "media.empty", [n])
        elif not is_http_url(media):
            r.error(where, "Media URL is not a web address", "media.not_url", [n])
        else:
            p = urlparse(media)
            host = p.netloc.lower()
            path = p.path.lower()
            if host in SHARE_HOSTS or host.endswith(".sharepoint.com"):
                r.error(where, f"Media URL is a {host} page, not a direct link to the "
                        "file; upload the image to your site and use its file URL",
                        "media.share_page", [n])
            elif path.endswith(IMAGE_EXT):
                kind = "image"
            elif path.endswith(VIDEO_EXT):
                kind = "video"
            elif path.endswith((".webp", ".gif", ".heic", ".avif")):
                r.warn(where, f"Media URL is a {path.rsplit('.', 1)[-1]} file; "
                       "Pinterest's help names JPEG, PNG and MP4. Convert if the row fails",
                       "media.format", [n])
            else:
                r.warn(where, "Media URL does not end in a file extension; open it in a "
                       "private window and check it shows only the image or video",
                       "media.no_extension", [n])
            if p.scheme == "http":
                r.warn(where, "Media URL uses http://; prefer https://", "media.http", [n])
            media_seen[media].append(n)

        thumb = get(row, "Thumbnail")
        if kind == "video" and not thumb:
            r.error(where, "video pin without a Thumbnail (mm:ss, seconds, or an image URL)",
                    "thumb.video_missing", [n])
        elif kind == "image" and thumb:
            r.warn(where, "Thumbnail is only for video; leave it empty for images",
                   "thumb.on_image", [n])
        if thumb and not (THUMB_TIME.match(thumb) or is_http_url(thumb)):
            r.error(where, f"Thumbnail '{thumb}' is not mm:ss, a number of seconds or a URL",
                    "thumb.invalid", [n])

        if not get(row, "Pinterest board"):
            r.error(where, "Pinterest board is empty", "board.empty", [n])

        desc_i = index.get("description")
        desc = row[desc_i] if desc_i is not None else ""
        if len(desc.strip()) > MAX_DESCRIPTION:
            r.error(where, f"Description is {len(desc.strip())} characters (max {MAX_DESCRIPTION})",
                    "desc.long", [n])
        if "\n" in desc or "\r" in desc:
            r.warn(where, "Description contains a line break; keep it on one line",
                   "desc.line_break", [n])

        link = get(row, "Link")
        if not link:
            r.warn(where, "no Link, so the pin will not send anyone to your site", "link.empty", [n])
        elif not is_http_url(link):
            r.error(where, f"Link '{link}' is not a full web address (https://...)",
                    "link.not_url", [n])
        elif urlparse(link).scheme == "http":
            r.warn(where, "Link uses http://; prefer https://", "link.http", [n])
        if link:
            link_seen[link].append(n)

        date = get(row, "Publish date")
        if not date:
            summary["immediate"] += 1
            now_rows.append(n)
        elif DATE_TIME.match(date) or DATE_ONLY.match(date):
            fmt = "%Y-%m-%d %H:%M:%S" if DATE_TIME.match(date) else "%Y-%m-%d"
            try:
                when = datetime.strptime(date.replace("T", " ").rstrip("Z"), fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                r.error(where, f"Publish date '{date}' is not a real date", "date.not_real", [n])
                continue
            if DATE_ONLY.match(date):
                dateonly_rows.append(n)
                if when.date() < now.date():
                    r.error(where, f"Publish date {date} is in the past", "date.past", [n])
                    continue
            elif when <= now:
                r.error(where, f"Publish date {date} UTC is in the past", "date.past", [n])
                continue
            if when > now + timedelta(days=HORIZON_DAYS):
                far_rows.append(n)
            summary["scheduled"] += 1
            summary["per_day"][when.date().isoformat()] += 1
        elif EXCEL_DATE.match(date):
            r.error(where, f"Publish date '{date}' looks rewritten by a spreadsheet app; "
                    "use yyyy-mm-dd hh:mm:ss (UTC)", "date.spreadsheet", [n])
        else:
            r.error(where, f"Publish date '{date}' is not yyyy-mm-ddThh:mm:ss or yyyy-mm-dd hh:mm:ss (UTC)",
                    "date.format", [n])

    def rows_label(nums):
        return "row " + str(nums[0]) if len(nums) == 1 else f"{len(nums)} rows ({', '.join(map(str, nums[:8]))}{', ...' if len(nums) > 8 else ''})"

    if now_rows:
        r.warn(rows_label(now_rows), "no Publish date, so these publish as soon as you upload",
               "date.empty", now_rows)
    if dateonly_rows:
        r.warn(rows_label(dateonly_rows), "date without a time publishes at the time of day "
               "you upload the file; add hh:mm:ss in UTC", "date.date_only", dateonly_rows)
    if far_rows:
        r.warn(rows_label(far_rows), f"Publish date more than {HORIZON_DAYS} days ahead. "
               "Pinterest's own scheduler stops at 30 days and its help does not say "
               "whether CSV pins can go further. A 35 day row was accepted in one "
               "test (October 2026): check that the pin shows under Scheduled Pins",
               "date.far", far_rows)
    for media, at in media_seen.items():
        if len(at) > 1:
            r.warn(f"rows {', '.join(map(str, at))}", "share one Media URL. Users on "
                   "Pinterest's community forum report that rows after the first can "
                   "fail; give each pin its own image file", "media.duplicate", at)
    # Pinterest refused a Link already used by an earlier row of the same file
    # ("Duplicate Pin link"), on any day; the first row went through. Any change
    # to the text made it a new link, and a link from an earlier upload was fine
    # (our uploads, October 2026).
    for link, at in link_seen.items():
        if len(at) > 1:
            r.error(("row " if len(at) == 2 else "rows ") + ", ".join(map(str, at[1:])), f"repeats the Link {link} from row {at[0]}; "
                    "Pinterest refuses a link used twice in one file (Duplicate Pin link). Give each "
                    "pin its own link, or put the repeats in another file", "link.duplicate", at[1:])
    return r, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--now", help=argparse.SUPPRESS)  # tests: fixed UTC time
    ap.add_argument("--json", action="store_true",
                    help="print findings as JSON (file, findings, summary) instead of text")
    args = ap.parse_args(argv)
    now = (datetime.fromisoformat(args.now).replace(tzinfo=timezone.utc)
           if args.now else None)
    failed = False
    out = []
    for path in args.files:
        try:
            with open(path, encoding="utf-8", newline="") as f:
                text = f.read()
        except UnicodeDecodeError:
            if args.json:
                out.append({"file": path, "findings": [
                    {"severity": "error", "code": "file.not_utf8", "rows": "file"}],
                    "summary": {"rows": 0, "scheduled": 0, "immediate": 0, "per_day": {}}})
            else:
                print(f"{path}\nERROR file: not UTF-8; re-save it as CSV UTF-8")
            failed = True
            continue
        report, s = check_text(text, now)
        if args.json:
            out.append({"file": path, "findings": report.findings,
                        "summary": {"rows": s["rows"], "scheduled": s["scheduled"],
                                    "immediate": s["immediate"], "per_day": dict(sorted(s["per_day"].items()))}})
            failed = failed or report.errors > 0
            continue
        print(path)
        for line in report.lines:
            print("  " + line)
        days = ", ".join(f"{d}: {c}" for d, c in sorted(s["per_day"].items()))
        print(f"  {s['rows']} pins: {s['scheduled']} scheduled, {s['immediate']} "
              f"publish on upload. Per day (UTC): {days or 'none'}")
        print(f"  {report.errors} error(s), {report.warnings} warning(s)")
        failed = failed or report.errors > 0
    if args.json:
        print(json.dumps(out, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
