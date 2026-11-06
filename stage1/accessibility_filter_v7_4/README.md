# Accessibility pre-filter v7.4 (SW350, Group 4), frozen 28 Oct 2026

**What it is:** plain Python code (no AI) that decides, for each of 144 **made-up** places in Riyadh and each of three travellers (wheelchair user, blind, Deaf), whether she can get in and do the main activity. It decides **eligibility, not preference**: ChatGPT later chooses among the places that are left.

**Version:** v7.4, 28 Oct 2026 (frozen; see `filter_output/rules_frozen.txt`).
- The decision logic has not changed since v6.
- v7 changed only the data (the facility swap, see below).
- v7.1 fixed the files around the code after a team review:
  - the sources now match the team documents, with printed page numbers;
  - the freeze also fingerprints the data;
  - real-data checks were added;
  - the swap can be reproduced;
  - this README was rewritten.
- v7.2 changed five descriptions (no time or loaded words: P066, P068, P071, P094, P143), added word and length checks, and marked the B1 and D1 sources as checked (quotes checked against the PDFs; approved by Alanoud). 
- v7.3 removed the district: the column is gone, the district phrase was taken out of every description, and six places whose names contained a real area were renamed (`data/renames.csv`). ChatGPT therefore decides from the listed information only, without a district's reputation.
- v7.4 (after the final data review) renamed 12 more places whose names were real, well-known places (for example Wadi Namar, Tuwaiq, Rawdat Al Khafs, the Red Sand Dunes) or real Riyadh districts (Al Ghadir, Al Hamra), and changed two description phrases that pointed to a real place (`data/renames.csv`, `swap_record/rename_real_names.py`). Region and city names that describe a style or cuisine (Najd, Najdi, Hail, Riyadh) are kept. Then the rules and the data were frozen.

## The three pieces (they never mix)

| Piece | File | Example |
|---|---|---|
| 1. The person's needs (15 rules, each with published sources) | `filter.py` (`RULES`) | B1: a blind traveller needs a non-visual way to experience a place whose main thing is seen |
| 2. The activity's demands (per category) | `categories.csv` | `history_museum`: indoor, visitors move around, main thing is seen = yes, heard = no |
| 3. The place's facilities (23 yes/no columns per place) | `places.csv` | `audio_guide = no`, `entrance_ramp = yes` |

**How one rule is checked:**
1. Does it apply here, and how strongly? This uses piece 2 and gives Essential, Important, or not applicable.
2. Is it met? This uses piece 3: the rule passes if **any** of its listed facilities is `yes`.

**The worst result wins:**
- any Essential rule fails → `EXCLUDED`;
- otherwise, any Important rule fails → `ELIGIBLE_WITH_CAVEATS` ("usable with a gap");
- otherwise → `ELIGIBLE` ("fully usable").

**Layer 1 (the kind of place)** follows the UN CRPD (2006) Art. 30 and the UNWTO (2013) Recommendations on Accessible Tourism: is the main thing **seen** (`visual_content`) or **heard** (`spoken_content`)?
- B1 is Essential only where the main thing is seen.
- D1 is Essential only where the main thing is heard.

So a blind traveller is never excluded from a park, market, mall or restaurant because of sight. She is excluded from a museum only if **that** museum offers nothing non-visual.

**The full rules table** with every source is generated from the code: `filter_output/rules_table.md`.
- Page numbers are **printed** page numbers.
- Gavurova & Polishchuk (2025) pp.429–432; Müller et al. (2022) article 13, pages 13:N; Theodorou et al. p.1636; Indrashwara et al. pp.192, 195.

## Results on the real data

| Traveller | Fully usable | Usable with a gap | Excluded | Places sent to ChatGPT in condition C |
|---|---|---|---|---|
| Wheelchair user | 72 | 24 | 48 | 96 |
| Blind | 72 | 52 | 20 | 124 |
| Deaf | 72 | 60 | 12 | 132 |

Rule failures: W1 22, W2 9, W3 1, W4 6, W5 1, W6 9, W7 39, W8 12, B1 20, B2 46, B3 27, D1 12, D2 27, D3 5, D4 28.

