# Render warnings

`render_pin` returns a `warnings` list when something may be wrong. Each has a `code` and a
`message`. Every render counts against the daily limit, so re-render only when a warning shows a
real problem in the preview, and never twice for the same warning.

| Code | What it means | What to do |
| - | - | - |
| `TITLE_CLAMPED` | The title is cut off even at the smallest size. | Always fix: shorten the headline. |
| `DESCRIPTION_CUT` | The subtitle (or the end of the title) is longer than the template shows. | Shorten the subtitle, or choose a template with more room. |
| `LIST_ITEMS_CUT` | On `numbered-steps` or `checklist`, some list items were left off (only so many fit at this text size) or cut short. The message says which. | Give fewer items, shorten the long ones (about 45 characters), or use a smaller `text_size`. |
| `TITLE_SHRUNK` | The title was shrunk well below the requested size to fit. | Shorten the headline if it now looks small in the preview. |
| `TITLE_SMALL` | The title uses only a small part of its room. | Re-render with `text_size: "auto"`. It doesn't fire on every template (for example `recipe-card`), so judge the title size in the preview too, and use "auto" from the first render. |
| `IMAGE_CROPPED` | Only part of the photo is visible (for example a wide photo in a tall frame). It is raised while `image_focus` is the default centre or `"auto"`, and not once you set a point or side yourself. | Look at the preview. If the subject is in view, keep the pin. If it is cut off, set `image_focus` on it (or use `"auto"` on the first render); to show more of the photo, use `image_fit: "contain"`, a panel template or another photo. `image_focus` only chooses which part shows, not how much. |
| `IMAGE_UPSCALED` | A small photo is enlarged a lot, so it may look soft. | Prefer a larger photo from `image_details` or a template with a smaller photo area. Fine to keep if the preview looks sharp enough; lower `image_zoom` if you raised it. |
| `SUBTITLE_HIDDEN` | The template has no subtitle, so the description isn't shown. | Expected if you chose that template on purpose; otherwise pick one with `supports_subtitle: true`. No re-render needed just for this. |
| `IMAGE_IGNORED` | The template has no photo (`uses_photo: false`). | Expected for text-only templates. |
| `EXTRA_IMAGES_IGNORED` | Extra photos were sent to a one-photo template. | Use a template with `uses_extra_images: true`, or leave the extras out next time. |
| `LAYOUT_UNSETTLED` | The title size hadn't settled when the pin was captured. | Re-render only if the preview looks wrong. |
| `OVERLAY_LOW_CONTRAST` | `overlay_strength` is below 60 on a template whose text sits on the overlay, so the text may be hard to read on this photo. | Check the title and site name in the preview; if they are hard to read, raise `overlay_strength` (or leave it at 100). |
| `LOW_CONTRAST` | The title, subtitle or button is below 3:1 contrast on the chosen palette. The message names the element, the ratio and up to five palettes that work with the template (worked out with the same elements shown). | Re-render once with a palette the message names, or one from the template's `readable_palettes`. If the user chose the palette, keep it: hide what fails (`show_cta: false` for the button, `show_description: false` for the subtitle) or switch to a template whose `readable_palettes` has it, and tell them why. A failing title can only be fixed by another palette or template. |
| `OVERLAY_IGNORED` | `overlay_strength` was set on a template without an overlay (`overlay: "none"`). | Nothing changed in the pin; leave the parameter out next time. No re-render needed. |

`image_focus`, `image_zoom` and `image_fit` apply to every photo in the pin and are meant for
single-photo templates; `side-panels` and the two lower `lifestyle-collage` tiles ignore them.

`LOW_CONTRAST` judges only the title, subtitle and button against the palette's colours.
The site name, small labels (a category or badge) and any text that sits on the photo are not
judged, so check them in the preview: `template-colors.md` notes where the site name is faint, and
`style-selection.md` explains the contrast rules.
