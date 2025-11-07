from git import Repo
from datetime import datetime
import json

# gets git based provenance of analyzed_data.json
repo = Repo(".")

file_path = "analyzed_data.json"

provenance = {}

for commit in repo.iter_commits(paths=file_path):
    try:
        blob = commit.tree / file_path
        content = blob.data_stream.read().decode("utf-8", errors="replace").strip()
        content = json.loads(content)
        provenance[commit.committed_datetime.date().isoformat()] = content
    except:
        pass # just ignore initial commits

# get current
with open(file_path, "r") as f:
    content = json.load(f)
    provenance[datetime.now().date().isoformat()] = content

print(json.dumps(provenance, indent=2))
