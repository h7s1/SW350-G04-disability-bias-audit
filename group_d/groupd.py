"""Group D (added after Study 1): the filtered list of C + the disability sentence of A. SW350 Group 4.

Nothing from Study 1 is changed. This file only builds the 300 group D requests from Study 1's own parts:
  - the hidden list: exactly C's list for the same repeat and disability (the filter's places, same order);
  - the traveller's message: exactly A's message for the same disability and interest ("I'm blind." etc.).
So D differs from C only by the disability sentence, and from A only by the filter.
See PLAN_D.md (written 29 Oct 2026, after Study 1's results, before the D run).
"""
import random

import study_common as S

RUN_DIR = S.HERE / "run_D"
D_SEED = f"{S.PLAN_SEED}|D"          # run order of the D requests (the list orders are Study 1's)
_STUDY1_MESSAGE = S.traveller_message  # Study 1's function, kept before run_d.py points S to the D versions


def build_plan_d() -> list:
    """300 requests: 3 disabilities x 5 interests x 20 repeats. The 20 repeats in a random order, and the 15
    requests of each repeat in a random order, as in Study 1."""
    blocks = list(range(1, S.REPEATS + 1))
    random.Random(D_SEED).shuffle(blocks)
    rows = []
    for rep in blocks:
        order = S.repeat_order(rep)                       # Study 1's list order for this repeat
        block = [{"condition": "D", "disability": d, "interest": it["interest_key"], "repeat": rep}
                 for it in S.INTERESTS for d in S.DISABILITIES]
        random.Random(f"{D_SEED}|block|r{rep:02d}").shuffle(block)
        for r in block:
            keep = set(S.FILTERED_IDS[r["disability"]])
            ids = [i for i in order if i in keep]          # C's list: excluded places removed, same order
            r["request_id"] = f"D_{r['disability']}_{r['interest']}_r{rep:02d}"
            r["list_variant"] = "filtered_" + r["disability"]
            r["cache_key"] = f"sw350g04-r{rep:02d}-{r['list_variant']}"
            r["list_order"] = " ".join(ids)
            r["n_places_shown"] = len(ids)
        rows.extend(block)
    for i, r in enumerate(rows, 1):
        r["run_position"] = i
    return rows


def traveller_message_d(request: dict) -> str:
    """A's message (with the disability sentence) for D; any other condition exactly as in Study 1."""
    if request["condition"] == "D":
        return _STUDY1_MESSAGE(dict(request, condition="A"))
    return _STUDY1_MESSAGE(request)


def fingerprint_d(request: dict) -> str:
    return S.prompt_fingerprint(S.hidden_instructions(request), traveller_message_d(request))
