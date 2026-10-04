---
plugins: ["../../plugins/insightpins"]
description: Check a Pinterest bulk upload CSV with several failing rows; tests the pinterest-bulk-csv skill and its checker script
tags: [csv]
max_turns: 15
allowed_tools: [Read, Glob, Bash, Skill]
---

I'm about to bulk upload my-pins.csv (in this folder) to Pinterest. Can you check it first and tell me what to fix?
