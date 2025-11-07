from git import Repo
from datetime import datetime
import json
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "no-latex", "nature", "high-vis"])

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
        pass  # just ignore initial commits

# get current
with open(file_path, "r") as f:
    content = json.load(f)
    provenance[datetime.now().date().isoformat()] = content


def plot(x, y, x_title, title, filename, type=None):
    plt.figure()
    if type == "bar":
        plt.bar(x, y)
    else:
        plt.plot(x, y)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Total downloads")
    plt.xlabel(x_title)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

items = sorted(provenance.items(), key=lambda x: x[0])
dates = [datetime.fromisoformat(d) for d, _ in items]
values = [sum(entry.get("platforms").values()) for _, entry in items if "platforms" in entry]
plot(dates, values, "Date", "Downloads (historical)", "history.png")

print(json.dumps(provenance, indent=2))
