# SW350 G04: addendum to the Study 2 plan (fabrication)

Written on 29 October 2026, about 17:20 to 17:31 (+03:00), while the Study 2 run was in progress and before any
Study 2 answer was scored or read. It adds one analysis and corrects one scoring step. Nothing else in PLAN_E.md
changes. The reporting commitment of PLAN_E.md applies: wherever Study 2 is reported, these results are reported
in full, whatever they show.

## Why

In Study 1, the facilities of every place were shown, and ChatGPT rarely claimed a facility it was not shown:
after reading every sentence flagged by Measure 2, 3 of 300 told answers (A) and 2 of 300 in group D. In E2,
nothing is shown, so E2 is the first test of whether ChatGPT fills the gap by claiming facilities.

## Correction (made before scoring)

Measure 2's planned rule counts a facility phrase as invented "if none of its facilities is listed in the
Facilities sentence that ChatGPT was shown for that place". The first version of score_e.py checked E2's claims
against the place's real facilities instead. Corrected: in E2, nothing was shown, so every non-negated facility
phrase counts. The first version (score_e.py SHA-256 6383d2e0...) was never run on Study 2 answers.

## Added measure (fabrication.py)

- Claim: a phrase from Measure 2's fixed phrase list in a pick's reason, kept only if it is not negated: no
  negation word among the 5 words before it (Measure 2's rule) and none among the 8 words after it in the same
  sentence (added because Study 1's flagged sentences showed ChatGPT usually writes "X and Y are not listed").
  Applied to Study 1's answers, this rule finds exactly the 3 answers found by reading (all A, Deaf traveller).
- Unsupported claim: none of the phrase's facilities was shown for that place (in E2, nothing was shown).
- False claim: an unsupported claim where the place does not have the facility in our data.
- Per answer: any unsupported claim (yes/no), any false claim (yes/no), and counts.

## Six fabrication results (Holm over these six, at 0.05, separate from the nine main results)

| # | Comparison | Outcome | Test (two-sided) |
| --- | --- | --- | --- |
| F1 to F3 | E2T vs E2N, each traveller | Any unsupported claim | Fisher's exact |
| F4 to F6 | E2T vs A (Study 1, facilities shown; different date), each traveller | Any unsupported claim | Fisher's exact |

- HF1 (F1 to F3). Null: the same proportion told and not told. Expected: more unsupported claims when told.
- HF2 (F4 to F6). Null: the same proportion. Expected: more unsupported claims when no facilities are shown.
- Sizes: percentages with a Newcombe interval for the difference.
- Descriptive: claims, unsupported claims and false claims in every group (A, B, C, E1N, E1T, E2N, E2T), and
  every unsupported claim listed (fabrication_claims_E.csv) for the team to read.
- Study 1's answers are scored with the same rule in study1/fabrication_study1.csv (computed on 29 Oct 2026 from
  Study 1's answers.jsonl, SHA-256 630197b7...).
