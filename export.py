#!/usr/bin/env python

# Export parts of Anki collection into text files for
# tracking in the repository.

import json
import os
from pathlib import Path
from anki.collection import Collection
import subprocess


out_dir = Path(__file__).absolute().parent.joinpath('out')


def dump_json(obj, f):
    json.dump(obj, f, sort_keys=True, indent=4, ensure_ascii=False)


profile = 'new'
user = os.getenv('USER')
profile_path = f"/home/{user}/.local/share/Anki2/{profile}/collection.anki2"

col = Collection(profile_path)
Path(f"{out_dir}/models").mkdir(parents=True, exist_ok=True)
for m in col.models.all():
    dname = f"{out_dir}/models/{m['name']}"
    Path(dname).mkdir(parents=True, exist_ok=True)
    with open(f"{dname}/index", 'w') as f:
        dump_json(m, f)
    notes = []
    for nid in col.models.nids(m['id']):
        note = col.get_note(nid)
        notes.append([note.id, note.fields, note.tags])
    with open(f"{dname}/notes", 'w') as f:
        dump_json(notes, f)

subprocess.run(['rsync', '-raP', '--delete', f"{col.media.dir()}", out_dir])

col.close()
