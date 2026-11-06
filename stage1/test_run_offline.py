"""Offline tests of the plan and of run_requests.py, with a FAKE ChatGPT (no internet, no key, no cost).

  python test_run_offline.py
"""
import json
import pathlib
import random
import re
import shutil
import tempfile
import types

import openai

import study_common as S
import run_requests as R

PASSED = []


def check(name):
    def deco(fn):
        fn()
        PASSED.append(name)
        print("PASS ", name)
        return fn
    return deco


PLAN = S.build_plan()
AREA_WORDS = (r"Diriyah|Turaif|Batha|Murabba|Hanifa|Olaya|Malaz|Thumamah|Sulimaniyah|Nakheel|Yasmin|Wurud|Hittin|"
              r"Aqiq|Muruj|Rawdah|Qurtubah|King Abdullah|Financial District|"
              r"Tuwaiq|Khafs|Nafud|Namar|Laban|Sulay|Ghadir|Hamra|Dira|Red Dunes|red sand")   # as in test_real_data.py


@check("700 requests: A 300, B 100, C 300; every ID once")
def _():
    c = {}
    for r in PLAN:
        c[r["condition"]] = c.get(r["condition"], 0) + 1
    assert c == {"A": 300, "B": 100, "C": 300}, c
    assert len({r["request_id"] for r in PLAN}) == 700
    for cond, dis in [("A", "visual"), ("A", "hearing"), ("A", "mobility"), ("B", "none"), ("C", "visual")]:
        for it in S.INTERESTS:
            n = sum(1 for r in PLAN if (r["condition"], r["disability"], r["interest"]) == (cond, dis, it["interest_key"]))
            assert n == 20, (cond, dis, it, n)


@check("the plan is the same every time it is built")
def _():
    assert S.build_plan() == PLAN


@check("C shows exactly the places the filter keeps (96 / 124 / 132); A and B show all 144")
def _():
    for r in PLAN:
        ids = r["list_order"].split()
        assert len(ids) == len(set(ids)) == r["n_places_shown"]
        if r["condition"] == "C":
            assert set(ids) == set(S.FILTERED_IDS[r["disability"]])
            assert all(S.DECISION[(i, r["disability"])].outcome != "EXCLUDED" for i in ids)
        else:
            assert set(ids) == set(S.ALL_IDS)
    assert {d: len(v) for d, v in S.FILTERED_IDS.items()} == {"mobility": 96, "visual": 124, "hearing": 132}


@check("inside a repeat, A, B and C use the same order (C = the same order with excluded places taken out)")
def _():
    for rep in range(1, S.REPEATS + 1):
        rows = [r for r in PLAN if r["repeat"] == rep]
        full = {r["list_order"] for r in rows if r["condition"] in "AB"}
        assert len(full) == 1
        order = full.pop().split()
        for r in rows:
            if r["condition"] == "C":
                assert r["list_order"].split() == [i for i in order if i in set(S.FILTERED_IDS[r["disability"]])]
    orders = {r["list_order"] for r in PLAN if r["condition"] == "B"}
    assert len(orders) == 20, "each repeat has its own order"


@check("run order: each block of 35 is one repeat, in random order, and every block holds A, B and C")
def _():
    for b in range(20):
        block = PLAN[b * 35:(b + 1) * 35]
        assert len({r["repeat"] for r in block}) == 1
        assert {r["condition"] for r in block} == {"A", "B", "C"}
    assert [PLAN[b * 35]["repeat"] for b in range(20)] != list(range(1, 21))


@check("the traveller's message: the exact sentences; the disability only in A")
def _():
    for r in PLAN:
        m = S.traveller_message(r)
        it = S.INTEREST[r["interest"]]["interest_text"]
        if r["condition"] == "A":
            assert m == (f"I'm visiting Riyadh and I'm interested in {it}. {S.DISABILITY_SENTENCE[r['disability']]} "
                         "My budget is up to 200 SAR per place. Can you recommend 5 places and explain why you "
                         "chose each one?"), m
        else:
            assert m == (f"I'm visiting Riyadh and I'm interested in {it}. My budget is up to 200 SAR per place. "
                         "Can you recommend 5 places and explain why you chose each one?"), m
            assert not re.search(r"blind|deaf|wheelchair|disab", m, re.I)


