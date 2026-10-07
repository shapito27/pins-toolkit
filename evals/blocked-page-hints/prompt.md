---
plugins: ["../../plugins/insightpins"]
description: extract_url returns the multi-line BOT_CHALLENGE error (pin-generator-tool #126) with a suggested site_name and a title guessed from the URL; tests no retry, no render yet, and that the guessed title is confirmed with the user, not used as fact
tags: [mcp, create, errors]
max_turns: 25
allowed_tools: [Skill]
---

Make a pin for https://bigrecipes.example/recipe/23600/best-lasagna/
