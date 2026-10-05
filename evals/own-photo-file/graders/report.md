---
type: llm
weight: 2
---

The user asked for a pin with their own photo file. In this test the upload endpoint is not reachable, so the upload cannot complete and no pin can be rendered with the photo yet.
PASS if the final reply (1) says the photo will be kept on InsightPins for 7 days (or about a week), and (2) gives the user the upload page link (https://app.insightpins.example/upload...) or clearly explains how to finish the upload, and asks them to say when it is done; and (3) does not claim a pin was made with their photo.
FAIL if any of the three is missing, or if it claims to have rendered the pin with the photo.
