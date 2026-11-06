"""Send the study's requests to ChatGPT (OpenAI API) and save every answer. SW350 Group 4.

Steps (from this folder, with the key in the OPENAI_API_KEY environment variable; never paste the key in a file):
  python run_requests.py --check            no internet: checks the frozen data, writes run/plan_requests.csv,
                                            prints one full example prompt
  python run_requests.py --models           lists the model names your account can use (find the dated name)
  python run_requests.py --test             ONE request (not study data): shows the answer, tokens and cost
  python run_requests.py --run              the study: 700 requests; safe to stop and start again
  python run_requests.py --status           progress, tokens and estimated cost so far

Rules kept by this script:
  - default model settings; every request is a new conversation (nothing is carried between requests);
  - the same wording in every repeat; only the list order changes between repeats (see study_common.py);
  - a request is sent again only after a technical error (no answer came back). Every answer that came back
    is kept and scored, whatever it says;
  - the run refuses to start if the filter or the data differ from the frozen versions, and refuses to mix
    model names inside one run.
"""
import argparse
import datetime
import json
import os
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import study_common as S

# --------------------------------------------------------------------------- #
# Settings. MODEL: replace with the dated name if --models shows one (e.g. gpt-6.1-sol-2026-09-29).
# --------------------------------------------------------------------------- #
MODEL = "gpt-6.1-sol"
WORKERS = 3                     # requests in flight at the same time
TIMEOUT_SECONDS = 900           # one request may take minutes (the model thinks before answering)
WAITS_AFTER_ERROR = [10, 30, 90, 180, 300]   # seconds; then the request is left for the next start
# Prices in US dollars per 1 million tokens (input, cached input, cache write, output), ONLY for the
# cost estimate printed by --test and --status.
# Check them on the OpenAI pricing page before the run; they do not change what is sent.
PRICE_INPUT, PRICE_CACHED_INPUT, PRICE_CACHE_WRITE, PRICE_OUTPUT = 2.00, 0.10, 2.50, 10.00

ANSWERS = S.RUN_DIR / "answers.jsonl"
FAILURES = S.RUN_DIR / "technical_errors.jsonl"
PLAN_FILE = S.RUN_DIR / "plan_requests.csv"
TEST_DIR = S.RUN_DIR / "test_not_data"

_lock = threading.Lock()
_stop = threading.Event()


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")


def append_line(path: pathlib.Path, record: dict) -> None:
    """One JSON object per line, written and flushed at once, so a crash loses at most the request in flight."""
    with _lock:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())


def read_lines(path: pathlib.Path) -> list:
    if not path.exists():
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"  note: line {n} of {path.name} is incomplete (probably cut off by a stop); it is ignored.")
    return out


def the_plan() -> list:
    """Build the plan; if a saved plan exists it must be identical (the plan never changes once written)."""
    S.RUN_DIR.mkdir(exist_ok=True)
    plan = S.build_plan()
    tmp = S.RUN_DIR / "_plan_check.csv"
    S.write_plan(plan, tmp)
    if PLAN_FILE.exists():
        if PLAN_FILE.read_bytes() != tmp.read_bytes():
            tmp.unlink()
            raise SystemExit("STOP: run/plan_requests.csv differs from the plan the code builds. Do not edit it.")
        tmp.unlink()
    else:
        tmp.replace(PLAN_FILE)
    return plan


# --------------------------------------------------------------------------- #
# One request
# --------------------------------------------------------------------------- #
def make_client():
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit("The OpenAI library is missing. Install it with:  pip install openai")
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set in this terminal (see README_RUN.md, step 3).")
    return OpenAI(timeout=TIMEOUT_SECONDS, max_retries=0)   # retries are done (and logged) here


