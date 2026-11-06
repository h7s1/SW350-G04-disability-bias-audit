"""Group D results, as PLAN_D.md says, next to Study 1's groups. SW350 Group 4.

  python analyse_d.py    reads results_D/scores_D.csv and study1/scores_per_answer.csv (Study 1, unchanged),
                         writes results_D/REPORT_D.md and one CSV per table

Uses Study 1's statistics code (analyse.py, unchanged): Fisher's exact test for yes/no, Mann-Whitney U for
scores, two-sided; Newcombe and bootstrap intervals (2,000 resamples, seed 20261028). Holm is applied to the six
D results on their own; they are not part of Study 1's nine main results. Numbers only: the team interprets.
"""
import csv
import hashlib
from collections import Counter

import numpy as np

import study_common as S
import analyse as AN            # Study 1's statistics helpers, used as they are

RESULTS = S.HERE / "results_D"
STUDY1 = S.HERE / "study1" / "scores_per_answer.csv"
STUDY1_SHA = "c617e7743e938a474b70d21982448e38b316a4f3a9c6c9c18ff4c27526280e5d"
DIS, DIS_NAME = AN.DIS, AN.DIS_NAME
LABEL = dict(AN.YESNO, **AN.SCORES)
MAIN_D = [("D vs C", "D", "C", d, "fully_suitable") for d in DIS] + \
         [("D vs A", "D", "A", d, "fully_suitable") for d in DIS]
SECTION4 = ["main_outcome", "accessibility", "fully_suitable", "budget", "interest_score", "diversity", "invalid"]


