# InsightPins plugin evals

`claude plugin eval` suite for [`plugins/insightpins`](../plugins/insightpins). The InsightPins MCP
tools are mocked (`mocks/insightpins/`, matching the server as deployed on 2026-10-05 (0.3.0): 8 tools,
38 templates with `photo_area`, `best_photo`, `preview_url`, `overlay` and `readable_palettes`, the darker palettes from #93, `image_details`
(with `hint`) and `structured` from `extract_url`, photo controls, `overlay_strength` and
`warnings` in `render_pin`), so a run uses no real renders and needs no InsightPins account.

```bash
claude plugin eval . --scaffold --no-publish          # all cases, 3 runs each, with and without the plugin
claude plugin eval . --case copy-only --runs 1        # one case
```

`--scaffold` is needed by `review-uploaded-pin` and `bulk-csv-check`, whose `fixture.sh` copies a
fixture into the run's workspace. `bulk-csv-check` also needs `--allow-tools Bash` (and, on Linux,
`bubblewrap` and `socat` for the sandbox). Results go to `results/` (git-ignored).

## Cases

| Case | Tests | Key graders |
| - | - | - |
| `recipe-from-url` | URL -> pin; `image_details` with a wide `primary_image`, a portrait food photo, an author headshot and an infographic; `structured` recipe data | picks the portrait food photo (or the wide one in a panel template whose `best_photo` is `landscape`), sets `text_size` ("auto" or >= 120), puts the page's cook time (25 min) on the pin and invents no price or other values, full report |
| `listicle-number` | "17 Easy Chicken Dinners" page | the real number 17 reaches the pin; no other list number |
| `blocked-page` | `extract_url` returns a "Just a moment..." bot-check page as a success (older servers) | no render; tells the user and asks for title/image |
| `blocked-page-error` | `extract_url` returns a `[BOT_CHALLENGE]` error (current server) | no render; tells the user and asks for title/image |
| `crop-warning` | Only a landscape photo; every render returns `IMAGE_CROPPED` | handles the crop (a panel template whose `best_photo` is `landscape` or `square`, `image_focus` or `image_fit`), renders at most twice instead of looping on the warning, honest report |
| `variations-low-quota` | 3 variations requested, 1 render left | checks quota before rendering, renders at most 1, explains the limit and reset |
| `copy-only` | Pinterest text for a blog post, no MCP | headline, title, description, alt text, board all present; keyword-led title; no invented claims |
| `bulk-csv-check` | Check a bulk upload CSV with 6 time-independent problems (`resources/my-pins.template.csv`, dates filled in relative to today) | runs `check_csv.py` (indicator), finds at least 5 of 6 tied to the right pin, doesn't silently shorten titles or guess the day/month order |
| `review-uploaded-pin` | review of a weak quote pin (`resources/quote-pin.jpg`) | finds the real problems (contrast, thin/small text, empty space, vague CTA), gives a score and ranked fixes |
| `winter-palette` | Winter travel page with a bright, snowy landscape photo | a palette is set; no off-mood red or orange palette (`coral-reef`, `sunset-glow`, `terracotta`) |
| `optimize-variants` | Optimize the weak quote pin; it gets saves but few clicks | `optimize-pin` fires; 2-3 renders; diagnosis tied to clicks, variants that each change one thing, rate-based test plan; pin copy invents no facts |
| `optimize-one-render` | Same, with 1 render left | checks quota first, renders exactly once, says the one version combines fixes and can't show which helped, offers the rest for later |
| `optimize-no-renders` | Same, with 0 renders left (render returns a limit error) | no render; still delivers the review, copy and settings, and says when the limit resets |
| `brand-palette` | User asks for their brand palette `coral-reef` (readable on every template since #93) | keeps `coral-reef`; doesn't hide the button; invents no recipe facts |
| `hinted-photos` | The page's only portrait image is an author headshot with `hint: "author"`; a logo has `hint: "logo"` | never renders a hinted image, uses one of the two landscape page photos, honest report |
| `own-photo-file` | The user's own photo is a file in the folder | creates an upload link, no base64 upload, no render before the upload, at most one `get_upload`, gives the 7-day notice |
| `own-photo-pasted` | The user pasted their photo into the chat (only `Skill` allowed) | creates an upload link, gives the upload page and the 7-day notice, waits; no render, no polling |
| `remake-no-upload` | Remake another blogger's quote pin (`resources/ref-pin.jpg`) for the user's post | never uploads the reference pin; renders with page photos only (or none); honest copy that doesn't reuse the quote |

## Reading the baseline

In the four MCP cases, the without-plugin arm has no InsightPins tools at all, so its low score
mostly measures "no connector", not the skills. The meaningful skill-vs-plain-Claude comparisons are
`copy-only` and `review-uploaded-pin`. For the MCP cases, look at the with-plugin scores on the
specific graders (photo choice, text size, honesty, quota handling).

## Latest results (2026-10-04, sonnet judge, mocks matching the October 4 server)

Run with `--judge-model sonnet` for stable verdicts: the default small judge once failed a complete
`copy-only` answer that a sonnet judge passed 3/3.

| Case | With plugin | Without | Delta |
| - | - | - | - |
| recipe-from-url | 1.00 | 0.14 | +0.86 |
| listicle-number | 1.00 | 0.33 | +0.67 |
| blocked-page | 1.00 | 0.67 | +0.33 |
| blocked-page-error | 1.00 | 0.67 | +0.33 |
| crop-warning | 1.00 | 0.00 | +1.00 |
| variations-low-quota | 1.00 | 0.50 | +0.50 |
| copy-only | 1.00 | 0.33 | +0.67 |
| review-uploaded-pin | 1.00 | 0.67 | +0.33 |
| bulk-csv-check | 1.00 | 0.00 | +1.00 |
| winter-palette | 1.00 | not run | |
| optimize-variants | 1.00 | not run | |
| optimize-one-render | 1.00 | not run | |
| optimize-no-renders | 1.00 | not run | |
| brand-palette | 1.00 | not run | |

The last five cases were added with the contrast and color rules and run with the plugin only
(`--ablation none`; without the plugin there are no InsightPins tools). Against the skills before
those rules (`main` at 8a15f47), `winter-palette` scored 0.67 (a white-text panel on a mid-tone
palette in 3/3 runs) and `optimize-variants` 0.76 (a result the page didn't state in the copy in
3/3 runs, a low-contrast palette in 1). A full run of all 14 cases with the plugin scored 1.00
(2026-10-04), after the fixes below.

History:
- After the pin generator's colour map (#85) showed buttons use the palette's light `background` on
  `primary`, `brand-palette` failed 3/3 on the new button grader: Claude kept `coral-reef` with the
  button on. `create-pin` step 5 now says to hide the button for the six palettes below 3:1.
- The `number-badge` subtitle grader failed 3/3 at first: the warning lived only in
  `style-selection.md`, which isn't read at the render step. `create-pin` step 8 and the template
  guide now say it too.
- `optimize-variants` once used `sage` on `split-horizontal` for variant C: only variant B was told
  to use the contrast table. Every variant except A (which keeps the original palette) now must.
- One `honest-copy` failure was a real audience claim ("perfect for anyone who wants a simpler
  home"); `optimize-pin`'s facts rule now names audiences.
- `optimize-variants` first failed `honest-copy` for "the 12 lessons that made it stick": the
  `pin-copy` facts rule didn't reach `optimize-pin`, which doesn't load `pin-copy`. The rule is now
  repeated in `optimize-pin`, `remake-pin` and `create-pin`. The grader was also scoped to the pin
  copy, after it failed an honest reply for the test plan's "2-4 weeks" and the link expiry date.
  It is still a little noisy: in a later run one reply whose copy was the page's own wording got
  PASS FAIL FAIL (case score 0.95). Read the reply before treating a single `honest-copy` failure
  as a regression.
- `bulk-csv-check` first failed plain Claude for numbering rows from the first pin instead of the
  header; the grader now accepts either numbering and matches problems by pin.
- `copy-only` first scored 0.83: one run added claims the post didn't make ("no remodel",
  "renters"). `pin-copy` got a "facts only from the source" rule; 3/3 since.
- `recipe-from-url` had one judge failure for giving an expiry date instead of "7 days" (grader now
  accepts a date). The same run's copy said "ready in one pan", which the page didn't state;
  `create-pin` now repeats the facts-only rule in its copy step.
- `variations-low-quota` had a mock bug (render result said 45 renders left after quota said 1);
  the case now has its own consistent `render_pin` mock.

Plain Claude already reviews an obviously weak pin well, so `review-uploaded-pin` shows little
delta; the skill's value there is the consistent rubric and format.
