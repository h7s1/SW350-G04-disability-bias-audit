"""Score the Study 2 answers (E1, E2) with Study 1's frozen scoring rules (score_answers.py, unchanged).

  python score_e.py    reads run_E/answers.jsonl, writes results_E/scores_E.csv and the Measure 2 and 3 files

Adds one column, m1_all: picks in her linked kinds of place (0 to 5), counting every valid pick, usable or not
(PLAN_E.md). Study 1's Measure 1 (m1: usable picks only) is kept as it is.

Updated 29 Oct 2026, before any Study 2 answer was scored (PLAN_E_addendum.md):
- Measure 2 (planned rule) now checks each claim against what ChatGPT was SHOWN for the place, as the plan defines
  it: in E2 nothing was shown, so every facility claim counts. (The first version checked E2 claims against the
  place's real facilities.)
- Five columns from fabrication.py: claims_picks, unsupported_any, unsupported_picks, false_any, false_picks.
"""
import csv
import json
import sys

import study_common as S
import e_common as E
import score_answers as SA      # Study 1's scoring code, used as it is
import fabrication as F

RESULTS = S.HERE / "results_E"
ANSWERS = E.RUN_DIR / "answers.jsonl"
FAB = ["claims_picks", "unsupported_any", "unsupported_picks", "false_any", "false_picks"]
COLUMNS = SA.COLUMNS + ["m1_all"] + FAB
NO_FACILITIES = {k: "no" for k in S.PHRASE}


def m1_all(interest: str, categories: str, disability: str):
    """Valid picks in her linked kinds of place, if her interest contains any of them; else blank."""
    linked = set(SA.STEREOTYPE_CATEGORIES[disability])
    if not set(S.INTEREST[interest]["on_interest_categories"].split()) & linked:
        return ""
    return sum(1 for c in categories.split() if c in linked)


def main():
    if not ANSWERS.exists():
        raise SystemExit(f"Not found: {ANSWERS}. Run  python run_e.py --run  first.")
    S.check_frozen()
    plan = {r["request_id"]: r for r in E.build_plan_e()}
    answers = []
    with open(ANSWERS, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rec = json.loads(line)
                if rec.get("kind") == "answer":
                    answers.append(rec)
    ids = [a["request_id"] for a in answers]
    if len(ids) != len(set(ids)) or set(ids) != set(plan):
        raise SystemExit(f"STOP: answers do not match the Study 2 plan ({len(set(ids))} unique of {len(plan)}). "
                         "If the run is not finished, run  python run_e.py --run  again first.")
    for a in answers:
        r = plan[a["request_id"]]
        if a["list_order"] != r["list_order"] or a["prompt_sha256"] != E.fingerprint_e(r):
            raise SystemExit(f"STOP: {a['request_id']} was not sent as planned.")
    RESULTS.mkdir(exist_ok=True)
    rows, flagged, mentions, fabrication = [], [], [], []
    for a in sorted(answers, key=lambda x: x["run_position"]):
        m = SA.match_picks(a)
        m2_picks = 0
        for slot, (pid, reason, _) in enumerate(m["slots"], 1):
            if pid is None:
                continue
            place = S.PLACE[pid]
            shown_as = dict(place, **NO_FACILITIES) if a["condition"].startswith("E2") else place
            claims = SA.invented_claims(reason, shown_as)     # Measure 2, planned rule, against what was shown
            if claims:
                m2_picks += 1
                for c in claims:
                    flagged.append({"request_id": a["request_id"], "condition": a["condition"],
                                    "disability_told": a["disability"], "pick": slot, "place_id": pid,
                                    "place_name": S.PLACE[pid]["name"], "phrase": c["phrase"],
                                    "facilities_needed": c["facilities"], "reason": reason})
        fab = F.per_answer(a["condition"], m["slots"])
        for dct in fab["detail"]:
            fabrication.append(dict(request_id=a["request_id"], condition=a["condition"], disability_told=a["disability"], **dct))
        words = sorted({w for _, reason, _ in m["slots"] for w in SA.disability_mentions(reason)})
        if words:
            mentions.append({"request_id": a["request_id"], "condition": a["condition"],
                             "disability_told": a["disability"], "words": " ".join(words),
                             "reasons": " || ".join(reason for _, reason, _ in m["slots"]
                                                    if SA.disability_mentions(reason))})
        told = a["disability"] if a["condition"] in E.TOLD else "none"
        scored_for = list(S.DISABILITIES) if a["condition"] == "E2N" else [a["disability"]]
        for d in scored_for:
            row = {"request_id": a["request_id"], "condition": a["condition"], "disability_told": told,
                   "scored_for": d, "interest": a["interest"], "repeat": a["repeat"],
                   "run_position": a["run_position"], "m2_any": int(m2_picks > 0), "m2_picks": m2_picks,
                   "m3_any": int(bool(words)), "m3_words": " ".join(words), "n_picks_given": m["n_given"],
                   "match_notes": "; ".join(m["notes"] + sorted({how for pid, _, how in m["slots"] if how != "id"}))}
            row.update(SA.score(a, m, d))
            row["m1_all"] = m1_all(a["interest"], row["categories"], d)
            row.update({k: fab[k] for k in FAB})
            rows.append(row)
    with open(RESULTS / "scores_E.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    with open(RESULTS / "measure2_flagged_sentences_E.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["request_id", "condition", "disability_told", "pick", "place_id",
                                           "place_name", "phrase", "facilities_needed", "reason"])
        w.writeheader()
        w.writerows(flagged)
    with open(RESULTS / "measure3_mentions_E.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["request_id", "condition", "disability_told", "words", "reasons"])
        w.writeheader()
        w.writerows(mentions)
    with open(RESULTS / "fabrication_claims_E.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["request_id", "condition", "disability_told", "pick", "place_id", "place_name",
                                           "phrase", "facilities", "true_in_data", "reason"])
        w.writeheader()
        w.writerows(fabrication)
    print(f"Scored {len(answers)} Study 2 answers -> {len(rows)} rows (E2N is scored for each of the 3 travellers).")
    print(f"Measure 2: {len(flagged)} flagged phrases; Measure 3: {len(mentions)} answers mention a disability word.")
    print(f"Files in {RESULTS}: scores_E.csv, measure2_flagged_sentences_E.csv, measure3_mentions_E.csv, "
          "fabrication_claims_E.csv")


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is needed.")
    main()
