# SW350 G04: Study 2 results, E1 and E2 (numbers only)

Study 2 was planned on 29 October 2026, after Study 1 and group D (PLAN_E.md). E1: only places fully usable for that traveller, facilities shown. E2: all 144 places without the Facilities sentence. A and B are Study 1's scores, unchanged, shown for reference; Study 2 ran on a different date. Holm is applied to Study 2's nine main results only. The interpretation is written by the team.

## S0. The Study 2 run

| Item | Value |
| --- | --- |
| Answers | E1N 300, E1T 300, E2N 100, E2T 300 |
| Model(s) returned | gpt-6.1-sol (1000) |
| First request sent / last answer received | 2026-10-29T16:43:59+03:00 / 2026-10-29T17:48:07+03:00 |
| Re-sends after a technical error | 0 |
| Answers with a format problem | 0 |
| Answers with fewer or more than 5 picks | 0 |
| Invalid picks | 0 |
| Tokens | input 13,158,600 (cached 12,077,240, written to cache 1,078,360); output 489,661 (reasoning 97,258) |

## All groups at a glance (descriptive)

| Traveller | Group | Answers | Main outcome yes | Accessibility | Fully suitable | Budget | Interest | Diversity | Linked kinds of place (all picks) | Mentions the disability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wheelchair | B (Study 1: not told, all places) | 100 | 89.0% | 3.26 | 2.81 | 5.00 | 5.00 | 2.23 | 3.28 | 0.0% |
| wheelchair | A (Study 1: told, all places) | 100 | 33.0% | 4.55 | 4.46 | 5.00 | 5.00 | 2.19 | 2.72 | 100.0% |
| wheelchair | E1N (E1: not told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.72 | 2.48 | 2.97 | 0.0% |
| wheelchair | E1T (E1: told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.77 | 2.43 | 2.57 | 98.0% |
| wheelchair | E2N (E2: not told, no facility information) | 100 | 98.0% | 2.96 | 2.30 | 5.00 | 5.00 | 2.24 | 3.13 | 0.0% |
| wheelchair | E2T (E2: told, no facility information) | 100 | 98.0% | 3.69 | 3.11 | 5.00 | 5.00 | 1.79 | 2.50 | 100.0% |
| blind | B (Study 1: not told, all places) | 100 | 40.0% | 4.28 | 2.49 | 5.00 | 5.00 | 2.23 | 2.68 | 0.0% |
| blind | A (Study 1: told, all places) | 100 | 1.0% | 4.99 | 4.34 | 5.00 | 4.93 | 2.26 | 3.17 | 56.0% |
| blind | E1N (E1: not told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.94 | 2.43 | 2.63 | 0.0% |
| blind | E1T (E1: told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.83 | 2.32 | 3.30 | 45.0% |
| blind | E2N (E2: not told, no facility information) | 100 | 49.0% | 4.19 | 2.14 | 5.00 | 5.00 | 2.24 | 2.72 | 0.0% |
| blind | E2T (E2: told, no facility information) | 100 | 21.0% | 4.59 | 2.58 | 5.00 | 4.86 | 1.54 | 1.63 | 22.0% |
| Deaf | B (Study 1: not told, all places) | 100 | 31.0% | 4.52 | 2.79 | 5.00 | 5.00 | 2.23 | 1.77 | 0.0% |
| Deaf | A (Study 1: told, all places) | 100 | 3.0% | 4.97 | 3.82 | 5.00 | 4.98 | 2.18 | 1.38 | 63.0% |
| Deaf | E1N (E1: not told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.80 | 2.51 | 0.97 | 0.0% |
| Deaf | E1T (E1: told, fully usable places only) | 100 | 0.0% | 5.00 | 5.00 | 5.00 | 4.80 | 2.34 | 0.78 | 80.0% |
| Deaf | E2N (E2: not told, no facility information) | 100 | 20.0% | 4.60 | 2.89 | 5.00 | 5.00 | 2.24 | 1.85 | 0.0% |
| Deaf | E2T (E2: told, no facility information) | 100 | 20.0% | 4.80 | 2.97 | 5.00 | 4.99 | 2.03 | 0.50 | 63.0% |

## The nine main results of Study 2 (Holm over these nine, at 0.05)

| # | Comparison | Traveller | Outcome | Answers | Told | Not told | Difference (told - not told) | 95% interval | Test | p | Holm threshold (9 tests) | Holm-adjusted p | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | E1: told vs not told, every place fully usable | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.57, median 3 | mean 2.97, median 3 | -0.40 | [-0.62, -0.18] | Mann-Whitney U | 0.0007 | 0.0083 | 0.0042 | passes Holm |
| S2 | E1: told vs not told, every place fully usable | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 3.30, median 3 | mean 2.63, median 2 | +0.67 | [+0.08, +1.20] | Mann-Whitney U | 0.0017 | 0.0100 | 0.0085 | passes Holm |
| S3 | E1: told vs not told, every place fully usable | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 0.78, median 1 | mean 0.97, median 1 | -0.20 | [-0.35, -0.07] | Mann-Whitney U | 0.0074 | 0.0167 | 0.0221 | passes Holm |
| S4 | E2: told vs not told, no facility information | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.50, median 3 | mean 3.13, median 3 | -0.63 | [-0.97, -0.32] | Mann-Whitney U | 0.0020 | 0.0125 | 0.0085 | passes Holm |
| S5 | E2: told vs not told, no facility information | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 1.63, median 0 | mean 2.72, median 2 | -1.08 | [-1.78, -0.33] | Mann-Whitney U | <0.0001 | 0.0063 | <0.0001 | passes Holm |
| S6 | E2: told vs not told, no facility information | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 0.50, median 0.5 | mean 1.85, median 1.5 | -1.35 | [-1.68, -1.05] | Mann-Whitney U | <0.0001 | 0.0056 | <0.0001 | passes Holm |
| S7 | E2: told vs not told, no facility information | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 98/100 = 98.0% | 98/100 = 98.0% | +0.0 points | [-5.2 pts, +5.2 pts] | Fisher's exact | 1.0000 | 0.0250 | 1.0000 | does not pass Holm |
| S8 | E2: told vs not told, no facility information | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 21/100 = 21.0% | 49/100 = 49.0% | -28.0 points | [-39.8 pts, -14.9 pts] | Fisher's exact | <0.0001 | 0.0071 | 0.0004 | passes Holm |
| S9 | E2: told vs not told, no facility information | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 20/100 = 20.0% | 20/100 = 20.0% | +0.0 points | [-11.1 pts, +11.1 pts] | Fisher's exact | 1.0000 | 0.0500 | 1.0000 | does not pass Holm |

## Secondary results (uncorrected p-values). E2T vs A and E2N vs B compare with Study 1, run on a different date

| Comparison | Traveller | Measure | Answers | First group | Second group | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1T vs E1N | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| E1T vs E1N | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| E1T vs E1N | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| E1T vs E1N | wheelchair | Fully suitable score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | blind | Fully suitable score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | Deaf | Fully suitable score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | wheelchair | Interest | 100 / 100 | mean 4.77, median 5 | mean 4.72, median 5 | +0.05 | [-0.07, +0.17] | Mann-Whitney U | 0.4194 |
| E1T vs E1N | blind | Interest | 100 / 100 | mean 4.83, median 5 | mean 4.94, median 5 | -0.11 | [-0.21, -0.02] | Mann-Whitney U | 0.0362 |
| E1T vs E1N | Deaf | Interest | 100 / 100 | mean 4.80, median 5 | mean 4.80, median 5 | +0.00 | [-0.12, +0.11] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | wheelchair | Diversity | 100 / 100 | mean 2.43, median 2 | mean 2.48, median 2 | -0.05 | [-0.22, +0.12] | Mann-Whitney U | 0.7779 |
| E1T vs E1N | blind | Diversity | 100 / 100 | mean 2.32, median 2 | mean 2.43, median 2 | -0.11 | [-0.34, +0.11] | Mann-Whitney U | 0.6953 |
| E1T vs E1N | Deaf | Diversity | 100 / 100 | mean 2.34, median 2 | mean 2.51, median 2 | -0.17 | [-0.35, +0.00] | Mann-Whitney U | 0.1249 |
| E1T vs E1N | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E1T vs E1N | wheelchair | Measure 2: invented facility | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| E1T vs E1N | blind | Measure 2: invented facility | 100 / 100 | 11/100 = 11.0% | 0/100 = 0.0% | +11.0 points | [+5.0 pts, +18.6 pts] | Fisher's exact | 0.0007 |
| E1T vs E1N | Deaf | Measure 2: invented facility | 100 / 100 | 2/100 = 2.0% | 0/100 = 0.0% | +2.0 points | [-2.0 pts, +7.0 pts] | Fisher's exact | 0.4975 |
| E2T vs E2N | wheelchair | Accessibility score | 100 / 100 | mean 3.69, median 4 | mean 2.96, median 3 | +0.73 | [+0.54, +0.93] | Mann-Whitney U | <0.0001 |
| E2T vs E2N | blind | Accessibility score | 100 / 100 | mean 4.59, median 5 | mean 4.19, median 5 | +0.40 | [+0.15, +0.64] | Mann-Whitney U | 0.0003 |
| E2T vs E2N | Deaf | Accessibility score | 100 / 100 | mean 4.80, median 5 | mean 4.60, median 5 | +0.20 | [+0.03, +0.38] | Mann-Whitney U | 0.4844 |
| E2T vs E2N | wheelchair | Fully suitable score | 100 / 100 | mean 3.11, median 3 | mean 2.30, median 2 | +0.81 | [+0.56, +1.08] | Mann-Whitney U | <0.0001 |
| E2T vs E2N | blind | Fully suitable score | 100 / 100 | mean 2.58, median 3 | mean 2.14, median 2 | +0.44 | [+0.15, +0.71] | Mann-Whitney U | 0.0045 |
| E2T vs E2N | Deaf | Fully suitable score | 100 / 100 | mean 2.97, median 3 | mean 2.89, median 3 | +0.08 | [-0.11, +0.26] | Mann-Whitney U | 0.3705 |
| E2T vs E2N | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | wheelchair | Interest | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | blind | Interest | 100 / 100 | mean 4.86, median 5 | mean 5.00, median 5 | -0.14 | [-0.21, -0.07] | Mann-Whitney U | 0.0001 |
| E2T vs E2N | Deaf | Interest | 100 / 100 | mean 4.99, median 5 | mean 5.00, median 5 | -0.01 | [-0.03, +0.00] | Mann-Whitney U | 0.3222 |
| E2T vs E2N | wheelchair | Diversity | 100 / 100 | mean 1.79, median 2 | mean 2.24, median 2 | -0.45 | [-0.64, -0.27] | Mann-Whitney U | <0.0001 |
| E2T vs E2N | blind | Diversity | 100 / 100 | mean 1.54, median 2 | mean 2.24, median 2 | -0.70 | [-0.90, -0.52] | Mann-Whitney U | <0.0001 |
| E2T vs E2N | Deaf | Diversity | 100 / 100 | mean 2.03, median 2 | mean 2.24, median 2 | -0.21 | [-0.42, +0.00] | Mann-Whitney U | 0.0691 |
| E2T vs E2N | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| E2T vs E2N | wheelchair | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 1.65, median 2 | mean 1.33, median 1 | +0.32 | [+0.07, +0.57] | Mann-Whitney U | 0.0058 |
| E2T vs E2N | blind | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 0.95, median 0 | mean 1.37, median 1 | -0.42 | [-0.85, +0.05] | Mann-Whitney U | 0.0208 |
| E2T vs E2N | Deaf | Measure 1: suitable picks in her stereotype categories | 40 / 40 | mean 0.00, median 0 | mean 0.85, median 1 | -0.85 | [-0.95, -0.72] | Mann-Whitney U | <0.0001 |
| E2T vs E2N | wheelchair | Measure 2: invented facility | 100 / 100 | 100/100 = 100.0% | 0/100 = 0.0% | +100.0 points | [+94.8 pts, +100.0 pts] | Fisher's exact | <0.0001 |
| E2T vs E2N | blind | Measure 2: invented facility | 100 / 100 | 39/100 = 39.0% | 0/100 = 0.0% | +39.0 points | [+29.3 pts, +48.8 pts] | Fisher's exact | <0.0001 |
| E2T vs E2N | Deaf | Measure 2: invented facility | 100 / 100 | 21/100 = 21.0% | 0/100 = 0.0% | +21.0 points | [+13.2 pts, +30.0 pts] | Fisher's exact | <0.0001 |
| E2T vs A | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 98/100 = 98.0% | 33/100 = 33.0% | +65.0 points | [+54.1 pts, +73.6 pts] | Fisher's exact | <0.0001 |
| E2T vs A | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 21/100 = 21.0% | 1/100 = 1.0% | +20.0 points | [+11.8 pts, +29.0 pts] | Fisher's exact | <0.0001 |
| E2T vs A | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 20/100 = 20.0% | 3/100 = 3.0% | +17.0 points | [+8.4 pts, +26.1 pts] | Fisher's exact | 0.0002 |
| E2T vs A | wheelchair | Fully suitable score | 100 / 100 | mean 3.11, median 3 | mean 4.46, median 5 | -1.35 | [-1.57, -1.14] | Mann-Whitney U | <0.0001 |
| E2T vs A | blind | Fully suitable score | 100 / 100 | mean 2.58, median 3 | mean 4.34, median 4 | -1.76 | [-2.00, -1.53] | Mann-Whitney U | <0.0001 |
| E2T vs A | Deaf | Fully suitable score | 100 / 100 | mean 2.97, median 3 | mean 3.82, median 4 | -0.85 | [-1.03, -0.68] | Mann-Whitney U | <0.0001 |
| E2T vs A | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.50, median 3 | mean 2.72, median 3 | -0.22 | [-0.53, +0.10] | Mann-Whitney U | 0.4926 |
| E2T vs A | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 1.63, median 0 | mean 3.17, median 3 | -1.53 | [-2.20, -0.88] | Mann-Whitney U | <0.0001 |
| E2T vs A | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 0.50, median 0.5 | mean 1.38, median 1.5 | -0.88 | [-1.12, -0.62] | Mann-Whitney U | <0.0001 |
| E2N vs B | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 98/100 = 98.0% | 89/100 = 89.0% | +9.0 points | [+2.1 pts, +16.8 pts] | Fisher's exact | 0.0184 |
| E2N vs B | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 49/100 = 49.0% | 40/100 = 40.0% | +9.0 points | [-4.7 pts, +22.2 pts] | Fisher's exact | 0.2550 |
| E2N vs B | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 20/100 = 20.0% | 31/100 = 31.0% | -11.0 points | [-22.7 pts, +1.1 pts] | Fisher's exact | 0.1042 |
| E2N vs B | wheelchair | Fully suitable score | 100 / 100 | mean 2.30, median 2 | mean 2.81, median 3 | -0.51 | [-0.80, -0.21] | Mann-Whitney U | 0.0034 |
| E2N vs B | blind | Fully suitable score | 100 / 100 | mean 2.14, median 2 | mean 2.49, median 3 | -0.35 | [-0.66, -0.04] | Mann-Whitney U | 0.0773 |
| E2N vs B | Deaf | Fully suitable score | 100 / 100 | mean 2.89, median 3 | mean 2.79, median 3 | +0.10 | [-0.10, +0.30] | Mann-Whitney U | 0.3816 |
| E2N vs B | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 3.13, median 3 | mean 3.28, median 3 | -0.15 | [-0.37, +0.07] | Mann-Whitney U | 0.2179 |
| E2N vs B | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.72, median 2 | mean 2.68, median 2 | +0.03 | [-0.58, +0.62] | Mann-Whitney U | 0.8257 |
| E2N vs B | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 1.85, median 1.5 | mean 1.77, median 1.5 | +0.08 | [-0.30, +0.45] | Mann-Whitney U | 0.7565 |

## Per interest: picks in her linked kinds of place (20 answers per cell, no tests)

| Traveller | Interest | B: linked kinds (all picks) | A: linked kinds (all picks) | E1N: linked kinds (all picks) | E1T: linked kinds (all picks) | E2N: linked kinds (all picks) | E2T: linked kinds (all picks) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| wheelchair | history | 3.35 | 2.90 | 2.85 | 2.60 | 3.05 | 1.15 |
| wheelchair | art | - | - | - | - | - | - |
| wheelchair | nature | 3.60 | 3.20 | 3.40 | 3.10 | 3.80 | 3.30 |
| wheelchair | shopping | 2.90 | 2.05 | 2.65 | 2.00 | 2.55 | 3.05 |
| wheelchair | food | - | - | - | - | - | - |
| blind | history | 1.65 | 2.75 | 1.85 | 2.95 | 1.95 | 0.05 |
| blind | art | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 4.85 |
| blind | nature | 1.40 | 1.75 | 1.05 | 1.95 | 1.20 | 0.00 |
| blind | shopping | - | - | - | - | - | - |
| blind | food | - | - | - | - | - | - |
| Deaf | history | 1.00 | 0.75 | 0.95 | 0.55 | 1.00 | 0.00 |
| Deaf | art | 2.55 | 2.00 | 1.00 | 1.00 | 2.70 | 1.00 |
| Deaf | nature | - | - | - | - | - | - |
| Deaf | shopping | - | - | - | - | - | - |
| Deaf | food | - | - | - | - | - | - |

## Kinds of place picked (share of valid picks; descriptive)

| Group | Traveller | Valid picks | history_museum | art_gallery | heritage_site | guided_heritage_tour | park_garden | desert_experience | nature_reserve | observation_deck | traditional_market | shopping_mall | restaurant_cafe | live_show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B | all | 500 | 6.6% | 9.8% | 9.4% | 4.0% | 4.8% | 0.8% | 8.8% | 5.6% | 11.6% | 8.4% | 20.0% | 10.2% |
| A | wheelchair | 500 | 8.4% | 11.2% | 7.8% | 3.8% | 6.0% | 0.0% | 6.8% | 7.2% | 8.2% | 11.8% | 20.0% | 8.8% |
| A | blind | 500 | 11.0% | 12.4% | 5.2% | 3.8% | 8.8% | 0.0% | 4.2% | 7.0% | 14.6% | 6.8% | 18.6% | 7.6% |
| A | Deaf | 500 | 8.2% | 12.0% | 8.6% | 3.0% | 4.4% | 0.2% | 8.0% | 7.4% | 10.0% | 10.4% | 19.8% | 8.0% |
| E1N | wheelchair | 500 | 8.2% | 10.6% | 6.2% | 4.0% | 6.2% | 0.0% | 7.4% | 6.4% | 15.6% | 9.6% | 16.0% | 9.8% |
| E1N | blind | 500 | 7.4% | 16.0% | 8.2% | 4.0% | 4.8% | 3.4% | 7.6% | 4.2% | 12.2% | 9.0% | 19.2% | 4.0% |
| E1N | Deaf | 500 | 7.2% | 16.0% | 9.0% | 3.8% | 3.4% | 3.0% | 9.2% | 4.4% | 15.2% | 8.8% | 16.0% | 4.0% |
| E1T | wheelchair | 500 | 9.4% | 11.4% | 6.0% | 4.0% | 8.0% | 0.0% | 4.4% | 7.6% | 11.8% | 12.6% | 16.0% | 8.8% |
| E1T | blind | 500 | 11.8% | 16.0% | 4.6% | 3.6% | 8.2% | 0.0% | 4.0% | 7.8% | 16.0% | 7.4% | 16.6% | 4.0% |
| E1T | Deaf | 500 | 10.0% | 16.0% | 7.8% | 2.2% | 5.0% | 0.6% | 8.0% | 6.4% | 12.4% | 11.6% | 16.0% | 4.0% |
| E2N | all | 500 | 7.8% | 9.2% | 8.2% | 4.0% | 3.0% | 2.0% | 10.2% | 4.8% | 10.2% | 9.8% | 20.0% | 10.8% |
| E2T | wheelchair | 500 | 15.4% | 12.2% | 4.6% | 0.0% | 13.2% | 0.0% | 0.0% | 6.8% | 12.2% | 7.8% | 20.0% | 7.8% |
| E2T | blind | 500 | 0.0% | 3.4% | 0.0% | 20.4% | 15.4% | 0.0% | 4.6% | 0.0% | 21.2% | 0.8% | 18.0% | 16.2% |
| E2T | Deaf | 500 | 9.0% | 16.0% | 11.0% | 0.0% | 6.6% | 0.4% | 8.6% | 4.4% | 13.4% | 6.8% | 19.8% | 4.0% |

## Measures 2 and 3 (descriptive)

| Group | Traveller | Answers | Measure 2: answers flagged (automatic rule) | Measure 3: answers mentioning a disability word | 95% interval (Wilson) |
| --- | --- | --- | --- | --- | --- |
| E1N | wheelchair | 100 | 0 | 0/100 = 0.0% | [0.0%, 3.7%] |
| E1N | blind | 100 | 0 | 0/100 = 0.0% | [0.0%, 3.7%] |
| E1N | Deaf | 100 | 0 | 0/100 = 0.0% | [0.0%, 3.7%] |
| E1T | wheelchair | 100 | 0 | 98/100 = 98.0% | [93.0%, 99.4%] |
| E1T | blind | 100 | 11 | 45/100 = 45.0% | [35.6%, 54.8%] |
| E1T | Deaf | 100 | 2 | 80/100 = 80.0% | [71.1%, 86.7%] |
| E2N | all | 100 | 0 | 0/100 = 0.0% | [0.0%, 3.7%] |
| E2T | wheelchair | 100 | 100 | 100/100 = 100.0% | [96.3%, 100.0%] |
| E2T | blind | 100 | 39 | 22/100 = 22.0% | [15.0%, 31.1%] |
| E2T | Deaf | 100 | 21 | 63/100 = 63.0% | [53.2%, 71.8%] |

Every flagged sentence is in measure2_flagged_sentences_E.csv, to be read by the team as in Study 1.

## Sensitivity check: the nine main results using only answers with no invalid pick

| # | Comparison | Traveller | Outcome | Answers | Told | Not told | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | E1: told vs not told, every place fully usable | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.57, median 3 | mean 2.97, median 3 | -0.40 | [-0.62, -0.18] | Mann-Whitney U | 0.0007 |
| S2 | E1: told vs not told, every place fully usable | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 3.30, median 3 | mean 2.63, median 2 | +0.67 | [+0.08, +1.20] | Mann-Whitney U | 0.0017 |
| S3 | E1: told vs not told, every place fully usable | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 0.78, median 1 | mean 0.97, median 1 | -0.20 | [-0.35, -0.07] | Mann-Whitney U | 0.0074 |
| S4 | E2: told vs not told, no facility information | wheelchair | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 2.50, median 3 | mean 3.13, median 3 | -0.63 | [-0.97, -0.32] | Mann-Whitney U | 0.0020 |
| S5 | E2: told vs not told, no facility information | blind | Picks in her linked kinds of place (all valid picks) | 60 / 60 | mean 1.63, median 0 | mean 2.72, median 2 | -1.08 | [-1.78, -0.33] | Mann-Whitney U | <0.0001 |
| S6 | E2: told vs not told, no facility information | Deaf | Picks in her linked kinds of place (all valid picks) | 40 / 40 | mean 0.50, median 0.5 | mean 1.85, median 1.5 | -1.35 | [-1.68, -1.05] | Mann-Whitney U | <0.0001 |
| S7 | E2: told vs not told, no facility information | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 98/100 = 98.0% | 98/100 = 98.0% | +0.0 points | [-5.2 pts, +5.2 pts] | Fisher's exact | 1.0000 |
| S8 | E2: told vs not told, no facility information | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 21/100 = 21.0% | 49/100 = 49.0% | -28.0 points | [-39.8 pts, -14.9 pts] | Fisher's exact | <0.0001 |
| S9 | E2: told vs not told, no facility information | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 20/100 = 20.0% | 20/100 = 20.0% | +0.0 points | [-11.1 pts, +11.1 pts] | Fisher's exact | 1.0000 |

## Fabrication: facility claims not supported by what ChatGPT was shown (PLAN_E_addendum.md; Holm over these six)

Unsupported = none of the claimed facilities was shown for that place (in E2 nothing was shown). False = unsupported, and the place does not have it in our data. Every claim is listed in fabrication_claims_E.csv. A vs E2T compares runs on different dates.

| # | Comparison | Traveller | Outcome | Answers | First group | Second group | Difference | 95% interval | Test | p | Holm threshold (6 tests) | Holm-adjusted p | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | No facility information: told vs not told | wheelchair | Unsupported facility claim (any pick) | 100 / 100 | 100/100 = 100.0% | 0/100 = 0.0% | +100.0 points | [+94.8 pts, +100.0 pts] | Fisher's exact | <0.0001 | 0.0083 | <0.0001 | passes Holm |
| F2 | No facility information: told vs not told | blind | Unsupported facility claim (any pick) | 100 / 100 | 21/100 = 21.0% | 0/100 = 0.0% | +21.0 points | [+13.2 pts, +30.0 pts] | Fisher's exact | <0.0001 | 0.0125 | <0.0001 | passes Holm |
| F3 | No facility information: told vs not told | Deaf | Unsupported facility claim (any pick) | 100 / 100 | 13/100 = 13.0% | 0/100 = 0.0% | +13.0 points | [+6.6 pts, +21.0 pts] | Fisher's exact | 0.0002 | 0.0250 | 0.0003 | passes Holm |
| F4 | Told: no facility information (E2T) vs facilities shown (A, Study 1) | wheelchair | Unsupported facility claim (any pick) | 100 / 100 | 100/100 = 100.0% | 0/100 = 0.0% | +100.0 points | [+94.8 pts, +100.0 pts] | Fisher's exact | <0.0001 | 0.0100 | <0.0001 | passes Holm |
| F5 | Told: no facility information (E2T) vs facilities shown (A, Study 1) | blind | Unsupported facility claim (any pick) | 100 / 100 | 21/100 = 21.0% | 0/100 = 0.0% | +21.0 points | [+13.2 pts, +30.0 pts] | Fisher's exact | <0.0001 | 0.0167 | <0.0001 | passes Holm |
| F6 | Told: no facility information (E2T) vs facilities shown (A, Study 1) | Deaf | Unsupported facility claim (any pick) | 100 / 100 | 13/100 = 13.0% | 3/100 = 3.0% | +10.0 points | [+2.4 pts, +18.2 pts] | Fisher's exact | 0.0165 | 0.0500 | 0.0165 | passes Holm |

### Facility claims in every group (descriptive; Study 1 groups scored with the same rule)

| Group |  | Traveller | Answers | With any facility claim | With an unsupported claim | With a false claim |
| --- | --- | --- | --- | --- | --- | --- |
| B | Study 1: not told, all places | all | 100 | 14.0% | 0.0% | 0.0% |
| A | Study 1: told, all places | wheelchair | 100 | 100.0% | 0.0% | 0.0% |
| A | Study 1: told, all places | blind | 100 | 100.0% | 0.0% | 0.0% |
| A | Study 1: told, all places | Deaf | 100 | 100.0% | 3.0% | 3.0% |
| C | Study 1: filter, not told | wheelchair | 100 | 6.0% | 0.0% | 0.0% |
| C | Study 1: filter, not told | blind | 100 | 13.0% | 0.0% | 0.0% |
| C | Study 1: filter, not told | Deaf | 100 | 8.0% | 0.0% | 0.0% |
| E1N | E1: not told, fully usable places only | wheelchair | 100 | 7.0% | 0.0% | 0.0% |
| E1N | E1: not told, fully usable places only | blind | 100 | 9.0% | 0.0% | 0.0% |
| E1N | E1: not told, fully usable places only | Deaf | 100 | 10.0% | 0.0% | 0.0% |
| E1T | E1: told, fully usable places only | wheelchair | 100 | 100.0% | 0.0% | 0.0% |
| E1T | E1: told, fully usable places only | blind | 100 | 100.0% | 0.0% | 0.0% |
| E1T | E1: told, fully usable places only | Deaf | 100 | 100.0% | 1.0% | 1.0% |
| E2N | E2: not told, no facility information | all | 100 | 0.0% | 0.0% | 0.0% |
| E2T | E2: told, no facility information | wheelchair | 100 | 100.0% | 100.0% | 21.0% |
| E2T | E2: told, no facility information | blind | 100 | 21.0% | 21.0% | 12.0% |
| E2T | E2: told, no facility information | Deaf | 100 | 13.0% | 13.0% | 3.0% |
