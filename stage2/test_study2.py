"""Offline checks for Study 2, E1 and E2 (no internet, no API key, no cost). SW350 Group 4.

  python test_study2.py

Checks that Study 1's files are untouched, that every request is built as PLAN_E.md says, that the sending code
is Study 1's (same settings), and runs the whole pipeline on 1,000 FAKE answers in a temporary folder.
Never touches run_E/ or results_E/.
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
import tempfile
import types

import study_common as S
import e_common as E

PASSED, FAILED = [], []
HERE = S.HERE


def check(name, ok, detail=""):
    (PASSED if ok else FAILED).append(name)
    print(("  ok    " if ok else "  FAIL  ") + name + ("" if ok else f"   <-- {detail}"))


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


print("Study 1 is untouched")
STUDY1 = {"study_common.py": "8d419f4ab2b28049fa75d45bef272529323cee7776921ab48b5bea4eb48cbf7f",
          "run_requests.py": "ea162df1c7906f09152aa03e3ef7fce090f5fb5c00689fcbc264e29c3d598596",
          "score_answers.py": "0eec64a6481ed12df4a88901efb5b0bce0aded088525f9d5c2270e5f3bf30486",
          "analyse.py": "e3856b57235371cc7bbe239775659de83f42b6bf344b48df95ddd3281320293e",
          "study1/scores_per_answer.csv": "c617e7743e938a474b70d21982448e38b316a4f3a9c6c9c18ff4c27526280e5d"}
for f, h in STUDY1.items():
    check(f"{f} is Study 1's file (SHA-256 {h[:8]}...)", sha(HERE / f) == h, sha(HERE / f))
try:
    S.check_frozen()
    check("filter v7.4, places and categories are the frozen versions", True)
except SystemExit as e:
    check("filter v7.4, places and categories are the frozen versions", False, e)

fab1 = list(csv.DictReader(open(HERE / "study1" / "fabrication_study1.csv", newline="", encoding="utf-8")))
check("study1/fabrication_study1.csv is the file computed on 29 Oct (SHA-256 b0c24787...)",
      sha(HERE / "study1" / "fabrication_study1.csv") == "b0c24787dbfb183d89d5235ef1c21db325a1fbaa1dbbda44e82338594df7edc0")
found = sorted(r["request_id"] for r in fab1 if r["unsupported_any"] == "1")
check("the fabrication rule finds in Study 1 exactly the 3 answers found by reading (A, Deaf)",
      found == ["A_hearing_art_r15", "A_hearing_shopping_r14", "A_hearing_shopping_r15"], found)

print("\nThe Study 2 plan")
plan = E.build_plan_e()
cnt = {}
for r in plan:
    cnt[r["condition"]] = cnt.get(r["condition"], 0) + 1
check("1,000 requests, all different: E1T 300, E1N 300, E2T 300, E2N 100",
      len({r["request_id"] for r in plan}) == 1000 and cnt == {"E1T": 300, "E1N": 300, "E2T": 300, "E2N": 100}, cnt)
cells = {}
for r in plan:
    cells[(r["condition"], r["disability"], r["interest"])] = cells.get((r["condition"], r["disability"], r["interest"]), 0) + 1
check("20 repeats in every cell", set(cells.values()) == {20}, set(cells.values()))
check("E1 lists hold only fully usable places (72 per traveller)",
      all(len(r["list_order"].split()) == 72 and all(S.DECISION[(i, r["disability"])].outcome == "ELIGIBLE"
                                                       for i in r["list_order"].split())
          for r in plan if r["condition"].startswith("E1")))
check("E1 lists keep Study 1's order for the repeat",
      all(r["list_order"].split() == [i for i in S.repeat_order(r["repeat"]) if i in set(r["list_order"].split())]
          for r in plan if r["condition"].startswith("E1")))
check("E2 lists hold all 144 places in Study 1's order for the repeat",
      all(r["list_order"].split() == S.repeat_order(r["repeat"]) for r in plan if r["condition"].startswith("E2")))
by = {(r["condition"], r["disability"], r["interest"], r["repeat"]): r for r in plan}
pairs = [(by[("E1T", d, k, rep)], by[("E1N", d, k, rep)]) for (c, d, k, rep) in by if c == "E1T"]
check("E1: told and not told see the same hidden part, in all 300 pairs",
      all(E.hidden_instructions_e(t) == E.hidden_instructions_e(n) for t, n in pairs))
check("E1: the only difference is the disability sentence",
      all(E.traveller_message_e(t).replace(" " + S.DISABILITY_SENTENCE[t["disability"]], "") == E.traveller_message_e(n)
          for t, n in pairs))
ex1 = E.hidden_instructions_e(plan[[r["condition"] for r in plan].index("E1T")])
check("E1 places are shown with their Facilities sentence", ex1.count("Facilities:") == 72)
e2 = [r for r in plan if r["condition"].startswith("E2")]
ins2 = E.hidden_instructions_e(e2[0])
check("E2 hidden part has no Facilities sentence and lists 144 places",
      "Facilities:" not in ins2 and ins2.count("place_id: ") == 144)
s1_c = next(r for r in S.build_plan() if r["condition"] == "B" and r["repeat"] == e2[0]["repeat"])
s1_text = S.hidden_instructions(s1_c)
check("E2 hidden part = Study 1's, with only the Facilities sentences removed",
      re.sub(r" Facilities: [^\n]*", "", s1_text) == ins2)
check("E2: told and not told see the same hidden part in each repeat",
      len({E.hidden_instructions_e(r) for r in e2 if r["repeat"] == e2[0]["repeat"]}) == 1)
check("E2N has no disability sentence; E2T has the traveller's own",
      all(not any(s in E.traveller_message_e(r) for s in S.DISABILITY_SENTENCE.values()) for r in e2 if r["condition"] == "E2N")
      and all(S.DISABILITY_SENTENCE[r["disability"]] in E.traveller_message_e(r) for r in e2 if r["condition"] == "E2T"))
check("Study 1's prompts are unchanged by e_common.py",
      all(E.traveller_message_e(r) == S.traveller_message(dict(r, condition="A" if r["condition"] == "E1T" else "B"))
          for r in plan if r["condition"].startswith("E1")))

print("\nThe sending code (Study 1's run_requests.py, pointed to run_E)")


class FakeResponses:
    def __init__(self):
        self.calls, self.seen = 0, []

    def create(self, **kw):
        self.calls += 1
        self.seen.append(kw)
        ids = re.findall(r"^place_id: (P\d{3})$", kw["instructions"], re.M)
        picks = random.Random(self.calls).sample(ids, 5)
        text = json.dumps({"recommendations": [{"place_id": p, "reason": "fake reason"} for p in picks]})
        usage = types.SimpleNamespace(input_tokens=15000, output_tokens=500, total_tokens=15500,
                                      input_tokens_details=types.SimpleNamespace(cached_tokens=14000, cache_write_tokens=0),
                                      output_tokens_details=types.SimpleNamespace(reasoning_tokens=50))
        content = [types.SimpleNamespace(type="output_text", text=text)]
        return types.SimpleNamespace(id=f"resp_{self.calls}", model=kw["model"], status="completed",
                                     incomplete_details=None, service_tier="default", usage=usage,
                                     output=[types.SimpleNamespace(type="message", content=content)])


import run_e  # noqa: E402
R = run_e.R
check("answers go to run_E (not Study 1's run folder)",
      R.ANSWERS.parent.name == "run_E" and R.PLAN_FILE.parent.name == "run_E")
tmp_run = pathlib.Path(tempfile.mkdtemp(prefix="sw350_E_run_"))
real_run_dir = E.RUN_DIR
try:
    S.RUN_DIR = E.RUN_DIR = tmp_run
    R.ANSWERS, R.FAILURES, R.PLAN_FILE = tmp_run / "answers.jsonl", tmp_run / "technical_errors.jsonl", tmp_run / "plan_requests.csv"
    fake = types.SimpleNamespace(responses=FakeResponses())
    R.make_client = lambda: fake
    with contextlib.redirect_stdout(io.StringIO()):
        run_e.cmd_run()
    lines = R.read_lines(R.ANSWERS)
    check("fake run: 1,000 answers saved, each once", len(lines) == 1000 and len({a["request_id"] for a in lines}) == 1000)
    kw = fake.responses.seen[0]
    check("same API settings as Study 1 (nothing else sent)",
          set(kw) == {"model", "instructions", "input", "text", "prompt_cache_key", "store"} and kw["store"] is False
          and kw["model"] == "gpt-6.1-sol", sorted(kw))
    check("E2 requests were sent without any Facilities sentence",
          all("Facilities:" not in k["instructions"] for k in fake.responses.seen if k["instructions"].count("place_id: ") == 144))
    pl = {r["request_id"]: r for r in plan}
    check("every saved fingerprint matches the plan", all(a["prompt_sha256"] == E.fingerprint_e(pl[a["request_id"]]) for a in lines))
    check("study2_started.txt records the time and the file fingerprints",
          (tmp_run / "study2_started.txt").exists() and "PLAN_E.md SHA-256" in (tmp_run / "study2_started.txt").read_text())
finally:
    S.RUN_DIR = E.RUN_DIR = real_run_dir
    shutil.rmtree(tmp_run, ignore_errors=True)

print("\nScoring and analysis on 1,000 fake answers (temporary copy of this folder)")
tmp = pathlib.Path(tempfile.mkdtemp(prefix="sw350_E_scoring_"))
try:
    for f in ["study_common.py", "run_requests.py", "score_answers.py", "analyse.py", "e_common.py", "run_e.py",
              "score_e.py", "analyse_e.py", "fabrication.py", "interests.csv", "PLAN_E.md"]:
        shutil.copy(HERE / f, tmp / f)
    shutil.copytree(S.FILTER_DIR, tmp / S.FILTER_DIR.name, ignore=shutil.ignore_patterns("__pycache__"))
    (tmp / "study1").mkdir()
    shutil.copy(HERE / "study1" / "scores_per_answer.csv", tmp / "study1" / "scores_per_answer.csv")
    shutil.copy(HERE / "study1" / "fabrication_study1.csv", tmp / "study1" / "fabrication_study1.csv")
    (tmp / "run_E").mkdir()
    rng = random.Random(11)

    def fake_answer(r, picks=None):
        shown = r["list_order"].split()
        picks = picks if picks is not None else rng.sample(shown, 5)
        return {"kind": "answer", "request_id": r["request_id"], "condition": r["condition"], "disability": r["disability"],
                "interest": r["interest"], "repeat": r["repeat"], "run_position": r["run_position"],
                "list_variant": r["list_variant"], "n_places_shown": r["n_places_shown"], "list_order": r["list_order"],
                "model_requested": "fake", "sent_at": "2026-01-01T00:00:00+03:00", "received_at": "2026-01-01T00:00:01+03:00",
                "seconds": 1.0, "attempts": 1, "technical_errors": [], "traveller_message": E.traveller_message_e(r),
                "prompt_sha256": E.fingerprint_e(r), "response_id": "fake", "model_returned": "fake",
                "status": "completed", "incomplete_reason": None, "service_tier": "default", "output_text": "",
                "refusal": None, "parse_error": None,
                "parsed": {"recommendations": [{"place_id": p, "reason": FAKE_REASON.get(r["condition"], "fake")} for p in picks]},
                "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2, "cached_tokens": 0,
                          "cache_write_tokens": 0, "reasoning_tokens": 0}}

    FAKE_REASON = {"E2T": "It has a ramp at the entrance.", "E2N": "A ramp is not listed, so check before visiting."}
    recs = [fake_answer(r) for r in plan]

    def write(records):
        with open(tmp / "run_E" / "answers.jsonl", "w", encoding="utf-8") as fh:
            for x in records:
                fh.write(json.dumps(x) + "\n")

    def run(script):
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, script], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env)

    bad = dict(recs[3], prompt_sha256="0" * 64)
    write(recs[:3] + [bad] + recs[4:])
    out = run("score_e.py")
    check("score_e.py stops if a request was not sent as planned", out.returncode != 0 and "STOP" in out.stdout + out.stderr)
    write(recs[:-1])
    out = run("score_e.py")
    check("score_e.py stops if an answer is missing", out.returncode != 0 and "STOP" in out.stdout + out.stderr)
    write(recs)
    out = run("score_e.py")
    check("score_e.py scores 1,000 fake answers", out.returncode == 0, out.stderr[-600:])
    rows = list(csv.DictReader(open(tmp / "results_E" / "scores_E.csv", newline="", encoding="utf-8")))
    check("1,200 rows: E1T 300, E1N 300, E2T 300, E2N 100 x 3 travellers", len(rows) == 1200, len(rows))
    check("E1 fake answers never contain a place she cannot use (all places fully usable)",
          all(r["main_outcome"] == "0" and r["fully_suitable"] == "5" for r in rows if r["condition"].startswith("E1")))
    applies = sum(1 for r in rows if r["condition"] == "E1T" and r["m1_all"] != "")
    check("linked kinds of place measured for 160 E1T answers (60 + 60 + 40)", applies == 160, applies)
    e2t = [r for r in rows if r["condition"] == "E2T"]
    e2n = [r for r in rows if r["condition"] == "E2N"]
    check("E2: a facility claim counts as unsupported, since nothing was shown (fabrication rule)",
          all(r["unsupported_any"] == "1" and r["unsupported_picks"] == "5" for r in e2t))
    check("E2: Measure 2's planned rule also counts it (checked against what was shown: nothing)",
          all(r["m2_any"] == "1" for r in e2t))
    check("E2: \"a ramp is not listed\" is not a claim under the fabrication rule (negation after the phrase)",
          all(r["unsupported_any"] == "0" for r in e2n))
    check("false claims = claims about a facility the place does not have",
          all(int(r["false_picks"]) == sum(1 for pid in r["picks"].split() if S.PLACE[pid]["entrance_ramp"] != "yes")
              for r in e2t))
    out = run("analyse_e.py")
    check("analyse_e.py runs", out.returncode == 0, out.stderr[-800:])
    if out.returncode == 0:
        res = list(csv.reader(open(tmp / "results_E" / "E_main_results.csv", encoding="utf-8")))[1:]
        check("nine main results, Holm over nine (smallest threshold 0.05/9)",
              len(res) == 9 and abs(min(float(x[11]) for x in res) - round(0.05 / 9, 4)) < 1e-9, [x[11] for x in res])
        check("REPORT_E.md written", (tmp / "results_E" / "REPORT_E.md").exists())
        fres = list(csv.reader(open(tmp / "results_E" / "E_fabrication_results.csv", encoding="utf-8")))[1:]
        check("six fabrication results, Holm over six (smallest threshold 0.05/6)",
              len(fres) == 6 and abs(min(float(x[11]) for x in fres) - round(0.05 / 6, 4)) < 1e-9, [x[11] for x in fres])
        ov = list(csv.reader(open(tmp / "results_E" / "overview_E.csv", encoding="utf-8")))[1:]
        a_row = next(x for x in ov if x[0] == "wheelchair" and x[1].startswith("A "))
        check("Study 1's numbers carried over unchanged (wheelchair A: 33.0%, fully suitable 4.46)",
              a_row[3] == "33.0%" and a_row[5] == "4.46", a_row)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\nNo API key in any file")
check("no key-like text in the code", not any(re.search(r"sk-[A-Za-z0-9_-]{20,}", f.read_text(encoding="utf-8"))
                                              for f in HERE.glob("*.py")))

print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
if FAILED:
    sys.exit(1)
