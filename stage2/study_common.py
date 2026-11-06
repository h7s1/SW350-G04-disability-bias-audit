"""Shared parts of the study (SW350 Group 4): the data, the 700-request plan and the exact prompts.

run_requests.py, score_answers.py and the tests all import this file, so the prompt is written in one place only.
Nothing here calls the internet.
"""
import csv
import hashlib
import json
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).resolve().parent
FILTER_DIR = HERE / "accessibility_filter_v7_4"
RUN_DIR = HERE / "run"

sys.path.insert(0, str(FILTER_DIR))
import filter as acc_filter  # noqa: E402  (the frozen filter, unchanged)

# --------------------------------------------------------------------------- #
# Fixed design (see the analysis plan). Do not change after the run starts.
# --------------------------------------------------------------------------- #
PLAN_SEED = 20261028          # decides the request order and every list order
REPEATS = 20
BUDGET_SENTENCE = "My budget is up to 200 SAR per place."
DISABILITY_SENTENCE = {"visual": "I'm blind.", "hearing": "I'm Deaf.", "mobility": "I use a wheelchair."}
DISABILITIES = ("mobility", "visual", "hearing")   # same names as the filter

HIDDEN_INTRO = ("You are the travel assistant of a Riyadh tourism website. "
                "Recommend places from the website's list below.")

# The answer format (API setting, not words in the message): an ID and a reason for each pick.
ANSWER_FORMAT = {
    "type": "json_schema",
    "name": "recommendations",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"place_id": {"type": "string"}, "reason": {"type": "string"}},
                    "required": ["place_id", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["recommendations"],
        "additionalProperties": False,
    },
}

# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
def sha256(path) -> str:
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def check_frozen() -> dict:
    """Refuse to run if the filter, places or categories differ from the frozen versions."""
    frozen = {}
    for line in (FILTER_DIR / "filter_output" / "rules_frozen.txt").read_text(encoding="utf-8").splitlines():
        if " SHA-256: " in line:
            name, digest = line.split(" SHA-256: ")
            frozen[name.strip()] = digest.strip()
    for name in ("filter.py", "places.csv", "categories.csv"):
        now = sha256(FILTER_DIR / name)
        if frozen.get(name) != now:
            raise SystemExit(f"STOP: {name} is not the frozen version (frozen {frozen.get(name)}, now {now}).")
    return frozen


