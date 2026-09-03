import argparse

from git import Repo
from datetime import datetime
import json
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "no-latex", "nature", "high-vis"])

parser = argparse.ArgumentParser("plotter")
parser.add_argument("--name", nargs="+", default=["sciwin", "sciwin_studio"], help="repo name(s)")

args = parser.parse_args()

# gets git based provenance of <name>_analyzed_data.json for each repo name
repo = Repo(".")


def load_provenance(name):
    file_path = f"{name}_analyzed_data.json"
    # "sciwin" was tracked prefix-less before per-repo prefixes were introduced,
    # so its whole git history still lives under the old, unprefixed filename.
    legacy_path = "analyzed_data.json" if name == "sciwin" else None
    candidate_paths = [file_path] + ([legacy_path] if legacy_path else [])

    provenance = {}

    for commit in repo.iter_commits(paths=candidate_paths):
        for path in candidate_paths:
            try:
                blob = commit.tree / path
                content = (
                    blob.data_stream.read().decode("utf-8", errors="replace").strip()
                )
                content = json.loads(content)
                provenance[commit.committed_datetime.date().isoformat()] = content
                break
            except:
                continue  # path not present at this commit, or initial commit

    # get current
    content = None
    for path in candidate_paths:
        try:
            with open(path, "r") as f:
                content = json.load(f)
            break
        except FileNotFoundError:
            continue
    if content is None:
        raise FileNotFoundError(f"none of {candidate_paths} exist")
    provenance[datetime.now().date().isoformat()] = content

    return provenance


provenance = {name: load_provenance(name) for name in args.name}

for name, name_provenance in provenance.items():
    with open(f"{name}_provenance_data.json", "w") as f:
        json.dump(name_provenance, f, indent=2)


def plot(series, x_title, title, filename, type=None):
    plt.figure()
    for label, (x, y) in series.items():
        if type == "bar":
            plt.bar(x, y, label=label)
        else:
            plt.plot(x, y, label=label)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Total downloads")
    plt.xlabel(x_title)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)


history_series = {}
for name, name_provenance in provenance.items():
    items = sorted(name_provenance.items(), key=lambda x: x[0])
    dates = [datetime.fromisoformat(d) for d, _ in items]
    values = [
        sum(entry.get("platforms").values())
        for _, entry in items
        if "platforms" in entry
    ]
    history_series[name] = (dates, values)

plot(history_series, "Date", "Downloads (historical)", "history.png")

print(json.dumps(provenance, indent=2))
