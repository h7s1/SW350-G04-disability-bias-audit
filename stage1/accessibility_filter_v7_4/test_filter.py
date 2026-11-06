"""
Hard-case tests for the filter (v7.1); 35 tests of the decision logic on made-up test places. The real data is checked in test_real_data.py. Run:  python test_filter.py   (or pytest)
Each test is a situation where one or more things are missing.
"""

import itertools

from filter import (CAVEATS, DEMANDS, DISABILITIES, ELIGIBLE, ESSENTIAL, EXCLUDED, FEATURES,
                    IMPORTANT, NOT_APPLICABLE, RULES, check_rule, decide, filter_candidates,
                    freeze, tier_for, validate_place)

CATS = {
    "restaurant":   dict(setting="indoor",  core_requires_movement="no",  visual_content="no",  spoken_content="no"),
    "art_museum":   dict(setting="indoor",  core_requires_movement="yes", visual_content="yes", spoken_content="no"),
    "heritage_walk": dict(setting="outdoor", core_requires_movement="yes", visual_content="no",  spoken_content="yes"),
    "viewpoint":    dict(setting="outdoor", core_requires_movement="no",  visual_content="yes", spoken_content="no"),
    "theatre":      dict(setting="indoor",  core_requires_movement="no",  visual_content="yes", spoken_content="yes"),
    "park":         dict(setting="outdoor", core_requires_movement="yes", visual_content="no",  spoken_content="no"),
    "talk_show":    dict(setting="indoor",  core_requires_movement="no",  visual_content="no",  spoken_content="yes"),
}


def place(category, default="yes", **features):
    """A place where every feature is `default`, then the given ones changed."""
    raw = dict(place_id="T", name="test", category=category)
    raw.update({f: default for f in FEATURES})
    raw.update(features)
    return validate_place(raw, CATS)


# ===================== Wheelchair: one or more things missing =====================
def test_level_entrance_no_but_ramp_yes_is_fine():
    d = decide(place("restaurant", level_entrance="no", entrance_ramp="yes", entrance_lift="no"), "mobility")
    assert d.outcome == ELIGIBLE


def test_all_three_entrance_options_no_is_excluded():
    d = decide(place("restaurant", level_entrance="no", entrance_ramp="no", entrance_lift="no"), "mobility")
    assert d.outcome == EXCLUDED and d.excluded_by == ["W2"]


def test_interior_elevator_does_not_fix_steps_at_the_door():
    d = decide(place("art_museum", level_entrance="no", entrance_ramp="no", entrance_lift="no",
                     step_free_interior="yes"), "mobility")
    assert d.outcome == EXCLUDED and "W2" in d.excluded_by


def test_good_entrance_but_steps_on_the_path_from_parking():          # the "P12" case
    d = decide(place("art_museum", step_free_approach="no"), "mobility")
    assert d.outcome == EXCLUDED and d.excluded_by == ["W1"]


def test_good_entrance_but_door_too_narrow():
    d = decide(place("restaurant", wide_entrance_door="no"), "mobility")
    assert d.excluded_by == ["W3"]


def test_restaurant_with_tables_only_upstairs_is_excluded_even_without_movement():
    d = decide(place("restaurant", activity_point_step_free="no", step_free_interior="no"), "mobility")
    assert d.outcome == EXCLUDED and d.excluded_by == ["W4"]
    assert d.results["W5"][0] == NOT_APPLICABLE        # moving around does not apply to a restaurant


def test_viewpoint_on_sand_is_fine_when_no_walking_is_needed():
    d = decide(place("viewpoint", paved_route="no", step_free_interior="no"), "mobility")
    assert d.results["W6"][0] == NOT_APPLICABLE and d.outcome == ELIGIBLE


def test_walking_tour_on_sand_is_excluded():
    d = decide(place("heritage_walk", paved_route="no"), "mobility")
    assert d.excluded_by == ["W6"]


def test_no_toilet_alone_gives_caveat_not_exclusion():
    d = decide(place("art_museum", accessible_toilet="no"), "mobility")
    assert d.outcome == CAVEATS and d.caveats == ["W7"]


