# SW350 G04: results (numbers only)

Produced by analyse.py from results/scores_per_answer.csv, exactly as the analysis plan v2.1 says. A = disability disclosed, all places; B = no disability disclosed, all places (scored for each disability); C = filter-first. The interpretation is written by the team.

## R0. The run

| Item | Value |
| --- | --- |
| Answers | 700 (A 300, B 100, C 300) |
| Model(s) returned | gpt-6.1-sol (700) |
| First request sent / last answer received | 2026-10-29T00:54:51+03:00 / 2026-10-29T01:29:27+03:00 |
| Re-sends after a technical error | 0 |
| Answers with a format problem | 0 |
| Answers with fewer or more than 5 picks | 0 |
| Invalid picks in all answers | 0 |
| Tokens | input 15,894,160 (cached 14,139,963, written to cache 1,752,097); output 325,342 (reasoning 58,052) |

## The nine main results (Holm over these nine, at 0.05)

| # | RQ | Comparison | Disability | Outcome | Answers | First group | Second group | Difference (first - second) | 95% interval | Test | p | Holm threshold | Holm-adjusted p | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RQ1 | A vs B | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 33/100 = 33.0% | 89/100 = 89.0% | -56.0 points | [-65.7 pts, -43.7 pts] | Fisher's exact | <0.0001 | 0.0063 | <0.0001 | passes Holm |
| 2 | RQ1 | A vs B | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 1/100 = 1.0% | 40/100 = 40.0% | -39.0 points | [-48.8 pts, -28.9 pts] | Fisher's exact | <0.0001 | 0.0071 | <0.0001 | passes Holm |
| 3 | RQ1 | A vs B | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 3/100 = 3.0% | 31/100 = 31.0% | -28.0 points | [-37.8 pts, -18.1 pts] | Fisher's exact | <0.0001 | 0.0125 | <0.0001 | passes Holm |
| 4 | RQ4 | A vs C | wheelchair | Fully suitable score | 100 / 100 | mean 4.46, median 5 | mean 4.16, median 4 | +0.30 | [+0.10, +0.51] | Mann-Whitney U | 0.0020 | 0.0500 | 0.0020 | passes Holm |
| 5 | RQ4 | A vs C | blind | Fully suitable score | 100 / 100 | mean 4.34, median 4 | mean 2.96, median 3 | +1.38 | [+1.15, +1.61] | Mann-Whitney U | <0.0001 | 0.0056 | <0.0001 | passes Holm |
| 6 | RQ4 | A vs C | Deaf | Fully suitable score | 100 / 100 | mean 3.82, median 4 | mean 3.18, median 3 | +0.64 | [+0.45, +0.84] | Mann-Whitney U | <0.0001 | 0.0083 | <0.0001 | passes Holm |
| 7 | RQ2 | A vs B | wheelchair | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 2.52, median 3 | mean 1.72, median 2 | +0.80 | [+0.48, +1.13] | Mann-Whitney U | <0.0001 | 0.0250 | <0.0001 | passes Holm |
| 8 | RQ2 | A vs B | blind | Measure 1: suitable picks in her stereotype categories | 60 / 60 | mean 3.15, median 3 | mean 1.48, median 2 | +1.67 | [+1.20, +2.12] | Mann-Whitney U | <0.0001 | 0.0100 | <0.0001 | passes Holm |
| 9 | RQ2 | A vs B | Deaf | Measure 1: suitable picks in her stereotype categories | 40 / 40 | mean 1.30, median 1 | mean 0.57, median 1 | +0.73 | [+0.47, +0.97] | Mann-Whitney U | <0.0001 | 0.0167 | <0.0001 | passes Holm |

Holm: the p-values are sorted from smallest; the smallest must be below 0.05/9, the next below 0.05/8, and so on; testing stops at the first that is not. Intervals: Newcombe for differences in percentages; percentile bootstrap (2,000 resamples, seed 20261028) for differences in means.

## Results 1 to 3, split (always reported)

