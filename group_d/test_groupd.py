"""Offline checks for group D (no internet, no API key, no cost). SW350 Group 4.

  python test_groupd.py

Checks that Study 1's files are untouched, that every D request is exactly C's list + A's message, that the
sending code is Study 1's (same settings), and runs the whole D pipeline on 300 FAKE answers in a temporary
folder. Never touches run_D/ or results_D/.
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
import groupd as G

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

print("\nThe D plan")
plan = G.build_plan_d()
s1 = S.build_plan()
by_key = {(r["condition"], r["disability"], r["interest"], r["repeat"]): r for r in s1}
check("300 requests, all different", len(plan) == 300 and len({r["request_id"] for r in plan}) == 300)
cnt = {}
for r in plan:
    cnt[(r["disability"], r["interest"])] = cnt.get((r["disability"], r["interest"]), 0) + 1
check("20 repeats for every traveller and interest (3 x 5 = 15 cells)", len(cnt) == 15 and set(cnt.values()) == {20})
check("D's hidden list is exactly C's (same places, same order) in all 300",
      all(r["list_order"] == by_key[("C", r["disability"], r["interest"], r["repeat"])]["list_order"] for r in plan))
check("places shown: 96 (wheelchair), 124 (blind), 132 (Deaf)",
      {r["disability"]: r["n_places_shown"] for r in plan} == {"mobility": 96, "visual": 124, "hearing": 132})
check("D's message is exactly A's message (with the disability sentence) in all 300",
      all(G.traveller_message_d(r) == S.traveller_message(by_key[("A", r["disability"], r["interest"], r["repeat"])])
          for r in plan))
check("the message contains the disability sentence",
      all(S.DISABILITY_SENTENCE[r["disability"]] in G.traveller_message_d(r) for r in plan))
check("D's hidden part is identical to C's in all 300",
      all(S.hidden_instructions(r) == S.hidden_instructions(by_key[("C", r["disability"], r["interest"], r["repeat"])])
          for r in plan))
check("so D differs from C only by the disability sentence",
      all(G.traveller_message_d(r).replace(" " + S.DISABILITY_SENTENCE[r["disability"]], "")
          == S.traveller_message(by_key[("C", r["disability"], r["interest"], r["repeat"])]) for r in plan))
check("Study 1's messages are unchanged by groupd.py (B and C still have no disability sentence)",
      all(G.traveller_message_d(r) == S.traveller_message(r) for r in s1))

print("\nThe sending code (Study 1's run_requests.py, pointed to run_D)")
REQ = types.SimpleNamespace(method="POST", url="https://api.openai.com/v1/responses")


class FakeResponses:
    def __init__(self):
        self.calls, self.seen = 0, []

    def create(self, **kw):
        self.calls += 1
        self.seen.append(kw)
        ids = re.findall(r"^place_id: (P\d{3})$", kw["instructions"], re.M)
        picks = random.Random(self.calls).sample(ids, 5)
        text = json.dumps({"recommendations": [{"place_id": p, "reason": "fake reason"} for p in picks]})
        usage = types.SimpleNamespace(input_tokens=20000, output_tokens=500, total_tokens=20500,
                                      input_tokens_details=types.SimpleNamespace(cached_tokens=19000, cache_write_tokens=0),
                                      output_tokens_details=types.SimpleNamespace(reasoning_tokens=50))
        content = [types.SimpleNamespace(type="output_text", text=text)]
        return types.SimpleNamespace(id=f"resp_{self.calls}", model=kw["model"], status="completed",
                                     incomplete_details=None, service_tier="default", usage=usage,
                                     output=[types.SimpleNamespace(type="message", content=content)])


import run_d  # noqa: E402  (points Study 1's sending code to group D)
R = run_d.R
check("answers go to run_D (not Study 1's run folder)",
      R.ANSWERS.parent.name == "run_D" and R.PLAN_FILE.parent.name == "run_D")
tmp_run = pathlib.Path(tempfile.mkdtemp(prefix="sw350_D_run_"))
real_run_dir = G.RUN_DIR
try:
    S.RUN_DIR = G.RUN_DIR = tmp_run
    R.ANSWERS, R.FAILURES, R.PLAN_FILE = tmp_run / "answers.jsonl", tmp_run / "technical_errors.jsonl", tmp_run / "plan_requests.csv"
    fake = types.SimpleNamespace(responses=FakeResponses())
    R.make_client = lambda: fake
    with contextlib.redirect_stdout(io.StringIO()):     # the fake run's progress and fake cost are not shown
        run_d.cmd_run()
    lines = R.read_lines(R.ANSWERS)
    check("fake run: 300 answers saved, each once", len(lines) == 300 and len({a["request_id"] for a in lines}) == 300)
    kw = fake.responses.seen[0]
    check("same API settings as Study 1 (model, instructions, input, answer format, cache key, store=False; nothing else)",
          set(kw) == {"model", "instructions", "input", "text", "prompt_cache_key", "store"} and kw["store"] is False
          and kw["model"] == "gpt-6.1-sol", sorted(kw))
    check("every request sent had the disability sentence and C's list",
          all(any(s in k["input"] for s in S.DISABILITY_SENTENCE.values()) for k in fake.responses.seen))
    check("every saved fingerprint matches the D plan",
          all(a["prompt_sha256"] == G.fingerprint_d(next(r for r in plan if r["request_id"] == a["request_id"]))
              for a in lines[:30]))
    check("groupD_started.txt records the time and the file fingerprints",
          (tmp_run / "groupD_started.txt").exists() and "PLAN_D.md SHA-256" in (tmp_run / "groupD_started.txt").read_text())
    check("run_started.txt (Study 1's record) is written in run_D too", (tmp_run / "run_started.txt").exists())
finally:
    S.RUN_DIR = G.RUN_DIR = real_run_dir
    shutil.rmtree(tmp_run, ignore_errors=True)

print("\nScoring and analysis on 300 fake answers (temporary copy of this folder)")
tmp = pathlib.Path(tempfile.mkdtemp(prefix="sw350_D_scoring_"))
try:
    for f in ["study_common.py", "run_requests.py", "score_answers.py", "analyse.py", "groupd.py", "run_d.py",
              "score_d.py", "analyse_d.py", "interests.csv", "PLAN_D.md"]:
        shutil.copy(HERE / f, tmp / f)
    shutil.copytree(S.FILTER_DIR, tmp / S.FILTER_DIR.name, ignore=shutil.ignore_patterns("__pycache__"))
    (tmp / "study1").mkdir()
    shutil.copy(HERE / "study1" / "scores_per_answer.csv", tmp / "study1" / "scores_per_answer.csv")
    (tmp / "run_D").mkdir()
    rng = random.Random(7)

    def fake_answer(r, picks=None):
        shown = r["list_order"].split()
        picks = picks if picks is not None else rng.sample(shown, 5)
        return {"kind": "answer", "request_id": r["request_id"], "condition": "D", "disability": r["disability"],
                "interest": r["interest"], "repeat": r["repeat"], "run_position": r["run_position"],
                "list_variant": r["list_variant"], "n_places_shown": r["n_places_shown"], "list_order": r["list_order"],
                "model_requested": "fake", "sent_at": "2026-01-01T00:00:00+03:00", "received_at": "2026-01-01T00:00:01+03:00",
                "seconds": 1.0, "attempts": 1, "technical_errors": [], "traveller_message": G.traveller_message_d(r),
                "prompt_sha256": G.fingerprint_d(r), "response_id": "fake", "model_returned": "fake",
                "status": "completed", "incomplete_reason": None, "service_tier": "default", "output_text": "",
                "refusal": None, "parse_error": None,
                "parsed": {"recommendations": [{"place_id": p, "reason": "Good for a Deaf visitor."} for p in picks]},
                "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2, "cached_tokens": 0,
                          "cache_write_tokens": 0, "reasoning_tokens": 0}}

    recs = [fake_answer(r) for r in plan]
    recs[0] = fake_answer(plan[0], picks=plan[0]["list_order"].split()[:3])     # 3 picks: 2 invalid

    def write(records):
        with open(tmp / "run_D" / "answers.jsonl", "w", encoding="utf-8") as fh:
            for x in records:
                fh.write(json.dumps(x) + "\n")

    def run(script):
        env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        return subprocess.run([sys.executable, script], cwd=tmp, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env)

    bad = dict(recs[3], prompt_sha256="0" * 64)
    write(recs[:3] + [bad] + recs[4:])
    out = run("score_d.py")
    check("score_d.py stops if a request was not sent as planned", out.returncode != 0 and "STOP" in out.stdout + out.stderr)
    write(recs[:-1])
    out = run("score_d.py")
    check("score_d.py stops if an answer is missing", out.returncode != 0 and "STOP" in out.stdout + out.stderr)
    write(recs)
    out = run("score_d.py")
    check("score_d.py scores 300 fake answers", out.returncode == 0, out.stderr[-600:])
    rows = list(csv.DictReader(open(tmp / "results_D" / "scores_D.csv", newline="", encoding="utf-8")))
    check("300 rows, condition D, scored for the traveller's own disability",
          len(rows) == 300 and all(r["condition"] == "D" and r["scored_for"] == r["disability_told"] for r in rows))
    r0 = next(r for r in rows if r["request_id"] == plan[0]["request_id"])
    check("the 3-pick fake answer has 2 invalid picks (Study 1's rule)", r0["invalid"] == "2", r0["invalid"])
    check("D's main outcome is 'no' unless a pick is invalid (the filter removed the unusable places)",
          all(r["has_unusable"] == "0" for r in rows))
    out = run("analyse_d.py")
    check("analyse_d.py runs", out.returncode == 0, out.stderr[-800:])
    if out.returncode == 0:
        res = list(csv.reader(open(tmp / "results_D" / "D_results.csv", encoding="utf-8")))[1:]
        check("six D results, with Holm over six (smallest threshold 0.05/6)", len(res) == 6 and
              abs(min(float(x[11]) for x in res) - round(0.05 / 6, 4)) < 1e-9, [x[11] for x in res])
        check("REPORT_D.md written", (tmp / "results_D" / "REPORT_D.md").exists())
        ov = list(csv.reader(open(tmp / "results_D" / "overview_ABCD.csv", encoding="utf-8")))[1:]
        check("overview has A, B, C and D for each traveller (12 rows)", len(ov) == 12)
        a_row = next(x for x in ov if x[0] == "wheelchair" and x[1] == "A")
        check("Study 1's numbers are carried over unchanged (wheelchair A: 33.0%, fully suitable 4.46)",
              a_row[3] == "33.0%" and a_row[5] == "4.46", a_row)
    (tmp / "study1" / "scores_per_answer.csv").write_text("changed", encoding="utf-8")
    out = run("analyse_d.py")
    check("analyse_d.py refuses a changed Study 1 scores file", out.returncode != 0 and "STOP" in out.stdout + out.stderr)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\nNo API key in any file")
check("no key-like text in the code", not any(re.search(r"sk-[A-Za-z0-9_-]{20,}", f.read_text(encoding="utf-8"))
                                              for f in HERE.glob("*.py")))

print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
if FAILED:
    sys.exit(1)