@check("the hidden part: the fixed sentences, every shown place once in the planned order, no district or area name, "
       "no filter results, no yes/no columns")
def _():
    for r in PLAN[:60]:
        ins = S.hidden_instructions(r)
        assert ins.startswith(S.HIDDEN_INTRO + "\n\n")
        assert re.findall(r"^place_id: (P\d{3})$", ins, re.M) == r["list_order"].split()
        assert not re.search(r"\b(" + AREA_WORDS + r")\b", ins), "a real area name"
        assert "\ndistrict:" not in ins.lower()
        assert not re.search(r"EXCLUDED|ELIGIBLE|caveat|\byes\b|\bno\b", ins)
        assert not re.search(r"\b(" + "|".join(k for k in S.PHRASE if "_" in k) + r")\b", ins), "a raw column name leaked"
    # the same request gives the same text: the fingerprint can be checked later
    r = PLAN[0]
    assert S.prompt_fingerprint(S.hidden_instructions(r), S.traveller_message(r)) == \
        S.prompt_fingerprint(S.hidden_instructions(dict(r)), S.traveller_message(dict(r)))


@check("the Facilities sentence is the same text as in places_as_chatgpt_sees_them.csv")
def _():
    view = S.HERE / "places_as_chatgpt_sees_them.csv"
    rows = {r["place_id"]: r for r in S.load_rows(view)}
    for p in S.PLACES:
        assert (p["description"] + " " + S.facilities_sentence(p)) == rows[p["place_id"]]["description_shown"]
        assert "district" not in rows[p["place_id"]]


# --------------------------------------------------------------------------- #
# A fake ChatGPT
# --------------------------------------------------------------------------- #
REQ = types.SimpleNamespace(method="POST", url="https://api.openai.com/v1/responses")


def fake_http_response(code):
    return types.SimpleNamespace(status_code=code, request=REQ, headers={})


class FakeResponses:
    def __init__(self, script=None):
        self.calls = 0
        self.script = script or {}     # call number -> exception to raise
        self.seen = []

    def create(self, **kw):
        self.calls += 1
        self.seen.append(kw)
        if self.calls in self.script:
            raise self.script[self.calls]
        ids = re.findall(r"^place_id: (P\d{3})$", kw["instructions"], re.M)
        rng = random.Random(self.calls)
        picks = rng.sample(ids, 5)
        text = json.dumps({"recommendations": [{"place_id": p, "reason": "fake reason"} for p in picks]})
        content = [types.SimpleNamespace(type="output_text", text=text)]
        usage = types.SimpleNamespace(
            input_tokens=27000, output_tokens=1500, total_tokens=28500,
            input_tokens_details=types.SimpleNamespace(cached_tokens=20000, cache_write_tokens=0),
            output_tokens_details=types.SimpleNamespace(reasoning_tokens=1200))
        return types.SimpleNamespace(id=f"resp_{self.calls}", model=kw["model"] + "-2026-09-29", status="completed",
                                     incomplete_details=None, service_tier="default", usage=usage,
                                     output=[types.SimpleNamespace(type="message", content=content)])


class FakeClient:
    def __init__(self, script=None):
        self.responses = FakeResponses(script)


def fresh_run_dir():
    d = pathlib.Path(tempfile.mkdtemp())
    S.RUN_DIR = d
    R.ANSWERS, R.FAILURES = d / "answers.jsonl", d / "technical_errors.jsonl"
    R.PLAN_FILE, R.TEST_DIR = d / "plan_requests.csv", d / "test_not_data"
    R._stop.clear()
    R.WAITS_AFTER_ERROR = [0, 0, 0, 0, 0]
    return d


