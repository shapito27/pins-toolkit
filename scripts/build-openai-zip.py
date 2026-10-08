"""Build the ZIP to upload in OpenAI's plugin submission portal.

    python3 scripts/build-openai-zip.py [out.zip]

Zips plugins/insightpins with `.codex-plugin/plugin.json` at the top level of the ZIP. Leaves out
the Claude manifest (`.claude-plugin/`), so OpenAI reads only the Codex one, and caches and system
files. The default output is insightpins-openai-<version>.zip in the current folder (*.zip is
git-ignored).
"""
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.join(HERE, "..", "plugins", "insightpins")
SKIP_DIRS = {".claude-plugin", "__pycache__", "__MACOSX"}
SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def plugin_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name not in SKIP_FILES and not name.endswith(".pyc"):
                path = os.path.join(dirpath, name)
                yield path, os.path.relpath(path, root).replace(os.sep, "/")


def build(out, root=PLUGIN):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, arcname in plugin_files(root):
            zf.write(path, arcname)
    return out


def main():
    with open(os.path.join(PLUGIN, ".codex-plugin", "plugin.json"), encoding="utf-8") as f:
        version = json.load(f)["version"]
    out = sys.argv[1] if len(sys.argv) > 1 else f"insightpins-openai-{version}.zip"
    build(out)
    print(out)


if __name__ == "__main__":
    main()