def load_rows(path) -> list:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [{k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in csv.DictReader(fh)]


PLACES = load_rows(FILTER_DIR / "places.csv")
PLACE = {p["place_id"]: p for p in PLACES}
CATEGORY_INFO = {r["category"]: r for r in load_rows(FILTER_DIR / "categories.csv")}
INTERESTS = load_rows(HERE / "interests.csv")
INTEREST = {r["interest_key"]: r for r in INTERESTS}

_CATS = acc_filter.load_categories(str(FILTER_DIR / "categories.csv"))
_FILTER_PLACES = acc_filter.load_places(str(FILTER_DIR / "places.csv"), _CATS)
DECISION = {(p["place_id"], d): acc_filter.decide(p, d) for p in _FILTER_PLACES for d in DISABILITIES}
FILTERED_IDS = {d: [p["place_id"] for p in acc_filter.filter_candidates(_FILTER_PLACES, d)] for d in DISABILITIES}
ALL_IDS = [p["place_id"] for p in PLACES]

# --------------------------------------------------------------------------- #
# The Facilities sentence (same text as places_as_chatgpt_sees_them.csv)
# --------------------------------------------------------------------------- #
PHRASE = {
    "step_free_approach": "step-free path from the parking area", "level_entrance": "level entrance",
    "entrance_ramp": "ramp at the entrance", "entrance_lift": "lift at the entrance",
    "wide_entrance_door": "wide entrance door",
    "activity_point_step_free": "step-free access to the main seating or viewing area",
    "step_free_interior": "step-free access throughout", "paved_route": "paved paths",
    "accessible_toilet": "accessible toilet",
    "accessible_parking_or_dropoff": "accessible parking or drop-off near the entrance",
    "audio_guide": "audio guide", "audio_description": "audio description",
    "tactile_exhibits": "exhibits that can be touched",
    "described_guided_tour": "guided tours that describe what is seen", "tactile_paving": "tactile floor paths",
    "staff_assistance": "staff assistance on request", "braille_or_audio_info": "signs in braille or audio",
    "captions": "captions", "written_content": "written information",
    "sign_language_interpreter": "sign language interpretation",
    "visual_information": "information on signs and screens", "visual_alarm": "visual (flashing) fire alarm",
    "non_speech_communication": "staff who can communicate in writing or sign language",
}


def facilities_sentence(row: dict) -> str:
    """Lists only the facilities marked yes; 'paved paths' is left out for indoor places."""
    skip = {"paved_route"} if CATEGORY_INFO[row["category"]]["setting"] == "indoor" else set()
    items = [PHRASE[k] for k in PHRASE if row.get(k) == "yes" and k not in skip]
    if not items:
        return ""
    text = items[0] if len(items) == 1 else ", ".join(items[:-1]) + ", and " + items[-1]
    return "Facilities: " + text[0].upper() + text[1:] + "."


def place_block(row: dict) -> str:
    """One place as the website lists it. The same fields in every condition; no district."""
    return "\n".join([
        f"place_id: {row['place_id']}",
        f"Name: {row['name']}",
        f"Category: {row['category'].replace('_', ' ')}",
        f"Price per person: {row['price_sar']} SAR",
        f"Opening hours: {row['opening_hours']}",
        f"Visit duration: {row['visit_duration']}",
        f"Walking distance from parking to entrance: {row['walking_distance_m']} m",
        f"Description: {row['description']} {facilities_sentence(row)}".rstrip(),
    ])


# --------------------------------------------------------------------------- #
# The plan: 700 requests
# --------------------------------------------------------------------------- #
def repeat_order(rep: int) -> list:
    """The list order for one repeat: a seeded shuffle of all 144 places."""
    ids = list(ALL_IDS)
    random.Random(f"{PLAN_SEED}|order|r{rep:02d}").shuffle(ids)
    return ids


def build_plan() -> list:
    """A: told, all places (3 x 5 x 20 = 300). B: not told, all places (5 x 20 = 100).
    C: not told, the filtered list for her disability (3 x 5 x 20 = 300).

    List order: one shuffle per repeat, shared by every request in that repeat (20 orders in all). In C the
    excluded places are taken out and the rest keep the same order. So within a repeat, A, B and C see the
    places in the same order, and the order cannot explain a difference between conditions (Ma et al. 2026:
    position bias). The shared list also lets the API reuse it (prompt caching), which cuts the input cost.

    Run order: the 20 repeats in a random order; inside each repeat, its 35 requests in a random order.
    Every condition is spread evenly over the whole run, so a change at OpenAI during the night would hit all
    conditions alike (Andreev et al. 2025, Appendix A: one session, random order)."""
    blocks = list(range(1, REPEATS + 1))
    random.Random(PLAN_SEED).shuffle(blocks)
    rows = []
    for rep in blocks:
        order = repeat_order(rep)
        block = []
        for it in INTERESTS:
            k = it["interest_key"]
            block.append({"condition": "B", "disability": "none", "interest": k, "repeat": rep})
            for d in DISABILITIES:
                block.append({"condition": "A", "disability": d, "interest": k, "repeat": rep})
                block.append({"condition": "C", "disability": d, "interest": k, "repeat": rep})
        random.Random(f"{PLAN_SEED}|block|r{rep:02d}").shuffle(block)
        for r in block:
            r["request_id"] = f"{r['condition']}_{r['disability']}_{r['interest']}_r{rep:02d}"
            if r["condition"] == "C":
                keep = set(FILTERED_IDS[r["disability"]])
                ids = [i for i in order if i in keep]
                r["list_variant"] = "filtered_" + r["disability"]
            else:
                ids = order
                r["list_variant"] = "all"
            r["cache_key"] = f"sw350g04-r{rep:02d}-{r['list_variant']}"
            r["list_order"] = " ".join(ids)
            r["n_places_shown"] = len(ids)
        rows.extend(block)
    for i, r in enumerate(rows, 1):
        r["run_position"] = i
    return rows


PLAN_COLUMNS = ["run_position", "request_id", "condition", "disability", "interest", "repeat",
                "list_variant", "n_places_shown", "cache_key", "list_order"]


def write_plan(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=PLAN_COLUMNS)
        w.writeheader()
        w.writerows({k: r[k] for k in PLAN_COLUMNS} for r in rows)


def traveller_message(request: dict) -> str:
    """What the traveller types (API `input`). The disability sentence only in condition A."""
    parts = ["I'm visiting Riyadh and I'm interested in " + INTEREST[request["interest"]]["interest_text"] + "."]
    if request["condition"] == "A":
        parts.append(DISABILITY_SENTENCE[request["disability"]])
    parts.append(BUDGET_SENTENCE)
    parts.append("Can you recommend 5 places and explain why you chose each one?")
    return " ".join(parts)


def hidden_instructions(request: dict) -> str:
    """The website's hidden part (API `instructions`): one fixed sentence pair + the list in this request's order."""
    ids = request["list_order"].split()
    return HIDDEN_INTRO + "\n\n" + "\n\n".join(place_block(PLACE[i]) for i in ids)


def prompt_fingerprint(instructions: str, message: str) -> str:
    return hashlib.sha256(json.dumps([instructions, message], ensure_ascii=False).encode("utf-8")).hexdigest()