| Disability | Condition | Answers | Main outcome yes | With an unusable place | With an invalid pick | With both |
| --- | --- | --- | --- | --- | --- | --- |
| wheelchair | A | 100 | 33 | 33 | 0 | 0 |
| wheelchair | B | 100 | 89 | 89 | 0 | 0 |
| blind | A | 100 | 1 | 1 | 0 | 0 |
| blind | B | 100 | 40 | 40 | 0 | 0 |
| Deaf | A | 100 | 3 | 3 | 0 | 0 |
| Deaf | B | 100 | 31 | 31 | 0 | 0 |

## RQ3: the filter (descriptive)

| Disability | Fully usable | Usable with a gap | Excluded | Sent in C |
| --- | --- | --- | --- | --- |
| wheelchair | 72 | 24 | 48 | 96 |
| blind | 72 | 52 | 20 | 124 |
| Deaf | 72 | 60 | 12 | 132 |

Rule failures over the 144 places: B1 20, B2 46, B3 27, D1 12, D2 27, D3 5, D4 28, W1 22, W2 9, W3 1, W4 6, W5 1, W6 9, W7 39, W8 12

## Secondary results (uncorrected p-values; labelled secondary in the paper)

| Comparison | Disability | Measure | Answers | First group | Second group | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A vs B | wheelchair | Accessibility score | 100 / 100 | mean 4.55, median 5 | mean 3.26, median 3 | +1.29 | [+1.05, +1.51] | Mann-Whitney U | <0.0001 |
| A vs B | blind | Accessibility score | 100 / 100 | mean 4.99, median 5 | mean 4.28, median 5 | +0.71 | [+0.51, +0.91] | Mann-Whitney U | <0.0001 |
| A vs B | Deaf | Accessibility score | 100 / 100 | mean 4.97, median 5 | mean 4.52, median 5 | +0.45 | [+0.30, +0.60] | Mann-Whitney U | <0.0001 |
| A vs B | wheelchair | Fully suitable score | 100 / 100 | mean 4.46, median 5 | mean 2.81, median 3 | +1.65 | [+1.39, +1.89] | Mann-Whitney U | <0.0001 |
| A vs B | blind | Fully suitable score | 100 / 100 | mean 4.34, median 4 | mean 2.49, median 3 | +1.85 | [+1.60, +2.11] | Mann-Whitney U | <0.0001 |
| A vs B | Deaf | Fully suitable score | 100 / 100 | mean 3.82, median 4 | mean 2.79, median 3 | +1.03 | [+0.85, +1.21] | Mann-Whitney U | <0.0001 |
| A vs B | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | wheelchair | Interest | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | blind | Interest | 100 / 100 | mean 4.93, median 5 | mean 5.00, median 5 | -0.07 | [-0.12, -0.02] | Mann-Whitney U | 0.0073 |
| A vs B | Deaf | Interest | 100 / 100 | mean 4.98, median 5 | mean 5.00, median 5 | -0.02 | [-0.05, +0.00] | Mann-Whitney U | 0.1583 |
| A vs B | wheelchair | Diversity | 100 / 100 | mean 2.19, median 2 | mean 2.23, median 2 | -0.04 | [-0.26, +0.18] | Mann-Whitney U | 0.7975 |
| A vs B | blind | Diversity | 100 / 100 | mean 2.26, median 2 | mean 2.23, median 2 | +0.03 | [-0.17, +0.24] | Mann-Whitney U | 0.7693 |
| A vs B | Deaf | Diversity | 100 / 100 | mean 2.18, median 2 | mean 2.23, median 2 | -0.05 | [-0.26, +0.16] | Mann-Whitney U | 0.6683 |
| A vs B | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 89/100 = 89.0% | 0/100 = 0.0% | +89.0 points | [+80.5 pts, +93.7 pts] | Fisher's exact | <0.0001 |
| B vs C | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 40/100 = 40.0% | 0/100 = 0.0% | +40.0 points | [+30.2 pts, +49.8 pts] | Fisher's exact | <0.0001 |
| B vs C | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 31/100 = 31.0% | 0/100 = 0.0% | +31.0 points | [+22.0 pts, +40.6 pts] | Fisher's exact | <0.0001 |
| B vs C | wheelchair | Accessibility score | 100 / 100 | mean 3.26, median 3 | mean 5.00, median 5 | -1.74 | [-1.94, -1.55] | Mann-Whitney U | <0.0001 |
| B vs C | blind | Accessibility score | 100 / 100 | mean 4.28, median 5 | mean 5.00, median 5 | -0.72 | [-0.92, -0.53] | Mann-Whitney U | <0.0001 |
| B vs C | Deaf | Accessibility score | 100 / 100 | mean 4.52, median 5 | mean 5.00, median 5 | -0.48 | [-0.63, -0.33] | Mann-Whitney U | <0.0001 |
| B vs C | wheelchair | Fully suitable score | 100 / 100 | mean 2.81, median 3 | mean 4.16, median 4 | -1.35 | [-1.59, -1.09] | Mann-Whitney U | <0.0001 |
| B vs C | blind | Fully suitable score | 100 / 100 | mean 2.49, median 3 | mean 2.96, median 3 | -0.47 | [-0.77, -0.17] | Mann-Whitney U | 0.0028 |
| B vs C | Deaf | Fully suitable score | 100 / 100 | mean 2.79, median 3 | mean 3.18, median 3 | -0.39 | [-0.60, -0.17] | Mann-Whitney U | 0.0002 |
| B vs C | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | wheelchair | Interest | 100 / 100 | mean 5.00, median 5 | mean 4.94, median 5 | +0.06 | [+0.02, +0.11] | Mann-Whitney U | 0.0133 |
| B vs C | blind | Interest | 100 / 100 | mean 5.00, median 5 | mean 4.99, median 5 | +0.01 | [+0.00, +0.03] | Mann-Whitney U | 0.3222 |
| B vs C | Deaf | Interest | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | wheelchair | Diversity | 100 / 100 | mean 2.23, median 2 | mean 2.26, median 2 | -0.03 | [-0.25, +0.20] | Mann-Whitney U | 0.8771 |
| B vs C | blind | Diversity | 100 / 100 | mean 2.23, median 2 | mean 2.26, median 2 | -0.03 | [-0.25, +0.20] | Mann-Whitney U | 0.8771 |
| B vs C | Deaf | Diversity | 100 / 100 | mean 2.23, median 2 | mean 2.25, median 2 | -0.02 | [-0.25, +0.21] | Mann-Whitney U | 0.9948 |
| B vs C | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| B vs C | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | wheelchair | Main outcome (unusable or invalid pick) | 100 / 100 | 33/100 = 33.0% | 0/100 = 0.0% | +33.0 points | [+23.8 pts, +42.7 pts] | Fisher's exact | <0.0001 |
| A vs C | blind | Main outcome (unusable or invalid pick) | 100 / 100 | 1/100 = 1.0% | 0/100 = 0.0% | +1.0 points | [-2.8 pts, +5.4 pts] | Fisher's exact | 1.0000 |
| A vs C | Deaf | Main outcome (unusable or invalid pick) | 100 / 100 | 3/100 = 3.0% | 0/100 = 0.0% | +3.0 points | [-1.2 pts, +8.5 pts] | Fisher's exact | 0.2462 |
| A vs C | wheelchair | Accessibility score | 100 / 100 | mean 4.55, median 5 | mean 5.00, median 5 | -0.45 | [-0.59, -0.32] | Mann-Whitney U | <0.0001 |
| A vs C | blind | Accessibility score | 100 / 100 | mean 4.99, median 5 | mean 5.00, median 5 | -0.01 | [-0.03, +0.00] | Mann-Whitney U | 0.3222 |
| A vs C | Deaf | Accessibility score | 100 / 100 | mean 4.97, median 5 | mean 5.00, median 5 | -0.03 | [-0.07, +0.00] | Mann-Whitney U | 0.0827 |
| A vs C | wheelchair | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | blind | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | Deaf | Budget | 100 / 100 | mean 5.00, median 5 | mean 5.00, median 5 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | wheelchair | Interest | 100 / 100 | mean 5.00, median 5 | mean 4.94, median 5 | +0.06 | [+0.02, +0.11] | Mann-Whitney U | 0.0133 |
| A vs C | blind | Interest | 100 / 100 | mean 4.93, median 5 | mean 4.99, median 5 | -0.06 | [-0.12, -0.01] | Mann-Whitney U | 0.0311 |
| A vs C | Deaf | Interest | 100 / 100 | mean 4.98, median 5 | mean 5.00, median 5 | -0.02 | [-0.05, +0.00] | Mann-Whitney U | 0.1583 |
| A vs C | wheelchair | Diversity | 100 / 100 | mean 2.19, median 2 | mean 2.26, median 2 | -0.07 | [-0.30, +0.14] | Mann-Whitney U | 0.6830 |
| A vs C | blind | Diversity | 100 / 100 | mean 2.26, median 2 | mean 2.26, median 2 | +0.00 | [-0.21, +0.21] | Mann-Whitney U | 0.8901 |
| A vs C | Deaf | Diversity | 100 / 100 | mean 2.18, median 2 | mean 2.25, median 2 | -0.07 | [-0.30, +0.15] | Mann-Whitney U | 0.6845 |
| A vs C | wheelchair | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | blind | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs C | Deaf | Invalid picks | 100 / 100 | mean 0.00, median 0 | mean 0.00, median 0 | +0.00 | [+0.00, +0.00] | Mann-Whitney U | 1.0000 |
| A vs B | wheelchair | Measure 2: invented facility | 100 / 100 | 6/100 = 6.0% | 0/100 = 0.0% | +6.0 points | [+1.1 pts, +12.5 pts] | Fisher's exact | 0.0289 |
| A vs B | blind | Measure 2: invented facility | 100 / 100 | 13/100 = 13.0% | 0/100 = 0.0% | +13.0 points | [+6.6 pts, +21.0 pts] | Fisher's exact | 0.0002 |
| A vs B | Deaf | Measure 2: invented facility | 100 / 100 | 8/100 = 8.0% | 0/100 = 0.0% | +8.0 points | [+2.6 pts, +15.0 pts] | Fisher's exact | 0.0068 |
| A vs C | wheelchair | Measure 2: invented facility | 100 / 100 | 6/100 = 6.0% | 0/100 = 0.0% | +6.0 points | [+1.1 pts, +12.5 pts] | Fisher's exact | 0.0289 |
| A vs C | blind | Measure 2: invented facility | 100 / 100 | 13/100 = 13.0% | 0/100 = 0.0% | +13.0 points | [+6.6 pts, +21.0 pts] | Fisher's exact | 0.0002 |
| A vs C | Deaf | Measure 2: invented facility | 100 / 100 | 8/100 = 8.0% | 0/100 = 0.0% | +8.0 points | [+2.6 pts, +15.0 pts] | Fisher's exact | 0.0068 |

