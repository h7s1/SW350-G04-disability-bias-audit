# SW350 G04: group D results (numbers only)

Group D was added on 29 October 2026, after Study 1's results (PLAN_D.md): the filtered list of C and the disability sentence of A. It was run on a different date from A, B and C. A, B and C are Study 1's scores, unchanged. Holm is applied to the six D results only; Study 1's nine main results are not changed. The interpretation is written by the team.

## D0. The D run

| Item | Value |
| --- | --- |
| Answers | 300 |
| Model(s) returned | gpt-6.1-sol (300) |
| First request sent / last answer received | 2026-10-29T03:44:26+03:00 / 2026-10-29T04:01:45+03:00 |
| Re-sends after a technical error | 0 |
| Answers with a format problem | 0 |
| Answers with fewer or more than 5 picks | 0 |
| Invalid picks | 0 |
| Tokens | input 6,045,840 (cached 4,825,280, written to cache 1,219,660); output 167,420 (reasoning 37,659) |

## All four groups at a glance (percentages and means; descriptive)

A = told, all places; B = not told, all places (scored for each traveller); C = not told, filtered; D = told, filtered (added later). Measure 2 here is the planned automatic count (see Study 1's check of the flagged sentences).

| Traveller | Group | Answers | Main outcome yes | Accessibility | Fully suitable | Budget | Interest | Diversity | Measure 1 | Measure 2 yes (automatic rule) | Measure 3 yes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wheelchair | A | 100 | 33.0% | 4.55 | 4.46 | 5.00 | 5.00 | 2.19 | 2.52 | 6.0% | 100.0% |
| wheelchair | B | 100 | 89.0% | 3.26 | 2.81 | 5.00 | 5.00 | 2.23 | 1.72 | 0.0% | 0.0% |
| wheelchair | C | 100 | 0.0% | 5.00 | 4.16 | 5.00 | 4.94 | 2.26 | 3.08 | 0.0% | 0.0% |
| wheelchair | D (added later) | 100 | 0.0% | 5.00 | 4.76 | 5.00 | 4.98 | 2.21 | 2.60 | 24.0% | 95.0% |
| blind | A | 100 | 1.0% | 4.99 | 4.34 | 5.00 | 4.93 | 2.26 | 3.15 | 13.0% | 56.0% |
| blind | B | 100 | 40.0% | 4.28 | 2.49 | 5.00 | 5.00 | 2.23 | 1.48 | 0.0% | 0.0% |
| blind | C | 100 | 0.0% | 5.00 | 2.96 | 5.00 | 4.99 | 2.26 | 2.58 | 0.0% | 0.0% |
| blind | D (added later) | 100 | 0.0% | 5.00 | 4.42 | 5.00 | 4.89 | 2.30 | 3.13 | 18.0% | 59.0% |
| Deaf | A | 100 | 3.0% | 4.97 | 3.82 | 5.00 | 4.98 | 2.18 | 1.30 | 8.0% | 63.0% |
| Deaf | B | 100 | 31.0% | 4.52 | 2.79 | 5.00 | 5.00 | 2.23 | 0.57 | 0.0% | 0.0% |
| Deaf | C | 100 | 0.0% | 5.00 | 3.18 | 5.00 | 5.00 | 2.25 | 1.50 | 0.0% | 0.0% |
| Deaf | D (added later) | 100 | 0.0% | 5.00 | 3.80 | 5.00 | 4.98 | 2.17 | 1.32 | 5.0% | 73.0% |

## The six D results (added later; Holm over these six, at 0.05)

D vs C: does telling ChatGPT the disability help when the list is already filtered? D vs A: does the filter help when ChatGPT is told?

| # | Comparison | Traveller | Outcome | Answers | First group | Second group | Difference (first - second) | 95% interval | Test | p | Holm threshold (6 tests) | Holm-adjusted p | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | D vs C | wheelchair | Fully suitable score | 100 / 100 | mean 4.76, median 5 | mean 4.16, median 4 | +0.60 | [+0.44, +0.77] | Mann-Whitney U | <0.0001 | 0.0100 | <0.0001 | passes Holm |
| D2 | D vs C | blind | Fully suitable score | 100 / 100 | mean 4.42, median 4 | mean 2.96, median 3 | +1.46 | [+1.23, +1.68] | Mann-Whitney U | <0.0001 | 0.0083 | <0.0001 | passes Holm |
| D3 | D vs C | Deaf | Fully suitable score | 100 / 100 | mean 3.80, median 4 | mean 3.18, median 3 | +0.62 | [+0.43, +0.81] | Mann-Whitney U | <0.0001 | 0.0125 | <0.0001 | passes Holm |
| D4 | D vs A | wheelchair | Fully suitable score | 100 / 100 | mean 4.76, median 5 | mean 4.46, median 5 | +0.30 | [+0.14, +0.48] | Mann-Whitney U | 0.0053 | 0.0167 | 0.0160 | passes Holm |
| D5 | D vs A | blind | Fully suitable score | 100 / 100 | mean 4.42, median 4 | mean 4.34, median 4 | +0.08 | [-0.10, +0.25] | Mann-Whitney U | 0.4272 | 0.0250 | 0.8545 | does not pass Holm |
| D6 | D vs A | Deaf | Fully suitable score | 100 / 100 | mean 3.80, median 4 | mean 3.82, median 4 | -0.02 | [-0.18, +0.14] | Mann-Whitney U | 0.9608 | 0.0500 | 0.9608 | does not pass Holm |

## D secondary results (uncorrected p-values)

| Comparison | Traveller | Measure | Answers | First group | Second group | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D vs C | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| D vs C | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| D vs C | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 0/100 = 0.0% | +0.0 points | [-3.7 pts, +3.7 pts] | Fisher's exact | 1.0000 |
| D vs C | wheelchair | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | blind | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | Deaf | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | wheelchair | Interest | 100 / 100 | mean 4.98, median 5 | mean 4.94, median 5 | +0.04 | [-0.01, +0.09] | Mann-Whitney U | 0.1510 |
| D vs C | blind | Interest | 100 / 100 | mean 4.89, median 5 | mean 4.99, median 5 | -0.10 | [-0.18, -0.03] | Mann-Whitney U | 0.0054 |
| D vs C | Deaf | Interest | 100 / 100 | mean 4.98, median 5 | mean 5.00, median 5 | -0.02 | [-0.05, +0.00] | Mann-Whitney U | 0.1583 |
| D vs C | wheelchair | Diversity | 100 / 100 | mean 2.21, median 2 | mean 2.26, median 2 | -0.05 | [-0.28, +0.17] | Mann-Whitney U | 0.7759 |
| D vs C | blind | Diversity | 100 / 100 | mean 2.30, median 2 | mean 2.26, median 2 | +0.04 | [-0.17, +0.26] | Mann-Whitney U | 0.6352 |
| D vs C | Deaf | Diversity | 100 / 100 | mean 2.17, median 2 | mean 2.25, median 2 | -0.08 | [-0.31, +0.15] | Mann-Whitney U | 0.5528 |
| D vs C | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs C | wheelchair | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 2.60, median 3 | mean 3.08, median 3 | -0.48 | [-0.72, -0.27] | Mann-Whitney U | <0.0001 |
| D vs C | blind | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 3.13, median 3 | mean 2.58, median 2 | +0.55 | [-0.05, +1.10] | Mann-Whitney U | 0.0120 |
| D vs C | Deaf | Measure 1: suitable picks in her stereotype categories | 40 / 40 | mean 1.32, median 1.5 | mean 1.50, median 1.5 | -0.18 | [-0.48, +0.10] | Mann-Whitney U | 0.4558 |
| D vs C | wheelchair | Measure 2: invented facility | 100 / 100 | 24/100 = 24.0% | 0/100 = 0.0% | +24.0 points | [+15.8 pts, +33.2 pts] | Fisher's exact | <0.0001 |
| D vs C | blind | Measure 2: invented facility | 100 / 100 | 18/100 = 18.0% | 0/100 = 0.0% | +18.0 points | [+10.7 pts, +26.7 pts] | Fisher's exact | <0.0001 |
| D vs C | Deaf | Measure 2: invented facility | 100 / 100 | 5/100 = 5.0% | 0/100 = 0.0% | +5.0 points | [+0.3 pts, +11.2 pts] | Fisher's exact | 0.0594 |
| D vs A | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 33/100 = 33.0% | -33.0 points | [-42.7 pts, -23.8 pts] | Fisher's exact | <0.0001 |
| D vs A | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 1/100 = 1.0% | -1.0 points | [-5.4 pts, +2.8 pts] | Fisher's exact | 1.0000 |
| D vs A | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 0/100 = 0.0% | 3/100 = 3.0% | -3.0 points | [-8.5 pts, +1.2 pts] | Fisher's exact | 0.2462 |
| D vs A | wheelchair | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 4.55, median 5 | +0.45 | [+0.32, +0.59] | Mann-Whitney U | <0.0001 |
| D vs A | blind | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 4.99, median 5 | +0.01 | [+0.00, +0.03] | Mann-Whitney U | 0.3222 |
| D vs A | Deaf | Accessibility score | 100 / 100 | mean 5.00, median 5 | mean 4.97, median 5 | +0.03 | [+0.00, +0.07] | Mann-Whitney U | 0.0827 |
| D vs A | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | wheelchair | Interest | 100 / 100 | mean 4.98, median 5 | mean 5.00, median 5 | -0.02 | [-0.05, +0.00] | Mann-Whitney U | 0.1583 |
| D vs A | blind | Interest | 100 / 100 | mean 4.89, median 5 | mean 4.93, median 5 | -0.04 | [-0.12, +0.04] | Mann-Whitney U | 0.4391 |
| D vs A | Deaf | Interest | 100 / 100 | mean 4.98, median 5 | mean 4.98, median 5 | +0.00 | [-0.04, +0.04] | Mann-Whitney U | 1.0000 |
| D vs A | wheelchair | Diversity | 100 / 100 | mean 2.21, median 2 | mean 2.19, median 2 | +0.02 | [-0.19, +0.24] | Mann-Whitney U | 0.9000 |
| D vs A | blind | Diversity | 100 / 100 | mean 2.30, median 2 | mean 2.26, median 2 | +0.04 | [-0.14, +0.22] | Mann-Whitney U | 0.7165 |
| D vs A | Deaf | Diversity | 100 / 100 | mean 2.17, median 2 | mean 2.18, median 2 | -0.01 | [-0.22, +0.20] | Mann-Whitney U | 0.8257 |
| D vs A | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| D vs A | wheelchair | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 2.60, median 3 | mean 2.52, median 3 | +0.08 | [-0.18, +0.35] | Mann-Whitney U | 0.6358 |
| D vs A | blind | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 3.13, median 3 | mean 3.15, median 3 | -0.02 | [-0.53, +0.52] | Mann-Whitney U | 0.9935 |
| D vs A | Deaf | Measure 1: suitable picks in her stereotype categories | 40 / 40 | mean 1.32, median 1.5 | mean 1.30, median 1 | +0.02 | [-0.30, +0.33] | Mann-Whitney U | 0.7607 |
| D vs A | wheelchair | Measure 2: invented facility | 100 / 100 | 24/100 = 24.0% | 6/100 = 6.0% | +18.0 points | [+8.2 pts, +27.8 pts] | Fisher's exact | 0.0006 |
| D vs A | blind | Measure 2: invented facility | 100 / 100 | 18/100 = 18.0% | 13/100 = 13.0% | +5.0 points | [-5.2 pts, +15.1 pts] | Fisher's exact | 0.4349 |
| D vs A | Deaf | Measure 2: invented facility | 100 / 100 | 5/100 = 5.0% | 8/100 = 8.0% | -3.0 points | [-10.6 pts, +4.3 pts] | Fisher's exact | 0.5679 |

## Measures 2 and 3 in D (descriptive)

| Traveller | Answers | Measure 2: answers flagged (automatic rule) | Measure 2: picks flagged | Measure 3: answers mentioning a disability word | 95% interval (Wilson) |
| --- | --- | --- | --- | --- | --- |
| wheelchair | 100 | 24 | 24 | 95/100 = 95.0% | [88.8%, 97.8%] |
| blind | 100 | 18 | 18 | 59/100 = 59.0% | [49.2%, 68.1%] |
| Deaf | 100 | 5 | 5 | 73/100 = 73.0% | [63.6%, 80.7%] |

Every flagged sentence is in measure2_flagged_sentences_D.csv, to be read by the team as in Study 1.

## D per interest (20 answers per cell, no tests)

| Group | Traveller | Interest | Answers | Main outcome yes | Accessibility | Fully suitable | Budget | Interest | Diversity | Invalid | Measure 1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D | wheelchair | history | 20 | 0.0% | 5.00 | 4.85 | 5.00 | 4.90 | 3.10 | 0.00 | 2.80 |
| D | wheelchair | art | 20 | 0.0% | 5.00 | 5.00 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| D | wheelchair | nature | 20 | 0.0% | 5.00 | 5.00 | 5.00 | 5.00 | 3.00 | 0.00 | 3.10 |
| D | wheelchair | shopping | 20 | 0.0% | 5.00 | 4.95 | 5.00 | 5.00 | 1.95 | 0.00 | 1.90 |
| D | wheelchair | food | 20 | 0.0% | 5.00 | 4.00 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| D | blind | history | 20 | 0.0% | 5.00 | 5.00 | 5.00 | 5.00 | 3.00 | 0.00 | 2.80 |
| D | blind | art | 20 | 0.0% | 5.00 | 3.90 | 5.00 | 5.00 | 2.00 | 0.00 | 5.00 |
| D | blind | nature | 20 | 0.0% | 5.00 | 4.05 | 5.00 | 5.00 | 3.00 | 0.00 | 1.60 |
| D | blind | shopping | 20 | 0.0% | 5.00 | 4.85 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| D | blind | food | 20 | 0.0% | 5.00 | 4.30 | 5.00 | 4.45 | 1.50 | 0.00 | - |
| D | Deaf | history | 20 | 0.0% | 5.00 | 4.15 | 5.00 | 5.00 | 2.65 | 0.00 | 0.65 |
| D | Deaf | art | 20 | 0.0% | 5.00 | 3.95 | 5.00 | 5.00 | 2.00 | 0.00 | 2.00 |
| D | Deaf | nature | 20 | 0.0% | 5.00 | 3.55 | 5.00 | 5.00 | 3.15 | 0.00 | - |
| D | Deaf | shopping | 20 | 0.0% | 5.00 | 3.65 | 5.00 | 5.00 | 1.95 | 0.00 | - |
| D | Deaf | food | 20 | 0.0% | 5.00 | 3.70 | 5.00 | 4.90 | 1.10 | 0.00 | - |

## Rules broken among the valid picks: A, C and D (descriptive)

**wheelchair**

| Group | Traveller | Valid picks | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | wheelchair | 500 | 9 | 36 | 0 | 0 | 0 | 0 | 5 | 4 |
| C | wheelchair | 500 | 0 | 0 | 0 | 0 | 0 | 0 | 38 | 46 |
| D | wheelchair | 500 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 22 |

**blind**

| Group | Traveller | Valid picks | B1 | B2 | B3 |
| --- | --- | --- | --- | --- | --- |
| A | blind | 500 | 1 | 55 | 32 |
| C | blind | 500 | 0 | 188 | 93 |
| D | blind | 500 | 0 | 52 | 28 |

**Deaf**

| Group | Traveller | Valid picks | D1 | D2 | D3 | D4 |
| --- | --- | --- | --- | --- | --- | --- |
| A | Deaf | 500 | 3 | 79 | 4 | 32 |
| C | Deaf | 500 | 0 | 70 | 0 | 112 |
| D | Deaf | 500 | 0 | 73 | 8 | 39 |

## Kinds of place: A, C and D (share of valid picks; descriptive)

| Group | Traveller | Valid picks | history_museum | art_gallery | heritage_site | guided_heritage_tour | park_garden | desert_experience | nature_reserve | observation_deck | traditional_market | shopping_mall | restaurant_cafe | live_show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | wheelchair | 500 | 8.4% | 11.2% | 7.8% | 3.8% | 6.0% | 0.0% | 6.8% | 7.2% | 8.2% | 11.8% | 20.0% | 8.8% |
| A | blind | 500 | 11.0% | 12.4% | 5.2% | 3.8% | 8.8% | 0.0% | 4.2% | 7.0% | 14.6% | 6.8% | 18.6% | 7.6% |
| A | Deaf | 500 | 8.2% | 12.0% | 8.6% | 3.0% | 4.4% | 0.2% | 8.0% | 7.4% | 10.0% | 10.4% | 19.8% | 8.0% |
| C | wheelchair | 500 | 7.0% | 11.2% | 7.6% | 4.2% | 5.4% | 0.0% | 7.6% | 7.0% | 12.2% | 9.0% | 20.0% | 8.8% |
| C | blind | 500 | 6.6% | 12.0% | 9.4% | 4.0% | 4.8% | 1.4% | 9.4% | 4.4% | 12.0% | 8.2% | 19.8% | 8.0% |
| C | Deaf | 500 | 6.2% | 12.0% | 9.8% | 4.0% | 4.0% | 1.4% | 8.6% | 6.0% | 12.0% | 8.0% | 20.0% | 8.0% |
| D | wheelchair | 500 | 8.8% | 11.6% | 6.8% | 4.0% | 8.0% | 0.0% | 4.4% | 7.6% | 8.0% | 12.4% | 20.0% | 8.4% |
| D | blind | 500 | 11.2% | 12.4% | 4.8% | 4.0% | 9.0% | 0.0% | 4.6% | 6.4% | 15.2% | 7.0% | 17.8% | 7.6% |
| D | Deaf | 500 | 8.8% | 12.0% | 8.6% | 2.6% | 5.6% | 0.6% | 7.4% | 6.4% | 9.6% | 10.8% | 19.6% | 8.0% |

## Sensitivity check: the six D results without invalid picks

| # | Comparison | Traveller | Version | Answers | First group | Second group | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | D vs C | wheelchair | answers with no invalid pick only | 100 / 100 | mean 4.76, median 5 | mean 4.16, median 4 | +0.60 | [+0.44, +0.77] | Mann-Whitney U | <0.0001 |
| D2 | D vs C | blind | answers with no invalid pick only | 100 / 100 | mean 4.42, median 4 | mean 2.96, median 3 | +1.46 | [+1.23, +1.68] | Mann-Whitney U | <0.0001 |
| D3 | D vs C | Deaf | answers with no invalid pick only | 100 / 100 | mean 3.80, median 4 | mean 3.18, median 3 | +0.62 | [+0.43, +0.81] | Mann-Whitney U | <0.0001 |
| D4 | D vs A | wheelchair | answers with no invalid pick only | 100 / 100 | mean 4.76, median 5 | mean 4.46, median 5 | +0.30 | [+0.14, +0.48] | Mann-Whitney U | 0.0053 |
| D5 | D vs A | blind | answers with no invalid pick only | 100 / 100 | mean 4.42, median 4 | mean 4.34, median 4 | +0.08 | [-0.10, +0.25] | Mann-Whitney U | 0.4272 |
| D6 | D vs A | Deaf | answers with no invalid pick only | 100 / 100 | mean 3.80, median 4 | mean 3.82, median 4 | -0.02 | [-0.18, +0.14] | Mann-Whitney U | 0.9608 |
