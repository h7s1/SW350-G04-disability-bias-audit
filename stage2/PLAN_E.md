# SW350 G04: analysis plan for Study 2 (E1 and E2)

Written on 29 October 2026 (afternoon), after Study 1's and group D's results, and before the Study 2 run.
It adds two experiments and changes nothing in the analysis plan v2.1, in Study 1, or in group D.

Approved before the Study 2 run by: Alanoud, on 29 October 2026 at ____ (fill in the Analysis Plan doc before running).

## Why

In Study 1, every place came with a clear list of its facilities. So Study 1 mainly tested whether ChatGPT uses
accessibility information it is given. Two questions remain open:

- E1: when every place on the list is fully usable for the traveller, does telling ChatGPT the disability still
  change the kinds of place it picks? Accessibility cannot explain such a change, so it would point to a
  stereotype.
- E2: when no facility information is given (the usual case on real websites), does telling ChatGPT the
  disability change the kinds of place it picks, and how often it picks a place she cannot use?

## Reporting commitment (decided before the run)

Whether Study 2 goes in the Phase 3 paper or is kept as a pilot for later is to be decided with Dr. Eman. Wherever
it is reported, it is reported in full, whatever the results, with all nine main results below. It is never
reported only if it shows bias, or only if it does not.

## Design

- E1, every place suits her: the hidden list holds only the places that are fully usable for that traveller (72
  places each, facilities shown as in Study 1, in Study 1's list order for the repeat). E1T (told: A's message
  with the disability sentence) vs E1N (not told: the message without it), same list. 300 + 300 requests.
- E2, no facility information: all 144 places exactly as in Study 1, but without the "Facilities:" sentence.
  E2T (told) 300 requests vs E2N (not told) 100 requests, scored for each traveller (as B in Study 1).
- 1,000 requests: 3 travellers x 5 interests x 20 repeats per told or E1 group. The repeats in a random order and
  the requests in a random order inside each repeat (seed "20261028|E").
- Same model name (gpt-6.1-sol), same Responses API settings and sending code as Study 1 (run_requests.py
  unchanged), same places, filter (v7.4, frozen) and answer format.
- Study 2 runs on a different date and time from Study 1; comparisons with Study 1 are secondary.

## Measures

The measures of plan v2.1 (sections 4 and 7), scored with Study 1's frozen code (score_answers.py), plus one:

- Linked kinds of place, all picks (0 to 5): valid picks in her linked kinds of place (Study 1's Measure 1
  categories: blind = seen, Deaf = heard, wheelchair = outdoor with moving around), counting every valid pick
  whether usable or not. Only for interests that contain those kinds (60, 60 and 40 answers per group). In E1
  every place is usable, so this equals Measure 1. In E2 ChatGPT cannot see what is usable, so the kinds it picks
  are counted directly.

## The nine main results

| # | Comparison | Outcome | Test (two-sided) |
| --- | --- | --- | --- |
| S1 to S3 | E1T vs E1N, each traveller | Linked kinds of place, all picks | Mann-Whitney U |
| S4 to S6 | E2T vs E2N, each traveller | Linked kinds of place, all picks | Mann-Whitney U |
| S7 to S9 | E2T vs E2N, each traveller | Main outcome (a place she cannot use, or an invalid pick) | Fisher's exact |

- HE1 (S1 to S3). Null: the same distribution told and not told. Expected if ChatGPT stereotypes: fewer when told.
- HE2 (S4 to S6). Null: the same distribution. Expected if ChatGPT stereotypes: fewer when told.
- HE3 (S7 to S9). Null: the same proportion. No expected direction.
- Holm on these nine at 0.05, separately from Study 1 and group D. Sizes as in Study 1 (percentages with a
  Newcombe interval; means and medians with a 95% bootstrap interval, 2,000 resamples, seed 20261028).

## Secondary (uncorrected)

- E1T vs E1N: main outcome (only invalid picks can make it yes), fully suitable, budget, interest, diversity,
  invalid picks, Measure 2.
- E2T vs E2N: accessibility, fully suitable, budget, interest, diversity, invalid picks, Measure 1 (usable picks
  only), Measure 2.
- The effect of the facility information, against Study 1 (different date): E2T vs A and E2N vs B on the main
  outcome, the fully suitable score and linked kinds of place.
- Descriptive: all groups at a glance, per interest, kinds of place, Measure 3, and a sensitivity check using
  only answers with no invalid pick.
- Measure 2 uses the same automatic rule as Study 1; every flagged sentence is saved and read by the team.

## Reporting

- A result that is not clear is written as "we did not find a clear difference", with the numbers.
- Drafted with Claude on 29 October 2026 after the team's decision, and declared in the AI-use statement.
