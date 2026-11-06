"""Study 2 results (E1, E2), as PLAN_E.md says. SW350 Group 4.

  python analyse_e.py    reads results_E/scores_E.csv and study1/scores_per_answer.csv (Study 1, unchanged),
                         writes results_E/REPORT_E.md and one CSV per table

Uses Study 1's statistics code (analyse.py, unchanged): Fisher's exact test for yes/no, Mann-Whitney U for
scores, two-sided; Newcombe and bootstrap intervals (2,000 resamples, seed 20261028). Holm over Study 2's nine
main results only; Study 1's and group D's results are not changed. Numbers only: the team interprets.

Updated 29 Oct 2026, before any Study 2 answer was scored (PLAN_E_addendum.md): the fabrication results F1 to F6
(Holm over these six), and a descriptive table of claims in every group.
"""
import csv
import hashlib
import json
from collections import Counter

import numpy as np

import study_common as S
import analyse as AN            # Study 1's statistics helpers, used as they are
import score_e as SE

RESULTS = S.HERE / "results_E"
STUDY1 = S.HERE / "study1" / "scores_per_answer.csv"
STUDY1_SHA = "c617e7743e938a474b70d21982448e38b316a4f3a9c6c9c18ff4c27526280e5d"
FAB1 = S.HERE / "study1" / "fabrication_study1.csv"      # Study 1's answers under fabrication.py's rule
FAB1_SHA = "b0c24787dbfb183d89d5235ef1c21db325a1fbaa1dbbda44e82338594df7edc0"
FAB = ["claims_picks", "unsupported_any", "unsupported_picks", "false_any", "false_picks"]
AN.YESNO["unsupported_any"] = "Unsupported facility claim (any pick)"   # yes/no: Fisher's exact test
AN.YESNO["false_any"] = "False facility claim (any pick)"
DIS, DIS_NAME = AN.DIS, AN.DIS_NAME
LABEL = dict(AN.YESNO, **AN.SCORES, m1_all="Picks in her linked kinds of place (all valid picks)")
FAB_MAIN = ([("No facility information: told vs not told", "E2T", "E2N", d, "unsupported_any") for d in DIS]
            + [("Told: no facility information (E2T) vs facilities shown (A, Study 1)", "E2T", "A", d, "unsupported_any")
               for d in DIS])
MAIN = ([("E1: told vs not told, every place fully usable", "E1T", "E1N", d, "m1_all") for d in DIS]
        + [("E2: told vs not told, no facility information", "E2T", "E2N", d, "m1_all") for d in DIS]
        + [("E2: told vs not told, no facility information", "E2T", "E2N", d, "main_outcome") for d in DIS])
GROUPS = [("B", "Study 1: not told, all places"), ("A", "Study 1: told, all places"),
          ("E1N", "E1: not told, fully usable places only"), ("E1T", "E1: told, fully usable places only"),
          ("E2N", "E2: not told, no facility information"), ("E2T", "E2: told, no facility information")]


def read_scores(path):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    for r in rows:
        for k in list(AN.YESNO) + list(AN.SCORES):
            if k not in r:              # the fabrication columns: added below for Study 1's rows
                continue
            r[k] = (int(r[k]) if r[k] != "" else None) if k == "m1" else int(r[k])
        r["m3_any"] = int(r["m3_any"])
        if "m1_all" not in r:            # Study 1 rows: computed the same way from their picks
            r["m1_all"] = SE.m1_all(r["interest"], r["categories"], r["scored_for"])
        r["m1_all"] = int(r["m1_all"]) if r["m1_all"] != "" else None
        for k in FAB:
            if k in r:
                r[k] = int(r[k])
    return rows


