import argparse
import json
from jinja2 import Environment, FileSystemLoader

SOFTWARE_META = {
    "sciwin": {
        "title": "SciWIn-Client",
        "description": "SciWIn-Client helps users creating **Computational Workflows** in CWL.",
        "url": "https://github.com/fairagro/sciwin",
    },
    "sciwin_studio": {
        "title": "SciWIn-Studio",
        "description": "SciWIn-Studio is the desktop application for SciWIn, available for Windows, macOS and Linux.",
        "url": "https://github.com/fairagro/sciwin_studio",
    },
}

parser = argparse.ArgumentParser("plotter")
parser.add_argument("--name", nargs="+", required=True, help="repo name(s)")
parser.add_argument(
    "--json", nargs="+", required=True, help="analyzed_data.json file(s), matching --name order"
)

args = parser.parse_args()
if len(args.name) != len(args.json):
    raise SystemExit("--name and --json must have the same number of values")

software = []
for name, json_path in zip(args.name, args.json):
    with open(json_path, "r") as f:
        data = json.load(f)

    downloads_per_tag = data["versions"]
    downloads_per_platform = data["platforms"]
    latest_tag, latest_downloads = next(iter(downloads_per_tag.items()))

    downloads_per_os = {}
    for key, value in downloads_per_platform.items():
        os_name = key.split()[0]  # split by space, take first part (OS)
        downloads_per_os[os_name] = downloads_per_os.get(os_name, 0) + value

    meta = SOFTWARE_META.get(
        name,
        {
            "title": name.replace("_", " ").title(),
            "description": "",
            "url": f"https://github.com/fairagro/{name}",
        },
    )

    software.append(
        {
            "name": name,
            "title": meta["title"],
            "description": meta["description"],
            "url": meta["url"],
            "versions": downloads_per_tag,
            "latest_version": latest_tag,
            "latest_downloads": latest_downloads,
            "downloads": sum(downloads_per_tag.values()),
            "platform": downloads_per_platform,
            "os": downloads_per_os,
        }
    )

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("template.md")

output = template.render(
    software=software,
    total_downloads=sum(s["downloads"] for s in software),
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(output)
