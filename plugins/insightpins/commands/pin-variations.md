---
description: Create several different Pinterest pins for one page with InsightPins
argument-hint: <url> [count, default 3]
---

Create several distinct Pinterest pins for one page using the `create-pin` skill: $ARGUMENTS

The count is the number after the URL; use 3 if none is given, and at most 5. Call `get_quota`
first and tell the user if the count is more than the renders left; then make as many as fit.

Make each pin clearly different: a different photo, a template from a different category and a
different headline angle (from the `pin-copy` skill). Changing only the color doesn't count.

Finish with a table (pin, angle, template, image link, edit link), one shared set of Pinterest
title, description, alt text and board (or one per pin when the angle needs it), and a tip to post
them a few days apart rather than all at once.
