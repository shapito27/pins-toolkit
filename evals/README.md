# InsightPins plugin evals

`claude plugin eval` suite for [`plugins/insightpins`](../plugins/insightpins). The InsightPins MCP
tools are mocked (`mocks/insightpins/`), so a run uses no real renders and needs no InsightPins account.

```bash
claude plugin eval . --scaffold --no-publish          # all cases, 3 runs each, with and without the plugin
claude plugin eval . --case copy-only --runs 1        # one case
```

`--scaffold` is needed by `review-uploaded-pin`, whose `fixture.sh` copies the test pin into the
run's workspace. Results go to `results/` (git-ignored).

## Cases

| Case | Tests | Key graders |
| - | - | - |
| `recipe-from-url` | URL -> pin; photo choice among logo, tracking pixel, headshot, thumbnail and real photos | picks the vertical food photo, sets `text_size` >= 120, invents no cook time/servings/price, full report (links, 7-day expiry, photo source, title/description/alt text) |
| `listicle-number` | "17 Easy Chicken Dinners" page | the real number 17 reaches the pin; no other list number |
| `blocked-page` | `extract_url` returns a "Just a moment..." bot-check page | no render; tells the user and asks for title/image |
| `variations-low-quota` | 3 variations requested, 1 render left | checks quota before rendering, renders at most 1, explains the limit and reset |
| `copy-only` | Pinterest text for a blog post, no MCP | headline, title, description, alt text, board all present; keyword-led title; no invented claims |
| `review-uploaded-pin` | review of a weak quote pin (`resources/quote-pin.jpg`) | finds the real problems (contrast, thin/small text, empty space, vague CTA), gives a score and ranked fixes |

## Reading the baseline

In the four MCP cases, the without-plugin arm has no InsightPins tools at all, so its low score
mostly measures "no connector", not the skills. The meaningful skill-vs-plain-Claude comparisons are
`copy-only` and `review-uploaded-pin`. For the MCP cases, look at the with-plugin scores on the
specific graders (photo choice, text size, honesty, quota handling).

## Latest results (2026-10-03, 2 runs per arm; copy-only re-run with 3)

| Case | With plugin | Without | Delta |
| - | - | - | - |
| recipe-from-url | 1.00 | 0.17 | +0.83 |
| listicle-number | 1.00 | 0.33 | +0.67 |
| blocked-page | 1.00 | 1.00 | 0.00 |
| variations-low-quota | 1.00 | 0.50 | +0.50 |
| copy-only | 1.00 | 0.33 | +0.67 |
| review-uploaded-pin | 1.00 | 1.00 | 0.00 |

`copy-only` first scored 0.83: one run added claims the post didn't make ("no remodel", "renters").
The `pin-copy` skill now has a "facts only from the source" rule; after it, 3/3 runs pass.
Plain Claude already reviews an obviously weak pin well, so `review-uploaded-pin` shows no delta; the
skill's value there is the consistent rubric and format.
