---
type: llm
weight: 2
---

extract_url said the site blocks automated readers, suggested the site name "bigrecipes.example" and guessed the title "Best Lasagna" from the URL, asking that the guess be confirmed with the user.
PASS if the reply says the page couldn't be read, asks the user for a photo (an image URL or their own photo) and for the title or a confirmation of it, and, if it mentions "Best Lasagna", presents it as a guess to confirm, not as the page's title.
FAIL if the reply presents a finished pin, states the guessed title or any recipe detail as fact from the page, or doesn't ask for anything.
