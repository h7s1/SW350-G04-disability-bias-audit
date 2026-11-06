# SW350 G04: scoring and analysis (after the run)

Four new files (plus this README) go in the same folder as `run_requests.py` (your `SW350_G04_study_code_FINAL_v7_4` folder,
the one that has `run\answers.jsonl` in it):

| File | What it does |
| --- | --- |
| `score_answers.py` | Step 1. Scores every answer exactly as the analysis plan v2.1 says (sections 4 and 7). No statistics. |
| `analyse.py` | Step 2. The statistics in the plan: the nine main results with Holm, the secondary results, per interest, rules broken, kinds of place, Measures 2 and 3, the sensitivity check. |
| `test_scoring.py` | Checks both scripts on hand-made cases and on 700 fake answers. Never touches your real answers. |
| `scoring_frozen.txt` | The SHA-256 of the three scripts, recorded before they were run on the real answers. |

No internet and no API key are needed. Nothing here sends anything to OpenAI.

## Steps (Windows, VS Code terminal)

1. Unzip, then copy the 5 files (the four above and this README) into that folder, next to `run_requests.py`. Open the folder in VS Code, then Terminal > New Terminal.
2. Check you are in the right folder:

   ```
   dir run\answers.jsonl
   ```

   You should see the file (about 3.4 MB). If it says "File Not Found", you are in the wrong folder.
3. Check the scripts are the frozen versions:

   ```
   python -c "import hashlib;[print(f, hashlib.sha256(open(f,'rb').read()).hexdigest()) for f in ('score_answers.py','analyse.py','test_scoring.py')]"
   ```

   The three codes must be the same as in `scoring_frozen.txt`.
4. Run the tests (about 10 to 20 seconds):

   ```
   python test_scoring.py
   ```

   Expected last line: `76 passed, 0 failed`. Any `FAIL` line: stop and send me a screenshot.
5. Score the answers (a few seconds):

   ```
   python score_answers.py
   ```

   Expected first line: `Scored 700 answers -> 900 rows (B is scored for each of the 3 disabilities).`
   The second line gives the Measure 2 and Measure 3 counts.
6. Check your scores are exactly the ones I got (same code, same answers, so they must match):

   ```
   python -c "import hashlib;print(hashlib.sha256(open('results/scores_per_answer.csv','rb').read()).hexdigest())"
   ```

   Compare with the code in `scoring_frozen.txt` under "Expected scores file".
7. Run the statistics (under a minute):

   ```
   python analyse.py
   ```

   It prints the nine main results, one line each, ending in `passes Holm` or `does not pass Holm`.
8. Open `results\REPORT.md` in VS Code and press `Ctrl+Shift+V` to see it with tables.

## What comes out (in the new `results` folder)

| File | What is in it | Goes to |
| --- | --- | --- |
| `REPORT.md` | Every table below in one readable page | R0 to R5 of the paper |
| `scores_per_answer.csv` | One row per answer and disability (900 rows: A 300, C 300, B 100 x 3) | Code appendix; the data behind every number |
| `main_results.csv` | The nine main results: percentages or means, difference with 95% interval, p, Holm threshold, Holm-adjusted p, decision | Main results table |
| `main_outcome_split.csv` | Results 1 to 3 split into "has an unusable place" and "has an invalid pick" | Always reported next to results 1 to 3 (plan, section 9) |
| `secondary_results.csv` | Every other planned comparison, uncorrected p | Secondary results |
| `sensitivity.csv` | The nine main results without invalid picks | Sensitivity check |
| `per_interest.csv` | Percentages and means per interest, no tests | Secondary, descriptive |
| `rules_broken_wheelchair.csv`, `_blind.csv`, `_Deaf.csv` | How often each rule fails among the picks | "Which needs ChatGPT misses" (RQ1) |
| `kinds_of_place.csv` | Share of picks in each category | Deldjoo and Di Noia style comparison |
| `measure2_summary.csv` | Answers and picks with an invented facility | RQ2, secondary |
| `measure2_flagged_sentences.csv` | Every flagged phrase with the full reason | Appendix, so readers can check each one |
| `measure3_mentions_summary.csv` | Share of answers that mention a disability word, with 95% interval | RQ2, descriptive |
| `measure3_mentions.csv` | The reasons that mention one | Quoted examples |

Open the CSV files in Excel to read them if you like; do not save them from Excel. Never open
`run\answers.jsonl` in Excel or Notepad and save it.

## If something goes wrong

| Message | Meaning | What to do |
| --- | --- | --- |
| `Not found: ...answers.jsonl` | Wrong folder, or the run folder is missing | `cd` to the folder that has `run\answers.jsonl` |
| `STOP: answers do not match the plan` or `was not sent as planned` | `answers.jsonl` is not the original file | Use your backup copy; send me a screenshot |
| `STOP: filter.py is not the frozen version` | The filter files were changed | Use the original folder from the zip |
| `scipy is missing` / `No module named numpy` | A package is missing | `python -m pip install scipy` then run again |
| The `scores_per_answer.csv` code is different from mine | Something differs in the files | Do not use the results; send me a screenshot |

## Rules (from the analysis plan)

- Do not change any script, list or setting after seeing the results. If a real error is found, the fix is
  dated and reported in the paper as a deviation (plan, section 9), with both the old and new numbers.
- "Did not pass Holm" is written as "we did not find a clear difference", with the numbers, never "no bias".
- In C, the main outcome is met by design (the filter removed those places). Say so every time C is reported.
- The interpretation (Results text and Discussion) is written by the team.

## Details the plan left open, decided in the code

These were decided on 29 October 2026 while writing the scoring code, after the run and before any answer was
scored. Record them in the Daily Tracker and in the methodology (M9) as clarifications made before scoring.

1. Sensitivity check ("the nine main results without invalid picks"): for results 1 to 3, the main outcome
   counts unusable places only (an invalid pick no longer makes it "yes"); for results 4 to 9, only answers with
   no invalid pick are kept.
2. Matching: an ID is matched after removing spaces at either end and making letters upper case; a name is
   matched if it equals a listed place's name, ignoring spaces at either end and upper or lower case.
3. Intervals: difference in percentages, Newcombe's method (built from two Wilson intervals); Measure 3
   percentages, Wilson interval; difference in means, percentile bootstrap that resamples answers within each
   group (2,000 resamples, seed 20261028, the same seed for every comparison).
4. Mann-Whitney U: scipy's default two-sided test (with ties, the normal approximation with tie and continuity
   correction). If every value in both groups is the same, p = 1.
5. Measure 2: the 5-word negation window can reach into the previous sentence; a phrase type is counted once per
   pick even if it appears twice; curly apostrophes and Unicode hyphens are read as plain ones. The number of
   picks with an invented facility is reported as counts, without a test (the plan's test is on yes/no).
   Measure 2 tests are A vs B and A vs C only, as the plan says.
6. Measure 3: whole words, any case (so "deafening" is not a mention). B is reported once, because its 100
   answers are the same for every disability.
7. Rules broken counts Essential and Important failures among the valid picks. Kinds of place also shows C
   (descriptive), next to A and B as the plan says.
