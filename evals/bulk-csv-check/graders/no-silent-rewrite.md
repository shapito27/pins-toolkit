---
type: llm
---

PASS if the reply does not claim to have shortened the long title, chosen a different image, or picked a day/month order for "10/7/2026" on its own; it should ask the user or leave those to them.
FAIL if it silently shortened the title, replaced the Drive link with a guessed URL, or converted the ambiguous date without asking.
