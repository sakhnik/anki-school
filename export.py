#!/usr/bin/env python

# Export parts of Anki collection into text files for
# tracking in the repository.

import json
import os
from pathlib import Path
from anki.collection import Collection
import subprocess
import glob


out_dir = Path(__file__).absolute().parent.joinpath('out')


# Only include the models relevant to School
def include_model(name):
    return any((n in name for n in ['Yaryna', 'Solomiia', 'Daryna']))


def dump_json(obj, f):
    json.dump(obj, f, sort_keys=True, indent=4, ensure_ascii=False)


profile = 'new'
user = os.getenv('USER')
profile_path = f"/home/{user}/.local/share/Anki2/{profile}/collection.anki2"

col = Collection(profile_path)
Path(f"{out_dir}/models").mkdir(parents=True, exist_ok=True)

# Media files to be fetched
media_files = set()

for m in col.models.all():
    mname = m['name']
    if not include_model(mname):
        continue
    dname = f"{out_dir}/models/{mname}"
    Path(dname).mkdir(parents=True, exist_ok=True)
    with open(f"{dname}/index", 'w') as f:
        dump_json(m, f)
    notes = []
    for nid in col.models.nids(m['id']):
        note = col.get_note(nid)
        notes.append([note.id, note.fields, note.tags])
        # Collect media files names mentioned in the notes
        for field in note.fields:
            media_files.update(col.media.files_in_str(m['id'], field))
    with open(f"{dname}/notes", 'w') as f:
        dump_json(notes, f)

# Copy scripts too
script_files = glob.glob(f"{col.media.dir()}/_*.js")
media_files = media_files.union({os.path.basename(f) for f in script_files})

# Use rsync to copy media files
file_list = set(f"{col.media.dir()}/./{f}" for f in media_files)
file_list = '\n'.join(sorted(file_list))
subprocess.run(['rsync', '-raP', '--delete', "--files-from=-", "/",
                out_dir.joinpath('collection.media')],
               input=file_list.encode('utf8'))

col.close()
