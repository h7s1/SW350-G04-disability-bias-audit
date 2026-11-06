# SW350 G04: group D (added after Study 1)

Group D = the filtered list of C + the disability sentence of A ("I'm blind." etc.).
300 requests, about 15 to 20 minutes, about $5 (estimate; check your credit first).
The plan for D is `PLAN_D.md`. Your Study 1 folder is not used and not touched: this folder has its own copy
of the frozen code, and Study 1's scores (`study1\scores_per_answer.csv`, checked by its fingerprint).

## Before you start

1. **Credit:** on the OpenAI usage page, check you have at least $10 left.
2. **Approval:** in the Analysis Plan doc, fill the group D approval line (name, date and time) **before**
   the run. This time the approval really is before the run.

## Steps (Windows, VS Code terminal)

1. Unzip `SW350_G04_groupD.zip` into `Documents` (not inside the Study 1 folder).
   In VS Code: File > Open Folder > the `SW350_G04_groupD` folder where you can see `run_d.py` (Windows may
   put one `SW350_G04_groupD` folder inside another; open the inner one). Then Terminal > New Terminal, and
   check with `dir run_d.py` that the file is there.
2. Offline checks (no internet, no key, no cost):

   ```
   python test_groupd.py
   ```

   Expected last line: `35 passed, 0 failed`. Any `FAIL`: stop and send a screenshot.
3. Check the plan:

   ```
   python run_d.py --check
   ```

   Expected: `Plan: 300 requests {'D': 300} -> run_D/plan_requests.csv`, then the first request, with the
   disability sentence in it (for example "I use a wheelchair.").
4. Put the key in this terminal (same as for Study 1; never in a file, never to Claude):

   ```
   $env:OPENAI_API_KEY = "paste-the-key-here"
   ```

   Then type `cls` to clear the screen.
5. The run:

   ```
   python run_d.py --run
   ```

   Expected: `0 done, 300 to send, with 3 at a time. Model: gpt-6.1-sol`, then lines `[1/300] ...` up to
   `[300/300] ...`, and at the end `Total: 300/300`. If it stops (internet, credit), run the same command
   again: it continues where it stopped and never sends a request twice.
6. Score the answers:

   ```
   python score_d.py
   ```

   Expected first line: `Scored 300 D answers -> 300 rows.`
7. The results:

   ```
   python analyse_d.py
   ```

   It prints the six D results (D1 to D3: D vs C; D4 to D6: D vs A).
8. Open `results_D\REPORT_D.md` and press `Ctrl+Shift+V`.
9. Back up the whole `SW350_G04_groupD` folder (a copy, plus the team Drive), and send Claude:
   `results_D` (zipped) and `run_D\groupD_started.txt`.

## What comes out

| File | What is in it |
| --- | --- |
| `run_D\answers.jsonl` | The 300 answers, exactly as they came back (never open in Excel or Notepad and save) |
| `run_D\groupD_started.txt` | When the D run started, and the fingerprints of the files that decide what is sent |
| `results_D\REPORT_D.md` | Every D table on one page |
| `results_D\overview_ABCD.csv` | All four groups side by side, per traveller (descriptive) |
| `results_D\D_results.csv` | The six D results, with Holm over the six |
| `results_D\D_secondary.csv` | D vs C and D vs A on every other measure (uncorrected) |
| `results_D\D_measures_2_3.csv`, `measure2_flagged_sentences_D.csv`, `measure3_mentions_D.csv` | Measures 2 and 3 for D |
| `results_D\D_per_interest.csv`, `D_rules_broken_*.csv`, `D_kinds_of_place.csv`, `D_sensitivity.csv` | The other tables |

## If something goes wrong

| Message | What to do |
| --- | --- |
| `OPENAI_API_KEY is not set in this terminal` | Do step 4 again in this terminal |
| `NO CREDIT LEFT` | Add credit, then `python run_d.py --run` again |
| `STOP: ... is not the frozen version` | Use the folder exactly as unzipped |
| `STOP: answers do not match the D plan` | The run is not finished: `python run_d.py --run` again |
| Anything else | Run `cls`, then send Claude a screenshot (no key on screen) |

## Rules

- D is reported as a group added after Study 1's results, in Methods and in every table where it appears.
- Study 1's nine main results do not change and stay the main results.
- Do not change any file after the D run starts. The interpretation is written by the team.
