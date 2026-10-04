"""Build Pinterest bulk upload CSV file(s) from pins.json.

    python scripts/build_csv.py pins.json --tz America/New_York \
        --start 2026-10-05 --end 2026-10-11 --window 09:00-21:00 \
        --out pinterest-bulk-upload.csv

Pins without "publish_at" are spread evenly over the days and the time window,
keeping two pins with the same link off the same day where possible. Every
time is local to --tz and converted to UTC with that date's own offset, so a
daylight-saving change inside the range is handled. Pinterest refuses a link
used twice in one file, so pins that share a link go into separate files: the
first pin for each link in one file, the second in the next, and so on. Each
file holds at most 200 pins; several files are named -part1.csv, -part2.csv,
... Each file is then checked with check_csv.py. Standard library only
(Python 3.9+).
"""
import argparse
import csv
import io
import json
import os
import sys
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_csv import HEADER, MAX_ROWS, check_text  # noqa: E402

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # Python < 3.9
    sys.exit("Needs Python 3.9 or newer (zoneinfo).")

FIELDS = {"title": "Title", "media_url": "Media URL", "board": "Pinterest board",
          "thumbnail": "Thumbnail", "description": "Description", "link": "Link",
          "keywords": "Keywords"}
NEEDED = ("title", "media_url", "board", "link")


def fail(msg):
    sys.exit(f"ERROR: {msg}")


def parse_hhmm(value):
    try:
        return datetime.strptime(value.strip(), "%H:%M").time()
    except ValueError:
        fail(f"time '{value}' is not HH:MM")


def to_utc(local_naive, tz):
    """Local wall time -> (UTC datetime, note). Moves times that do not exist
    (the spring-forward gap) one hour later; picks the first of two repeated
    times (the autumn fall-back hour)."""
    aware = local_naive.replace(tzinfo=tz, fold=0)
    utc = aware.astimezone(timezone.utc)
    if utc.astimezone(tz).replace(tzinfo=None) != local_naive:
        moved = local_naive + timedelta(hours=1)
        return moved.replace(tzinfo=tz).astimezone(timezone.utc), \
            f"{local_naive:%Y-%m-%d %H:%M} does not exist (clocks go forward); used {moved:%H:%M}"
    if aware.replace(fold=1).utcoffset() != aware.utcoffset():
        return utc, f"{local_naive:%Y-%m-%d %H:%M} happens twice (clocks go back); used the first"
    return utc, None


def one_line(value):
    return " ".join(str(value or "").split())


