# InsightPins plugin evals

`claude plugin eval` suite for [`plugins/insightpins`](../plugins/insightpins). The InsightPins MCP
tools are mocked (`mocks/insightpins/`), so a run uses no real renders and needs no InsightPins account.

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
| `recipe-from-url` | URL -> pin; photo choice among logo, tracking pixel, headshot, thumbnail and real photos | picks the vertical food photo, sets `text_size` >= 120, invents no cook time/servings/price, full report (links, 7-day expiry, photo source, title/description/alt text) |
| `listicle-number` | "17 Easy Chicken Dinners" page | the real number 17 reaches the pin; no other list number |
| `blocked-page` | `extract_url` returns a "Just a moment..." bot-check page as a success (older servers) | no render; tells the user and asks for title/image |
| `blocked-page-error` | `extract_url` returns a `[BOT_CHALLENGE]` error (current server) | no render; tells the user and asks for title/image |
| `variations-low-quota` | 3 variations requested, 1 render left | checks quota before rendering, renders at most 1, explains the limit and reset |
| `copy-only` | Pinterest text for a blog post, no MCP | headline, title, description, alt text, board all present; keyword-led title; no invented claims |
| `bulk-csv-check` | Check a bulk upload CSV with 6 time-independent problems (`resources/my-pins.csv`) | runs `check_csv.py` (indicator), finds at least 5 of 6 tied to the right pin, doesn't silently shorten titles or guess the day/month order |
| `review-uploaded-pin` | review of a weak quote pin (`resources/quote-pin.jpg`) | finds the real problems (contrast, thin/small text, empty space, vague CTA), gives a score and ranked fixes |

## Reading the baseline

In the four MCP cases, the without-plugin arm has no InsightPins tools at all, so its low score
mostly measures "no connector", not the skills. The meaningful skill-vs-plain-Claude comparisons are
`copy-only` and `review-uploaded-pin`. For the MCP cases, look at the with-plugin scores on the
specific graders (photo choice, text size, honesty, quota handling).

## Latest results (2026-10-04, 8 cases)

Run with `--judge-model sonnet` for stable verdicts: the default small judge once failed a complete
`copy-only` answer that a sonnet judge passed 3/3.

| Case | With plugin | Without | Delta |
| - | - | - | - |
| recipe-from-url | 1.00 | 0.17 | +0.83 |
| listicle-number | 1.00 | 0.33 | +0.67 |
| blocked-page | 1.00 | 0.67 | +0.33 |
| blocked-page-error | 1.00 | 0.67 | +0.33 |
| variations-low-quota | 1.00 | 0.50 | +0.50 |
| copy-only (sonnet judge, 3 runs) | 1.00 | 0.00 | +1.00 |
| review-uploaded-pin | 1.00 | 1.00 | 0.00 |
| bulk-csv-check | 1.00 | 0.38-0.75 | +0.25 to +0.63 |

History:
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