def test_no_toilet_and_no_parking_gives_two_caveats():
    d = decide(place("art_museum", accessible_toilet="no", accessible_parking_or_dropoff="no"), "mobility")
    assert d.outcome == CAVEATS and set(d.caveats) == {"W7", "W8"}


def test_essential_and_important_both_fail_exclusion_wins_and_caveats_still_reported():
    d = decide(place("art_museum", level_entrance="no", entrance_ramp="no", entrance_lift="no",
                     accessible_toilet="no"), "mobility")
    assert d.outcome == EXCLUDED and d.excluded_by == ["W2"] and d.caveats == ["W7"]


def test_many_good_extras_cannot_make_up_for_one_essential_failure():
    d = decide(place("restaurant", step_free_approach="no"), "mobility")   # everything else yes
    assert d.outcome == EXCLUDED


# ===================== Blind: one or more things missing =====================
def test_art_museum_with_no_non_visual_option_is_excluded():
    d = decide(place("art_museum", audio_guide="no", audio_description="no", tactile_exhibits="no",
                     described_guided_tour="no"), "visual")
    assert d.outcome == EXCLUDED and d.excluded_by == ["B1"]


def test_art_museum_with_only_tactile_exhibits_is_enough():
    d = decide(place("art_museum", audio_guide="no", audio_description="no", tactile_exhibits="yes",
                     described_guided_tour="no"), "visual")
    assert d.results["B1"][0] == "PASS"


def test_staff_help_does_not_replace_access_to_the_experience():
    # staff assistance is navigation, not a description of the art
    d = decide(place("art_museum", audio_guide="no", audio_description="no", tactile_exhibits="no",
                     described_guided_tour="no", staff_assistance="yes"), "visual")
    assert d.outcome == EXCLUDED


def test_park_without_audio_or_touch_is_not_affected_by_b1():
    d = decide(place("park", audio_guide="no", audio_description="no", tactile_exhibits="no",
                     described_guided_tour="no"), "visual")
    assert d.results["B1"][0] == NOT_APPLICABLE and d.outcome == ELIGIBLE


def test_low_visual_place_without_audio_guide_is_not_affected():       # the spice souq case
    d = decide(place("restaurant", audio_guide="no", audio_description="no", tactile_exhibits="no",
                     described_guided_tour="no"), "visual")
    assert d.results["B1"][0] == NOT_APPLICABLE and d.outcome == ELIGIBLE


def test_no_navigation_support_is_a_caveat_not_an_exclusion():
    d = decide(place("park", tactile_paving="no", staff_assistance="no", described_guided_tour="no"), "visual")
    assert d.outcome == CAVEATS and "B2" in d.caveats and d.excluded_by == []


# ===================== Deaf: one or more things missing =====================
def test_spoken_walking_tour_with_nothing_for_deaf_is_excluded():
    d = decide(place("heritage_walk", captions="no", written_content="no", sign_language_interpreter="no"), "hearing")
    assert d.excluded_by == ["D1"]


def test_sign_language_alone_is_enough():
    d = decide(place("theatre", captions="no", written_content="no", sign_language_interpreter="yes"), "hearing")
    assert d.results["D1"][0] == "PASS"


def test_spoken_talk_with_nothing_for_deaf_is_excluded():
    d = decide(place("talk_show", captions="no", written_content="no", sign_language_interpreter="no"), "hearing")
    assert d.outcome == EXCLUDED and d.excluded_by == ["D1"]


def test_art_museum_without_captions_is_fine_for_deaf():
    d = decide(place("art_museum", captions="no", written_content="no", sign_language_interpreter="no"), "hearing")
    assert d.results["D1"][0] == NOT_APPLICABLE and d.outcome == ELIGIBLE


def test_visual_alarm_only_counts_indoors():
    assert decide(place("park", visual_alarm="no"), "hearing").results["D3"][0] == NOT_APPLICABLE
    assert "D3" in decide(place("art_museum", visual_alarm="no"), "hearing").caveats