## Measure 3: answers that mention a disability word (descriptive)

| Condition | Disability told | Answers mentioning | Share | 95% interval (Wilson) |
| --- | --- | --- | --- | --- |
| A | wheelchair | 100/100 | 100.0% | [96.3%, 100.0%] |
| A | blind | 56/100 | 56.0% | [46.2%, 65.3%] |
| A | Deaf | 63/100 | 63.0% | [53.2%, 71.8%] |
| B | all (same 100 answers) | 0/100 | 0.0% | [0.0%, 3.7%] |
| C | wheelchair | 0/100 | 0.0% | [0.0%, 3.7%] |
| C | blind | 0/100 | 0.0% | [0.0%, 3.7%] |
| C | Deaf | 0/100 | 0.0% | [0.0%, 3.7%] |

Quoted examples: results/measure3_mentions.csv. Measure 2 flagged sentences: results/measure2_flagged_sentences.csv.

## Per interest (percentages and means only; 20 answers per cell, no tests)

| Condition | Scored for | Interest | Answers | Main outcome yes | Accessibility | Fully suitable | Budget | Interest | Diversity | Invalid | Measure 1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | wheelchair | history | 20 | 25.0% | 4.60 | 4.30 | 5.00 | 5.00 | 2.95 | 0.00 | 2.50 |
| A | wheelchair | art | 20 | 20.0% | 4.80 | 4.75 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| A | wheelchair | nature | 20 | 0.0% | 5.00 | 5.00 | 5.00 | 5.00 | 3.00 | 0.00 | 3.20 |
| A | wheelchair | shopping | 20 | 20.0% | 4.80 | 4.80 | 5.00 | 5.00 | 2.00 | 0.00 | 1.85 |
| A | wheelchair | food | 20 | 100.0% | 3.55 | 3.45 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| A | blind | history | 20 | 0.0% | 5.00 | 5.00 | 5.00 | 5.00 | 2.95 | 0.00 | 2.75 |
| A | blind | art | 20 | 5.0% | 4.95 | 3.85 | 5.00 | 5.00 | 2.00 | 0.00 | 4.95 |
| A | blind | nature | 20 | 0.0% | 5.00 | 3.75 | 5.00 | 5.00 | 3.00 | 0.00 | 1.75 |
| A | blind | shopping | 20 | 0.0% | 5.00 | 4.85 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| A | blind | food | 20 | 0.0% | 5.00 | 4.25 | 5.00 | 4.65 | 1.35 | 0.00 | - |
| A | Deaf | history | 20 | 0.0% | 5.00 | 4.00 | 5.00 | 4.95 | 2.80 | 0.00 | 0.75 |
| A | Deaf | art | 20 | 15.0% | 4.85 | 3.75 | 5.00 | 5.00 | 2.00 | 0.00 | 1.85 |
| A | Deaf | nature | 20 | 0.0% | 5.00 | 3.70 | 5.00 | 5.00 | 3.05 | 0.00 | - |
| A | Deaf | shopping | 20 | 0.0% | 5.00 | 3.80 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| A | Deaf | food | 20 | 0.0% | 5.00 | 3.85 | 5.00 | 4.95 | 1.05 | 0.00 | - |
| B | wheelchair | history | 20 | 100.0% | 2.00 | 1.50 | 5.00 | 5.00 | 3.00 | 0.00 | 0.90 |
| B | wheelchair | art | 20 | 100.0% | 3.15 | 3.05 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| B | wheelchair | nature | 20 | 90.0% | 3.45 | 3.20 | 5.00 | 5.00 | 3.15 | 0.00 | 2.05 |
| B | wheelchair | shopping | 20 | 55.0% | 4.30 | 3.75 | 5.00 | 5.00 | 2.00 | 0.00 | 2.20 |
| B | wheelchair | food | 20 | 100.0% | 3.40 | 2.55 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| B | blind | history | 20 | 0.0% | 5.00 | 3.45 | 5.00 | 5.00 | 3.00 | 0.00 | 1.65 |
| B | blind | art | 20 | 100.0% | 2.70 | 1.00 | 5.00 | 5.00 | 2.00 | 0.00 | 2.70 |
| B | blind | nature | 20 | 100.0% | 3.70 | 1.85 | 5.00 | 5.00 | 3.15 | 0.00 | 0.10 |
| B | blind | shopping | 20 | 0.0% | 5.00 | 3.15 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| B | blind | food | 20 | 0.0% | 5.00 | 3.00 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| B | Deaf | history | 20 | 55.0% | 4.45 | 3.20 | 5.00 | 5.00 | 3.00 | 0.00 | 0.45 |
| B | Deaf | art | 20 | 100.0% | 3.15 | 2.40 | 5.00 | 5.00 | 2.00 | 0.00 | 0.70 |
| B | Deaf | nature | 20 | 0.0% | 5.00 | 3.05 | 5.00 | 5.00 | 3.15 | 0.00 | - |
| B | Deaf | shopping | 20 | 0.0% | 5.00 | 2.30 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| B | Deaf | food | 20 | 0.0% | 5.00 | 3.00 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| C | wheelchair | history | 20 | 0.0% | 5.00 | 3.15 | 5.00 | 4.70 | 3.30 | 0.00 | 3.25 |
| C | wheelchair | art | 20 | 0.0% | 5.00 | 4.80 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| C | wheelchair | nature | 20 | 0.0% | 5.00 | 4.40 | 5.00 | 5.00 | 3.00 | 0.00 | 3.25 |
| C | wheelchair | shopping | 20 | 0.0% | 5.00 | 4.45 | 5.00 | 5.00 | 2.00 | 0.00 | 2.75 |
| C | wheelchair | food | 20 | 0.0% | 5.00 | 4.00 | 5.00 | 5.00 | 1.00 | 0.00 | - |
| C | blind | history | 20 | 0.0% | 5.00 | 3.70 | 5.00 | 5.00 | 3.00 | 0.00 | 1.65 |
| C | blind | art | 20 | 0.0% | 5.00 | 2.10 | 5.00 | 5.00 | 2.00 | 0.00 | 5.00 |
| C | blind | nature | 20 | 0.0% | 5.00 | 2.50 | 5.00 | 5.00 | 3.30 | 0.00 | 1.10 |
| C | blind | shopping | 20 | 0.0% | 5.00 | 3.15 | 5.00 | 5.00 | 1.95 | 0.00 | - |
| C | blind | food | 20 | 0.0% | 5.00 | 3.35 | 5.00 | 4.95 | 1.05 | 0.00 | - |
| C | Deaf | history | 20 | 0.0% | 5.00 | 3.40 | 5.00 | 5.00 | 3.00 | 0.00 | 1.00 |
| C | Deaf | art | 20 | 0.0% | 5.00 | 3.90 | 5.00 | 5.00 | 2.00 | 0.00 | 2.00 |
| C | Deaf | nature | 20 | 0.0% | 5.00 | 3.05 | 5.00 | 5.00 | 3.25 | 0.00 | - |
| C | Deaf | shopping | 20 | 0.0% | 5.00 | 2.25 | 5.00 | 5.00 | 2.00 | 0.00 | - |
| C | Deaf | food | 20 | 0.0% | 5.00 | 3.30 | 5.00 | 5.00 | 1.00 | 0.00 | - |

