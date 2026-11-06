# SW350 G04: Study 2 (E1 and E2)

- **E1, every place suits her:** ChatGPT sees only places that are fully usable for that traveller (facilities
  shown). Told vs not told. If the kinds of place change when she says "I'm blind", accessibility cannot be
  the reason.
- **E2, no facility information:** all 144 places without the "Facilities:" sentence. Told vs not told.
  ChatGPT has to assume.

1,000 requests, about 50 minutes, about $9 (estimate). The plan is `PLAN_E.md`. Your Study 1 and group D
folders are not used and not touched.

## Before you start

1. **Credit:** on the OpenAI usage page, check you have at least $12 left.
2. **Approval:** in the Analysis Plan doc, fill the Study 2 approval line (name, date and time) **before** the
   run.
3. **Laptop:** charger in; sleep set to "Never" while it runs (as for Study 1).

## Steps (Windows, VS Code terminal)

1. Unzip `SW350_G04_study2.zip` into `Documents`. In VS Code: File > Open Folder > the `SW350_G04_study2`
   folder where you can see `run_e.py` (open the inner one if there are two). Terminal > New Terminal, then
   check: `dir run_e.py`
2. Offline checks (no internet, no key, no cost):

   ```
   python test_study2.py
   ```

   Expected last line: `36 passed, 0 failed`.
3. Check the plan:

   ```
   python run_e.py --check
   ```

   Expected: `Plan: 1000 requests {'E1T': 300, 'E2N': 100, 'E1N': 300, 'E2T': 300}` and
   `Places in E1's lists (fully usable only): {'mobility': 72, 'visual': 72, 'hearing': 72}`.
4. Put the key in this terminal (never in a file, never to Claude), then `cls`:

   ```
   $env:OPENAI_API_KEY = "paste-the-key-here"
   ```

5. The run:

   ```
   python run_e.py --run
   ```

   Expected: `0 done, 1000 to send, with 3 at a time. Model: gpt-6.1-sol`, then `[1/1000]` up to
   `[1000/1000]`, and `Total: 1000/1000`. If it stops (internet, credit), run the same command again: it
   continues and never sends a request twice.
6. Score, then analyse:

   ```
   python score_e.py
   python analyse_e.py
   ```

   Expected: `Scored 1000 Study 2 answers -> 1200 rows`, then the nine main results (S1 to S9).
7. Open `results_E\REPORT_E.md` (`Ctrl+Shift+V`). Back up the whole folder, then send Claude `results_E`
   (zipped), `run_E\study2_started.txt` and `run_E\answers.jsonl`.

## If something goes wrong

| Message | What to do |
| --- | --- |
| `OPENAI_API_KEY is not set in this terminal` | Do step 4 again in this terminal |
| `NO CREDIT LEFT` | Add credit, then `python run_e.py --run` again |
| `STOP: ... is not the frozen version` | Use the folder exactly as unzipped |
| `STOP: answers do not match the Study 2 plan` | The run is not finished: `python run_e.py --run` again |
| Anything else | Run `cls`, then send Claude a screenshot (no key on screen) |

## Rules

- Whether Study 2 goes in the Phase 3 paper or stays a pilot is decided with Dr. Eman; wherever it is reported,
  all nine main results are reported, whatever they show.
- Do not change any file after the run starts. The interpretation is written by the team.
