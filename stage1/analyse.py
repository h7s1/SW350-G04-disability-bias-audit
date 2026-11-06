"""Step 2 of the analysis: the statistics in the analysis plan (v2.1), nothing more. SW350 Group 4.

  python analyse.py        reads results/scores_per_answer.csv (from score_answers.py) and run/answers.jsonl,
                           writes results/REPORT.md and one CSV per table

Fixed in the plan before the run: the nine main tests (Fisher's exact test for yes/no, Mann-Whitney U for
scores, two-sided), Holm on those nine at 0.05, sizes with 95% intervals (bootstrap: 2,000 resamples, seed
20261028), everything else secondary and uncorrected, per-interest results without tests, the sensitivity check.
This script reports numbers only; the interpretation is written by the team.
"""
import csv
import json
import math
from collections import Counter, defaultdict

try:
    import numpy as np
    from scipy import stats
except ImportError:
    raise SystemExit("scipy is missing. Run:  python -m pip install scipy   then run analyse.py again.")

import study_common as S

RESULTS = S.HERE / "results"
SEED = 20261028
N_BOOT = 2000
ALPHA = 0.05
DIS = ["mobility", "visual", "hearing"]
DIS_NAME = {"mobility": "wheelchair", "visual": "blind", "hearing": "Deaf"}
YESNO = {"main_outcome": "Main outcome (unusable or invalid pick)", "has_unusable": "Has an unusable place",
         "has_invalid": "Has an invalid pick", "m2_any": "Measure 2: invented facility"}
SCORES = {"accessibility": "Accessibility score", "fully_suitable": "Fully suitable score", "budget": "Budget",
          "interest_score": "Interest", "diversity": "Diversity", "invalid": "Invalid picks",
          "m1": "Measure 1: suitable picks in her stereotype categories", "m2_picks": "Measure 2: picks with an invented facility"}


# --------------------------------------------------------------------------- #
# Small statistics helpers
# --------------------------------------------------------------------------- #
def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def newcombe(k1, n1, k2, n2):
    """95% interval for p1 - p2 (Newcombe's method 10, built from two Wilson intervals)."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2))


def fisher(x, y):
    a, b = sum(x), len(x) - sum(x)
    c, d = sum(y), len(y) - sum(y)
    return stats.fisher_exact([[a, b], [c, d]], alternative="two-sided")[1]


def mann_whitney(x, y):
    if len(set(x) | set(y)) == 1:     # every value identical in both groups
        return 1.0
    return float(stats.mannwhitneyu(x, y, alternative="two-sided").pvalue)


def boot_diff(x, y):
    rng = np.random.default_rng(SEED)
    x, y = np.asarray(x, float), np.asarray(y, float)
    d = [rng.choice(x, len(x)).mean() - rng.choice(y, len(y)).mean() for _ in range(N_BOOT)]
    return (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)))


def holm(pvals):
    """Holm step-down at ALPHA: returns, in the original order, (adjusted p, threshold, passes)."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj, thr, ok = [0.0] * m, [0.0] * m, [False] * m
    running, still = 0.0, True
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvals[i]))
        adj[i] = running
        thr[i] = ALPHA / (m - rank)
        still = still and pvals[i] < thr[i]
        ok[i] = still
    return adj, thr, ok


def pct(v):
    return f"{100 * v:.1f}%"


def fmt_ci(lo, hi, scale=1.0, unit="", dp=1):
    return f"[{lo * scale:+.{dp}f}{unit}, {hi * scale:+.{dp}f}{unit}]"


# --------------------------------------------------------------------------- #
# Load
# --------------------------------------------------------------------------- #
def load():
    rows = list(csv.DictReader(open(RESULTS / "scores_per_answer.csv", newline="", encoding="utf-8")))
    for r in rows:
        for k in list(YESNO) + list(SCORES):
            if k == "m1":
                r[k] = int(r[k]) if r[k] != "" else None
            else:
                r[k] = int(r[k])
        r["m3_any"] = int(r["m3_any"])
    return rows


