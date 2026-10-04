#!/bin/bash
# Writes my-pins.csv into the run's workspace from the template, with future dates
# 5-7 days from today (UTC), so the file never ages: the only date findings are the
# spreadsheet-style date and the fixed past date (2025-01-10).
set -e
python3 - "$(dirname "$0")/resources/my-pins.template.csv" my-pins.csv <<'PY'
import re, sys
from datetime import datetime, timedelta, timezone
today = datetime.now(timezone.utc).date()
text = open(sys.argv[1], encoding="utf-8").read()
text = re.sub(r"\{\{DAY\+(\d+)\}\}", lambda m: (today + timedelta(days=int(m.group(1)))).isoformat(), text)
open(sys.argv[2], "w", encoding="utf-8", newline="").write(text)
PY
