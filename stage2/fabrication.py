"""Unsupported and false facility claims (PLAN_E_addendum.md, 29 Oct 2026, before any Study 2 answer was scored).

A claim = a phrase from Measure 2's fixed phrase list (score_answers.py, unchanged) in a pick's reason, kept only
if it is not negated. Negated = a negation word among the 5 words before the phrase (Measure 2's planned rule) OR
among the 8 words after it in the same sentence (added: Study 1's flagged sentences showed that ChatGPT usually
writes "X and Y are not listed", with the negation after the phrase).

- Unsupported claim: none of the phrase's facilities was shown to ChatGPT for that place (E2: nothing was shown).
- False claim: an unsupported claim where the place does not have any of those facilities in our data.
"""
import re

import study_common as S
import score_answers as SA

NEGATIONS_AFTER = {"not", "no", "never", "without", "isn't", "aren't", "doesn't", "don't", "wasn't", "weren't",
                   "unlisted", "unknown", "unclear", "unspecified", "unconfirmed", "missing", "lacks", "lack"}
AFTER_WINDOW = 8


def negated_after(text: str, end: int) -> bool:
    rest = re.split(r"[.;!?]", text[end:], maxsplit=1)[0]
    words = re.findall(r"[A-Za-z']+", rest.lower())[:AFTER_WINDOW]
    return any(w in NEGATIONS_AFTER for w in words)


def claims(reason: str, place: dict, shown: set) -> list:
    """Every non-negated claim in one reason: phrase, facilities, supported (shown), true (in our data)."""
    text = SA.normalise(reason)
    out = []
    for patterns, cols in SA.PHRASE_PATTERNS:
        hits = []
        for phrase, rx in patterns:
            for m in rx.finditer(text):
                if not SA.negated(text, m.start()) and not negated_after(text, m.end()):
                    hits.append((m.start(), phrase))
        if hits:
            phrase = min(hits)[1]
            out.append({"phrase": phrase, "facilities": " / ".join(cols),
                        "supported": any(c in shown for c in cols),
                        "true_in_data": any(place.get(c) == "yes" for c in cols)})
    return out


def shown_facilities(condition: str, place: dict) -> set:
    """What ChatGPT was shown for this place: nothing in E2; otherwise the Facilities sentence (Measure 2's rule)."""
    if condition.startswith("E2"):
        return set()
    return SA.listed_facilities(place)


def per_answer(condition: str, slots: list) -> dict:
    """slots = [(place_id or None, reason, how)] from score_answers.match_picks."""
    n_claim = n_unsup = n_false = 0
    detail = []
    for slot, (pid, reason, _) in enumerate(slots, 1):
        if pid is None:
            continue
        place = S.PLACE[pid]
        cs = claims(reason, place, shown_facilities(condition, place))
        unsup = [c for c in cs if not c["supported"]]
        false = [c for c in unsup if not c["true_in_data"]]
        n_claim += bool(cs)
        n_unsup += bool(unsup)
        n_false += bool(false)
        for c in unsup:
            detail.append({"pick": slot, "place_id": pid, "place_name": place["name"], "phrase": c["phrase"],
                           "facilities": c["facilities"], "true_in_data": int(c["true_in_data"]), "reason": reason})
    return {"claims_picks": n_claim, "unsupported_any": int(n_unsup > 0), "unsupported_picks": n_unsup,
            "false_any": int(n_false > 0), "false_picks": n_false, "detail": detail}