def group(rows, cond, d, measure, extra=None):
    out = []
    for r in rows:
        if r["condition"] == cond and r["scored_for"] == d and r[measure] is not None:
            if extra is None or extra(r):
                out.append(r[measure])
    return out


def compare(rows, g1, g2, d, measure, extra=None):
    x, y = group(rows, g1, d, measure, extra), group(rows, g2, d, measure, extra)
    res = {"comparison": f"{g1} vs {g2}", "disability": DIS_NAME[d], "measure": measure, "n1": len(x), "n2": len(y)}
    if not x or not y:
        res.update({"test": "-", "p": float("nan"), "summary1": "", "summary2": "", "difference": "", "ci": ""})
        return res
    if measure in YESNO:
        k1, k2 = sum(x), sum(y)
        lo, hi = newcombe(k1, len(x), k2, len(y))
        res.update({"test": "Fisher's exact", "p": fisher(x, y),
                    "summary1": f"{k1}/{len(x)} = {pct(k1 / len(x))}", "summary2": f"{k2}/{len(y)} = {pct(k2 / len(y))}",
                    "difference": f"{100 * (k1 / len(x) - k2 / len(y)):+.1f} points",
                    "ci": fmt_ci(lo, hi, 100, " pts")})
    else:
        lo, hi = boot_diff(x, y)
        res.update({"test": "Mann-Whitney U", "p": mann_whitney(x, y),
                    "summary1": f"mean {np.mean(x):.2f}, median {np.median(x):g}",
                    "summary2": f"mean {np.mean(y):.2f}, median {np.median(y):g}",
                    "difference": f"{np.mean(x) - np.mean(y):+.2f}", "ci": fmt_ci(lo, hi, dp=2)})
    return res