def read_response(resp) -> dict:
    """Everything useful from the API's answer object."""
    text_parts, refusals = [], []
    for item in resp.output or []:
        if getattr(item, "type", None) == "message":
            for c in item.content or []:
                if c.type == "output_text":
                    text_parts.append(c.text or "")
                elif c.type == "refusal":
                    refusals.append(getattr(c, "refusal", "") or "")
    text = "".join(text_parts)
    parsed, parse_error = None, None
    if text:
        try:
            parsed = json.loads(text)
            if not isinstance(parsed, dict) or not isinstance(parsed.get("recommendations"), list):
                parse_error = "JSON without a 'recommendations' list"
        except json.JSONDecodeError as e:
            parse_error = f"not valid JSON: {e}"
    else:
        parse_error = "no text in the answer"
    u = resp.usage
    usage = None
    if u is not None:
        itd = getattr(u, "input_tokens_details", None)
        otd = getattr(u, "output_tokens_details", None)
        usage = {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens, "total_tokens": u.total_tokens,
                 "cached_tokens": getattr(itd, "cached_tokens", None) if itd else None,
                 "cache_write_tokens": getattr(itd, "cache_write_tokens", None) if itd else None,
                 "reasoning_tokens": getattr(otd, "reasoning_tokens", None) if otd else None}
    inc = getattr(resp, "incomplete_details", None)
    return {"response_id": resp.id, "model_returned": resp.model, "status": resp.status,
            "incomplete_reason": getattr(inc, "reason", None) if inc else None,
            "service_tier": getattr(resp, "service_tier", None),
            "output_text": text, "refusal": " ".join(refusals) or None,
            "parsed": parsed, "parse_error": parse_error, "usage": usage}


class StopRun(Exception):
    """A problem that more requests would not fix (no credit, wrong key, wrong model name...)."""


def send(client, request: dict, model: str) -> dict:
    """Send one request. Returns the answer record, or raises StopRun. Technical errors are retried."""
    import openai
    instructions = S.hidden_instructions(request)
    message = S.traveller_message(request)
    errors = []
    for attempt in range(1, len(WAITS_AFTER_ERROR) + 2):
        if _stop.is_set():
            raise StopRun("stopped")
        sent = now()
        t0 = time.time()
        try:
            resp = client.responses.create(
                model=model,
                instructions=instructions,
                input=message,
                text={"format": S.ANSWER_FORMAT},
                prompt_cache_key=request["cache_key"],
                store=False,
            )
        except openai.RateLimitError as e:
            body = str(e)
            if getattr(e, "code", None) == "insufficient_quota" or "quota" in body.lower():
                raise StopRun("NO CREDIT LEFT (insufficient_quota). Add credit, then run --run again: "
                              "it continues where it stopped.")
            errors.append(f"{sent} rate limit: {body[:300]}")
        except (openai.APIConnectionError, openai.APITimeoutError, openai.InternalServerError) as e:
            errors.append(f"{sent} {type(e).__name__}: {str(e)[:300]}")
        except openai.APIStatusError as e:          # 400, 401, 403, 404...: more requests will not help
            raise StopRun(f"{type(e).__name__} ({getattr(e, 'status_code', '?')}): {str(e)[:500]}")
        else:
            if resp.status == "failed":           # the API's own failure: no answer came back
                errors.append(f"{sent} response status failed: {getattr(resp, 'error', None)}")
            else:
                rec = {"kind": "answer", "request_id": request["request_id"],
                       "condition": request["condition"], "disability": request["disability"],
                       "interest": request["interest"], "repeat": request["repeat"],
                       "run_position": request["run_position"], "list_variant": request["list_variant"],
                       "n_places_shown": request["n_places_shown"], "list_order": request["list_order"],
                       "model_requested": model, "sent_at": sent, "received_at": now(),
                       "seconds": round(time.time() - t0, 1), "attempts": attempt, "technical_errors": errors,
                       "traveller_message": message,
                       "prompt_sha256": S.prompt_fingerprint(instructions, message)}
                rec.update(read_response(resp))
                return rec
        if attempt <= len(WAITS_AFTER_ERROR):
            wait = WAITS_AFTER_ERROR[attempt - 1]
            print(f"  {request['request_id']}: technical error, trying again in {wait} s")
            for _ in range(wait):
                if _stop.is_set():
                    raise StopRun("stopped")
                time.sleep(1)
    return {"kind": "technical_failure", "request_id": request["request_id"], "at": now(), "errors": errors}


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cost(usage_list) -> float:
    total = 0.0
    for u in usage_list:
        if not u:
            continue
        cached = u.get("cached_tokens") or 0
        written = u.get("cache_write_tokens") or 0      # tokens stored for reuse: priced a little higher
        if cached + written <= u["input_tokens"]:       # both counted inside input_tokens
            normal = u["input_tokens"] - cached - written
        else:                                           # reported separately
            normal = u["input_tokens"]
        total += (normal * PRICE_INPUT + cached * PRICE_CACHED_INPUT + written * PRICE_CACHE_WRITE
                  + u["output_tokens"] * PRICE_OUTPUT) / 1e6
    return total


