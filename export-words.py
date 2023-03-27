#!/usr/bin/env python

# Export English words to stdout

import json
import os
from anki.collection import Collection


def dump_json(obj, f):
    json.dump(obj, f, sort_keys=True, indent=4, ensure_ascii=False)


profile = 'new'
user = os.getenv('USER')
profile_path = f"/home/{user}/.local/share/Anki2/{profile}/collection.anki2"

col = Collection(profile_path)

# Media files to be fetched
media_files = set()

for m in col.models.all():
    mname = m['name']
    if mname != 'English Yaryna':
        continue
    for nid in col.models.nids(m['id']):
        note = col.get_note(nid)
        print(note.fields[0])

col.close()
