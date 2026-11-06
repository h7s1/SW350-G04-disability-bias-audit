"""Remove district names from the data (28 Oct 2026, decided by Alanoud): ChatGPT must decide from the listed
information only, without a district's reputation. Drops the district column, removes the district phrase from
every description, and renames six places whose names contained a real area name.
Usage: python remove_districts.py <v7.2 places.csv> <out places.csv> <out descriptions.csv> <out renames.csv>"""
import csv, re, sys
SRC, OUT_PLACES, OUT_DESC, OUT_RENAMES = sys.argv[1:5]
P = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
RENAME = {
 'P019': ('Atelier Al Nakheel', 'Atelier Al Ishraq'),
 'P037': ('Footsteps of Turaif Walking Tour', 'Footsteps of the Elders Walking Tour'),
 'P038': ('Murabba Palace Lanes Tour', 'Palace Lanes Heritage Tour'),
 'P039': ('Batha Old Trade Route Tour', 'Old Trade Route Tour'),
 'P042': ('Whispers of Old Batha Tour', 'Whispers of the Old Quarter Tour'),
 'P043': ('Wadi Hanifa Heritage Trail Tour', 'Valley Heritage Trail Tour'),
}
MANUAL = {  # descriptions where the district is part of the sentence, rewritten by hand
 'P019': 'Atelier Al Ishraq is a gallery and studio space for painting and mixed media. Visitors see finished works and observe the techniques artists use.',
 'P037': 'Footsteps of the Elders Walking Tour is a guided heritage tour of a historic area. A guide leads visitors through the old quarter and explains the history of its buildings.',
 'P038': 'Palace Lanes Heritage Tour is a guided walk through the old lanes around a historic palace district. A guide explains the history of the buildings and the people who lived there.',
 'P039': 'Old Trade Route Tour follows a historic merchant route through the old city with a guide. Visitors walk the old streets while the guide explains how goods and travellers once moved through the area.',
 'P042': 'Whispers of the Old Quarter Tour is a guided heritage walk through the historic streets of the old city. The guide shares accounts of daily life in the old neighbourhood as the group moves between sites.',
 'P043': 'Valley Heritage Trail Tour is a guided walk along a historic wadi. A guide explains how the valley supported farms and settlements in earlier times.',
 'P045': 'Lamps of the Old City Tour is a guided walk through a historic quarter. The guide explains how lighting and evening life shaped the old city\'s routines.',
 'P091': 'Qimat Al Mashhad Tower is a tower with a viewing area at its top. Visitors survey the skyline and the roads that run through it.',
 'P011': 'Bayt Al Dhakira Museum preserves objects that record local memory and history. Visitors study the displays to understand how residents lived, worked and gathered.',
 'P093': 'Manar Al Madina Deck is a lookout on a slim tower that rises above the neighbourhood. Visitors look over the city in every direction.',
}
renames = []
for r in P:
    pid, d = r['place_id'], r['district']
    if pid in RENAME:
        old, new = RENAME[pid]; assert r['name'] == old, pid
        r['name'] = new; renames.append((pid, old, new))
    if pid in MANUAL:
        r['description'] = MANUAL[pid]
    else:
        t = r['description']
        t2 = re.sub(r',? located in (the )?' + re.escape(d) + r',?', '', t, count=1)
        if t2 == t: t2 = re.sub(r' in (the )?' + re.escape(d) + r'\b', '', t, count=1)
        assert t2 != t, pid
        r['description'] = re.sub(r'\s{2,}', ' ', t2)
cols = [c for c in P[0].keys() if c != 'district']
with open(OUT_PLACES, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(P)
with open(OUT_DESC, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh); w.writerow(['place_id', 'description'])
    for r in P: w.writerow([r['place_id'], r['description']])
with open(OUT_RENAMES, 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.writer(fh); w.writerow(['place_id', 'old_name', 'new_name']); w.writerows(renames)
print('done', len(P), 'places;', len(renames), 'renamed')