def cmd_check():
    frozen = S.check_frozen()
    plan = the_plan()
    counts = {}
    for r in plan:
        counts[r["condition"]] = counts.get(r["condition"], 0) + 1
    print("Frozen data OK:", ", ".join(f"{k} {v[:12]}..." for k, v in frozen.items()))
    print("Plan:", len(plan), "requests", counts, "-> run/plan_requests.csv")
    print("Places sent in C:", {d: len(v) for d, v in S.FILTERED_IDS.items()})
    r = plan[0]
    ins, msg = S.hidden_instructions(r), S.traveller_message(r)
    ex = S.RUN_DIR / "example_prompt.txt"
    ex.write_text("=== instructions (hidden part) ===\n" + ins + "\n\n=== input (what the traveller types) ===\n"
                  + msg + "\n\n=== answer format (API setting) ===\n" + json.dumps(S.ANSWER_FORMAT, indent=2),
                  encoding="utf-8")
    print(f"\nFirst request: {r['request_id']}\nTraveller types: {msg}")
    print(f"Hidden part: {len(ins):,} characters (about {len(ins) // 4:,} tokens); full text in {ex}")


def cmd_models():
    client = make_client()
    names = sorted(m.id for m in client.models.list() if "6.1" in m.id or "sol" in m.id)
    print("Models with '6.1' or 'sol' in the name:\n  " + "\n  ".join(names or ["(none found)"]))
    print("\nIf a dated name is listed (with a date at the end), put it in MODEL at the top of run_requests.py.")


def cmd_test():
    S.check_frozen()
    client = make_client()
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    plan = the_plan()
    req = dict(next(r for r in plan if r["condition"] == "A" and r["disability"] == "visual"
                    and r["interest"] == "history"))
    req["request_id"] = "TEST_" + req["request_id"]
    print(f"Sending ONE test request ({req['request_id']}) to {MODEL}. This is not study data.")
    try:
        rec = send(client, req, MODEL)
    except StopRun as e:
        raise SystemExit(f"STOP: {e}")
    out = TEST_DIR / f"test_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    if rec["kind"] != "answer":
        raise SystemExit(f"No answer after retries: {rec['errors']}")
    print(f"Model that answered: {rec['model_returned']}   status: {rec['status']}   time: {rec['seconds']} s")
    if rec["parse_error"]:
        print("ANSWER FORMAT PROBLEM:", rec["parse_error"])
        print(rec["output_text"][:2000])
    else:
        shown = set(req["list_order"].split())
        for i, p in enumerate(rec["parsed"]["recommendations"], 1):
            pid = p.get("place_id", "")
            name = S.PLACE[pid]["name"] if pid in S.PLACE else "(not a place ID from the list)"
            flag = "" if pid in shown else "   <- not in the list shown"
            print(f"  {i}. {pid} {name}{flag}\n     {p.get('reason', '')}")
    u = rec["usage"]
    print("Tokens:", u)
    one = cost([u])
    print(f"Cost of this request (estimate, prices at the top of the script): ${one:.4f}")
    print(f"Rough cost of 700 requests at this size, with no cache reuse: ${one * 700:.2f}. With cache reuse "
          "it is lower; run --test a second time within a few minutes to see 'cached_tokens' above 0.")
    print(f"Saved to {out}")