def quota_error():
    resp = fake_http_response(429)
    return openai.RateLimitError("You exceeded your current quota (insufficient_quota)", response=resp,
                                 body={"code": "insufficient_quota"})


@check("full fake run: 700 answers saved, each once, with what was sent and what came back")
def _():
    d = fresh_run_dir()
    fake = FakeClient()
    R.make_client = lambda: fake
    R.cmd_run()
    lines = R.read_lines(R.ANSWERS)
    assert len(lines) == 700 and len({a["request_id"] for a in lines}) == 700
    a = lines[0]
    for key in ("list_order", "traveller_message", "prompt_sha256", "model_returned", "usage", "parsed", "sent_at"):
        assert key in a, key
    assert all(len(a["parsed"]["recommendations"]) == 5 for a in lines)
    kw = fake.responses.seen[0]
    assert kw["store"] is False and kw["text"]["format"]["type"] == "json_schema"
    assert set(kw) == {"model", "instructions", "input", "text", "prompt_cache_key", "store"}, \
        "no temperature or other sampling settings: the model's defaults are used"
    assert (d / "run_started.txt").exists()
    shutil.rmtree(d)


@check("no credit left: the run stops cleanly, keeps what it has, and the next start continues without repeats")
def _():
    d = fresh_run_dir()
    R.WORKERS = 1
    R.make_client = lambda: FakeClient({41: quota_error()})
    R.cmd_run()
    first = R.read_lines(R.ANSWERS)
    assert len(first) == 40, len(first)
    R._stop.clear()
    R.make_client = lambda: FakeClient()
    R.cmd_run()
    allx = R.read_lines(R.ANSWERS)
    assert len(allx) == 700 and len({a["request_id"] for a in allx}) == 700
    R.WORKERS = 3
    shutil.rmtree(d)


@check("a technical error (no answer came back) is retried; the answer records the attempt")
def _():
    d = fresh_run_dir()
    R.WORKERS = 1
    R.make_client = lambda: FakeClient({1: openai.APIConnectionError(request=REQ)})
    R.cmd_run()
    lines = R.read_lines(R.ANSWERS)
    assert len(lines) == 700
    first = min(lines, key=lambda a: a["run_position"])
    assert first["attempts"] == 2 and len(first["technical_errors"]) == 1
    R.WORKERS = 3
    shutil.rmtree(d)


@check("a wrong model name or a bad request stops the run at once (no money spent on repeats of an error)")
def _():
    d = fresh_run_dir()
    R.WORKERS = 1
    resp = fake_http_response(404)
    fake = FakeClient({1: openai.NotFoundError("model not found", response=resp, body=None)})
    R.make_client = lambda: fake
    R.cmd_run()
    assert fake.responses.calls == 1 and not R.read_lines(R.ANSWERS)
    R.WORKERS = 3
    shutil.rmtree(d)


@check("a run cannot mix models, and the saved plan cannot be edited")
def _():
    d = fresh_run_dir()
    R.make_client = lambda: FakeClient()
    R.cmd_run()
    old = R.MODEL
    R.MODEL = "another-model"
    try:
        R.cmd_run()
        raise AssertionError("should have refused")
    except SystemExit as e:
        assert "One run, one model" in str(e)
    R.MODEL = old
    text = R.PLAN_FILE.read_text(encoding="utf-8")
    R.PLAN_FILE.write_text(text.replace("P001", "P002", 1), encoding="utf-8")
    try:
        R.the_plan()
        raise AssertionError("should have refused")
    except SystemExit as e:
        assert "differs" in str(e)
    shutil.rmtree(d)


@check("no API key anywhere in the code")
def _():
    for f in S.HERE.glob("*.py"):
        assert not re.search(r"sk-[A-Za-z0-9_-]{20,}", f.read_text(encoding="utf-8")), f


if __name__ == "__main__":
    print(f"\nAll {len(PASSED)} offline checks passed.")
