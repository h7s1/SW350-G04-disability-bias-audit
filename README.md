# SW350 Group 4: Disability disclosure and an accessibility filter in LLM tourism recommendations for Riyadh

Code and data for the SW350 Phase 3 paper (Princess Nourah bint Abdulrahman University, first semester 2026-2027).

The study sent tourism recommendation requests for Riyadh to OpenAI's gpt-6.1-sol through the Responses API and scored every answer with a rule-based accessibility filter. All requests were sent on 29 October 2026 (Riyadh time).

## Folders

| Folder | Contents |
|---|---|
| `stage1/` | Stage 1, groups A, B and C (700 requests): code, the request plan, all 700 answers (`run/answers.jsonl`), and results (`results/`). |
| `group_d/` | Group D (300 requests), added after the results of groups A, B and C: code, plan (`PLAN_D.md`), the request plan, all 300 answers (`run_D/answers.jsonl`), and results (`results_D/`). |
| `stage2/` | Stage 2, follow-up experiments E1 and E2 (1,000 requests): code, plan (`PLAN_E.md`, `PLAN_E_addendum.md`), the request plan, all 1,000 answers (`run_E/answers.jsonl`), and results (`results_E/`). |

Each folder is self-contained and has its own copy of `accessibility_filter_v7_4/` (the filter, the 144 places, the 12 categories, the rules and the filter's decisions). The three copies are identical.

## Data

- The 144 places are fictional, so the data contains no personal information.
- `accessibility_filter_v7_4/places.csv`: the places and their 23 accessibility facilities.
- `accessibility_filter_v7_4/filter_output/decisions.csv`: the filter's decision for every place and traveller.
- `accessibility_filter_v7_4/swap_record/`: the data before the facility swap and the code that produced the swap (Section 3.2 of the paper).
- `places_as_chatgpt_sees_them.csv`: the place information exactly as the model received it.

## Running the code

- Python 3.14.4, with `pip install openai==2.31.0 scipy`.
- The API key is read from the `OPENAI_API_KEY` environment variable. It is never written in the code or in any file here.
- Run instructions: `stage1/README_RUN.md`, `group_d/README_D.md`, `stage2/README_E.md`.
- All three folders can be rescored and reanalysed from the files here without calling the API: Stage 1 with `score_answers.py`, then `analyse.py`; group D with `score_d.py`, then `analyse_d.py`; Stage 2 with `score_e.py`, then `analyse_e.py`.

## Notes

- `stage2/` also contains the outputs of a fabrication check (`fabrication.py`, `E_fabrication_*.csv`, `fabrication_claims_E.csv`, `study1/fabrication_study1.csv`) that is not reported in the paper.

## License

- Code (`.py` files): MIT License, see `LICENSE`.
- Data (`.csv`, `.jsonl` and `.txt` files): Creative Commons Attribution 4.0 International (CC BY 4.0).
