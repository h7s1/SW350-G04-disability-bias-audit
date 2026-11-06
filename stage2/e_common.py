"""Study 2 (E1 and E2): two follow-up experiments on stereotyped steering. SW350 Group 4.

Nothing from Study 1 is changed. This file builds the 1,000 Study 2 requests from Study 1's own parts.

E1, "every place suits her": the hidden list holds only the places that are FULLY usable for that traveller
   (72 per traveller, facilities shown, Study 1's list order for the repeat). Told (E1T, A's message) vs not told
   (E1N, the message without the disability sentence), same list. Accessibility cannot explain a shift in the
   kinds of place picked.
E2, "no facility information": all 144 places, exactly as in Study 1 but WITHOUT the "Facilities:" sentence.
   Told (E2T) vs not told (E2N, one group scored for each traveller, like B). ChatGPT has to assume.

See PLAN_E.md (written 29 Oct 2026, before the Study 2 run).
"""
import random

import study_common as S

RUN_DIR = S.HERE / "run_E"
E_SEED = f"{S.PLAN_SEED}|E"
_STUDY1_MESSAGE = S.traveller_message        # Study 1's functions, kept before run_e.py points S to these
_STUDY1_INSTRUCTIONS = S.hidden_instructions
TOLD = {"E1T", "E2T"}
FULLY_USABLE = {d: [p["place_id"] for p in S.PLACES if S.DECISION[(p["place_id"], d)].outcome == "ELIGIBLE"]
                for d in S.DISABILITIES}


def build_plan_e() -> list:
    """1,000 requests: E1T 300, E1N 300, E2T 300, E2N 100. The 20 repeats in a random order, and the 50 requests
    of each repeat in a random order, as in Study 1."""
    blocks = list(range(1, S.REPEATS + 1))
    random.Random(E_SEED).shuffle(blocks)
    rows = []
    for rep in blocks:
        order = S.repeat_order(rep)                  # Study 1's list order for this repeat
        block = []
        for it in S.INTERESTS:
            k = it["interest_key"]
            block.append({"condition": "E2N", "disability": "none", "interest": k, "repeat": rep})
            for d in S.DISABILITIES:
                for c in ("E1T", "E1N", "E2T"):
                    block.append({"condition": c, "disability": d, "interest": k, "repeat": rep})
        random.Random(f"{E_SEED}|block|r{rep:02d}").shuffle(block)
        for r in block:
            c, d = r["condition"], r["disability"]
            r["request_id"] = f"{c}_{d}_{r['interest']}_r{rep:02d}"
            if c.startswith("E1"):
                keep = set(FULLY_USABLE[d])
                ids = [i for i in order if i in keep]
                r["list_variant"] = "fully_usable_" + d
            else:
                ids = order
                r["list_variant"] = "all_no_facilities"
            r["cache_key"] = f"sw350g04-e-r{rep:02d}-{r['list_variant']}"
            r["list_order"] = " ".join(ids)
            r["n_places_shown"] = len(ids)
        rows.extend(block)
    for i, r in enumerate(rows, 1):
        r["run_position"] = i
    return rows


def traveller_message_e(request: dict) -> str:
    """Told: A's message with the disability sentence. Not told: Study 1's message without it."""
    return _STUDY1_MESSAGE(dict(request, condition="A" if request["condition"] in TOLD else "B"))


def place_block_no_facilities(row: dict) -> str:
    """Study 1's place block without the "Facilities:" sentence (everything else identical)."""
    return "\n".join([
        f"place_id: {row['place_id']}",
        f"Name: {row['name']}",
        f"Category: {row['category'].replace('_', ' ')}",
        f"Price per person: {row['price_sar']} SAR",
        f"Opening hours: {row['opening_hours']}",
        f"Visit duration: {row['visit_duration']}",
        f"Walking distance from parking to entrance: {row['walking_distance_m']} m",
        f"Description: {row['description']}",
    ])


def hidden_instructions_e(request: dict) -> str:
    if request["condition"].startswith("E2"):
        ids = request["list_order"].split()
        return S.HIDDEN_INTRO + "\n\n" + "\n\n".join(place_block_no_facilities(S.PLACE[i]) for i in ids)
    return _STUDY1_INSTRUCTIONS(request)        # E1 (and Study 1): the places with their Facilities sentence


def fingerprint_e(request: dict) -> str:
    return S.prompt_fingerprint(hidden_instructions_e(request), traveller_message_e(request))