def cmd_status():
    plan = the_plan()
    answers = [a for a in read_lines(ANSWERS) if a.get("kind") == "answer"]
    done = {a["request_id"] for a in answers}
    per = {}
    for r in plan:
        c = per.setdefault(r["condition"], [0, 0])
        c[1] += 1
        c[0] += r["request_id"] in done
    print("Done per condition:", {k: f"{v[0]}/{v[1]}" for k, v in sorted(per.items())})
    print(f"Total: {len(done)}/{len(plan)}")
    if answers:
        models = sorted({a["model_returned"] for a in answers})
        bad = sum(1 for a in answers if a["parse_error"])
        print("Model(s) that answered:", models)
        print("Answers with a format problem (kept, scored as they are):", bad)
        print(f"Estimated cost so far: ${cost(a['usage'] for a in answers):.2f}")
    fails = read_lines(FAILURES)
    if fails:
        print("Technical failures logged (retried on the next --run):", len(fails))


def cmd_run():
    frozen = S.check_frozen()
    plan = the_plan()
    previous = [a for a in read_lines(ANSWERS) if a.get("kind") == "answer"]
    used = {a["model_requested"] for a in previous}
    if used and used != {MODEL}:
        raise SystemExit(f"STOP: earlier answers used {used}, but MODEL is now {MODEL!r}. One run, one model.")
    done = {a["request_id"] for a in previous}
    todo = [r for r in plan if r["request_id"] not in done]
    if not todo:
        print("All", len(plan), "requests already have an answer. Nothing to do.")
        return
    if not previous:
        (S.RUN_DIR / "run_started.txt").write_text(
            f"Run started: {now()}\nModel: {MODEL}\n" + "\n".join(f"{k} SHA-256: {v}" for k, v in frozen.items())
            + "\n", encoding="utf-8")
    print(f"{len(done)} done, {len(todo)} to send, with {WORKERS} at a time. Model: {MODEL}")
    print("You can stop at any time with Ctrl+C; run --run again later and it continues.")
    client = make_client()
    counter = {"n": len(done)}
    stop_reason = []

    def work(req):
        if _stop.is_set():
            return
        try:
            rec = send(client, req, MODEL)
        except StopRun as e:
            if not _stop.is_set():
                stop_reason.append(str(e))
            _stop.set()
            return
        if rec["kind"] == "answer":
            append_line(ANSWERS, rec)
            with _lock:
                counter["n"] += 1
                n = counter["n"]
            note = f"  FORMAT PROBLEM: {rec['parse_error']}" if rec["parse_error"] else ""
            print(f"[{n}/{len(plan)}] {req['request_id']}  {rec['seconds']} s{note}")
        else:
            append_line(FAILURES, rec)
            print(f"  {req['request_id']}: no answer after {len(WAITS_AFTER_ERROR) + 1} tries; "
                  "it will be tried again on the next --run")

    pool = ThreadPoolExecutor(max_workers=WORKERS)
    try:
        futures = [pool.submit(work, r) for r in todo]
        for f in futures:
            while not f.done():
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping: the requests already sent will finish and be saved; nothing new is sent.")
        _stop.set()
    pool.shutdown(wait=True, cancel_futures=True)
    if stop_reason:
        print("\nSTOPPED:", stop_reason[0])
    cmd_status()


def main():
    for stream in (sys.stdout, sys.stderr):          # Windows terminals: never crash on an unusual character
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is needed (python --version shows yours).")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    for name in ("check", "models", "test", "run", "status"):
        g.add_argument("--" + name, action="store_true")
    a = ap.parse_args()
    {"check": cmd_check, "models": cmd_models, "test": cmd_test, "run": cmd_run, "status": cmd_status}[
        next(k for k, v in vars(a).items() if v)]()


if __name__ == "__main__":
    main()