MAIN = ([("RQ1", "A", "B", d, "main_outcome") for d in DIS] + [("RQ4", "A", "C", d, "fully_suitable") for d in DIS]
        + [("RQ2", "A", "B", d, "m1") for d in DIS])


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def write_csv(name, header, rows):
    with open(RESULTS / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def p_text(p):
    return "nan" if p != p else (f"{p:.4f}" if p >= 0.0001 else "<0.0001")


def main():
    if not (RESULTS / "scores_per_answer.csv").exists():
        raise SystemExit("Not found: results/scores_per_answer.csv. Run  python score_answers.py  first.")
    rows = load()
    if len(rows) != 900:
        raise SystemExit(f"STOP: scores_per_answer.csv has {len(rows)} rows, not 900. Run score_answers.py again.")
    rep = ["# SW350 G04: results (numbers only)", "",
           "Produced by analyse.py from results/scores_per_answer.csv, exactly as the analysis plan v2.1 says. "
           "A = disability disclosed, all places; B = no disability disclosed, all places (scored for each disability); "
           "C = filter-first. The interpretation is written by the team.", ""]

    # ---------- run summary ----------
    answers = [json.loads(l) for l in open(S.RUN_DIR / "answers.jsonl", encoding="utf-8") if l.strip()]
    answers = [a for a in answers if a.get("kind") == "answer"]
    tok = Counter()
    for a in answers:
        for k, v in (a.get("usage") or {}).items():
            tok[k] += v or 0
    sent = sorted(a["sent_at"] for a in answers)
    recv = sorted(a["received_at"] for a in answers)
    rep += ["## R0. The run", "", md_table(["Item", "Value"], [
        ["Answers", f"{len(answers)} (A {sum(a['condition'] == 'A' for a in answers)}, B {sum(a['condition'] == 'B' for a in answers)}, C {sum(a['condition'] == 'C' for a in answers)})"],
        ["Model(s) returned", ", ".join(f"{m} ({n})" for m, n in Counter(a['model_returned'] for a in answers).items())],
        ["First request sent / last answer received", f"{sent[0]} / {recv[-1]}"],
        ["Re-sends after a technical error", sum(a["attempts"] - 1 for a in answers)],
        ["Answers with a format problem", sum(1 for a in answers if a["parse_error"])],
        ["Answers with fewer or more than 5 picks", sum(1 for a in answers if not a["parse_error"] and len(a["parsed"]["recommendations"]) != 5)],
        ["Invalid picks in all answers", sum(int(r["invalid"]) for r in rows if r["condition"] != "B" or r["scored_for"] == "mobility")],
        ["Tokens", f"input {tok['input_tokens']:,} (cached {tok['cached_tokens']:,}, written to cache {tok['cache_write_tokens']:,}); output {tok['output_tokens']:,} (reasoning {tok['reasoning_tokens']:,})"],
    ]), ""]

    # ---------- the nine main results ----------
    main_res = [compare(rows, g1, g2, d, m) for _, g1, g2, d, m in MAIN]
    adj, thr, ok = holm([r["p"] for r in main_res])
    table, csv_rows = [], []
    for i, ((rq, g1, g2, d, m), r) in enumerate(zip(MAIN, main_res), 1):
        decision = "passes Holm" if ok[i - 1] else "does not pass Holm"
        line = [i, rq, r["comparison"], r["disability"], YESNO.get(m) or SCORES.get(m), f"{r['n1']} / {r['n2']}",
                r["summary1"], r["summary2"], r["difference"], r["ci"], r["test"], p_text(r["p"]),
                f"{thr[i - 1]:.4f}", p_text(adj[i - 1]), decision]
        table.append(line)
        csv_rows.append(line)
    header = ["#", "RQ", "Comparison", "Disability", "Outcome", "Answers", "First group", "Second group",
              "Difference (first - second)", "95% interval", "Test", "p", "Holm threshold", "Holm-adjusted p",
              "Decision"]
    write_csv("main_results.csv", header, csv_rows)
    rep += ["## The nine main results (Holm over these nine, at 0.05)", "", md_table(header, table), "",
            "Holm: the p-values are sorted from smallest; the smallest must be below 0.05/9, the next below 0.05/8, "
            "and so on; testing stops at the first that is not. Intervals: Newcombe for differences in percentages; "
            f"percentile bootstrap ({N_BOOT:,} resamples, seed {SEED}) for differences in means.", ""]

    # ---------- split of results 1 to 3 ----------
    split = []
    for d in DIS:
        for g in ("A", "B"):
            x = [r for r in rows if r["condition"] == g and r["scored_for"] == d]
            split.append([DIS_NAME[d], g, len(x), sum(r["main_outcome"] for r in x), sum(r["has_unusable"] for r in x),
                          sum(r["has_invalid"] for r in x), sum(r["has_unusable"] and r["has_invalid"] for r in x)])
    sh = ["Disability", "Condition", "Answers", "Main outcome yes", "With an unusable place", "With an invalid pick", "With both"]
    write_csv("main_outcome_split.csv", sh, split)
    rep += ["## Results 1 to 3, split (always reported)", "", md_table(sh, split), ""]

    # ---------- RQ3: the filter ----------
    counts = []
    for d in DIS:
        c = Counter(S.DECISION[(p["place_id"], d)].outcome for p in S.PLACES)
        counts.append([DIS_NAME[d], c["ELIGIBLE"], c["ELIGIBLE_WITH_CAVEATS"], c["EXCLUDED"], len(S.FILTERED_IDS[d])])
    fails = Counter()
    for (pid, d), dec in S.DECISION.items():
        for rid in dec.excluded_by + dec.caveats:
            fails[rid] += 1
    rep += ["## RQ3: the filter (descriptive)", "",
            md_table(["Disability", "Fully usable", "Usable with a gap", "Excluded", "Sent in C"], counts), "",
            "Rule failures over the 144 places: " + ", ".join(f"{k} {v}" for k, v in sorted(fails.items(), key=lambda kv: (kv[0][0], int(kv[0][1:])))), ""]

    # ---------- secondary comparisons ----------
    # Plan section 6: every section 4 measure for A vs B, B vs C and A vs C, each disability, the nine main
    # results excepted. Plan section 7: Measure 2 (yes/no) for A vs B and A vs C, Fisher.
    main_keys = {(g1, g2, d, m) for _, g1, g2, d, m in MAIN}
    section4 = ["main_outcome", "accessibility", "fully_suitable", "budget", "interest_score", "diversity", "invalid"]
    planned = [(g1, g2, m) for g1, g2 in (("A", "B"), ("B", "C"), ("A", "C")) for m in section4]
    planned += [("A", "B", "m2_any"), ("A", "C", "m2_any")]
    sec, sec_csv = [], []
    for g1, g2, m in planned:
        for d in DIS:
            if (g1, g2, d, m) in main_keys:
                continue
            r = compare(rows, g1, g2, d, m)
            line = [r["comparison"], r["disability"], YESNO.get(m) or SCORES.get(m), f"{r['n1']} / {r['n2']}",
                    r["summary1"], r["summary2"], r["difference"], r["ci"], r["test"], p_text(r["p"])]
            sec.append(line)
            sec_csv.append(line)
    sh = ["Comparison", "Disability", "Measure", "Answers", "First group", "Second group", "Difference", "95% interval",
          "Test", "p (uncorrected)"]
    write_csv("secondary_results.csv", sh, sec_csv)
    rep += ["## Secondary results (uncorrected p-values; labelled secondary in the paper)", "", md_table(sh, sec), ""]

    # ---------- Measure 3 (descriptive) ----------
    m3 = []
    for g in ("A", "B", "C"):
        for d in DIS:
            x = [r["m3_any"] for r in rows if r["condition"] == g and r["scored_for"] == d]
            if g == "B" and d != "mobility":
                continue   # B's answers are the same 100 for every disability
            k, n = sum(x), len(x)
            lo, hi = wilson(k, n)
            m3.append([g, "all (same 100 answers)" if g == "B" else DIS_NAME[d], f"{k}/{n}", pct(k / n),
                       f"[{100 * lo:.1f}%, {100 * hi:.1f}%]"])
    write_csv("measure3_mentions_summary.csv", ["Condition", "Disability told", "Answers mentioning", "Share", "95% interval"], m3)
    rep += ["## Measure 3: answers that mention a disability word (descriptive)", "",
            md_table(["Condition", "Disability told", "Answers mentioning", "Share", "95% interval (Wilson)"], m3), "",
            "Quoted examples: results/measure3_mentions.csv. Measure 2 flagged sentences: results/measure2_flagged_sentences.csv.", ""]

    # ---------- per interest (no tests) ----------
    pi = []
    for g in ("A", "B", "C"):
        for d in DIS:
            for it in S.INTERESTS:
                x = [r for r in rows if r["condition"] == g and r["scored_for"] == d and r["interest"] == it["interest_key"]]
                if not x:
                    continue
                m1 = [r["m1"] for r in x if r["m1"] is not None]
                pi.append([g, DIS_NAME[d], it["interest_key"], len(x), pct(np.mean([r["main_outcome"] for r in x])),
                           f"{np.mean([r['accessibility'] for r in x]):.2f}",
                           f"{np.mean([r['fully_suitable'] for r in x]):.2f}", f"{np.mean([r['budget'] for r in x]):.2f}",
                           f"{np.mean([r['interest_score'] for r in x]):.2f}", f"{np.mean([r['diversity'] for r in x]):.2f}",
                           f"{np.mean([r['invalid'] for r in x]):.2f}", f"{np.mean(m1):.2f}" if m1 else "-"])
    ph = ["Condition", "Scored for", "Interest", "Answers", "Main outcome yes", "Accessibility", "Fully suitable",
          "Budget", "Interest", "Diversity", "Invalid", "Measure 1"]
    write_csv("per_interest.csv", ph, pi)
    rep += ["## Per interest (percentages and means only; 20 answers per cell, no tests)", "", md_table(ph, pi), ""]

    # ---------- Measure 2: number of picks with an invented facility (descriptive) ----------
    m2 = []
    for g in ("A", "B", "C"):
        for d in DIS:
            if g == "B" and d != "mobility":
                continue   # B's answers are the same 100 for every disability
            x = [r["m2_picks"] for r in rows if r["condition"] == g and r["scored_for"] == d]
            m2.append([g, "all (same 100 answers)" if g == "B" else DIS_NAME[d], len(x), sum(1 for v in x if v),
                       sum(x), f"{np.mean(x):.2f}"])
    mh = ["Condition", "Disability told", "Answers", "Answers with an invented facility", "Picks with one",
          "Mean picks per answer"]
    write_csv("measure2_summary.csv", mh, m2)
    rep += ["## Measure 2: invented facilities, counts (descriptive; the tests are in the secondary table)", "",
            md_table(mh, m2), ""]

    # ---------- rules broken ----------
    rep += ["## Rules broken among the valid picks (descriptive)", "",
            "How many valid picks fail each rule for that traveller (Essential and Important failures together).", ""]
    for d in DIS:
        rids = [r.rule_id for r in S.acc_filter.RULES if r.disability == d]
        sub = []
        for g in ("A", "B", "C"):
            c = Counter()
            n_valid = 0
            for r in rows:
                if r["condition"] == g and r["scored_for"] == d:
                    n_valid += 5 - r["invalid"]
                    for part in r["rules_broken"].split():
                        k, v = part.split(":")
                        c[k] += int(v)
            sub.append([g, DIS_NAME[d], n_valid] + [c.get(k, 0) for k in rids])
        rep += [f"**{DIS_NAME[d]}**", "", md_table(["Condition", "Scored for", "Valid picks"] + rids, sub), ""]
        write_csv(f"rules_broken_{DIS_NAME[d]}.csv", ["Condition", "Scored for", "Valid picks"] + rids, sub)

    # ---------- kinds of place ----------
    cats = list(S.CATEGORY_INFO)
    kp = []
    for g in ("A", "B", "C"):
        for d in DIS:
            if g == "B" and d != "mobility":
                continue
            c = Counter()
            for r in rows:
                if r["condition"] == g and r["scored_for"] == d:
                    c.update(x for x in r["categories"].split() if x != "INVALID")
            total = sum(c.values()) or 1
            kp.append([g, "all" if g == "B" else DIS_NAME[d], total] + [pct(c[k] / total) for k in cats])
    write_csv("kinds_of_place.csv", ["Condition", "Disability told", "Valid picks"] + cats, kp)
    rep += ["## Kinds of place picked (share of valid picks; descriptive)", "",
            md_table(["Condition", "Disability told", "Valid picks"] + cats, kp), ""]

    # ---------- sensitivity check ----------
    sens = []
    for i, (rq, g1, g2, d, m) in enumerate(MAIN, 1):
        if m == "main_outcome":
            r = compare(rows, g1, g2, d, "has_unusable")
            how = "main outcome counting unusable places only (invalid picks ignored)"
        else:
            r = compare(rows, g1, g2, d, m, extra=lambda row: row["invalid"] == 0)
            how = "answers with no invalid pick only"
        sens.append([i, rq, r["comparison"], r["disability"], how, f"{r['n1']} / {r['n2']}", r["summary1"], r["summary2"],
                     r["difference"], r["ci"], r["test"], p_text(r["p"])])
    sh = ["#", "RQ", "Comparison", "Disability", "Version", "Answers", "First group", "Second group", "Difference",
          "95% interval", "Test", "p (uncorrected)"]
    write_csv("sensitivity.csv", sh, sens)
    rep += ["## Sensitivity check: the nine main results without invalid picks (secondary)", "", md_table(sh, sens), ""]

    (RESULTS / "REPORT.md").write_text("\n".join(rep), encoding="utf-8")
    print("Wrote results/REPORT.md and the CSV tables:")
    for r, line in zip(main_res, table):
        print(f"  {line[0]}. {line[1]} {line[2]} {line[3]:<10} {line[4][:40]:<40} p={line[11]:<8} {line[14]}")


if __name__ == "__main__":
    main()
