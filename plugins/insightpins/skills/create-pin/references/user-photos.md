# Putting the user's own photo on a pin

`render_pin` needs an image URL. When the photo is the user's own (a file on their computer, or a
photo they pasted into the chat), upload it with the InsightPins tools to get one.

## Which photos to upload

- **Only the user's own photo, and only when they want it on a pin.** A request like "use my photo"
  or "make a pin with this picture of my cake" is enough.
- **Never upload a pin someone shares for review** (`review-pin` uses no uploads), **a pin made by
  someone else** that is only a style reference (`remake-pin`), **or an old pin as a background**:
  its text is baked in and would show under the new text. Ask for the original photo instead.
- If the photo shows other people or is clearly not theirs (a stock photo with a watermark, a
  screenshot of someone's site), remind them they need the right to publish it.

## Before the first upload

Tell the user, in one line, that the photo is stored on InsightPins for 7 days so the pin can be
drawn, with location and camera data removed, and that anyone with its link can open it. This
applies both when you send the file and when you give them the upload page: put it in the same
message as the link. Their request to use the photo is their go-ahead; you don't need to ask again.

## How to upload

1. **You can read the file and run commands** (Claude Code, Cowork, Codex; the user gave a file
   path or the file is in the working folder): call `create_upload_link` and send the file the way
   its result explains. If that fails (no network, the command isn't allowed), use step 2 with the same link,
   and include the 7-day notice in that message even though you meant to send the file yourself.
2. **You can't read the file** (a photo pasted into a chat, or into the terminal): call
   `create_upload_link`, give the user its `upload_page_url` exactly as returned (never change its
   domain or path) together with the 7-day notice above,
   ask them to upload the photo there and say when it's done, and end your turn. Don't render yet.
3. When they say it's done, call `get_upload` once with the `upload_id`:
   - `ready`: use its `image_url` as the pin photo;
   - `waiting`: nothing has arrived yet; ask them to try the page again;
   - `expired`: links work for 15 minutes, once; make a new one.
   Never call `get_upload` in a loop while you wait.
4. `upload_image` (the file as base64 text) is only for small images you already have as base64:
   a large photo costs a huge amount of text. Prefer the link.

Never put a guessed or local path in `image_url`, and never render with the photo before an upload
has returned its `image_url`.

## Limits and errors

| Problem | What to do |
| - | - |
| Not JPEG, PNG or WebP (for example HEIC, the iPhone default) | Ask for a JPEG or PNG copy of the photo |
| Too large (over 4.5 MB through the link, 3 MB through `upload_image`, or over 40 megapixels) | Ask for a smaller version, or a JPEG export |
| `[UPLOAD_LIMIT_REACHED]`: daily upload limit reached (10 per account per day) | Say so, say it resets at 00:00 UTC, and offer to use a photo URL instead |
| `[UPLOADS_OFF]`: uploads are turned off on the server | Say so, don't retry, and ask for a photo URL instead |
| 5 upload links already open | Use one of them, or wait 15 minutes |

## After rendering

Say that the photo came from the user, and that the uploaded photo and the pin image are kept for 7
days: the `edit_url` stops showing the photo after that, so they should finish editing within the
week or upload again.
