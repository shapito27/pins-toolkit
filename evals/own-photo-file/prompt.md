---
plugins: ["../../plugins/insightpins"]
description: The user wants their own photo file on the pin; tests that Claude uploads it through an upload link (falling back to the upload page), never renders with a local path, and says the photo is kept for 7 days
tags: [mcp, create, upload]
max_turns: 30
allowed_tools: [Read, Glob, Skill, Bash]
---

Make a Pinterest pin for my post https://snowtrails.example/yosemite-in-spring/ but use my own photo, my-photo.jpg in this folder, not the one on the page.
