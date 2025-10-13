import argparse
import json
import anybadge
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "no-latex", "nature", "high-vis"])

parser = argparse.ArgumentParser("plotter")
parser.add_argument("--json", help="json file")

args = parser.parse_args()
with open(args.json, "r") as f:
    data = json.load(f)


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


# plot by Tag
downloads_per_tag = {
    entry["tag"]: sum(asset["downloads"] for asset in entry["assets"]) for entry in data
}
tags = list(downloads_per_tag.keys())
tag_downloads = list(downloads_per_tag.values())
tags.reverse()
tag_downloads.reverse()

plot(tags, tag_downloads, "Releases", "Downloads by Release", "release.png")

def get_os(name: str):
    os = "Unknown"
    if "apple" in name:
        os = "MacOS"
    if "linux" in name:
        os = "Linux"
    if "windows" in name:
        os = "Windows"

    if "aarch64" in name:
        os += " (ARM)"
    if "x86_64" in name:
        os += " (x64)"
    return os


# plot by OS
downloads_per_os = {}
for release in data:
    for asset in release["assets"]:
        os_name = get_os(asset["name"])
        downloads_per_os[os_name] = (
            downloads_per_os.get(os_name, 0) + asset["downloads"]
        )

os = list(downloads_per_os.keys())
downloads = list(downloads_per_os.values())

plot(os, downloads, "Platform", "Downloads by Platform", "platform.png", "bar")

badge = anybadge.Badge("Total downloads", sum(downloads))
badge.write_badge("badge.svg", True)

results = {
    "versions": downloads_per_tag,
    "platforms": downloads_per_os
}

print(json.dumps(results, indent=2))