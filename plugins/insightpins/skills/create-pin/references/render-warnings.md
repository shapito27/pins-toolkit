# Render warnings

`render_pin` returns a `warnings` list when something may be wrong. Each has a `code` and a
`message`. Every render counts against the daily limit, so re-render only when a warning shows a
real problem in the preview, and never twice for the same warning.

| Code | What it means | What to do |
| - | - | - |
| `TITLE_CLAMPED` | The title is cut off even at the smallest size. | Always fix: shorten the headline. |
| `DESCRIPTION_CUT` | The subtitle (or the end of the title) is longer than the template shows. | Shorten the subtitle, or choose a template with more room. |
| `TITLE_SHRUNK` | The title was shrunk well below the requested size to fit. | Shorten the headline if it now looks small in the preview. |
| `TITLE_SMALL` | The title uses only a small part of its room. | Re-render with `text_size: "auto"`. Use "auto" from the first render and this rarely appears. |
| `IMAGE_CROPPED` | Only part of the photo is visible (for example a wide photo in a tall frame). | Look at the preview. If the subject is cut off, set `image_focus` on it, or `image_fit: "contain"`, or choose a panel template. If the subject is in view, keep the pin: the warning stays because the crop itself doesn't change. |
| `IMAGE_UPSCALED` | A small photo is enlarged a lot, so it may look soft. | Prefer a larger photo from `image_details` or a template with a smaller photo area. Fine to keep if the preview looks sharp enough; lower `image_zoom` if you raised it. |
| `SUBTITLE_HIDDEN` | The template has no subtitle, so the description isn't shown. | Expected if you chose that template on purpose; otherwise pick one with `supports_subtitle: true`. No re-render needed just for this. |
| `IMAGE_IGNORED` | The template has no photo (`uses_photo: false`). | Expected for text-only templates. |
| `EXTRA_IMAGES_IGNORED` | Extra photos were sent to a one-photo template. | Use a template with `uses_extra_images: true`, or leave the extras out next time. |
| `LAYOUT_UNSETTLED` | The title size hadn't settled when the pin was captured. | Re-render only if the preview looks wrong. |

`image_focus`, `image_zoom` and `image_fit` apply to every photo in the pin and are meant for
single-photo templates; `side-panels` and the two lower `lifestyle-collage` tiles ignore them.