# ===================== One place, three people =====================
def test_same_place_different_result_per_person():
    p = place("art_museum", audio_guide="no", audio_description="no", tactile_exhibits="no",
              described_guided_tour="no", captions="no")
    assert decide(p, "mobility").outcome == ELIGIBLE
    assert decide(p, "visual").outcome == EXCLUDED
    assert decide(p, "hearing").outcome == ELIGIBLE


def test_place_with_nothing_at_all():
    p = place("restaurant", default="no")
    assert decide(p, "mobility").outcome == EXCLUDED
    assert decide(p, "visual").outcome == CAVEATS     # low sight: only navigation and information missing
    assert decide(p, "hearing").outcome == CAVEATS


# ===================== Properties: no contradictions, no bias =====================
def test_every_demand_combination_gives_each_rule_exactly_one_meaning():
    keys = list(DEMANDS)
    for combo in itertools.product(*(sorted(DEMANDS[k]) for k in keys)):
        demo = dict(zip(keys, combo))
        for r in RULES:
            assert tier_for(r, demo) in {ESSENTIAL, IMPORTANT, None}


def test_every_place_gets_exactly_one_outcome_for_all_demand_combinations():
    keys = list(DEMANDS)
    for combo in itertools.product(*(sorted(DEMANDS[k]) for k in keys)):
        cats = {"c": dict(zip(keys, combo))}
        for default in ("yes", "no"):
            raw = dict(place_id="X", name="x", category="c", **{f: default for f in FEATURES})
            p = validate_place(raw, cats)
            for d in DISABILITIES:
                assert decide(p, d).outcome in {ELIGIBLE, CAVEATS, EXCLUDED}


def test_fully_accessible_place_is_eligible_for_everyone_in_every_category():
    for c in CATS:
        for d in DISABILITIES:
            assert decide(place(c), d).outcome == ELIGIBLE, (c, d)


def test_rules_only_read_place_features():
    for r in RULES:
        assert set(r.met_by) <= set(FEATURES), r.rule_id
        assert set(r.only_if) <= set(DEMANDS), r.rule_id


def test_only_essential_rules_can_exclude():
    for c in CATS:
        p = place(c, default="no")
        for d in DISABILITIES:
            x = decide(p, d)
            for rid in x.excluded_by:
                assert x.results[rid][1] == ESSENTIAL


def test_every_essential_rule_can_exclude_on_its_own():
    reachable = set()
    keys = list(DEMANDS)
    for combo in itertools.product(*(sorted(DEMANDS[k]) for k in keys)):
        raw = dict(place_id="X", name="x", category="c", **{f: "no" for f in FEATURES})
        p = validate_place(raw, {"c": dict(zip(keys, combo))})
        for d in DISABILITIES:
            reachable.update(decide(p, d).excluded_by)
    can_be_essential = {r.rule_id for r in RULES
                        if r.base_tier == ESSENTIAL or (r.tier_by and ESSENTIAL in r.tier_by[1].values())}
    assert can_be_essential <= reachable, can_be_essential - reachable


def test_no_disability_sends_the_full_list():
    ps = [place("restaurant", default="no") for _ in range(4)]
    assert len(filter_candidates(ps, None)) == 4


# ===================== Data safety =====================
def test_blank_or_unknown_values_are_refused():
    for bad in ("", "unknown", "maybe"):
        try:
            place("restaurant", captions=bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad!r}")


def test_unknown_category_is_refused():
    try:
        validate_place(dict(place_id="X", category="zoo", **{f: "yes" for f in FEATURES}), CATS)
    except ValueError:
        return
    raise AssertionError("accepted unknown category")


def test_freeze_refuses_while_sources_are_unchecked():
    if all(r.source_checked for r in RULES):
        return
    try:
        freeze("should_not_exist.txt")
    except RuntimeError:
        return
    raise AssertionError("froze with unchecked sources")


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS  {t.__name__}")
    print(f"\nAll {len(tests)} tests passed.")
