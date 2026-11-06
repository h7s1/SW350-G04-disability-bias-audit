"""Score the group D answers with Study 1's frozen scoring rules (score_answers.py, unchanged). SW350 Group 4.

  python score_d.py    reads run_D/answers.jsonl, writes results_D/scores_D.csv and the Measure 2 and 3 files
"""
import csv
import json
import sys

import study_common as S
import groupd as G
import score_answers as SA      # Study 1's scoring code, used as it is

RESULTS = S.HERE / "results_D"
ANSWERS = G.RUN_DIR / "answers.jsonl"


def main():
    if not ANSWERS.exists():
        raise SystemExit(f"Not found: {ANSWERS}. Run  python run_d.py --run  first.")
    S.check_frozen()
    plan = {r["request_id"]: r for r in G.build_plan_d()}
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
        raise SystemExit(f"STOP: answers do not match the D plan ({len(set(ids))} unique of {len(plan)}). "
                         "If the run is not finished, run  python run_d.py --run  again first.")
    for a in answers:
        r = plan[a["request_id"]]
        if a["list_order"] != r["list_order"] or a["prompt_sha256"] != G.fingerprint_d(r):
            raise SystemExit(f"STOP: {a['request_id']} was not sent as planned.")
    RESULTS.mkdir(exist_ok=True)
    rows, flagged, mentions = [], [], []
    for a in sorted(answers, key=lambda x: x["run_position"]):
        m = SA.match_picks(a)
        m2_picks = 0
        for slot, (pid, reason, _) in enumerate(m["slots"], 1):
            if pid is None:
                continue
            claims = SA.invented_claims(reason, S.PLACE[pid])
            if claims:
                m2_picks += 1
                for c in claims:
                    flagged.append({"request_id": a["request_id"], "condition": a["condition"],
                                    "disability_told": a["disability"], "pick": slot, "place_id": pid,
                                    "place_name": S.PLACE[pid]["name"], "phrase": c["phrase"],
                                    "facilities_needed": c["facilities"], "reason": reason})
        words = sorted({w for _, reason, _ in m["slots"] for w in SA.disability_mentions(reason)})
        if words:
            mentions.append({"request_id": a["request_id"], "condition": a["condition"],
                             "disability_told": a["disability"], "words": " ".join(words),
                             "reasons": " || ".join(reason for _, reason, _ in m["slots"]
                                                    if SA.disability_mentions(reason))})
        d = a["disability"]
        row = {"request_id": a["request_id"], "condition": "D", "disability_told": d, "scored_for": d,
               "interest": a["interest"], "repeat": a["repeat"], "run_position": a["run_position"],
               "m2_any": int(m2_picks > 0), "m2_picks": m2_picks, "m3_any": int(bool(words)),
               "m3_words": " ".join(words), "n_picks_given": m["n_given"],
               "match_notes": "; ".join(m["notes"] + sorted({how for pid, _, how in m["slots"] if how != "id"}))}
        row.update(SA.score(a, m, d))
        rows.append(row)
    with open(RESULTS / "scores_D.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=SA.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    with open(RESULTS / "measure2_flagged_sentences_D.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["request_id", "condition", "disability_told", "pick", "place_id",
                                           "place_name", "phrase", "facilities_needed", "reason"])
        w.writeheader()
        w.writerows(flagged)
    with open(RESULTS / "measure3_mentions_D.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["request_id", "condition", "disability_told", "words", "reasons"])
        w.writeheader()
        w.writerows(mentions)
    print(f"Scored {len(answers)} D answers -> {len(rows)} rows.")
    print(f"Measure 2: {len(flagged)} flagged phrases; Measure 3: {len(mentions)} answers mention a disability word.")
    print(f"Files in {RESULTS}: scores_D.csv, measure2_flagged_sentences_D.csv, measure3_mentions_D.csv")


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is needed.")
    main()
