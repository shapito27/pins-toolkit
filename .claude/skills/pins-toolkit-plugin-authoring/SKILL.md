---
name: pins-toolkit-plugin-authoring
description: Use when editing insightpins plugin files or references.
category: plugin-authoring
---

# pins-toolkit plugin authoring

Plugin files under `plugins/insightpins/` must pass the repo's text guards. Check them before saving, not after the test run fails.

- No em or en dashes in plugin files.
- No `curl`, `-F file=`, `/api/uploads` or `multipart` in plugin files; describe uploads in words and point to `user-photos.md`.
- No `assets/` paths outside the plugin README.
- No `<script>`, and no external URLs in any HTML shown in a reference. Keep HTML examples to a few lines of plain HTML and inline CSS, or leave them out.

The plugin ships no scripts, hooks, agents or `bin/` (decided in `docs/PLAN.md`). Repo helpers such as the eval date refresh go in the top-level `scripts/` folder, never in the plugin.

Server-side work (new tools or `hint` fields in `pin-generator-tool`) is not plugin work; it goes in `docs/MCP-IMPROVEMENTS.md`, and the plugin must still work on older servers. Each such item gets a numbered row, a status line (Observed or Inferred, with the date), an effort and a priority, and a short write-up under the matching heading; the plugin change that works around it is noted in the same entry.

Do not bump the plugin version or edit the plugin README as part of a guidance edit unless the user asks for a release.