def spread(pins, days, start_t, end_t):
    """Assign pins without publish_at to (day, local time) slots.

    Days get an even share (the counts differ by at most one). Pins are placed
    most-repeated link first, each on the emptiest day that still has room and
    does not already carry that link, so one link lands on the same day only
    when there is no other way to fit it.
    """
    n, d = len(pins), len(days)
    capacity = {day: n // d + (1 if k < n % d else 0) for k, day in enumerate(days)}
    by_link = {}
    for i, pin in enumerate(pins):
        by_link.setdefault(pin.get("link"), []).append(i)
    load = Counter()
    links_on = {day: set() for day in days}
    plan = {day: [] for day in days}
    for link, idxs in sorted(by_link.items(), key=lambda kv: -len(kv[1])):
        for i in idxs:
            open_days = [day for day in days if load[day] < capacity[day]]
            fresh = [day for day in open_days if link not in links_on[day]]
            day = min(fresh or open_days, key=lambda x: (load[x], x))
            plan[day].append(i)
            load[day] += 1
            links_on[day].add(link)
    span = (datetime.combine(date.min, end_t) - datetime.combine(date.min, start_t)).seconds // 60
    slots = {}
    for day, idxs in plan.items():
        idxs.sort()  # keep the user's order within a day
        k = len(idxs)
        for j, i in enumerate(idxs):
            minute = round(((j + 0.5) * span / k) / 5) * 5  # evenly spaced, on 5 minutes
            slots[i] = datetime.combine(day, start_t) + timedelta(minutes=minute)
    return slots


def write_csv(path, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(HEADER)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return buf.getvalue()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pins")
    ap.add_argument("--tz", required=True, help="IANA time zone, e.g. Europe/London")
    ap.add_argument("--start", help="first day, yyyy-mm-dd (needed unless every pin has publish_at)")
    ap.add_argument("--end", help="last day, yyyy-mm-dd (default: --start)")
    ap.add_argument("--window", default="09:00-21:00", help="local HH:MM-HH:MM")
    ap.add_argument("--out", default="pinterest-bulk-upload.csv")
    ap.add_argument("--min-lead", type=float, default=2,
                    help="warn when a pin is due sooner than this many hours from now")
    ap.add_argument("--now", help=argparse.SUPPRESS)  # tests: fixed UTC time
    a = ap.parse_args(argv)

    try:
        tz = ZoneInfo(a.tz)
    except (ZoneInfoNotFoundError, ValueError):
        fail(f"unknown time zone '{a.tz}'. Use an IANA name such as America/New_York "
             "(if every name fails, run: pip install tzdata)")
    now = (datetime.fromisoformat(a.now).replace(tzinfo=timezone.utc)
           if a.now else datetime.now(timezone.utc))

    with open(a.pins, encoding="utf-8") as f:
        pins = json.load(f)
    if not isinstance(pins, list) or not pins:
        fail("pins.json must be a non-empty list of pins")
    problems = [f"pin {i + 1}: no {k}" for i, p in enumerate(pins)
                for k in NEEDED if not one_line(p.get(k))]
    if problems:
        fail("missing fields - " + "; ".join(problems))

    try:
        w_start, w_end = (parse_hhmm(x) for x in a.window.split("-"))
    except ValueError:
        fail(f"--window '{a.window}' is not HH:MM-HH:MM")
    if w_end <= w_start:
        fail("--window must end after it starts, within one day")

    auto = [i for i, p in enumerate(pins) if not one_line(p.get("publish_at"))]
    slots = {}
    if auto:
        if not a.start:
            fail(f"{len(auto)} pin(s) have no publish_at: give --start (and --end)")
        first = date.fromisoformat(a.start)
        last = date.fromisoformat(a.end) if a.end else first
        if last < first:
            fail("--end is before --start")
        days = [first + timedelta(days=n) for n in range((last - first).days + 1)]
        auto_slots = spread([pins[i] for i in auto], days, w_start, w_end)
        slots = {auto[j]: t for j, t in auto_slots.items()}
    for i, p in enumerate(pins):
        if i in slots:
            continue
        raw = one_line(p["publish_at"])
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                slots[i] = datetime.strptime(raw, fmt)
                break
            except ValueError:
                pass
        else:
            fail(f"pin {i + 1}: publish_at '{raw}' is not 'yyyy-mm-dd hh:mm' local time")

    rows, notes, past, soon = [], [], [], []
    for i, p in enumerate(pins):
        utc, note = to_utc(slots[i], tz)
        if note:
            notes.append(f"pin {i + 1}: {note}")
        if utc <= now:
            past.append(f"pin {i + 1} ({slots[i]:%Y-%m-%d %H:%M} local)")
        elif utc < now + timedelta(hours=a.min_lead):
            soon.append(f"pin {i + 1} ({slots[i]:%Y-%m-%d %H:%M} local)")
        row = {FIELDS[k]: one_line(p.get(k)) for k in FIELDS}
        row["Publish date"] = utc.strftime("%Y-%m-%d %H:%M:%S")
        rows.append((utc, slots[i], [row[h] for h in HEADER]))
    if past:
        fail("in the past: " + ", ".join(past) + ". Move --start or fix publish_at")

    rows.sort(key=lambda r: r[0])
    # Pinterest refused a Link already used by an earlier row of the same file
    # ("Duplicate Pin link"), while a link from an earlier upload was accepted
    # (our uploads, October 2026). So the n-th pin for a link goes in the n-th
    # group of files.
    groups, uses = [], Counter()
    for r in rows:
        link = r[2][HEADER.index("Link")]
        k = uses[link]
        uses[link] += 1
        if k == len(groups):
            groups.append([])
        groups[k].append(r)
    chunks = [g[n:n + MAX_ROWS] for g in groups for n in range(0, len(g), MAX_ROWS)]
    base, ext = os.path.splitext(a.out)
    paths = [a.out] if len(chunks) == 1 else [f"{base}-part{n + 1}{ext or '.csv'}"
                                              for n in range(len(chunks))]
    errors = 0
    for path, chunk in zip(paths, chunks):
        text = write_csv(path, [r[2] for r in chunk])
        report, _ = check_text(text, now)
        errors += report.errors
        print(f"Wrote {path}: {len(chunk)} pins")
        for line in report.lines:
            print("  " + line)

    per_day = Counter(r[1].date().isoformat() for r in rows)
    boards = Counter(r[2][2] for r in rows)
    print(f"\n{len(rows)} pins, {rows[0][1]:%a %Y-%m-%d %H:%M} to "
          f"{rows[-1][1]:%a %Y-%m-%d %H:%M} ({a.tz})")
    print("Per day: " + ", ".join(f"{d} {c}" for d, c in sorted(per_day.items())))
    print("Boards: " + ", ".join(f"{b} {c}" for b, c in boards.most_common()))
    for n in notes:
        print("NOTE " + n)
    if soon:
        print(f"WARN due within {a.min_lead:g} h, upload right away or move them: " + ", ".join(soon))
    if len(groups) > 1:
        shared = sum(1 for c in uses.values() if c > 1)
        print(f"NOTE {shared} link(s) are used by more than one pin. Pinterest refuses a link "
              f"used twice in one file, so those pins are spread over {len(groups)} groups of files")
    if len(chunks) > 1:
        print(f"NOTE {len(chunks)} files: upload them on different days to stay clear "
              "of Pinterest's rate limits")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
