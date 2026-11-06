# SW350 G04: analysis plan addendum for group D

Written on 29 October 2026, after Study 1's run (00:54:48 to 01:29:27) and results (about 02:45), and before
the group D run. It adds one group; it changes nothing in the analysis plan v2.1 or in Study 1's data,
answers, scores or nine main results. In the paper, D is reported as a group added after the first results
(plan v2.1, section 9: kept, dated and reported).

Approved before the D run by: Alanoud, on 29 October 2026 at ____ (fill in the Analysis Plan doc before running).

## Why D was added

Study 1 showed that the filter (C) gave no answer with a place the traveller cannot use, but fewer fully
suitable places than telling ChatGPT the disability (A); telling gave more fully suitable places, but some
answers still included a place she cannot use. Group D tests the two together. The team decided this on
29 October 2026, after seeing Study 1's results.

## Design

- D = the filtered list of C + the traveller message of A ("I'm blind.", "I'm Deaf." or "I use a wheelchair.").
- For each repeat and traveller, D's hidden list is exactly C's (same places, same order: Study 1's list
  orders, seed 20261028). So D differs from C only by the disability sentence, and from A only by the filter.
- 300 requests: 3 travellers x 5 interests x 20 repeats. The repeats in a random order and the requests in a
  random order inside each repeat (seed "20261028|D").
- Same model name (gpt-6.1-sol), same Responses API settings and sending code as Study 1 (run_requests.py
  unchanged: default settings, store=False, strict JSON answer format, up to 3 requests at once, re-send only
  after a technical error).
- D runs on a different date and time from A, B and C. The model name is the same, but OpenAI may have
  updated the model in between (no dated version name exists). This is stated as a limitation.

## Measures

Unchanged: the measures of plan v2.1 (sections 4 and 7) and its special cases, scored with Study 1's frozen
scoring code (score_answers.py, SHA-256 0eec64a6...). A, B and C are Study 1's scores, unchanged.

## The six D results

| # | Comparison | Outcome | Test (two-sided) |
| --- | --- | --- | --- |
| D1 to D3 | D vs C, for the wheelchair user, the blind traveller and the Deaf traveller | Fully suitable score (0 to 5) | Mann-Whitney U |
| D4 to D6 | D vs A, for each traveller | Fully suitable score (0 to 5) | Mann-Whitney U |

- HD1 (D1 to D3). Null: the fully suitable score has the same distribution in D and C. Alternative: the
  distributions differ. Expected: higher in D (telling helps when the list is already filtered).
- HD2 (D4 to D6). Null: the fully suitable score has the same distribution in D and A. Alternative: the
  distributions differ. Expected: higher in D (the filter helps when ChatGPT is told).
- Holm on these six p-values at 0.05, separately from Study 1's nine main results, which are not changed.
- Sizes as in Study 1: mean and median in each group, difference in means with a 95% bootstrap interval
  (2,000 resamples, seed 20261028).

## Secondary (uncorrected, labelled "added later")

- Every measure of section 4, Measure 1 and Measure 2 (yes/no), for D vs C and D vs A, each traveller.
- The main outcome in D is met by design, as in C (the filter removed those places); this is stated
  whenever it is reported.
- Measure 3 in D (percentage with a 95% Wilson interval), per interest (no tests), rules broken, kinds of
  place, and a sensitivity check (the six D results using only answers with no invalid pick).
- Measure 2 uses the same automatic rule as Study 1. Every flagged sentence is saved, and the team reads them,
  as for Study 1.

## Reporting

- D is marked "added after the first results" in Methods and in every table where it appears.
- Study 1's nine main results stay the main results of the paper.
- A result that is not clear is written as "we did not find a clear difference", with the numbers.
- Drafted with Claude on 29 October 2026 after the team's decision, and declared in the AI-use statement.
