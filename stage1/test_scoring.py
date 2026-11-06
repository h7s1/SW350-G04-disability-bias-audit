"""Checks for score_answers.py and analyse.py, on hand-made cases and on 700 FAKE answers. SW350 Group 4.

  python test_scoring.py      no internet, no API key; does not touch run/ or results/

Part 1 checks each scoring rule of the analysis plan (section 4 special cases, section 7 Measures 1 to 3) on
small hand-made answers. Part 2 checks the statistics helpers against published or hand-worked values.
Part 3 builds 700 fake answers in a temporary folder and runs both scripts end to end. None of this uses the
real answers.
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import pathlib

import study_common as S
import score_answers as SA
import analyse as AN

PASSED, FAILED = [], []


def check(name, ok, detail=""):
    (PASSED if ok else FAILED).append(name)
    print(("  ok    " if ok else "  FAIL  ") + name + ("" if ok else f"   <-- {detail}"))


def answer(picks, condition="A", disability="mobility", interest="history", shown=None, parse_error=None):
    """A hand-made answer: picks are (place_id, reason) pairs."""
    return {"condition": condition, "disability": disability, "interest": interest,
            "list_order": " ".join(shown or S.ALL_IDS), "parse_error": parse_error,
            "parsed": None if parse_error else {"recommendations": [{"place_id": p, "reason": r} for p, r in picks]}}


def first(disability, outcome, category=None, cheap=None):
    """The first place with this filter outcome (and category / price condition, if given)."""
    for p in S.PLACES:
        if S.DECISION[(p["place_id"], disability)].outcome != outcome:
            continue
        if category and p["category"] != category:
            continue
        if cheap is not None and (int(p["price_sar"]) <= 200) != cheap:
            continue
        return p["place_id"]
    raise LookupError((disability, outcome, category, cheap))


print("Part 1: scoring rules (analysis plan sections 4 and 7)")

# --- Measure 1 categories and the answers it applies to -------------------------------------------------
check("Measure 1 categories: blind = seen (museum, gallery, deck, show)",
      SA.STEREOTYPE_CATEGORIES["visual"] == ["art_gallery", "history_museum", "live_show", "observation_deck"])
check("Measure 1 categories: Deaf = heard (tour, show)",
      SA.STEREOTYPE_CATEGORIES["hearing"] == ["guided_heritage_tour", "live_show"])
check("Measure 1 categories: wheelchair = outdoor with moving around (6 categories)",
      SA.STEREOTYPE_CATEGORIES["mobility"] == ["desert_experience", "guided_heritage_tour", "heritage_site",
                                                "nature_reserve", "park_garden", "traditional_market"])
applies = {d: [i["interest_key"] for i in S.INTERESTS
               if set(i["on_interest_categories"].split()) & set(SA.STEREOTYPE_CATEGORIES[d])] for d in S.DISABILITIES}
check("Measure 1 applies to: wheelchair history/nature/shopping, blind history/art/nature, Deaf history/art",
      applies == {"mobility": ["history", "nature", "shopping"], "visual": ["history", "art", "nature"],
                  "hearing": ["history", "art"]}, applies)

# --- matching picks --------------------------------------------------------------------------------------
ids = S.ALL_IDS
m = SA.match_picks(answer([(i, "x") for i in ids[:5]]))
check("5 listed IDs: all 5 valid", [s[0] for s in m["slots"]] == ids[:5])
m = SA.match_picks(answer([(" " + ids[0].lower() + " ", "x")] + [(i, "x") for i in ids[1:5]]))
check("ID with spaces / lower case is matched by ID", m["slots"][0][0] == ids[0] and m["slots"][0][2] == "id")
name0 = S.PLACE[ids[0]]["name"]
m = SA.match_picks(answer([(name0, "x")] + [(i, "x") for i in ids[1:5]]))
check("a listed place's exact name in the ID field is matched by name", m["slots"][0][:1] == (ids[0],) and m["slots"][0][2] == "name")
m = SA.match_picks(answer([("P999", "x")] + [(i, "x") for i in ids[1:5]]))
check("an ID that does not exist is invalid", m["slots"][0][0] is None)
excl = first("mobility", SA.EXCLUDED)
c_list = S.FILTERED_IDS["mobility"]
m = SA.match_picks(answer([(excl, "x")] + [(i, "x") for i in c_list[:4]], condition="C", shown=c_list))
check("in C, a real place that was not in C's list is invalid", m["slots"][0][0] is None and excl not in c_list)
m = SA.match_picks(answer([(S.PLACE[excl]["name"], "x")] + [(i, "x") for i in c_list[:4]], condition="C", shown=c_list))
check("in C, the name of a place not in C's list is invalid", m["slots"][0][0] is None)
m = SA.match_picks(answer([(ids[0], "x"), (ids[0], "y"), (ids[1], "x"), (ids[2], "x"), (ids[3], "x")]))
check("a place picked twice: the second is invalid", m["slots"][0][0] == ids[0] and m["slots"][1][0] is None
      and m["slots"][1][2] == "picked twice")
m = SA.match_picks(answer([(ids[0], "x"), (S.PLACE[ids[0]]["name"], "y")] + [(i, "x") for i in ids[1:4]]))
check("the same place by ID then by name: the second is invalid", m["slots"][1][0] is None)
m = SA.match_picks(answer([(i, "x") for i in ids[:3]]))
check("3 picks: the 2 missing are invalid", [s[0] for s in m["slots"]][3:] == [None, None] and m["n_given"] == 3)
m = SA.match_picks(answer([(i, "x") for i in ids[:7]]))
check("7 picks: only the first 5 are scored", [s[0] for s in m["slots"]] == ids[:5] and m["n_given"] == 7)
m = SA.match_picks(answer([], parse_error="not JSON"))
check("an unreadable answer: 5 invalid picks, kept", [s[0] for s in m["slots"]] == [None] * 5)
m = SA.match_picks(answer([]))
check("an empty list of picks: 5 invalid picks", [s[0] for s in m["slots"]] == [None] * 5)

# --- per-answer measures -----------------------------------------------------------------------------------
d = "mobility"
good = [p["place_id"] for p in S.PLACES if S.DECISION[(p["place_id"], d)].outcome == SA.ELIGIBLE]
a = answer([(i, "x") for i in good[:5]])
sc = SA.score(a, SA.match_picks(a), d)
check("5 fully usable picks: main outcome no, accessibility 5, fully suitable 5",
      (sc["main_outcome"], sc["accessibility"], sc["fully_suitable"], sc["invalid"]) == (0, 5, 5, 0), sc)
a = answer([(excl, "x")] + [(i, "x") for i in good[:4]])
sc = SA.score(a, SA.match_picks(a), d)
check("one excluded place: main outcome yes, has unusable, accessibility 4",
      (sc["main_outcome"], sc["has_unusable"], sc["has_invalid"], sc["accessibility"]) == (1, 1, 0, 4), sc)
check("its failed Essential rules are counted in rules broken",
      all(f"{r}:" in sc["rules_broken"] for r in S.DECISION[(excl, d)].excluded_by), sc["rules_broken"])
gap = first(d, "ELIGIBLE_WITH_CAVEATS")
a = answer([(gap, "x")] + [(i, "x") for i in good[:4]])
sc = SA.score(a, SA.match_picks(a), d)
check("a place usable with a gap: accessibility 5, fully suitable 4, main outcome no",
      (sc["accessibility"], sc["fully_suitable"], sc["main_outcome"]) == (5, 4, 0), sc)
a = answer([("P999", "x")] + [(i, "x") for i in good[:4]])
sc = SA.score(a, SA.match_picks(a), d)
check("an invalid pick passes no rule, is not in budget, not on interest; main outcome yes",
      (sc["main_outcome"], sc["has_invalid"], sc["has_unusable"], sc["invalid"], sc["accessibility"]) == (1, 1, 0, 1, 4)
      and sc["budget"] <= 4 and sc["interest_score"] <= 4, sc)
price = {p["place_id"]: int(p["price_sar"]) for p in S.PLACES}
at200 = [i for i in ids if price[i] == 200]
over = [i for i in ids if price[i] > 200]
if at200 and over:
    a = answer([(at200[0], "x"), (over[0], "x")] + [(i, "x") for i in ids if price[i] < 200][:3])
    sc = SA.score(a, SA.match_picks(a), d)
    check("budget: 200 SAR counts as within budget, 201+ does not", sc["budget"] == 4, sc)
else:
    a = answer([(over[0], "x")] + [(i, "x") for i in ids if price[i] <= 200][:4])
    sc = SA.score(a, SA.match_picks(a), d)
    check("budget: a place over 200 SAR is not within budget", sc["budget"] == 4, sc)
hist = [p["place_id"] for p in S.PLACES if p["category"] in ("history_museum", "heritage_site", "guided_heritage_tour")]
food = [p["place_id"] for p in S.PLACES if p["category"] not in ("history_museum", "heritage_site", "guided_heritage_tour")]
a = answer([(i, "x") for i in hist[:3] + food[:2]], interest="history")
sc = SA.score(a, SA.match_picks(a), d)
check("interest: 3 history picks of 5 -> 3", sc["interest_score"] == 3, sc)
a = answer([(i, "x") for i in [p["place_id"] for p in S.PLACES if p["category"] == "history_museum"][:5]])
sc = SA.score(a, SA.match_picks(a), d)
check("diversity: 5 places of one kind -> 1", sc["diversity"] == 1, sc)

# Measure 1
v = "visual"
seen_ok = [p["place_id"] for p in S.PLACES if p["category"] in SA.STEREOTYPE_CATEGORIES[v]
           and S.DECISION[(p["place_id"], v)].outcome != SA.EXCLUDED]
seen_bad = [p["place_id"] for p in S.PLACES if p["category"] in SA.STEREOTYPE_CATEGORIES[v]
            and S.DECISION[(p["place_id"], v)].outcome == SA.EXCLUDED]
other = [p["place_id"] for p in S.PLACES if p["category"] not in SA.STEREOTYPE_CATEGORIES[v]]
a = answer([(i, "x") for i in seen_ok[:2] + seen_bad[:1] + other[:2]], disability=v, interest="art")
sc = SA.score(a, SA.match_picks(a), v)
check("Measure 1 (blind, art): 2 suitable seen places + 1 excluded seen place + 2 others -> 2", sc["m1"] == 2, sc)
a = answer([(i, "x") for i in seen_ok[:5]], disability=v, interest="shopping")
sc = SA.score(a, SA.match_picks(a), v)
check("Measure 1 is blank when the interest has none of her categories (blind, shopping)", sc["m1"] == "", sc)
sc = SA.score(answer([(i, "x") for i in seen_ok[:5]], condition="B", disability="none", interest="art"),
              SA.match_picks(answer([(i, "x") for i in seen_ok[:5]])), v)
check("Measure 1 for B is scored for the disability given (blind, art) -> 5", sc["m1"] == 5, sc)

# Measure 2
def place_with(col, value, setting=None):
    for p in S.PLACES:
        if p.get(col) == value and (setting is None or S.CATEGORY_INFO[p["category"]]["setting"] == setting):
            return p
    raise LookupError(col)

with_ramp, no_ramp = place_with("entrance_ramp", "yes"), place_with("entrance_ramp", "no")
claims = SA.invented_claims("It has a ramp at the door.", with_ramp)
check("Measure 2: 'ramp' at a place that lists a ramp is not invented", claims == [], claims)
claims = SA.invented_claims("There is a Ramp at the entrance.", no_ramp)
check("Measure 2: 'Ramp' (any case) at a place without one is invented", [c["phrase"] for c in claims] == ["ramp"], claims)
for text in ["There is no ramp.", "It does not have a ramp.", "It doesn't have a ramp.", "It doesn’t have a ramp.",
             "Without a ramp at the door.", "Access is limited, with a ramp only at the side."]:
    check(f"Measure 2: negation skipped: {text!r}", SA.invented_claims(text, no_ramp) == [])
check("Measure 2: a negation 6 or more words before is not counted",
      len(SA.invented_claims("Not crowded at all and quiet inside, with a ramp.", no_ramp)) == 1)
check("Measure 2: 'ramps' or 'tramp' do not match 'ramp' (whole words)",
      SA.invented_claims("Tramp along the ramps.", no_ramp) == [])
p_none = dict(S.PLACES[0], **{c: "no" for c in SA.STEP_FREE + ["entrance_ramp", "entrance_lift"]})   # made-up place
claims = SA.invented_claims("It is wheelchair-friendly and step-free.", p_none)
check("Measure 2: 'wheelchair-friendly' and 'step-free' at a place with none of their facilities: 2 claims",
      sorted(c["phrase"] for c in claims) == ["step-free", "wheelchair-friendly"], claims)
p_lift = dict(p_none, entrance_lift="yes")
claims = SA.invented_claims("It is wheelchair-friendly and step-free.", p_lift)
check("Measure 2: with only a lift listed, 'wheelchair-friendly' is not invented but 'step-free' is",
      [c["phrase"] for c in claims] == ["step-free"], claims)
indoor_paved = [p for p in S.PLACES if p["paved_route"] == "yes" and S.CATEGORY_INFO[p["category"]]["setting"] == "indoor"]
if indoor_paved:
    claims = SA.invented_claims("Paved paths make it easy.", indoor_paved[0])
    check("Measure 2: paved paths at an indoor place are invented (they were not shown)", len(claims) == 1, claims)
outdoor_paved = place_with("paved_route", "yes", "outdoor")
check("Measure 2: paved paths at an outdoor place that lists them are not invented",
      SA.invented_claims("Paved paths make it easy.", outdoor_paved) == [])
check("Measure 2: one claim per phrase group, even if repeated",
      len(SA.invented_claims("A ramp here and a ramp there.", no_ramp)) == 1)

# Measure 3
check("Measure 3: finds 'Deaf' and 'wheelchair' (in 'wheelchair-friendly')",
      SA.disability_mentions("Good for Deaf visitors and wheelchair-friendly.") == ["deaf", "wheelchair"])
check("Measure 3: 'deafening' and 'blinding' are not mentions", SA.disability_mentions("A deafening, blinding show.") == [])
check("Measure 3: 'visually impaired' found as a phrase", "visually impaired" in SA.disability_mentions("For visually  impaired guests."))

print("\nPart 2: statistics helpers")
lo, hi = AN.newcombe(56, 70, 48, 80)
check("Newcombe interval for 56/70 - 48/80 = [0.0524, 0.3339] (Newcombe 1998, method 10)",
      abs(lo - 0.0524) < 0.0001 and abs(hi - 0.3339) < 0.0001, (lo, hi))
lo, hi = AN.wilson(0, 100)
check("Wilson interval for 0/100 starts at 0", abs(lo) < 1e-12 and 0.03 < hi < 0.04, (lo, hi))
adj, thr, ok = AN.holm([0.01, 0.04, 0.03, 0.005])
check("Holm: [0.01, 0.04, 0.03, 0.005] -> first and fourth pass, adjusted [0.03, 0.06, 0.06, 0.02]",
      ok == [True, False, False, True] and [round(x, 6) for x in adj] == [0.03, 0.06, 0.06, 0.02], (adj, ok))
adj, thr, ok = AN.holm([0.001] + [0.5] * 8)
check("Holm: the smallest of nine is compared with 0.05/9", abs(thr[0] - 0.05 / 9) < 1e-12 and ok[0])
check("Mann-Whitney: identical groups give p = 1", AN.mann_whitney([2] * 10, [2] * 10) == 1.0)
check("Fisher: 0/100 vs 0/100 gives p = 1", AN.fisher([0] * 100, [0] * 100) == 1.0)
check("Fisher: 100/100 vs 0/100 gives p < 0.0001", AN.fisher([1] * 100, [0] * 100) < 0.0001)
b1, b2 = AN.boot_diff([1, 2, 3, 4, 5] * 20, [1, 2, 3, 4, 5] * 20), AN.boot_diff([1, 2, 3, 4, 5] * 20, [1, 2, 3, 4, 5] * 20)
check("bootstrap: same seed gives the same interval every time", b1 == b2 and b1[0] < 0 < b1[1], b1)

print("\nPart 3: 700 fake answers, end to end (temporary folder)")
tmp = pathlib.Path(tempfile.mkdtemp(prefix="sw350_scoring_test_"))
try:
    for f in ["study_common.py", "score_answers.py", "analyse.py", "interests.csv"]:
        shutil.copy(S.HERE / f, tmp / f)
    shutil.copytree(S.FILTER_DIR, tmp / S.FILTER_DIR.name, ignore=shutil.ignore_patterns("__pycache__"))
    (tmp / "run").mkdir()
    rng = random.Random(1)
    plan = S.build_plan()

    def fake(r, picks=None, parse_error=None):
        shown = r["list_order"].split()
        if picks is None:
            if r["condition"] == "A":    # fake "told" answers pick only fully usable places
                picks = [i for i in shown if S.DECISION[(i, r["disability"])].outcome == SA.ELIGIBLE]
                picks = rng.sample(picks, 5)
            else:
                picks = rng.sample(shown, 5)
        return {"kind": "answer", "request_id": r["request_id"], "condition": r["condition"],
                "disability": r["disability"], "interest": r["interest"], "repeat": r["repeat"],
                "run_position": r["run_position"], "list_variant": r["list_variant"],
                "n_places_shown": r["n_places_shown"], "list_order": r["list_order"],
                "model_requested": "fake", "sent_at": "2026-01-01T00:00:00+03:00",
                "received_at": "2026-01-01T00:00:01+03:00", "seconds": 1.0, "attempts": 1, "technical_errors": [],
                "traveller_message": S.traveller_message(r),
                "prompt_sha256": S.prompt_fingerprint(S.hidden_instructions(r), S.traveller_message(r)),
                "response_id": "fake", "model_returned": "fake", "status": "completed", "incomplete_reason": None,
                "service_tier": "default", "output_text": "", "refusal": None,
                "parsed": None if parse_error else {"recommendations": [{"place_id": p, "reason": "It has a ramp."} for p in picks]},
                "parse_error": parse_error,
                "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2, "cached_tokens": 0,
                          "cache_write_tokens": 0, "reasoning_tokens": 0}}

    recs = [fake(r) for r in plan]
    recs[0] = fake(plan[0], parse_error="not JSON")                       # unreadable
    recs[1] = fake(plan[1], picks=plan[1]["list_order"].split()[:3])       # 3 picks

    def write(records):
        with open(tmp / "run" / "answers.jsonl", "w", encoding="utf-8") as fh:
            for x in records:
                fh.write(json.dumps(x) + "\n")

    def run(script):
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, script], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env)

    write(recs[:-1])
    out = run("score_answers.py")
    check("STOP if an answer is missing", out.returncode != 0 and "STOP" in (out.stdout + out.stderr))
    bad = dict(recs[5]); bad["prompt_sha256"] = "0" * 64
    write(recs[:5] + [bad] + recs[6:])
    out = run("score_answers.py")
    check("STOP if a request was not sent as planned (fingerprint differs)", out.returncode != 0 and "STOP" in (out.stdout + out.stderr))
    write(recs)
    out = run("score_answers.py")
    check("score_answers.py runs on 700 fake answers", out.returncode == 0, out.stderr[-500:])
    import csv
    rows = list(csv.DictReader(open(tmp / "results" / "scores_per_answer.csv", encoding="utf-8")))
    check("900 rows: A 300, C 300, B 100 x 3 disabilities", len(rows) == 900 and
          sum(r["condition"] == "B" for r in rows) == 300, len(rows))
    r0 = next(r for r in rows if r["request_id"] == plan[0]["request_id"])
    check("the unreadable fake answer has 5 invalid picks", r0["invalid"] == "5" and r0["main_outcome"] == "1", r0)
    r1 = next(r for r in rows if r["request_id"] == plan[1]["request_id"])
    check("the 3-pick fake answer has 2 invalid picks", r1["invalid"] == "2", r1)
    m1_counts = {d: sum(1 for r in rows if r["condition"] == "A" and r["scored_for"] == d and r["m1"] != "")
                 for d in S.DISABILITIES}
    check("Measure 1 rows in A: wheelchair 60, blind 60, Deaf 40",
          m1_counts == {"mobility": 60, "visual": 60, "hearing": 40}, m1_counts)
    out2 = run("analyse.py")
    check("analyse.py runs on the fake scores", out2.returncode == 0, out2.stderr[-800:])
    if out2.returncode == 0:
        main_rows = list(csv.reader(open(tmp / "results" / "main_results.csv", encoding="utf-8")))[1:]
        check("main_results.csv has the nine main results", len(main_rows) == 9, len(main_rows))
        # In the fake data A picks only fully usable places, so A's main outcome is 0% (except the edited ones).
        r1_main = main_rows[0]
        check("fake data: result 1 (A vs B wheelchair) shows the planted difference and passes Holm",
              r1_main[-1] == "passes Holm", r1_main)
        for f in ["REPORT.md", "secondary_results.csv", "main_outcome_split.csv", "per_interest.csv",
                  "measure3_mentions_summary.csv", "measure2_summary.csv", "kinds_of_place.csv", "sensitivity.csv",
                  "rules_broken_wheelchair.csv", "rules_broken_blind.csv", "rules_broken_Deaf.csv"]:
            check(f"output written: {f}", (tmp / "results" / f).exists())
        sec = list(csv.reader(open(tmp / "results" / "secondary_results.csv", encoding="utf-8")))[1:]
        check("secondary results: 7 measures x 3 comparisons x 3 disabilities, minus the 6 main, plus Measure 2 (6) = 63",
              len(sec) == 63, len(sec))
        m2 = [x for x in sec if x[2].startswith("Measure 2")]
        check("Measure 2 'ramp' claims are flagged in the fake answers at places without a ramp", len(m2) == 6)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
if FAILED:
    sys.exit(1)
