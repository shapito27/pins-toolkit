#!/usr/bin/env python3
"""Move the dates in the eval mocks into the future, relative to now.

    python3 scripts/refresh-eval-dates.py

The mocks under evals/ carry three kinds of time: the quota reset (`resets_at`, and "It resets at"
in the limit error), a render's `expires_at` (7 days) and an upload link's `expires_at` (15
minutes). A time that is already past makes Claude say the quota or the link looks stale, so run
this before running the suite.
"""
import datetime
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EVALS = os.path.join(HERE, "..", "evals")
STAMP = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z"


def stamp(when):
    return when.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
    midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0)
    reset = stamp(midnight)
    render = stamp((now + datetime.timedelta(days=7)).replace(hour=12, minute=0))
    link = stamp(now + datetime.timedelta(minutes=15))
    changed = 0
    for path in sorted(glob.glob(os.path.join(EVALS, "**", "mocks", "**", "*.md"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            old = f.read()
        new = re.sub(r'("resets_at": ")' + STAMP, r"\g<1>" + reset, old)
        new = re.sub(r"(It resets at )" + STAMP, r"\g<1>" + reset, new)
        expires = link if os.path.basename(path) == "create_upload_link.md" else render
        new = re.sub(r'("expires_at": ")' + STAMP, r"\g<1>" + expires, new)
        if new != old:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            changed += 1
            print("updated", os.path.relpath(path, os.path.join(HERE, "..")))
    print(f"{changed} file(s) updated: reset {reset}, render links {render}, upload links {link}")


if __name__ == "__main__":
    main()
