"""v7.4 (28 Oct 2026, decided by Alanoud after the final data review): rename 12 places whose names are (or very likely are) real,
well-known places or real Riyadh district names, so ChatGPT cannot pick or avoid them for a real place's fame or
an area's reputation. Same reason as the district removal in v7.3. Facilities, prices and all other columns are
unchanged. Only the name (and two description phrases that named a real place) change.
Usage: python rename_real_names.py <v7.3 places.csv> <out places.csv> <out descriptions.csv> <renames.csv to extend>
"""
import csv, sys
SRC, OUT_PLACES, OUT_DESC, RENAMES = sys.argv[1:5]
RENAME = {  # place_id: (old name, new name, why the old name was a problem)
 'P034': ('Hisn Al Dira Fort', 'Hisn Al Turab Fort', 'Al Dira: very likely the name of old Riyadh\'s historic centre (renamed to be safe)'),
 'P061': ('Red Dunes Camp', 'Sand Valley Camp', 'the Red Sand Dunes are a well-known Riyadh attraction'),
 'P062': ('Edge of Tuwaiq Dune Safari', 'Rocky Rim Dune Safari', 'Tuwaiq escarpment / Edge of the World'),
 'P065': ('Nafud Falcon Camp', 'Falcon Wing Desert Camp', 'the Nafud is a real desert'),
 'P073': ('Wadi Namar Reserve', 'Wadi Al Qata Reserve', 'Wadi Namar: real park and dam in Riyadh'),
 'P074': ('Tuwaiq Escarpment Reserve', 'Hafat Al Sakhr Reserve', 'Tuwaiq escarpment'),
 'P075': ('Raudat Al Khafs Reserve', 'Raudat Al Zuhur Reserve', 'Rawdat Al Khafs: real, well-known place'),
 'P076': ('Wadi Laban Nature Reserve', 'Wadi Al Uqab Nature Reserve', 'Wadi Laban: real valley in Riyadh'),
 'P077': ('Shaib Al Ghadir Reserve', 'Shaib Al Sail Reserve', 'Al Ghadir: real Riyadh district'),
 'P080': ('Jabal Al Hamra Reserve', 'Jabal Al Sawan Reserve', 'Al Hamra: real Riyadh district'),
 'P082': ('Wadi Sulay Nature Reserve', 'Wadi Al Dhib Nature Reserve', 'Wadi Al Sulay: believed to be a real valley in Riyadh (renamed to be safe)'),
 'P112': ('Mujamma Al Ghadir Mall', 'Mujamma Al Yaqut Mall', 'Al Ghadir: real Riyadh district'),
}
PHRASES = {  # description phrases that named or pointed to a real place
 'P061': ('set among red sand dunes', 'set among sand dunes'),
 'P062': ('near the Tuwaiq escarpment', 'near a rocky escarpment'),
}
P = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
cols = list(P[0].keys())
new_rows = []
for r in P:
    pid = r['place_id']
    if pid in RENAME:
        old, new, why = RENAME[pid]
        assert r['name'] == old, pid
        assert r['description'].startswith(old + ' '), pid
        r['name'] = new
        r['description'] = new + r['description'][len(old):]
        new_rows.append({'place_id': pid, 'old_name': old, 'new_name': new, 'version': 'v7.4', 'reason': why})
    if pid in PHRASES:
        a, b = PHRASES[pid]
        assert a in r['description'], pid
        r['description'] = r['description'].replace(a, b)
assert len(new_rows) == len(RENAME)
with open(OUT_PLACES, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(P)
with open(OUT_DESC, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh); w.writerow(['place_id', 'description'])
    for r in P: w.writerow([r['place_id'], r['description']])
old = list(csv.DictReader(open(RENAMES, encoding='utf-8-sig')))
for r in old:
    r.setdefault('version', 'v7.3'); r['version'] = r.get('version') or 'v7.3'
    r.setdefault('reason', 'name contained a real Riyadh area'); r['reason'] = r.get('reason') or 'name contained a real Riyadh area'
old = [r for r in old if r['version'] != 'v7.4'] + new_rows
with open(RENAMES, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=['place_id', 'old_name', 'new_name', 'version', 'reason'])
    w.writeheader(); w.writerows(old)
print('renamed', len(new_rows), 'places; renames.csv now has', len(old), 'rows')