## Measure 2: invented facilities, counts (descriptive; the tests are in the secondary table)

| Condition | Disability told | Answers | Answers with an invented facility | Picks with one | Mean picks per answer |
| --- | --- | --- | --- | --- | --- |
| A | wheelchair | 100 | 6 | 6 | 0.06 |
| A | blind | 100 | 13 | 13 | 0.13 |
| A | Deaf | 100 | 8 | 8 | 0.08 |
| B | all (same 100 answers) | 100 | 0 | 0 | 0.00 |
| C | wheelchair | 100 | 0 | 0 | 0.00 |
| C | blind | 100 | 0 | 0 | 0.00 |
| C | Deaf | 100 | 0 | 0 | 0.00 |

## Rules broken among the valid picks (descriptive)

How many valid picks fail each rule for that traveller (Essential and Important failures together).

**wheelchair**

| Condition | Scored for | Valid picks | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | wheelchair | 500 | 9 | 36 | 0 | 0 | 0 | 0 | 5 | 4 |
| B | wheelchair | 500 | 55 | 74 | 19 | 17 | 0 | 9 | 115 | 34 |
| C | wheelchair | 500 | 0 | 0 | 0 | 0 | 0 | 0 | 38 | 46 |

**blind**

| Condition | Scored for | Valid picks | B1 | B2 | B3 |
| --- | --- | --- | --- | --- | --- |
| A | blind | 500 | 1 | 55 | 32 |
| B | blind | 500 | 72 | 161 | 84 |
| C | blind | 500 | 0 | 188 | 93 |

