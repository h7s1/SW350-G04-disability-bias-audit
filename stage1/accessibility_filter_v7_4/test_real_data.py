"""
Checks on the REAL study data (places.csv, categories.csv, data/plan.csv), so the numbers reported
for RQ2 can be reproduced from this folder alone. Run:  python test_real_data.py   (or pytest)
"""
import collections, csv, os, re, statistics as st
from filter import DISABILITIES, FEATURES, RULES, FAIL, decide, load_categories, load_places

HERE = os.path.dirname(os.path.abspath(__file__))
CATS = load_categories(os.path.join(HERE, "categories.csv"))
PLACES = load_places(os.path.join(HERE, "places.csv"), CATS)   # refuses blanks or unknown values
RAW = {r["place_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "places.csv"), encoding="utf-8-sig"))}
PLAN = {r["place_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "data", "plan.csv"), encoding="utf-8-sig"))}
DEC = {(p["place_id"], d): decide(p, d) for p in PLACES for d in DISABILITIES}
WORD = {"ELIGIBLE": "usable", "ELIGIBLE_WITH_CAVEATS": "caveat", "EXCLUDED": "excluded"}
COL = {"mobility": "wheelchair_target", "visual": "blind_target", "hearing": "deaf_target"}


def test_144_places_12_per_category():
    ids = [p["place_id"] for p in PLACES]
    assert len(ids) == 144 and len(set(ids)) == 144
    assert ids == [f"P{i:03d}" for i in range(1, 145)]
    assert set(collections.Counter(p["category"] for p in PLACES).values()) == {12}
    assert len(collections.Counter(p["category"] for p in PLACES)) == 12


def test_totals_per_disability():
    expected = {"mobility": (72, 24, 48), "visual": (72, 52, 20), "hearing": (72, 60, 12)}
    for d, (e, c, x) in expected.items():
        n = collections.Counter(DEC[(p["place_id"], d)].outcome for p in PLACES)
        assert (n["ELIGIBLE"], n["ELIGIBLE_WITH_CAVEATS"], n["EXCLUDED"]) == (e, c, x), (d, n)


def test_zero_mismatches_with_the_plan():
    bad = [(pid, d) for (pid, d), dec in DEC.items() if WORD[dec.outcome] != PLAN[pid][COL[d]]]
    assert not bad, bad[:5]


def test_rule_failure_counts_match_the_documents():
    expected = dict(W1=22, W2=9, W3=1, W4=6, W5=1, W6=9, W7=39, W8=12,
                    B1=20, B2=46, B3=27, D1=12, D2=27, D3=5, D4=28)
    got = collections.Counter(rid for dec in DEC.values() for rid, (s, t) in dec.results.items() if s == FAIL)
    assert dict(got) == expected, dict(got)


def test_realism_rules():
    for p in PLACES:
        outdoor = CATS[p["category"]]["setting"] == "outdoor"
        if outdoor:
            assert p["entrance_lift"] == "no", p["place_id"]
            assert p["visual_alarm"] == "no", p["place_id"]
        if p["category"] in ("park_garden", "desert_experience", "nature_reserve"):
            assert p["tactile_paving"] == "no", p["place_id"]
        assert any(p[f] == "yes" for f in FEATURES), p["place_id"]


def test_price_and_distance_balanced_after_swap():
    worst_price = worst_walk = 0
    for d in DISABILITIES:
        for cat in CATS:
            ex = [p["place_id"] for p in PLACES if p["category"] == cat and DEC[(p["place_id"], d)].outcome == "EXCLUDED"]
            ok = [p["place_id"] for p in PLACES if p["category"] == cat and DEC[(p["place_id"], d)].outcome != "EXCLUDED"]
            if ex and ok:
                worst_price = max(worst_price, abs(st.mean(float(RAW[i]["price_sar"]) for i in ex) - st.mean(float(RAW[i]["price_sar"]) for i in ok)))
                worst_walk = max(worst_walk, abs(st.mean(float(RAW[i]["walking_distance_m"]) for i in ex) - st.mean(float(RAW[i]["walking_distance_m"]) for i in ok)))
    assert round(worst_price) <= 22 and round(worst_walk) <= 35, (worst_price, worst_walk)


def test_every_description_is_two_sentences():
    for pid, r in RAW.items():
        t = r["description"].strip()
        assert t, pid
        parts = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])', t) if s]
        assert len(parts) == 2, (pid, t)


# Words a neutral description must not contain (whole words only, so "ramparts" is not "ramp").
# The place's own name is removed before checking (names never change).
FORBIDDEN = {
    "facilities": r"entrance|entrances|step|steps|stair|stairs|staircase|ramp|ramps|lift|lifts|elevator|elevators|escalator|path|paths|pathway|walkway|floor|floors|parking|toilet|toilets|restroom|restrooms|seat|seats|seating|bench|benches|audio|sign|signs|signage|label|labels|labelled|braille|caption|captions|subtitle|subtitles|staff|wheelchair|accessible|accessibility|tactile|touch|alarm|paved|flat",
    "people or suitability": r"disabled|disability|disabilities|blind|deaf|elderly|seniors?|children|kids|family|families|family-friendly|suitable|ideal|perfect|everyone|inclusive|easy|easily|comfortable|quiet|calm|safe",
    "praise": r"best|stunning|must-see|unique|hidden gem|unforgettable|breathtaking|spectacular|amazing|world-class|iconic|famous|renowned|popular|favoured|favored|well-known",
    "price or opening times": r"price|prices|priced|cost|costs|free|ticket|tickets|SAR|riyals?|cheap|expensive|affordable|hours?|minutes?|daily opening|open daily|o'clock|pm|am|weekend|weekends",
    "describe": r"describe|describes|described|describing",
}
# Time-of-day words are allowed only where they are the activity itself (decided 28 Oct 2026).
TIME_WORDS = r"morning|afternoon|evening|evenings|night|nights|overnight|sunset|sunrise|sun set|dusk|dawn|after dark"
TIME_ALLOWED = {"P045": "evening life (history of the quarter)", "P063": "night sky (Starlit Sands Camp)",
                "P064": "watch the sun set (Sunset Ridge Dune Drive)", "P068": "a night, after dark (Overnight Camp)",
                "P094": "watch the sun set (Burj Al Ghurub, sunset deck)", "P144": "evening gathering (the venue's concept)"}


def _without_name(pid):
    return RAW[pid]["description"].replace(RAW[pid]["name"], " ")


def test_descriptions_have_no_forbidden_words():
    bad = []
    for pid in RAW:
        text = _without_name(pid)
        for group, pat in FORBIDDEN.items():
            found = re.findall(r"\b(" + pat + r")\b", text, flags=re.I)
            if found:
                bad.append((pid, group, sorted(set(w.lower() for w in found))))
    assert not bad, bad


def test_time_words_only_where_they_are_the_activity():
    bad = [pid for pid in RAW if re.search(r"\b(" + TIME_WORDS + r")\b", _without_name(pid), flags=re.I) and pid not in TIME_ALLOWED]
    assert not bad, bad


def test_description_length_does_not_follow_the_verdict():
    """Compared inside each category, because categories differ in typical length (decks and shows have
    shorter descriptions than heritage sites), so an overall difference can come from the category mix."""
    words = {pid: len(r["description"].split()) for pid, r in RAW.items()}
    for d in DISABILITIES:
        ex = [pid for pid in RAW if DEC[(pid, d)].outcome == "EXCLUDED"]
        ok = [pid for pid in RAW if DEC[(pid, d)].outcome != "EXCLUDED"]
        gap = st.mean(words[i] for i in ex) - st.mean(words[i] for i in ok)
        print(f"      overall {d}: excluded {st.mean(words[i] for i in ex):.2f} vs usable {st.mean(words[i] for i in ok):.2f} words (gap {gap:+.2f}, reported, not a pass/fail)")
        for cat in CATS:
            e = [i for i in ex if RAW[i]["category"] == cat]; o = [i for i in ok if RAW[i]["category"] == cat]
            if e and o:
                assert abs(st.mean(words[i] for i in e) - st.mean(words[i] for i in o)) <= 4.0, (d, cat)


AREA_WORDS = (r"Diriyah|Turaif|Batha|Murabba|Hanifa|Olaya|Malaz|Thumamah|Sulimaniyah|Nakheel|Yasmin|Wurud|Hittin|Aqiq|"
              r"Muruj|Rawdah|Qurtubah|King Abdullah|Financial District|"
              r"Tuwaiq|Khafs|Nafud|Namar|Laban|Sulay|Ghadir|Hamra|Dira|Red Dunes|red sand")  # v7.4: real places and districts


def test_no_district_column_and_no_district_names():
    assert "district" not in next(iter(RAW.values()))
    bad = [pid for pid, r in RAW.items() if re.search(r"\b(" + AREA_WORDS + r")\b", r["name"] + " " + r["description"])]
    assert not bad, bad


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t(); print("PASS ", t.__name__)
    print(f"\nAll {len(tests)} real-data checks passed.")
