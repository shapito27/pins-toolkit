"""Checks for the InsightPins plugin: directory requirements, the palette contrast table, the CSV
scripts and the eval suite's graders. Standard library only.

    python3 -m unittest discover -s tests
"""
import importlib.util
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN = os.path.join(ROOT, "plugins", "insightpins")
SKILLS = os.path.join(PLUGIN, "skills")
CSV_SCRIPTS = os.path.join(SKILLS, "pinterest-bulk-csv", "scripts")
STYLE_GUIDE = os.path.join(SKILLS, "create-pin", "references", "style-selection.md")
EVALS = os.path.join(ROOT, "evals")
MCP_TOOL = "mcp__plugin_insightpins_insightpins__"

KIB = 1024


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_frontmatter(text):
    """Return (frontmatter, body) for a file that starts with a --- block."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def plugin_files():
    for dirpath, dirnames, filenames in os.walk(PLUGIN):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in filenames:
            yield os.path.join(dirpath, name)


# --- Contrast helpers (WCAG 2.x) -------------------------------------------------------------

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"not a #rrggbb color: {h!r}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a, b):
    la, lb = sorted((luminance(hex_to_rgb(a)), luminance(hex_to_rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def palettes():
    """Palettes from the list_styles mock, which mirrors the live server (2026-10-04)."""
    _, body = strip_frontmatter(read(os.path.join(EVALS, "mocks", "insightpins", "list_styles.md")))
    return {p["id"]: p["colors"] for p in json.loads(body)["palettes"]}


def contrast_table():
    """Rows of the contrast table in style-selection.md: id -> (ratio, rating text)."""
    text = read(STYLE_GUIDE)
    section = text.split("## Contrast: which palettes keep text readable", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for m in re.finditer(r"^\| ([a-z-]+) \| ([\d.]+) \| (.+?) \|$", section, re.M):
        rows[m.group(1)] = (float(m.group(2)), m.group(3))
    return rows


def light_on_primary(colors):
    """The pair most templates use for panels and buttons: palette background on primary."""
    return contrast(colors["background"], colors["primary"])


def rating_for(ratio):
    if ratio >= 4.5:
        return "Strong"
    if ratio >= 3.0:
        return "Good"
    return "Fails"


TEMPLATE_COLORS = os.path.join(SKILLS, "create-pin", "references", "template-colors.md")


def template_colors():
    """template-colors.md rows: id -> (readable, readable without a button, notes)."""
    rows = {}
    for line in read(TEMPLATE_COLORS).splitlines():
        m = re.match(r"^\| `([a-z-]+)` \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if m:
            split = lambda cell: [p.strip() for p in cell.split(",") if p.strip() and p.strip() != "none"]
            rows[m.group(1)] = (split(m.group(2)), split(m.group(3)), m.group(4))
    return rows


def mood_table_columns():
    """Palettes named in the 'On panel templates' and 'On light templates' columns."""
    text = read(STYLE_GUIDE)
    section = text.split("## Palette by mood and topic", 1)[1].split("\n## ", 1)[0]
    panel, light = set(), set()
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Mood / topic", "-"):
            continue
        for cell, out in ((cells[1], panel), (cells[2], light)):
            cell = re.sub(r"\([^)]*\)", "", cell)  # "berry-blush (desserts)" names one palette
            out.update(name.strip() for name in cell.split(",") if name.strip())
    return panel, light


class ContrastFormulaTest(unittest.TestCase):
    def test_known_values(self):
        self.assertAlmostEqual(contrast("#FFFFFF", "#000000"), 21.0, places=2)
        self.assertAlmostEqual(contrast("#777777", "#777777"), 1.0, places=6)

    def test_symmetric(self):
        self.assertAlmostEqual(contrast("#FF5252", "#FFFFFF"), contrast("#FFFFFF", "#FF5252"))

    def test_rejects_bad_hex(self):
        for bad in ("#FFF", "white", "#GG0000", ""):
            with self.assertRaises(ValueError):
                hex_to_rgb(bad)

    def test_rating_boundaries(self):
        self.assertEqual(rating_for(4.5), "Strong")
        self.assertEqual(rating_for(4.49), "Good")
        self.assertEqual(rating_for(3.0), "Good")
        self.assertEqual(rating_for(2.99), "Fails")


class StyleGuideTest(unittest.TestCase):
    """The contrast table and mood table in style-selection.md must match the palette colors."""

    @classmethod
    def setUpClass(cls):
        cls.palettes = palettes()
        cls.table = contrast_table()

    def test_table_covers_every_palette_once(self):
        self.assertEqual(set(self.table), set(self.palettes))
        self.assertEqual(len(self.table), 15)

    def test_ratios_match_palette_colors(self):
        for pid, (ratio, _) in self.table.items():
            computed = light_on_primary(self.palettes[pid])
            self.assertAlmostEqual(ratio, round(computed, 1), delta=0.051,
                                   msg=f"{pid}: table says {ratio}, colors give {computed:.2f}")

    def test_table_sorted_by_ratio(self):
        ratios = [r for r, _ in self.table.values()]
        self.assertEqual(ratios, sorted(ratios, reverse=True))

    def test_ratings_follow_ratio(self):
        for pid, (_, rating) in self.table.items():
            exact = light_on_primary(self.palettes[pid])
            self.assertTrue(rating.startswith(rating_for(exact)),
                            f"{pid}: {exact:.3f} is rated '{rating}', expected '{rating_for(exact)}'")

    def test_panel_suggestions_are_readable_on_panel_templates(self):
        panel, _ = mood_table_columns()
        self.assertTrue(panel, "mood table has no panel column entries")
        colors = template_colors()
        for pid in panel:
            self.assertIn(pid, self.table, f"unknown palette {pid} in mood table")
            for template in ("split-horizontal", "diagonal-cut"):
                self.assertIn(pid, colors[template][0], f"{pid} is not readable on {template}")

    def test_light_suggestions_have_readable_buttons(self):
        _, light = mood_table_columns()
        self.assertTrue(light, "mood table has no light column entries")
        for pid in light:
            self.assertIn(pid, self.palettes, f"unknown palette {pid} in mood table")
            self.assertGreaterEqual(light_on_primary(self.palettes[pid]), 3.0,
                                    f"{pid}: button text below 3:1")

    def test_every_palette_passes_for_headline_on_light_templates(self):
        for pid, c in self.palettes.items():
            self.assertGreaterEqual(contrast(c["text"], c["background"]), 4.5, pid)

    def test_left_out_palettes_fail_buttons(self):
        text = read(STYLE_GUIDE).split("## Palette by mood and topic", 1)[1].split("## Font", 1)[0]
        for pid in ("forest-calm", "cool-mint", "sage", "electric", "coral-reef", "sunset-glow"):
            self.assertIn(pid, text)
            self.assertLess(light_on_primary(self.palettes[pid]), 3.0, pid)


class TemplateColorsTest(unittest.TestCase):
    """template-colors.md is generated from the pin generator's colour map."""

    @classmethod
    def setUpClass(cls):
        cls.rows = template_colors()
        _, body = strip_frontmatter(read(os.path.join(EVALS, "mocks", "insightpins", "list_templates.md")))
        cls.templates = [t["id"] for t in json.loads(body)]
        cls.palettes = palettes()

    def test_covers_every_template_once(self):
        self.assertEqual(sorted(self.rows), sorted(self.templates))

    def test_palettes_are_known_and_columns_disjoint(self):
        for template, (readable, extra, _) in self.rows.items():
            for pid in readable + extra:
                self.assertIn(pid, self.palettes, f"{template}: {pid}")
            self.assertFalse(set(readable) & set(extra), template)

    def test_readable_palettes_pass_the_common_pair(self):
        # Every template but collage-style (accent-coloured button) uses background-on-primary
        # for its button, so its readable palettes must reach 3:1 on that pair.
        for template, (readable, _, _) in self.rows.items():
            if template == "collage-style":
                continue
            for pid in readable:
                self.assertGreaterEqual(light_on_primary(self.palettes[pid]), 3.0, f"{template}: {pid}")

    def test_style_guide_names_the_secondary_subtitle_templates(self):
        flagged = sorted(t for t, (_, _, notes) in self.rows.items() if "never readable" in notes)
        self.assertEqual(flagged, sorted(["number-badge", "dashed-accent", "starburst-badge",
                                          "arch-window", "side-panels", "lifestyle-collage"]))
        guide = read(STYLE_GUIDE)
        for template in flagged:
            self.assertIn(f"`{template}`", guide)

    def test_up_to_date_with_the_colour_map(self):
        source = os.path.join(ROOT, "..", "pin-generator-tool", "docs", "TEMPLATE_COLOR_ROLES.md")
        if not os.path.isfile(source):
            self.skipTest("pin-generator-tool is not checked out next to this repo")
        spec = importlib.util.spec_from_file_location(
            "build_template_colors", os.path.join(ROOT, "scripts", "build-template-colors.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        text, _ = module.build(read(source))
        self.assertEqual(text, read(TEMPLATE_COLORS),
                         "run: python3 scripts/build-template-colors.py ../pin-generator-tool")

    def test_parser_rejects_unknown_palettes(self):
        spec = importlib.util.spec_from_file_location(
            "build_template_colors", os.path.join(ROOT, "scripts", "build-template-colors.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.palettes("15/15: all"), module.ALL)
        self.assertEqual(module.palettes("0/15: none"), [])
        self.assertEqual(module.palettes("-"), [])
        self.assertEqual(module.palettes("2/15: Ocean Breeze, Midnight"), ["ocean-breeze", "midnight"])
        with self.assertRaises(SystemExit):
            module.palettes("1/15: Neon Pink")


# --- Directory requirements ------------------------------------------------------------------

def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("not a PNG")
    return struct.unpack(">II", head[16:24])


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise ValueError("no frame header")


class ImageHelpersTest(unittest.TestCase):
    def test_png_size_rejects_other_files(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"GIF89a" + b"\0" * 30)
        try:
            with self.assertRaises(ValueError):
                png_size(f.name)
        finally:
            os.unlink(f.name)

    def test_jpeg_size_rejects_other_files(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\0" * 30)
        try:
            with self.assertRaises(ValueError):
                jpeg_size(f.name)
        finally:
            os.unlink(f.name)


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(read(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))

    def test_required_fields(self):
        for key in ("name", "description", "version", "author", "license", "homepage", "repository"):
            self.assertTrue(self.manifest.get(key), key)
        self.assertRegex(self.manifest["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+$")

    def test_privacy_policy_url_matches_readme(self):
        url = self.manifest.get("privacyPolicyUrl")
        self.assertEqual(url, "https://insightpins.com/privacy.html")
        self.assertIn(url, read(os.path.join(PLUGIN, "README.md")))

    def test_listing_links(self):
        readme = read(os.path.join(PLUGIN, "README.md"))
        self.assertEqual(self.manifest.get("termsOfServiceUrl"), "https://insightpins.com/terms-of-use.html")
        self.assertIn(self.manifest["termsOfServiceUrl"], readme)
        self.assertEqual(self.manifest.get("supportUrl"), "https://insightpins.com/contacts.html")
        self.assertIn(self.manifest["supportUrl"], readme)
        doc = self.manifest.get("documentationUrl", "")
        self.assertTrue(doc.startswith(self.manifest["repository"] + "/blob/main/plugins/insightpins/"), doc)
        self.assertTrue(os.path.isfile(os.path.join(ROOT, doc.split("/blob/main/", 1)[1])), doc)

    def test_icon(self):
        path = self.manifest.get("icon", ".claude-plugin/icon.png")
        full = os.path.join(PLUGIN, path)
        self.assertTrue(os.path.isfile(full), f"no icon at {path}")
        w, h = png_size(full)
        self.assertEqual(w, h, "icon must be square")
        self.assertTrue(512 <= w <= 2048, f"icon is {w}px, needs 512-2048")
        self.assertLess(os.path.getsize(full), 2 * 1024 * KIB)

    def test_connector(self):
        mcp = json.loads(read(os.path.join(PLUGIN, ".mcp.json")))["mcpServers"]
        self.assertEqual(list(mcp), ["insightpins"])
        server = mcp["insightpins"]
        self.assertEqual(server, {"type": "http", "url": "https://app.insightpins.com/api/mcp"})


class PluginFilesTest(unittest.TestCase):
    def test_limits_and_no_junk(self):
        files = list(plugin_files())
        self.assertLessEqual(len(files), 512)
        for path in files:
            rel = os.path.relpath(path, PLUGIN)
            self.assertFalse(os.path.islink(path), f"symlink: {rel}")
            self.assertLess(os.path.getsize(path), 256 * KIB, f"too big: {rel}")
            self.assertNotIn(os.path.basename(path), (".DS_Store", "Thumbs.db", ".gitattributes"))
            self.assertNotIn("__MACOSX", rel)

    def test_readme_word_count(self):
        text = re.sub(r"```.*?```", "", read(os.path.join(PLUGIN, "README.md")), flags=re.S)
        self.assertGreaterEqual(len(text.split()), 40)

    def test_readme_images(self):
        readme = read(os.path.join(PLUGIN, "README.md"))
        refs = re.findall(r"!\[[^\]]+\]\(([^)\s]+)\)", readme)
        self.assertTrue(refs, "README has no example images")
        for ref in refs:
            self.assertFalse(ref.startswith(("http:", "https:", "/")), f"{ref} must be a relative path")
            full = os.path.join(PLUGIN, ref)
            self.assertTrue(os.path.isfile(full), f"missing image {ref}")
            w, h = jpeg_size(full) if ref.endswith(".jpg") else png_size(full)
            self.assertGreater(w, 0)
        assets = {f"assets/{n}" for n in os.listdir(os.path.join(PLUGIN, "assets"))}
        self.assertEqual(assets, set(refs), "every asset should be used by the README, and only there")

    def test_images_not_referenced_outside_readme(self):
        for path in plugin_files():
            if path.endswith((".md", ".py", ".json")) and not path.endswith(os.sep + "README.md"):
                self.assertNotIn("assets/", read(path), os.path.relpath(path, PLUGIN))

    def test_no_em_or_en_dashes_in_authored_text(self):
        for path in plugin_files():
            if path.endswith((".md", ".json")):
                text = read(path)
                self.assertNotIn("—", text, os.path.relpath(path, PLUGIN))
                self.assertNotIn("–", text, os.path.relpath(path, PLUGIN))


# --- CSV scripts --------------------------------------------------------------------------

# Patterns the directory's scanner reads as "uses the installer's environment" or as network
# access. The scripts must stay free of them, or the plugin is held for review again.
FORBIDDEN_IN_SCRIPTS = [
    (r"^#!", "shebang line (the skill runs the scripts with python3 -B)"),
    (r"/usr/bin/env\b", "env command"),
    (r"\bprintenv\b", "printenv"),
    (r"\bexport\b", "the word 'export'"),
    (r"\bos\.environ\b|\bgetenv\b", "environment access"),
    (r"^\s*(import|from)\s+(socket|urllib\.request|http\.client|requests|subprocess)\b",
     "network or process import"),
]


class CsvScriptsTest(unittest.TestCase):
    scripts = ("check_csv.py", "build_csv.py")

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, "-B", os.path.join(CSV_SCRIPTS, name), *args],
                              capture_output=True, text=True)

    def test_scanner_triggers_absent(self):
        for name in self.scripts:
            text = read(os.path.join(CSV_SCRIPTS, name))
            for pattern, what in FORBIDDEN_IN_SCRIPTS:
                self.assertIsNone(re.search(pattern, text, re.M), f"{name}: {what}")

    def test_forbidden_patterns_catch_the_old_header(self):
        old = "#!/usr/bin/env python3\nimport os\nx = os.environ['TOKEN']\n"
        hits = [what for pattern, what in FORBIDDEN_IN_SCRIPTS if re.search(pattern, old, re.M)]
        self.assertEqual(len(hits), 3, hits)

    def test_check_valid_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ok.csv")
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write("Title,Media URL,Pinterest board,Thumbnail,Description,Link,Publish date,Keywords\n"
                        "Easy Soup,https://example.com/a.jpg,Soups,,Warm soup,https://example.com/soup,,\n")
            p = self.run_script("check_csv.py", "--json", "--now", "2026-10-04T00:00:00", path)
            self.assertEqual(p.returncode, 0, p.stderr)
            doc = json.loads(p.stdout)[0]
            self.assertEqual([f["code"] for f in doc["findings"]], ["date.empty"])
            self.assertEqual(doc["summary"]["rows"], 1)

    def test_check_semicolon_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "semi.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("Title;Media URL\nA;B\n")
            p = self.run_script("check_csv.py", path)
            self.assertEqual(p.returncode, 1)
            self.assertIn("separated by semicolons (a regional Excel format)", p.stdout)

    def test_check_missing_file_fails(self):
        p = self.run_script("check_csv.py", os.path.join(tempfile.gettempdir(), "no-such-file.csv"))
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("No such file", p.stderr)

    def test_build_then_check(self):
        start = date.today() + timedelta(days=3)
        pins = [{"title": f"Pin {i}", "media_url": f"https://example.com/{i}.jpg", "board": "Soups",
                 "description": "Warm soup", "link": f"https://example.com/soup-{i}/"} for i in range(3)]
        with tempfile.TemporaryDirectory() as tmp:
            src, out = os.path.join(tmp, "pins.json"), os.path.join(tmp, "out.csv")
            with open(src, "w", encoding="utf-8") as f:
                json.dump(pins, f)
            p = self.run_script("build_csv.py", src, "--tz", "America/New_York",
                                "--start", start.isoformat(), "--end", (start + timedelta(days=2)).isoformat(),
                                "--out", out)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertTrue(os.path.isfile(out))
            c = self.run_script("check_csv.py", "--json", out)
            self.assertEqual(c.returncode, 0, c.stdout)
            doc = json.loads(c.stdout)[0]
            self.assertEqual(doc["summary"]["scheduled"], 3)
            self.assertFalse([f for f in doc["findings"] if f["severity"] == "error"])

    def test_build_rejects_past_dates(self):
        past = date.today() - timedelta(days=10)
        pins = [{"title": "Pin", "media_url": "https://example.com/a.jpg", "board": "Soups",
                 "link": "https://example.com/soup/"}]
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "pins.json")
            with open(src, "w", encoding="utf-8") as f:
                json.dump(pins, f)
            p = self.run_script("build_csv.py", src, "--tz", "America/New_York",
                                "--start", past.isoformat(), "--end", (past + timedelta(days=1)).isoformat(),
                                "--out", os.path.join(tmp, "out.csv"))
            self.assertNotEqual(p.returncode, 0)


# --- Eval suite ---------------------------------------------------------------------------

def eval_cases():
    for name in sorted(os.listdir(EVALS)):
        path = os.path.join(EVALS, name)
        if os.path.isfile(os.path.join(path, "prompt.md")):
            yield name, path


def grader(case, name):
    front, body = strip_frontmatter(read(os.path.join(EVALS, case, "graders", name + ".md")))
    m = re.search(r"^input_match: '(.*)'$", front, re.M)
    return front, (m.group(1).replace("''", "'") if m else None), body


def render_input(**fields):
    """A render_pin input as the eval runner sees it: one line of JSON."""
    return json.dumps(fields)


class EvalSuiteTest(unittest.TestCase):
    def test_cases_are_well_formed(self):
        cases = list(eval_cases())
        self.assertGreaterEqual(len(cases), 11)
        for name, path in cases:
            front, body = strip_frontmatter(read(os.path.join(path, "prompt.md")))
            self.assertIsNotNone(front, f"{name}: prompt.md has no frontmatter")
            self.assertIn('plugins: ["../../plugins/insightpins"]', front, name)
            self.assertTrue(body.strip(), f"{name}: empty prompt")
            graders = os.listdir(os.path.join(path, "graders"))
            self.assertTrue(graders, f"{name}: no graders")
            for g in graders:
                gfront, gbody = strip_frontmatter(read(os.path.join(path, "graders", g)))
                self.assertIsNotNone(gfront, f"{name}/{g}: no frontmatter")
                kind = re.search(r"^type: (\w+)$", gfront, re.M).group(1)
                self.assertIn(kind, ("tool_used", "tool_order", "regex", "llm"), f"{name}/{g}")
                if kind == "llm":
                    self.assertIn("PASS", gbody, f"{name}/{g}")
                    self.assertIn("FAIL", gbody, f"{name}/{g}")
                tool = re.search(r"^tool: (\S+)$", gfront, re.M)
                if tool and tool.group(1) not in ("Skill", "Bash", "Read", "Glob", "Write"):
                    self.assertTrue(tool.group(1).startswith(MCP_TOOL), f"{name}/{g}: {tool.group(1)}")
                m = re.search(r"^input_match: '(.*)'$", gfront, re.M)
                if m:
                    re.compile(m.group(1))

    def test_mock_responses_are_json(self):
        for dirpath, _, filenames in os.walk(EVALS):
            if "results" in dirpath.split(os.sep):
                continue
            for n in filenames:
                if dirpath.endswith(os.path.join("mocks", "insightpins")) and n.endswith(".md"):
                    path = os.path.join(dirpath, n)
                    front, body = strip_frontmatter(read(path))
                    self.assertIn("type: fixed", front, path)
                    if re.search(r"^error: true$", front, re.M):
                        self.assertTrue(body.strip(), f"{path}: empty error message")
                        continue
                    try:
                        json.loads(re.sub(r"\{\{input\.\w+\}\}", "x", body))
                    except ValueError as e:
                        self.fail(f"{path}: not JSON ({e})")

    def test_scaffold_scripts_exist(self):
        for name, path in eval_cases():
            case_yaml = os.path.join(path, "case.yaml")
            if os.path.isfile(case_yaml):
                m = re.search(r"scaffold_script: (\S+)", read(case_yaml))
                if m:
                    script = os.path.join(path, m.group(1))
                    self.assertTrue(os.access(script, os.X_OK), f"{name}: {m.group(1)} not executable")

    def test_no_faded_panel_grader(self):
        _, pattern, _ = grader("winter-palette", "no-faded-panel")
        rx = re.compile(pattern)
        bad = [render_input(template_id="split-horizontal", title="T", palette_id="coral-reef"),
               render_input(palette_id="ocean-breeze", title="T", template_id="diagonal-cut")]
        good = [render_input(template_id="diagonal-cut", title="T", palette_id="midnight"),
                render_input(template_id="split-horizontal", title="T", palette_id="rose-gold"),
                render_input(template_id="minimal-clean", title="T", palette_id="coral-reef"),
                render_input(template_id="split-horizontal", title="T")]
        for s in bad:
            self.assertTrue(rx.search(s), s)
        for s in good:
            self.assertFalse(rx.search(s), s)

    def test_weak_palette_graders(self):
        _, winter, _ = grader("winter-palette", "no-weak-palette")
        _, optimize, _ = grader("optimize-variants", "no-weak-palette")
        self.assertTrue(re.search(winter, render_input(template_id="minimal-clean", palette_id="coral-reef")))
        self.assertFalse(re.search(winter, render_input(template_id="minimal-clean", palette_id="midnight")))
        # optimize: a failing palette is fine only without a button, and never on a colour panel
        self.assertTrue(re.search(optimize, render_input(template_id="minimal-clean", palette_id="coral-reef")))
        self.assertFalse(re.search(optimize, render_input(template_id="minimal-clean", palette_id="sage",
                                                          show_cta=False)))
        self.assertTrue(re.search(optimize, render_input(template_id="split-horizontal", palette_id="sage",
                                                         show_cta=False)))
        self.assertTrue(re.search(optimize, render_input(palette_id="ocean-breeze", template_id="split-horizontal")))
        self.assertFalse(re.search(optimize, render_input(template_id="split-horizontal", palette_id="lavender")))
        self.assertFalse(re.search(optimize, render_input(template_id="collage-style", palette_id="sage")))

    def test_number_badge_subtitle_grader(self):
        _, pattern, _ = grader("listicle-number", "no-faded-badge-subtitle")
        rx = re.compile(pattern)
        self.assertTrue(rx.search(render_input(template_id="number-badge", description="Sub")))
        self.assertTrue(rx.search(render_input(description="Sub", show_description=True,
                                               template_id="number-badge")))
        self.assertFalse(rx.search(render_input(template_id="number-badge", description="Sub",
                                                show_description=False)))
        self.assertFalse(rx.search(render_input(template_id="number-badge", title="T")))
        self.assertFalse(rx.search(render_input(template_id="numbered-steps", description="Sub")))

    def test_brand_palette_graders(self):
        _, keeps, _ = grader("brand-palette", "keeps-brand-palette")
        _, panel, _ = grader("brand-palette", "no-faded-panel")
        _, button, _ = grader("brand-palette", "no-faded-button")
        self.assertTrue(re.search(keeps, render_input(template_id="minimal-clean", palette_id="coral-reef")))
        self.assertFalse(re.search(keeps, render_input(template_id="minimal-clean", palette_id="midnight")))
        self.assertTrue(re.search(panel, render_input(template_id="split-horizontal", palette_id="coral-reef")))
        self.assertFalse(re.search(panel, render_input(template_id="minimal-clean", palette_id="coral-reef")))
        self.assertTrue(re.search(button, render_input(template_id="minimal-clean", palette_id="coral-reef")))
        self.assertFalse(re.search(button, render_input(template_id="minimal-clean", palette_id="coral-reef",
                                                        show_cta=False)))
        self.assertFalse(re.search(button, render_input(template_id="collage-style", palette_id="coral-reef")))
        self.assertFalse(re.search(button, render_input(template_id="minimal-clean", palette_id="midnight")))

if __name__ == "__main__":
    unittest.main()