**Deaf**

| Condition | Scored for | Valid picks | D1 | D2 | D3 | D4 |
| --- | --- | --- | --- | --- | --- | --- |
| A | Deaf | 500 | 3 | 79 | 4 | 32 |
| B | Deaf | 500 | 48 | 65 | 0 | 108 |
| C | Deaf | 500 | 0 | 70 | 0 | 112 |

## Kinds of place picked (share of valid picks; descriptive)

| Condition | Disability told | Valid picks | history_museum | art_gallery | heritage_site | guided_heritage_tour | park_garden | desert_experience | nature_reserve | observation_deck | traditional_market | shopping_mall | restaurant_cafe | live_show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | wheelchair | 500 | 8.4% | 11.2% | 7.8% | 3.8% | 6.0% | 0.0% | 6.8% | 7.2% | 8.2% | 11.8% | 20.0% | 8.8% |
| A | blind | 500 | 11.0% | 12.4% | 5.2% | 3.8% | 8.8% | 0.0% | 4.2% | 7.0% | 14.6% | 6.8% | 18.6% | 7.6% |
| A | Deaf | 500 | 8.2% | 12.0% | 8.6% | 3.0% | 4.4% | 0.2% | 8.0% | 7.4% | 10.0% | 10.4% | 19.8% | 8.0% |
| B | all | 500 | 6.6% | 9.8% | 9.4% | 4.0% | 4.8% | 0.8% | 8.8% | 5.6% | 11.6% | 8.4% | 20.0% | 10.2% |
| C | wheelchair | 500 | 7.0% | 11.2% | 7.6% | 4.2% | 5.4% | 0.0% | 7.6% | 7.0% | 12.2% | 9.0% | 20.0% | 8.8% |
| C | blind | 500 | 6.6% | 12.0% | 9.4% | 4.0% | 4.8% | 1.4% | 9.4% | 4.4% | 12.0% | 8.2% | 19.8% | 8.0% |
| C | Deaf | 500 | 6.2% | 12.0% | 9.8% | 4.0% | 4.0% | 1.4% | 8.6% | 6.0% | 12.0% | 8.0% | 20.0% | 8.0% |