def read_scores(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    for r in rows:
        for k in list(AN.YESNO) + list(AN.SCORES):
            r[k] = (int(r[k]) if r[k] != "" else None) if k == "m1" else int(r[k])
        r["m3_any"] = int(r["m3_any"])
    return rows


def write_csv(name, header, rows):
    with open(RESULTS / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    if not (RESULTS / "scores_D.csv").exists():
        raise SystemExit("Not found: results_D/scores_D.csv. Run  python score_d.py  first.")
    if hashlib.sha256(STUDY1.read_bytes()).hexdigest() != STUDY1_SHA:
        raise SystemExit("STOP: study1/scores_per_answer.csv is not Study 1's original scores file.")
    d_rows = read_scores(RESULTS / "scores_D.csv")
    if len(d_rows) != 300:
        raise SystemExit(f"STOP: scores_D.csv has {len(d_rows)} rows, not 300. Run score_d.py again.")
    rows = read_scores(STUDY1) + d_rows
    rep = ["# SW350 G04: group D results (numbers only)", "",
           "Group D was added on 29 October 2026, after Study 1's results (PLAN_D.md): the filtered list of C "
           "and the disability sentence of A. It was run on a different date from A, B and C. A, B and C are "
           "Study 1's scores, unchanged. Holm is applied to the six D results only; Study 1's nine main results "
           "are not changed. The interpretation is written by the team.", ""]

    # ---------- the run ----------
    import json
    answers = [json.loads(x) for x in open(S.HERE / "run_D" / "answers.jsonl", encoding="utf-8") if x.strip()]
    answers = [a for a in answers if a.get("kind") == "answer"]
    tok = Counter()
    for a in answers:
        for k, v in (a.get("usage") or {}).items():
            tok[k] += v or 0
    rep += ["## D0. The D run", "", AN.md_table(["Item", "Value"], [
        ["Answers", len(answers)],
        ["Model(s) returned", ", ".join(f"{m} ({n})" for m, n in Counter(a["model_returned"] for a in answers).items())],
        ["First request sent / last answer received",
         f"{min(a['sent_at'] for a in answers)} / {max(a['received_at'] for a in answers)}"],
        ["Re-sends after a technical error", sum(a["attempts"] - 1 for a in answers)],
        ["Answers with a format problem", sum(1 for a in answers if a["parse_error"])],
        ["Answers with fewer or more than 5 picks",
         sum(1 for a in answers if not a["parse_error"] and len(a["parsed"]["recommendations"]) != 5)],
        ["Invalid picks", sum(r["invalid"] for r in d_rows)],
        ["Tokens", f"input {tok['input_tokens']:,} (cached {tok['cached_tokens']:,}, written to cache "
                   f"{tok['cache_write_tokens']:,}); output {tok['output_tokens']:,} (reasoning {tok['reasoning_tokens']:,})"],
    ]), ""]

    # ---------- overview: all four groups ----------
    ov = []
    for d in DIS:
        for g in ("A", "B", "C", "D"):
            x = [r for r in rows if r["condition"] == g and r["scored_for"] == d]
            m1 = [r["m1"] for r in x if r["m1"] is not None]
            ov.append([DIS_NAME[d], g + (" (added later)" if g == "D" else ""), len(x),
                       AN.pct(np.mean([r["main_outcome"] for r in x])),
                       f"{np.mean([r['accessibility'] for r in x]):.2f}", f"{np.mean([r['fully_suitable'] for r in x]):.2f}",
                       f"{np.mean([r['budget'] for r in x]):.2f}", f"{np.mean([r['interest_score'] for r in x]):.2f}",
                       f"{np.mean([r['diversity'] for r in x]):.2f}", f"{np.mean(m1):.2f}" if m1 else "-",
                       AN.pct(np.mean([r["m2_any"] for r in x])), AN.pct(np.mean([r["m3_any"] for r in x]))])
    oh = ["Traveller", "Group", "Answers", "Main outcome yes", "Accessibility", "Fully suitable", "Budget",
          "Interest", "Diversity", "Measure 1", "Measure 2 yes (automatic rule)", "Measure 3 yes"]
    write_csv("overview_ABCD.csv", oh, ov)
    rep += ["## All four groups at a glance (percentages and means; descriptive)", "",
            "A = told, all places; B = not told, all places (scored for each traveller); C = not told, filtered; "
            "D = told, filtered (added later). Measure 2 here is the planned automatic count (see Study 1's "
            "check of the flagged sentences).", "", AN.md_table(oh, ov), ""]

    # ---------- the six D results ----------
    res = [AN.compare(rows, g1, g2, d, m) for _, g1, g2, d, m in MAIN_D]
    adj, thr, ok = AN.holm([r["p"] for r in res])
    table = []
    for i, ((name, g1, g2, d, m), r) in enumerate(zip(MAIN_D, res), 1):
        table.append([f"D{i}", r["comparison"], r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"],
                      r["summary2"], r["difference"], r["ci"], r["test"], AN.p_text(r["p"]), f"{thr[i - 1]:.4f}",
                      AN.p_text(adj[i - 1]), "passes Holm" if ok[i - 1] else "does not pass Holm"])
    th = ["#", "Comparison", "Traveller", "Outcome", "Answers", "First group", "Second group",
          "Difference (first - second)", "95% interval", "Test", "p", "Holm threshold (6 tests)", "Holm-adjusted p",
          "Decision"]
    write_csv("D_results.csv", th, table)
    rep += ["## The six D results (added later; Holm over these six, at 0.05)", "",
            "D vs C: does telling ChatGPT the disability help when the list is already filtered? "
            "D vs A: does the filter help when ChatGPT is told?", "", AN.md_table(th, table), ""]

    # ---------- secondary ----------
    main_keys = {(g1, g2, d, m) for _, g1, g2, d, m in MAIN_D}
    sec = []
    for g2 in ("C", "A"):
        for m in SECTION4 + ["m1", "m2_any"]:
            for d in DIS:
                if ("D", g2, d, m) in main_keys:
                    continue
                r = AN.compare(rows, "D", g2, d, m)
                sec.append([r["comparison"], r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"],
                            r["summary2"], r["difference"], r["ci"], r["test"], AN.p_text(r["p"])])
    sh = ["Comparison", "Traveller", "Measure", "Answers", "First group", "Second group", "Difference",
          "95% interval", "Test", "p (uncorrected)"]
    write_csv("D_secondary.csv", sh, sec)
    rep += ["## D secondary results (uncorrected p-values)", "", AN.md_table(sh, sec), ""]

    # ---------- Measures 2 and 3 for D ----------
    m23 = []
    for d in DIS:
        x = [r for r in d_rows if r["scored_for"] == d]
        k3 = sum(r["m3_any"] for r in x)
        lo, hi = AN.wilson(k3, len(x))
        m23.append([DIS_NAME[d], len(x), sum(r["m2_any"] for r in x), sum(r["m2_picks"] for r in x),
                    f"{k3}/{len(x)} = {AN.pct(k3 / len(x))}", f"[{100 * lo:.1f}%, {100 * hi:.1f}%]"])
    mh = ["Traveller", "Answers", "Measure 2: answers flagged (automatic rule)", "Measure 2: picks flagged",
          "Measure 3: answers mentioning a disability word", "95% interval (Wilson)"]
    write_csv("D_measures_2_3.csv", mh, m23)
    rep += ["## Measures 2 and 3 in D (descriptive)", "", AN.md_table(mh, m23), "",
            "Every flagged sentence is in measure2_flagged_sentences_D.csv, to be read by the team as in Study 1.", ""]

    # ---------- per interest (D) ----------
    pi = []
    for d in DIS:
        for it in S.INTERESTS:
            x = [r for r in d_rows if r["scored_for"] == d and r["interest"] == it["interest_key"]]
            m1 = [r["m1"] for r in x if r["m1"] is not None]
            pi.append(["D", DIS_NAME[d], it["interest_key"], len(x), AN.pct(np.mean([r["main_outcome"] for r in x])),
                       f"{np.mean([r['accessibility'] for r in x]):.2f}", f"{np.mean([r['fully_suitable'] for r in x]):.2f}",
                       f"{np.mean([r['budget'] for r in x]):.2f}", f"{np.mean([r['interest_score'] for r in x]):.2f}",
                       f"{np.mean([r['diversity'] for r in x]):.2f}", f"{np.mean([r['invalid'] for r in x]):.2f}",
                       f"{np.mean(m1):.2f}" if m1 else "-"])
    ph = ["Group", "Traveller", "Interest", "Answers", "Main outcome yes", "Accessibility", "Fully suitable",
          "Budget", "Interest", "Diversity", "Invalid", "Measure 1"]
    write_csv("D_per_interest.csv", ph, pi)
    rep += ["## D per interest (20 answers per cell, no tests)", "", AN.md_table(ph, pi), ""]

    # ---------- rules broken ----------
    rep += ["## Rules broken among the valid picks: A, C and D (descriptive)", ""]
    for d in DIS:
        rids = [r.rule_id for r in S.acc_filter.RULES if r.disability == d]
        sub = []
        for g in ("A", "C", "D"):
            c, n_valid = Counter(), 0
            for r in rows:
                if r["condition"] == g and r["scored_for"] == d:
                    n_valid += 5 - r["invalid"]
                    for part in r["rules_broken"].split():
                        k, v = part.split(":")
                        c[k] += int(v)
            sub.append([g, DIS_NAME[d], n_valid] + [c.get(k, 0) for k in rids])
        rep += [f"**{DIS_NAME[d]}**", "", AN.md_table(["Group", "Traveller", "Valid picks"] + rids, sub), ""]
        write_csv(f"D_rules_broken_{DIS_NAME[d]}.csv", ["Group", "Traveller", "Valid picks"] + rids, sub)

    # ---------- kinds of place ----------
    cats = list(S.CATEGORY_INFO)
    kp = []
    for g in ("A", "C", "D"):
        for d in DIS:
            c = Counter()
            for r in rows:
                if r["condition"] == g and r["scored_for"] == d:
                    c.update(x for x in r["categories"].split() if x != "INVALID")
            total = sum(c.values()) or 1
            kp.append([g, DIS_NAME[d], total] + [AN.pct(c[k] / total) for k in cats])
    write_csv("D_kinds_of_place.csv", ["Group", "Traveller", "Valid picks"] + cats, kp)
    rep += ["## Kinds of place: A, C and D (share of valid picks; descriptive)", "",
            AN.md_table(["Group", "Traveller", "Valid picks"] + cats, kp), ""]

    # ---------- sensitivity ----------
    sens = []
    for i, (name, g1, g2, d, m) in enumerate(MAIN_D, 1):
        r = AN.compare(rows, g1, g2, d, m, extra=lambda row: row["invalid"] == 0)
        sens.append([f"D{i}", r["comparison"], r["disability"], "answers with no invalid pick only",
                     f"{r['n1']} / {r['n2']}", r["summary1"], r["summary2"], r["difference"], r["ci"], r["test"],
                     AN.p_text(r["p"])])
    sh = ["#", "Comparison", "Traveller", "Version", "Answers", "First group", "Second group", "Difference",
          "95% interval", "Test", "p (uncorrected)"]
    write_csv("D_sensitivity.csv", sh, sens)
    rep += ["## Sensitivity check: the six D results without invalid picks", "", AN.md_table(sh, sens), ""]

    (RESULTS / "REPORT_D.md").write_text("\n".join(rep), encoding="utf-8")
    print("Wrote results_D/REPORT_D.md and the CSV tables:")
    for line in table:
        print(f"  {line[0]}. {line[1]} {line[2]:<10} {line[3]:<22} {line[5]:<22} {line[6]:<22} p={line[10]:<8} {line[13]}")


if __name__ == "__main__":
    main()
