"""Step 1 of the facility swap (28 Oct 2026): find which facility row goes to which place.

Whole facility rows (all 23 yes/no columns) are moved only between places of the SAME category,
so every category keeps the same rows and every count per category and disability stays the same.
The search looks for the arrangement where excluded, gap and usable places have similar price and
walking distance, for all three disabilities at once. Places used as examples in the team documents
are not moved. Seeded random search (seed 20261028), so the result is reproducible.

Run from the filter folder:  python swap_record/find_assignment.py
Writes swap_record/assignment_reproduced.json and says whether it equals assignment.json.
"""
import collections, csv, json, os, random, statistics as st, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from filter import DISABILITIES, decide, load_categories, load_places

FIXED = {"P001", "P009", "P027", "P034", "P045", "P046"}
cats = load_categories(os.path.join(ROOT, "categories.csv"))
v6 = load_places(os.path.join(HERE, "places_v6_before_swap.csv"), cats)
out = {(p["place_id"], d): decide(p, d).outcome for p in v6 for d in DISABILITIES}
P = list(csv.DictReader(open(os.path.join(HERE, "places_v6_before_swap.csv"), encoding="utf-8-sig")))
bycat = collections.defaultdict(list)
for r in P: bycat[r["category"]].append(r)

def cost(places, rows):
    price = [float(p["price_sar"]) for p in places]; walk = [float(p["walking_distance_m"]) for p in places]
    sp = st.pstdev(price) or 1; sw = st.pstdev(walk) or 1; c = 0
    for dis in DISABILITIES:
        for grp, w in (("EXCLUDED", 3), ("ELIGIBLE_WITH_CAVEATS", 1)):
            idx = [i for i, r in enumerate(rows) if out[(r, dis)] == grp]
            rest = [i for i in range(len(rows)) if i not in idx]
            if not idx or not rest: continue
            dp = (st.mean(price[i] for i in idx) - st.mean(price[i] for i in rest)) / sp
            dw = (st.mean(walk[i] for i in idx) - st.mean(walk[i] for i in rest)) / sw
            c += w * (dp * dp + dw * dw)
    return c

random.seed(20261028)
result = {}
for cat, places in bycat.items():
    rows = [p["place_id"] for p in places]
    best = rows[:]; bc = cost(places, best)
    free = [i for i, p in enumerate(places) if p["place_id"] not in FIXED]
    for restart in range(6):
        cur = rows[:]
        fr = [cur[i] for i in free]; random.shuffle(fr)
        for k, i in enumerate(free): cur[i] = fr[k]
        cc = cost(places, cur)
        for it in range(800):
            a, b = random.sample(free, 2); cur[a], cur[b] = cur[b], cur[a]
            nc = cost(places, cur)
            if nc <= cc: cc = nc
            else: cur[a], cur[b] = cur[b], cur[a]
        if cc < bc: bc, best = cc, cur[:]
    result[cat] = [[p["place_id"], r] for p, r in zip(places, best)]
json.dump(result, open(os.path.join(HERE, "assignment_reproduced.json"), "w"))
saved = json.load(open(os.path.join(HERE, "assignment.json")))
print("Reproduced assignment equals assignment.json:", result == saved)
