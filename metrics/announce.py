import argparse
import json
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser("plotter")
parser.add_argument("--json", help="json file")

args = parser.parse_args()
with open(args.json, "r") as f:
    data = json.load(f)

downloads_per_tag = data["versions"]
downloads_per_platform = data["platforms"]
latest_tag, latest_downloads = next(iter(downloads_per_tag.items()))

downloads_per_os = {}
for key, value in downloads_per_platform.items():
    os_name = key.split()[0]  # split by space, take first part (OS)
    downloads_per_os[os_name] = downloads_per_os.get(os_name, 0) + value

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("template.md")

output = template.render(
    versions=downloads_per_tag,
    latest_version=latest_tag,
    latest_downloads=latest_downloads,
    downloads=sum(downloads_per_tag.values()),
    platform=downloads_per_platform,
    os=downloads_per_os
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(output)
