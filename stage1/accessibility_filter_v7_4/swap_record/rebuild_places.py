"""Step 2: rebuild places.csv from the v6 file, the swap assignment, the six renames (data/renames.csv), the
final descriptions, and the removal of the district column (28 Oct 2026); check it equals places.csv.

Run from the filter folder:  python swap_record/rebuild_places.py
"""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from filter import FEATURES

assign = json.load(open(os.path.join(HERE, "assignment.json")))
src_of = {p: r for pairs in assign.values() for p, r in pairs}
v6 = list(csv.DictReader(open(os.path.join(HERE, "places_v6_before_swap.csv"), encoding="utf-8-sig")))
cols = list(v6[0].keys()); byid = {r["place_id"]: r for r in v6}
desc = {r["place_id"]: r["description"] for r in csv.DictReader(open(os.path.join(ROOT, "data", "descriptions_final.csv"), encoding="utf-8-sig"))}
new_name = {r["place_id"]: r["new_name"] for r in csv.DictReader(open(os.path.join(ROOT, "data", "renames.csv"), encoding="utf-8-sig"))}
cols = [c for c in cols if c != "district"]
rebuilt = []
for p in v6:
    s = byid[src_of[p["place_id"]]]
    assert s["category"] == p["category"], "a row moved across categories"
    q = dict(p)
    for f in FEATURES: q[f] = s[f]
    q["description"] = desc[p["place_id"]]
    q["name"] = new_name.get(p["place_id"], q["name"])
    q.pop("district", None)
    rebuilt.append({c: q[c] for c in cols})
current = list(csv.DictReader(open(os.path.join(ROOT, "places.csv"), encoding="utf-8-sig")))
print("Rebuilt places identical to places.csv:", rebuilt == current)
# the plan moves with the rows in the same way
plan6 = {r["place_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "plan_v6_before_swap.csv"), encoding="utf-8-sig"))}
plan7 = list(csv.DictReader(open(os.path.join(ROOT, "data", "plan.csv"), encoding="utf-8-sig")))
ok = all({k: v for k, v in plan6[src_of[r["place_id"]]].items() if k not in ("place_id", "category")} ==
         {k: v for k, v in r.items() if k not in ("place_id", "category")} for r in plan7)
print("data/plan.csv equals the v6 plan moved with the rows:", ok)