## Files

| File | What it is |
|---|---|
| `filter.py` | The rules, the decision logic, the outputs and `--freeze` |
| `categories.csv` | The 12 categories: setting, movement, main thing seen, main thing heard |
| `places.csv` | The final 144 places: name, category, price, opening hours, visit duration, walking distance, the 2-sentence description, 23 facility columns, `old_id` (no district) |
| `test_filter.py` | 35 hard-case tests of the decision logic on made-up test places |
| `test_real_data.py` | 11 checks on the real data: 144 places, 12 per category; the totals above; 0 mismatches with the plan; the rule failure counts; realism rules; price and distance balanced; every description 2 sentences; no forbidden words (whole words); time words only where they are the activity (listed by place ID); description length does not follow the verdict (inside each category); no district column or district names |
| `data/plan.csv` | The planned result for every place and traveller, with reasons. The facilities were generated from this plan |
| `data/descriptions_final.csv` | The final descriptions (Claude Sonnet 5.5, then checked and edited by hand; edits, including the district removal, are in the generation log) |
| `data/renames.csv` | The 18 renamed places (6 in v7.3, 12 in v7.4): old name, new name, version and reason |
| `filter_output/` | Generated, never edited by hand: `decisions.csv` (432 rows), `report.md`, `rules_table.md`, `truth_table.md` |
| `swap_record/` | Everything needed to repeat the facility swap (below) |

## How to run (from this folder)

```
python test_filter.py         # 35 logic tests
python test_real_data.py      # 11 real-data checks
python filter.py              # writes filter_output/
python filter.py --freeze     # writes filter_output/rules_frozen.txt
```

`--freeze` refuses to run while any rule's source is not marked as checked. All 15 are checked, and the freeze was run on 28 Oct 2026.

When it runs, `rules_frozen.txt` records the date and the SHA-256 fingerprints of `filter.py`, `places.csv` and `categories.csv`. Any later change to the rules or the data then leaves a trace.

## The facility swap (v7)

A check showed that, by chance, excluded places were sometimes pricier or farther away than usable places in the same category. ChatGPT could then avoid them for the wrong reason.

**What we did:**
- Moved whole facility rows (all 23 columns) between places of the **same** category.
- Every count per category and traveller stays identical.
- The six example places in the team documents did not move (P001, P009, P027, P034, P045, P046).
- Result: the largest gap between excluded and usable places fell from 131 SAR and 257 m to 22 SAR and 35 m.

**To repeat it:**
```
python swap_record/find_assignment.py    # seeded search (seed 20261028); confirms it reproduces assignment.json
python swap_record/rebuild_places.py     # v6 places + assignment + renames + descriptions, district removed -> confirms identical to places.csv
```

`swap_record/remove_districts.py` (v7.3) and `swap_record/rename_real_names.py` (v7.4) are the record of how the district phrase was removed and which names were changed; both re-run to identical files.

Remaining small differences (reported as internal threats): in `traditional_market`, excluded places for wheelchair users are open longer (12.8 h vs 8.8 h); in `desert_experience`, their visits are shorter (6.1 h vs 7.8 h).

Description length: inside each category, excluded and usable places differ by at most 4 words. Across all places, excluded places for the blind traveller are about 1.2 words shorter on average (24.6 vs 25.75), and this comes from which categories they fall in (if every place had its category's average length, the gap would be 1.4 words); the test prints these overall gaps and the paper reports them.

## What ChatGPT sees

ChatGPT never sees the yes/no columns, the categories file or the filter's results. For each place it sees:
- place_id, name, category, price, opening hours, visit duration and walking distance (no district);
- the 2-sentence description followed by one **Facilities sentence**, written by code from the yes/no columns. It lists only the facilities marked yes, and leaves out "paved paths" for indoor places.

So the information is the same as the yes/no columns, written the way a tourism website would write it (UNWTO 2013, p.6).

## AI use (to be declared)

- The places and descriptions were generated with Claude Sonnet 5.5.
- This code was written with Claude's help and checked by the team.
- A team review of v7 was produced with Claude.
- All of this is listed in the AI-use declaration.
