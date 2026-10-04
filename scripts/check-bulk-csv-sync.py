#!/usr/bin/env python3
"""Check the plugin's copy of check_csv.py against the insightpins.com fixtures.

    python3 scripts/check-bulk-csv-sync.py ../insightpins.com

Runs the plugin's check_csv.py on every fixture in
<insightpins.com>/tests/fixtures/csv-checker/ with the clock fixed to expected.json's
"now", and compares the findings (severity, code, rows) and summary with expected.json.
Exits 1 on any mismatch.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, "..", "plugins", "insightpins", "skills", "pinterest-bulk-csv", "scripts", "check_csv.py")


def canonical(findings):
    return sorted(findings, key=lambda f: (f["severity"], f["code"], json.dumps(f["rows"])))


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: check-bulk-csv-sync.py <path to insightpins.com repo>")
    fixtures = os.path.join(sys.argv[1], "tests", "fixtures", "csv-checker")
    expected = json.load(open(os.path.join(fixtures, "expected.json"), encoding="utf-8"))
    mismatches = 0
    for name, want in sorted(expected["cases"].items()):
        p = subprocess.run([sys.executable, "-B", CHECKER, "--json", "--now", expected["now"],
                            os.path.join(fixtures, name + ".csv")], capture_output=True, text=True)
        doc = json.loads(p.stdout)[0]
        got = {"findings": canonical(doc["findings"]), "summary": doc["summary"]}
        if got != want:
            mismatches += 1
            print("MISMATCH", name)
    print(f"{len(expected['cases'])} fixtures, {mismatches} mismatches")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