## Sensitivity check: the nine main results without invalid picks (secondary)

| # | RQ | Comparison | Disability | Version | Answers | First group | Second group | Difference | 95% interval | Test | p (uncorrected) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | RQ1 | A vs B | wheelchair | main outcome counting unusable places only (invalid picks ignored) | 100 / 100 | 33/100 = 33.0% | 89/100 = 89.0% | -56.0 points | [-65.7 pts, -43.7 pts] | Fisher's exact | <0.0001 |
| 2 | RQ1 | A vs B | blind | main outcome counting unusable places only (invalid picks ignored) | 100 / 100 | 1/100 = 1.0% | 40/100 = 40.0% | -39.0 points | [-48.8 pts, -28.9 pts] | Fisher's exact | <0.0001 |
| 3 | RQ1 | A vs B | Deaf | main outcome counting unusable places only (invalid picks ignored) | 100 / 100 | 3/100 = 3.0% | 31/100 = 31.0% | -28.0 points | [-37.8 pts, -18.1 pts] | Fisher's exact | <0.0001 |
| 4 | RQ4 | A vs C | wheelchair | answers with no invalid pick only | 100 / 100 | mean 4.46, median 5 | mean 4.16, median 4 | +0.30 | [+0.10, +0.51] | Mann-Whitney U | 0.0020 |
| 5 | RQ4 | A vs C | blind | answers with no invalid pick only | 100 / 100 | mean 4.34, median 4 | mean 2.96, median 3 | +1.38 | [+1.15, +1.61] | Mann-Whitney U | <0.0001 |
| 6 | RQ4 | A vs C | Deaf | answers with no invalid pick only | 100 / 100 | mean 3.82, median 4 | mean 3.18, median 3 | +0.64 | [+0.45, +0.84] | Mann-Whitney U | <0.0001 |
| 7 | RQ2 | A vs B | wheelchair | answers with no invalid pick only | 60 / 60 | mean 2.52, median 3 | mean 1.72, median 2 | +0.80 | [+0.48, +1.13] | Mann-Whitney U | <0.0001 |
| 8 | RQ2 | A vs B | blind | answers with no invalid pick only | 60 / 60 | mean 3.15, median 3 | mean 1.48, median 2 | +1.67 | [+1.20, +2.12] | Mann-Whitney U | <0.0001 |
| 9 | RQ2 | A vs B | Deaf | answers with no invalid pick only | 40 / 40 | mean 1.30, median 1 | mean 0.57, median 1 | +0.73 | [+0.47, +0.97] | Mann-Whitney U | <0.0001 |
