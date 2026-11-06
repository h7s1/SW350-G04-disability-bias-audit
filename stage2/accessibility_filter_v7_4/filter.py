"""
Rule-based accessibility pre-filter, v7.4 (SW350, Group 4, 28 Oct 2026).
History: built on the team's v2. v3 three outcomes and activity-based tiers. v4 removed D3. v5 replaced
sight/hearing levels with yes/no "main thing is seen / heard" (UN CRPD Art. 30; UNWTO 2013). v6 restored D3
(UNWTO 2013 p.8). v7 data only (facility swap, see swap_record/). v7.1 (after a team review): every rule's
sources now match the team documents, page numbers are printed page numbers, freeze() also fingerprints
places.csv and categories.csv, and test_real_data.py checks the real data. v7.2: five description edits (no loaded or time words),
word and length checks added to test_real_data.py, B1 and D1 sources marked checked. v7.3: district column
removed and district names taken out of every description and six place names (data/renames.csv), so ChatGPT
decides from the listed information only; data re-frozen. v7.4 (after the final data review): 12 more places
renamed because their names were real, well-known places or real Riyadh districts (data/renames.csv); re-frozen.
The decision logic is unchanged since v6.

WHAT THE FILTER DOES
    It decides eligibility, not preference. A place is removed only when an
    Essential barrier exists for that activity. ChatGPT ranks what is left.

THE THREE PIECES (they never mix)
    1. Person's needs      -> the RULES below (each from a source)
    2. Activity's demands  -> categories.csv (setting, movement, visual content, spoken content)
    3. Place's features    -> places.csv (yes / no for every feature)

HOW ONE RULE IS CHECKED (same two questions for every rule)
    Q1  Does this rule apply here, and how strongly?   (uses piece 2)
        -> "essential", "important", or not applicable
    Q2  Is it met?                                     (uses piece 3)
        -> PASS if ANY listed feature is "yes", otherwise FAIL

HOW THE RESULT IS DECIDED (fixed order, the worst result wins)
    any Essential rule FAILS  -> EXCLUDED
    else any Important FAILS  -> ELIGIBLE_WITH_CAVEATS (reasons listed)
    else                      -> ELIGIBLE
    Rule order never matters, rules never override each other, and a rule
    can only read place features, never traits of the traveller.

PROFILES
    mobility = wheelchair user (own wheelchair, travels independently)
    visual   = blind traveller (no usable sight, cane, travels independently)
    hearing  = Deaf traveller (uses sign language, reads text, no hearing aid)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field

DISABILITIES = ("mobility", "visual", "hearing")
ESSENTIAL, IMPORTANT = "essential", "important"
PASS, FAIL, NOT_APPLICABLE = "PASS", "FAIL", "NOT_APPLICABLE"
ELIGIBLE, CAVEATS, EXCLUDED = "ELIGIBLE", "ELIGIBLE_WITH_CAVEATS", "EXCLUDED"

# --------------------------------------------------------------------------- #
# Piece 2: activity demands (set per CATEGORY in categories.csv)
# --------------------------------------------------------------------------- #
DEMANDS = {
    "setting": {"indoor", "outdoor"},
    "core_requires_movement": {"yes", "no"},
    # Is the category DEFINED by content that is seen / heard (art displayed, a view,
    # a guide's explanation, a performance)? A fact about the activity, not a judgment
    # about how much a person would enjoy it.
    "visual_content": {"yes", "no"},
    "spoken_content": {"yes", "no"},
}

# --------------------------------------------------------------------------- #
# Piece 3: place features (every place must have yes or no for every one)
# --------------------------------------------------------------------------- #
FEATURES = {
    # mobility
    "step_free_approach":       "Step-free path from parking or drop-off to the entrance",
    "level_entrance":           "Entrance has no steps",
    "entrance_ramp":            "Ramp at the entrance",
    "entrance_lift":            "Lift or platform lift at the entrance",
    "wide_entrance_door":       "Entrance door wide enough for a wheelchair",
    "activity_point_step_free": "Seat, table or viewpoint reachable from the entrance without steps",
    "step_free_interior":       "All core areas reachable without steps (level, ramps or elevator)",
    "paved_route":              "Firm, paved route through an outdoor site",
    "accessible_toilet":        "Accessible toilet on site",
    "accessible_parking_or_dropoff": "Accessible parking or drop-off near the entrance",
    # visual
    "audio_guide":              "Audio guide available",
    "audio_description":        "Audio description of the main experience",
    "tactile_exhibits":         "Exhibits or models that can be touched",
    "described_guided_tour":    "Guided tour that describes what is seen",
    "tactile_paving":           "Tactile paths or marked lanes",
    "staff_assistance":         "Staff assistance on request",
    "braille_or_audio_info":    "Signs or labels in braille or audio",
    # hearing
    "captions":                 "Captions or subtitles for spoken content",
    "written_content":          "Written script or text version of spoken content",
    "sign_language_interpreter": "Sign-language interpretation of the main experience",
    "visual_information":       "Information shown on signs or screens",
    "visual_alarm":             "Flashing (visual) emergency alarm",
    "non_speech_communication": "Staff can communicate without speech (signing staff, writing, screen)",
}


# --------------------------------------------------------------------------- #
# Piece 1: the rules (person's needs). Declarative, so the table can go in the
# appendix exactly as written here.
#   tier_by   : which demand decides the tier, and the tier for each level.
#               Levels not listed -> rule does not apply.
#               None means the tier never changes ("always").
#   only_if   : extra demand values that must ALL hold for the rule to apply.
#   met_by    : place features; ANY one "yes" meets the rule.
#   source_checked : True only after a team member opened the page and
#               confirmed the wording. freeze() refuses while any is False.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Rule:
    rule_id: str
    disability: str
    stage: str
    requirement: str
    met_by: tuple
    source: str
    source_checked: bool
    base_tier: str = ESSENTIAL                 # used when tier_by is None
    tier_by: tuple | None = None               # (demand, {level: tier, ...})
    only_if: dict = field(default_factory=dict)


RULES = [
    # Page numbers are the PRINTED page numbers of the published version (checked 28 Oct 2026):
    #   Gavurova & Polishchuk (2025) Oeconomia Copernicana 16(1) 417-462 -> pp.429-432
    #   Muller et al. (2022) ACM TACCESS, Article 13 -> pages written 13:N
    #   Theodorou et al. (2024/2025) Tourism Review 80(9) 1635-1653 -> p.1636
    #   Indrashwara et al. (2024) ICSCC 2024 -> pp.192, 195
    #   Alhajaj, Li, Nasser, Alasim, Alqraini: page N of the article (same as the PDF page)
    # ---------- Wheelchair user ----------
    Rule("W1", "mobility", "3 Approach", "Step-free path from parking or drop-off to the entrance",
         ("step_free_approach",),
         "Gavurova & Polishchuk (2025) p.431 'sidewalks and roads ... barrier-free', p.429 'no curbs'; "
         "Alhajaj & Habibullah (2025) p.15 'absence of curb ramps'; Muller et al. (2022) p.13:5 'high curbs, missing ramps'", True),
    Rule("W2", "mobility", "4 Entrance", "Entrance without steps",
         ("level_entrance", "entrance_ramp", "entrance_lift"),
         "Gavurova & Polishchuk (2025) p.429 entrance barrier-free, ramp, lifting platform; "
         "Alhajaj & Habibullah (2025) p.18 'entrances with a single step'; Muller et al. (2022) p.13:5 'steps'", True),
    Rule("W3", "mobility", "4 Entrance", "Entrance door wide enough",
         ("wide_entrance_door",),
         "Gavurova & Polishchuk (2025) p.429 'width of the entrance door'; Muller et al. (2022) p.13:22 'narrow doorframes'", True),
    Rule("W4", "mobility", "5 Reach activity point", "Seat, table or viewpoint reachable without steps",
         ("activity_point_step_free",),
         "Gavurova & Polishchuk (2025) p.430 elevators; p.431 'interior of catering establishments is adapted'", True),
    Rule("W5", "mobility", "5 Moving around", "All core areas reachable without steps",
         ("step_free_interior",),
         "Gavurova & Polishchuk (2025) p.430 'elevators'; Muller et al. (2022) p.13:5 'steps, uneven ground surfaces', "
         "p.13:22 'No elevator or ramp'", True,
         only_if={"core_requires_movement": "yes"}),
    Rule("W6", "mobility", "5 Moving around", "Firm, paved route",
         ("paved_route",),
         "Gavurova & Polishchuk (2025) p.431 'sidewalks and roads ... barrier-free'; "
         "Alhajaj & Habibullah (2025) p.9 'free of breaks, potholes, or cracks'; Muller et al. (2022) p.13:5 'uneven ground surfaces'", True,
         only_if={"setting": "outdoor", "core_requires_movement": "yes"}),
    Rule("W7", "mobility", "7 Facilities", "Accessible toilet",
         ("accessible_toilet",),
         "Gavurova & Polishchuk (2025) p.432 'toilets adapted'; Muller et al. (2022) p.13:5 'inaccessible bathrooms for wheelchairs'", True, base_tier=IMPORTANT),
    Rule("W8", "mobility", "3 Parking", "Accessible parking or drop-off near the entrance",
         ("accessible_parking_or_dropoff",),
         "Gavurova & Polishchuk (2025) p.431 'closest to the entrance'; "
         "Muller et al. (2022) p.13:17 'location of accessible entrance and parking lots'", True, base_tier=IMPORTANT),

    # ---------- Blind traveller ----------
    Rule("B1", "visual", "6 Main experience", "Non-visual way to experience it",
         ("audio_guide", "audio_description", "tactile_exhibits", "described_guided_tour"),
         "Li et al. (2023) p.1 'most art is consumed visually ... poses access barriers', p.2 audio descriptions "
         "and tactile options, p.3 'Touching is one of the main methods'; Nasser et al. (2025) p.2 'primarily visual nature'; "
         "Alasim & Alqraini (2025) p.2 'audio-visual guides that assist individuals with hearing and visual disabilities'; "
         "UN CRPD (2006) Art. 30(1)(a)-(c) accessible formats; UNWTO (2013) p.11-12 museums and buildings of tourism interest "
         "'all information ... in both written and audio format', theatres 'audio description'",
         True,  # quotes checked against the PDFs on 28 Oct 2026 (Claude), approved by Alanoud
         tier_by=("visual_content", {"yes": ESSENTIAL})),
    Rule("B2", "visual", "3-5 Navigation", "Navigation support (to the entrance, seat and around)",
         ("tactile_paving", "staff_assistance", "described_guided_tour"),
         "Gavurova & Polishchuk (2025) p.430 'lanes for the visually impaired', p.431 'assistance services'; "
         "Muller et al. (2022) p.13:15 'in the building, priority is given to an assistant', p.13:20 orientation strategies "
         "('I ask for my way', 'I have an assistant'); Theodorou et al. (2024) p.1636 'dependence on others for navigation'",
         True, base_tier=IMPORTANT),
    Rule("B3", "visual", "8 Information", "Information in braille or audio",
         ("braille_or_audio_info", "staff_assistance"),
         "Gavurova & Polishchuk (2025) p.431 'information signs for people with disabilities'; "
         "Muller et al. (2022) p.13:16 tactile labels, p.13:22 'No voice output or Braille'; "
         "Theodorou et al. (2024) p.1636 'difficulty accessing ... visual or textual information'", True, base_tier=IMPORTANT),

    # ---------- Deaf traveller ----------
    Rule("D1", "hearing", "6 Main experience", "Non-audio way to experience it",
         ("captions", "written_content", "sign_language_interpreter"),
         "Indrashwara et al. (2024) p.192 'Deaf people often have difficulty getting this information independently', "
         "p.195 sign language video 'overcoming the communication barriers'; Alasim & Alqraini (2025) p.2 'audio-visual guides'; "
         "UN CRPD (2006) Art. 30(1)(b) theatre and cultural activities in accessible formats; UNWTO (2013) p.12 excursions "
         "'sign language interpreters ... and/or printed descriptive material', theatres 'subtitling and/or sign language'",
         True,  # quotes checked against the PDFs on 28 Oct 2026 (Claude), approved by Alanoud
         tier_by=("spoken_content", {"yes": ESSENTIAL})),
    Rule("D2", "hearing", "8 Information", "Information shown visually",
         ("visual_information",),
         "Gavurova & Polishchuk (2025) p.431 'information signs for people with disabilities'; "
         "Indrashwara et al. (2024) p.192 public address system 'limited for deaf people'", True,
         base_tier=IMPORTANT),
    # D3 removed 27 Oct 2026 (no source); restored 28 Oct 2026 after the UNWTO (2013) Recommendations were checked.
    Rule("D3", "hearing", "8 Safety", "Visual emergency alarm",
         ("visual_alarm",),
         "UNWTO (2013) Recommendations on Accessible Tourism p.8 'Fire alarms should emit both visual and acoustic signals'",
         True, base_tier=IMPORTANT, only_if={"setting": "indoor"}),
    Rule("D4", "hearing", "4 Tickets / help", "Staff can communicate without speech",
         ("non_speech_communication",),
         "Alqraini & Alasim (2026) p.7 staff training in 'disability etiquette and communication'; "
         "Alasim & Alqraini (2025) p.3 providers 'do not strive to facilitate effective communication'", True,
         base_tier=IMPORTANT),
]


# --------------------------------------------------------------------------- #
# Loading and validation: nothing is guessed, every gap is reported.
# --------------------------------------------------------------------------- #
CODED = set(DEMANDS) | set(FEATURES) | {"category"}


def _clean(row: dict) -> dict:
    """Trim spaces everywhere; lower-case only the coded fields (names and descriptions keep their case)."""
    out = {}
    for k, v in row.items():
        if k is None:
            raise ValueError(f"row {row.get('place_id', '?')} has more values than column names (check commas)")
        k = k.strip()
        v = v.strip() if isinstance(v, str) else v
        out[k] = v.lower() if (k in CODED and isinstance(v, str)) else v
    return out


def load_categories(path: str) -> dict:
    cats = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for raw in csv.DictReader(fh):
            row = _clean(raw)
            name = row.get("category", "")
            for key, allowed in DEMANDS.items():
                if row.get(key) not in allowed:
                    raise ValueError(f"category '{name}': '{key}' must be one of {sorted(allowed)}, got {row.get(key)!r}")
            if name in cats:
                raise ValueError(f"category '{name}' appears twice")
            cats[name] = {k: row[k] for k in DEMANDS}
    return cats


def validate_place(raw: dict, categories: dict) -> dict:
    p = _clean(raw)
    pid = p.get("place_id", "?")
    if p.get("category") not in categories:
        raise ValueError(f"{pid}: category {p.get('category')!r} is not in categories.csv")
    for f in FEATURES:
        if p.get(f) not in {"yes", "no"}:
            raise ValueError(f"{pid}: feature '{f}' must be yes or no, got {p.get(f)!r}")
    p.update(categories[p["category"]])          # activity demands come from the category only
    return p


def load_places(path: str, categories: dict) -> list:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        places = [validate_place(r, categories) for r in csv.DictReader(fh)]
    ids = [p["place_id"] for p in places]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate place_id in places.csv")
    return places


# --------------------------------------------------------------------------- #
# Decision
# --------------------------------------------------------------------------- #
def tier_for(rule: Rule, place: dict):
    """Q1: does the rule apply here, and how strongly? Returns a tier or None."""
    if any(place[k] != v for k, v in rule.only_if.items()):
        return None
    if rule.tier_by is None:
        return rule.base_tier
    demand, levels = rule.tier_by
    return levels.get(place[demand])             # level not listed -> None (not applicable)


def check_rule(rule: Rule, place: dict):
    """Returns (status, tier). Q2: met if ANY listed feature is 'yes'."""
    tier = tier_for(rule, place)
    if tier is None:
        return NOT_APPLICABLE, None
    return (PASS if any(place[f] == "yes" for f in rule.met_by) else FAIL), tier


@dataclass
class Decision:
    place_id: str
    name: str
    category: str
    disability: str
    outcome: str
    excluded_by: list        # Essential rules that failed
    caveats: list            # Important rules that failed (shown to the traveller)
    results: dict            # rule_id -> (status, tier)


def decide(place: dict, disability: str) -> Decision:
    if disability not in DISABILITIES:
        raise ValueError(f"disability must be one of {DISABILITIES}")
    results = {r.rule_id: check_rule(r, place) for r in RULES if r.disability == disability}
    excluded_by = [rid for rid, (s, t) in results.items() if s == FAIL and t == ESSENTIAL]
    caveats = [rid for rid, (s, t) in results.items() if s == FAIL and t == IMPORTANT]
    outcome = EXCLUDED if excluded_by else (CAVEATS if caveats else ELIGIBLE)
    return Decision(place["place_id"], place.get("name", ""), place["category"], disability,
                    outcome, excluded_by, caveats, results)


def caveat_text(decision: Decision) -> str:
    """Plain-language note for the interface, e.g. 'No accessible toilet'."""
    req = {r.rule_id: r.requirement for r in RULES}
    return "; ".join(f"Missing: {req[rid]}" for rid in decision.caveats)


def filter_candidates(places: list, disability: str | None) -> list:
    """Places sent to ChatGPT. No disability disclosed -> the full list, unchanged."""
    if disability is None:
        return list(places)
    return [p for p in places if decide(p, disability).outcome != EXCLUDED]


# --------------------------------------------------------------------------- #
# Reports for the paper
# --------------------------------------------------------------------------- #
def rules_table_markdown() -> str:
    out = ["| Rule | Person | Stage | Requirement | Applies when / tier | Met if any one is yes | Source | Checked |",
           "|---|---|---|---|---|---|---|---|"]
    for r in RULES:
        cond = " AND ".join(f"{k} = {v}" for k, v in r.only_if.items())
        if r.tier_by:
            demand, levels = r.tier_by
            when = ", ".join(f"{demand} = {lvl}: {t}" for lvl, t in levels.items()) + "; other levels: not applicable"
        else:
            when = f"{cond or 'always'}: {r.base_tier}"
        if r.tier_by and cond:
            when = f"{cond}; {when}"
        out.append(f"| {r.rule_id} | {r.disability} | {r.stage} | {r.requirement} | {when} | "
                   f"{', '.join(r.met_by)} | {r.source} | {'yes' if r.source_checked else 'NO'} |")
    return "\n".join(out) + "\n"


def truth_table_markdown() -> str:
    """Every rule under every combination of activity demands: shows each case has exactly one meaning."""
    import itertools
    keys = list(DEMANDS)
    out = ["| " + " | ".join(keys) + " | " + " | ".join(r.rule_id for r in RULES) + " |",
           "|" + "---|" * (len(keys) + len(RULES))]
    for combo in itertools.product(*(sorted(DEMANDS[k]) for k in keys)):
        demo = dict(zip(keys, combo))
        cells = [(tier_for(r, demo) or "-") for r in RULES]
        out.append("| " + " | ".join(combo) + " | " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def exclusion_report(places: list, min_remaining: int = 5) -> str:
    cats = sorted({p["category"] for p in places})
    dec = {d: [decide(p, d) for p in places] for d in DISABILITIES}
    out = ["# Filter report", "", f"Places: {len(places)}", "",
           "## Outcomes per disability", "",
           "| Disability | Eligible | With caveats | Excluded | % excluded |", "|---|---|---|---|---|"]
    for d in DISABILITIES:
        n = {o: sum(x.outcome == o for x in dec[d]) for o in (ELIGIBLE, CAVEATS, EXCLUDED)}
        out.append(f"| {d} | {n[ELIGIBLE]} | {n[CAVEATS]} | {n[EXCLUDED]} | {100 * n[EXCLUDED] / len(places):.1f}% |")
    out += ["", "## Failures per rule", "", "| Rule | Requirement | Tier(s) | Places failing |", "|---|---|---|---|"]
    for r in RULES:
        fails = [x for x in dec[r.disability] if x.results[r.rule_id][0] == FAIL]
        tiers = sorted({x.results[r.rule_id][1] for x in fails})
        out.append(f"| {r.rule_id} | {r.requirement} | {', '.join(tiers) or '-'} | {len(fails)} |")
    out += ["", f"## Places still available per category (flag = fewer than {min_remaining})", "",
            "| Category | Total | " + " | ".join(DISABILITIES) + " |", "|---|---|" + "---|" * len(DISABILITIES)]
    for c in cats:
        total = sum(p["category"] == c for p in places)
        cells = []
        for d in DISABILITIES:
            kept = sum(x.category == c and x.outcome != EXCLUDED for x in dec[d])
            cells.append(f"{kept}{' (!)' if kept < min_remaining else ''}")
        out.append(f"| {c} | {total} | " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def write_decisions(places: list, path: str) -> None:
    ids = [r.rule_id for r in RULES]
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["place_id", "name", "category", "disability", "outcome", "excluded_by", "caveats"] + ids)
        for d in DISABILITIES:
            for p in places:
                x = decide(p, d)
                w.writerow([x.place_id, x.name, x.category, d, x.outcome, ";".join(x.excluded_by),
                            ";".join(x.caveats)] + [x.results.get(rid, ("", None))[0] for rid in ids])


def freeze(path: str, places_path: str = "places.csv", categories_path: str = "categories.csv") -> str:
    """Record a dated fingerprint of the rules AND the data. Refuses while any source is unchecked.

    rules_frozen.txt gets the SHA-256 of filter.py, places.csv and categories.csv, so any later
    change to the rules or the data leaves a trace (compare the hashes)."""
    import datetime
    import hashlib
    import pathlib
    unchecked = [r.rule_id for r in RULES if not r.source_checked]
    if unchecked:
        raise RuntimeError(f"Cannot freeze: sources not checked for {', '.join(unchecked)}")
    files = {"filter.py": pathlib.Path(__file__), "places.csv": pathlib.Path(places_path),
             "categories.csv": pathlib.Path(categories_path)}
    digests = {name: hashlib.sha256(f.read_bytes()).hexdigest() for name, f in files.items()}
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [f"Frozen at: {stamp}"] + [f"{name} SHA-256: {d}" for name, d in digests.items()]
    pathlib.Path(path).write_text("\n".join(lines) + "\n\n" + rules_table_markdown(), encoding="utf-8")
    return digests["filter.py"]


if __name__ == "__main__":
    import argparse
    import os

    ap = argparse.ArgumentParser(description="Apply the accessibility pre-filter.")
    ap.add_argument("--places", default="places.csv")
    ap.add_argument("--categories", default="categories.csv")
    ap.add_argument("--out", default="filter_output")
    ap.add_argument("--freeze", action="store_true", help="Write rules_frozen.txt and stop.")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.freeze:
        h = freeze(os.path.join(args.out, "rules_frozen.txt"), args.places, args.categories)
        print(f"Rules and data frozen (filter.py SHA-256 {h[:16]}...); see rules_frozen.txt")
        raise SystemExit(0)

    cats = load_categories(args.categories)
    places = load_places(args.places, cats)
    write_decisions(places, os.path.join(args.out, "decisions.csv"))
    for name, text in [("report.md", exclusion_report(places)),
                       ("rules_table.md", rules_table_markdown()),
                       ("truth_table.md", truth_table_markdown())]:
        with open(os.path.join(args.out, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    for d in DISABILITIES:
        print(f"{d:9s} sent to ChatGPT: {len(filter_candidates(places, d))}/{len(places)}")
    unchecked = [r.rule_id for r in RULES if not r.source_checked]
    if unchecked:
        print(f"WARNING: sources not checked for {', '.join(unchecked)}; do not use results yet.")
