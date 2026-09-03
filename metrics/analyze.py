import argparse
import json
import re
import anybadge
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "no-latex", "nature", "high-vis"])

parser = argparse.ArgumentParser("plotter")
parser.add_argument("--name", help="repo name")
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

plot(
    tags, tag_downloads, "Releases", "Downloads by Release", f"{args.name}_release.png"
)


_OS_PATTERNS = [
    (r"apple|darwin|macos|osx|\.dmg$", "MacOS"),
    (r"windows|\.exe$|\.msi$", "Windows"),
    (r"linux|\.deb$|\.rpm$|appimage", "Linux"),
]

_ARCH_PATTERNS = [
    (r"aarch64|arm64", "ARM64"),
    (r"armv[67]|armhf|\barm\b", "ARM"),
    (r"x86_64|amd64|x64", "x64"),
    (r"i686|i386|\bx86\b", "x86"),
]


def get_os(name: str) -> str:
    name = name.lower()
    os_name = next(
        (label for pattern, label in _OS_PATTERNS if re.search(pattern, name)),
        "Unknown",
    )
    if os_name == "Unknown":
        return os_name
    arch = next(
        (label for pattern, label in _ARCH_PATTERNS if re.search(pattern, name)), None
    )
    return f"{os_name} ({arch})" if arch else os_name


# plot by OS
downloads_per_os = {}
for release in data:
    for asset in release["assets"]:
        os_name = get_os(asset["name"])
        if os_name == "Unknown":
            continue
        downloads_per_os[os_name] = (
            downloads_per_os.get(os_name, 0) + asset["downloads"]
        )

os = list(downloads_per_os.keys())
downloads = list(downloads_per_os.values())

plot(
    os,
    downloads,
    "Platform",
    "Downloads by Platform",
    f"{args.name}_platform.png",
    "bar",
)

badge = anybadge.Badge("Total downloads", sum(downloads))
badge.write_badge(f"{args.name}_badge.svg", True)

results = {"versions": downloads_per_tag, "platforms": downloads_per_os}

print(json.dumps(results, indent=2))