def write_csv(name, header, rows):
    with open(RESULTS / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    if not (RESULTS / "scores_E.csv").exists():
        raise SystemExit("Not found: results_E/scores_E.csv. Run  python score_e.py  first.")
    if hashlib.sha256(STUDY1.read_bytes()).hexdigest() != STUDY1_SHA:
        raise SystemExit("STOP: study1/scores_per_answer.csv is not Study 1's original scores file.")
    e_rows = read_scores(RESULTS / "scores_E.csv")
    if len(e_rows) != 1200:
        raise SystemExit(f"STOP: scores_E.csv has {len(e_rows)} rows, not 1,200. Run score_e.py again.")
    if hashlib.sha256(FAB1.read_bytes()).hexdigest() != FAB1_SHA:
        raise SystemExit("STOP: study1/fabrication_study1.csv is not the file computed on 29 Oct 2026.")
    fab1 = {r["request_id"]: r for r in csv.DictReader(open(FAB1, newline="", encoding="utf-8"))}
    s1 = [r for r in read_scores(STUDY1) if r["condition"] in ("A", "B", "C")]
    for r in s1:
        r.update({k: int(fab1[r["request_id"]][k]) for k in FAB})
    rows = s1 + e_rows
    rep = ["# SW350 G04: Study 2 results, E1 and E2 (numbers only)", "",
           "Study 2 was planned on 29 October 2026, after Study 1 and group D (PLAN_E.md). E1: only places fully "
           "usable for that traveller, facilities shown. E2: all 144 places without the Facilities sentence. A and B "
           "are Study 1's scores, unchanged, shown for reference; Study 2 ran on a different date. Holm is applied "
           "to Study 2's nine main results only. The interpretation is written by the team.", ""]

    # ---------- the run ----------
    answers = [json.loads(x) for x in open(S.HERE / "run_E" / "answers.jsonl", encoding="utf-8") if x.strip()]
    answers = [a for a in answers if a.get("kind") == "answer"]
    tok = Counter()
    for a in answers:
        for k, v in (a.get("usage") or {}).items():
            tok[k] += v or 0
    rep += ["## S0. The Study 2 run", "", AN.md_table(["Item", "Value"], [
        ["Answers", ", ".join(f"{c} {n}" for c, n in sorted(Counter(a["condition"] for a in answers).items()))],
        ["Model(s) returned", ", ".join(f"{m} ({n})" for m, n in Counter(a["model_returned"] for a in answers).items())],
        ["First request sent / last answer received",
         f"{min(a['sent_at'] for a in answers)} / {max(a['received_at'] for a in answers)}"],
        ["Re-sends after a technical error", sum(a["attempts"] - 1 for a in answers)],
        ["Answers with a format problem", sum(1 for a in answers if a["parse_error"])],
        ["Answers with fewer or more than 5 picks",
         sum(1 for a in answers if not a["parse_error"] and len(a["parsed"]["recommendations"]) != 5)],
        ["Invalid picks", sum(r["invalid"] for r in e_rows if r["condition"] != "E2N" or r["scored_for"] == "mobility")],
        ["Tokens", f"input {tok['input_tokens']:,} (cached {tok['cached_tokens']:,}, written to cache "
                   f"{tok['cache_write_tokens']:,}); output {tok['output_tokens']:,} (reasoning {tok['reasoning_tokens']:,})"],
    ]), ""]

    # ---------- overview ----------
    ov = []
    for d in DIS:
        for g, name in GROUPS:
            x = [r for r in rows if r["condition"] == g and r["scored_for"] == d]
            m1a = [r["m1_all"] for r in x if r["m1_all"] is not None]
            ov.append([DIS_NAME[d], f"{g} ({name})", len(x), AN.pct(np.mean([r["main_outcome"] for r in x])),
                       f"{np.mean([r['accessibility'] for r in x]):.2f}", f"{np.mean([r['fully_suitable'] for r in x]):.2f}",
                       f"{np.mean([r['budget'] for r in x]):.2f}", f"{np.mean([r['interest_score'] for r in x]):.2f}",
                       f"{np.mean([r['diversity'] for r in x]):.2f}", f"{np.mean(m1a):.2f}" if m1a else "-",
                       AN.pct(np.mean([r["m3_any"] for r in x]))])
    oh = ["Traveller", "Group", "Answers", "Main outcome yes", "Accessibility", "Fully suitable", "Budget", "Interest",
          "Diversity", "Linked kinds of place (all picks)", "Mentions the disability"]
    write_csv("overview_E.csv", oh, ov)
    rep += ["## All groups at a glance (descriptive)", "", AN.md_table(oh, ov), ""]

    # ---------- the nine main results ----------
    res = [AN.compare(rows, g1, g2, d, m) for _, g1, g2, d, m in MAIN]
    adj, thr, ok = AN.holm([r["p"] for r in res])
    table = []
    for i, ((what, g1, g2, d, m), r) in enumerate(zip(MAIN, res), 1):
        table.append([f"S{i}", what, r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"], r["summary2"],
                      r["difference"], r["ci"], r["test"], AN.p_text(r["p"]), f"{thr[i - 1]:.4f}",
                      AN.p_text(adj[i - 1]), "passes Holm" if ok[i - 1] else "does not pass Holm"])
    th = ["#", "Comparison", "Traveller", "Outcome", "Answers", "Told", "Not told", "Difference (told - not told)",
          "95% interval", "Test", "p", "Holm threshold (9 tests)", "Holm-adjusted p", "Decision"]
    write_csv("E_main_results.csv", th, table)
    rep += ["## The nine main results of Study 2 (Holm over these nine, at 0.05)", "", AN.md_table(th, table), ""]

    # ---------- secondary ----------
    planned = ([("E1T", "E1N", m) for m in ["main_outcome", "fully_suitable", "budget", "interest_score", "diversity",
                                             "invalid", "m2_any"]]
               + [("E2T", "E2N", m) for m in ["accessibility", "fully_suitable", "budget", "interest_score",
                                               "diversity", "invalid", "m1", "m2_any"]]
               + [("E2T", "A", m) for m in ["main_outcome", "fully_suitable", "m1_all"]]
               + [("E2N", "B", m) for m in ["main_outcome", "fully_suitable", "m1_all"]])
    sec = []
    for g1, g2, m in planned:
        for d in DIS:
            r = AN.compare(rows, g1, g2, d, m)
            sec.append([r["comparison"], r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"],
                        r["summary2"], r["difference"], r["ci"], r["test"], AN.p_text(r["p"])])
    sh = ["Comparison", "Traveller", "Measure", "Answers", "First group", "Second group", "Difference", "95% interval",
          "Test", "p (uncorrected)"]
    write_csv("E_secondary.csv", sh, sec)
    rep += ["## Secondary results (uncorrected p-values). E2T vs A and E2N vs B compare with Study 1, run on a "
            "different date", "", AN.md_table(sh, sec), ""]

    # ---------- per interest ----------
    pi = []
    for d in DIS:
        for it in S.INTERESTS:
            line = [DIS_NAME[d], it["interest_key"]]
            for g, _ in GROUPS:
                x = [r for r in rows if r["condition"] == g and r["scored_for"] == d and r["interest"] == it["interest_key"]]
                m1a = [r["m1_all"] for r in x if r["m1_all"] is not None]
                line.append(f"{np.mean(m1a):.2f}" if m1a else "-")
            pi.append(line)
    ph = ["Traveller", "Interest"] + [f"{g}: linked kinds (all picks)" for g, _ in GROUPS]
    write_csv("E_per_interest.csv", ph, pi)
    rep += ["## Per interest: picks in her linked kinds of place (20 answers per cell, no tests)", "",
            AN.md_table(ph, pi), ""]

    # ---------- kinds of place ----------
    cats = list(S.CATEGORY_INFO)
    kp = []
    for g, _ in GROUPS:
        for d in DIS:
            if g in ("B", "E2N") and d != "mobility":
                continue
            c = Counter()
            for r in rows:
                if r["condition"] == g and r["scored_for"] == d:
                    c.update(x for x in r["categories"].split() if x != "INVALID")
            total = sum(c.values()) or 1
            kp.append([g, "all" if g in ("B", "E2N") else DIS_NAME[d], total] + [AN.pct(c[k] / total) for k in cats])
    write_csv("E_kinds_of_place.csv", ["Group", "Traveller", "Valid picks"] + cats, kp)
    rep += ["## Kinds of place picked (share of valid picks; descriptive)", "",
            AN.md_table(["Group", "Traveller", "Valid picks"] + cats, kp), ""]

    # ---------- Measures 2 and 3 ----------
    m23 = []
    for g, _ in GROUPS[2:]:
        for d in DIS:
            if g == "E2N" and d != "mobility":
                continue
            x = [r for r in e_rows if r["condition"] == g and r["scored_for"] == d]
            k3 = sum(r["m3_any"] for r in x)
            lo, hi = AN.wilson(k3, len(x))
            m23.append([g, "all" if g == "E2N" else DIS_NAME[d], len(x), sum(r["m2_any"] for r in x),
                        f"{k3}/{len(x)} = {AN.pct(k3 / len(x))}", f"[{100 * lo:.1f}%, {100 * hi:.1f}%]"])
    mh = ["Group", "Traveller", "Answers", "Measure 2: answers flagged (automatic rule)",
          "Measure 3: answers mentioning a disability word", "95% interval (Wilson)"]
    write_csv("E_measures_2_3.csv", mh, m23)
    rep += ["## Measures 2 and 3 (descriptive)", "", AN.md_table(mh, m23), "",
            "Every flagged sentence is in measure2_flagged_sentences_E.csv, to be read by the team as in Study 1.", ""]

    # ---------- sensitivity ----------
    sens = []
    for i, (what, g1, g2, d, m) in enumerate(MAIN, 1):
        r = AN.compare(rows, g1, g2, d, m, extra=lambda row: row["invalid"] == 0)
        sens.append([f"S{i}", what, r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"], r["summary2"],
                     r["difference"], r["ci"], r["test"], AN.p_text(r["p"])])
    sh2 = ["#", "Comparison", "Traveller", "Outcome", "Answers", "Told", "Not told", "Difference", "95% interval",
           "Test", "p (uncorrected)"]
    write_csv("E_sensitivity.csv", sh2, sens)
    rep += ["## Sensitivity check: the nine main results using only answers with no invalid pick", "",
            AN.md_table(sh2, sens), ""]

    # ---------- fabrication (PLAN_E_addendum.md) ----------
    fres = [AN.compare(rows, g1, g2, d, m) for _, g1, g2, d, m in FAB_MAIN]
    fadj, fthr, fok = AN.holm([r["p"] for r in fres])
    ftable = []
    for i, ((what, g1, g2, d, m), r) in enumerate(zip(FAB_MAIN, fres), 1):
        ftable.append([f"F{i}", what, r["disability"], LABEL[m], f"{r['n1']} / {r['n2']}", r["summary1"], r["summary2"],
                       r["difference"], r["ci"], r["test"], AN.p_text(r["p"]), f"{fthr[i - 1]:.4f}",
                       AN.p_text(fadj[i - 1]), "passes Holm" if fok[i - 1] else "does not pass Holm"])
    fh = ["#", "Comparison", "Traveller", "Outcome", "Answers", "First group", "Second group", "Difference",
          "95% interval", "Test", "p", "Holm threshold (6 tests)", "Holm-adjusted p", "Decision"]
    write_csv("E_fabrication_results.csv", fh, ftable)
    fd = []
    for g, name in [("B", "Study 1: not told, all places"), ("A", "Study 1: told, all places"),
                    ("C", "Study 1: filter, not told")] + GROUPS[2:]:
        for d in DIS:
            if g in ("B", "E2N") and d != "mobility":
                continue
            x = [r for r in rows if r["condition"] == g and r["scored_for"] == d]
            fd.append([g, name, "all" if g in ("B", "E2N") else DIS_NAME[d], len(x),
                       AN.pct(np.mean([r["claims_picks"] > 0 for r in x])), AN.pct(np.mean([r["unsupported_any"] for r in x])),
                       AN.pct(np.mean([r["false_any"] for r in x]))])
    fdh = ["Group", "", "Traveller", "Answers", "With any facility claim", "With an unsupported claim",
           "With a false claim"]
    write_csv("E_fabrication_by_group.csv", fdh, fd)
    rep += ["## Fabrication: facility claims not supported by what ChatGPT was shown (PLAN_E_addendum.md; "
            "Holm over these six)", "", "Unsupported = none of the claimed facilities was shown for that place (in E2 "
            "nothing was shown). False = unsupported, and the place does not have it in our data. Every claim is listed "
            "in fabrication_claims_E.csv. A vs E2T compares runs on different dates.", "", AN.md_table(fh, ftable), "",
            "### Facility claims in every group (descriptive; Study 1 groups scored with the same rule)", "",
            AN.md_table(fdh, fd), ""]

    (RESULTS / "REPORT_E.md").write_text("\n".join(rep), encoding="utf-8")
    print("Wrote results_E/REPORT_E.md and the CSV tables:")
    for line in table:
        print(f"  {line[0]}. {line[1][:3]} {line[2]:<10} {line[3][:28]:<28} told {line[5]:<20} not told {line[6]:<20} "
              f"p={line[10]:<8} {line[13]}")
    print("Fabrication (F1 to F3: E2 told vs not told; F4 to F6: E2 told vs A):")
    for line in ftable:
        print(f"  {line[0]}. {line[2]:<10} {line[5]:<20} vs {line[6]:<20} p={line[10]:<8} {line[13]}")


if __name__ == "__main__":
    main()
