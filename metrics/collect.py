import argparse

import requests
import jmespath
import json
import os

parser = argparse.ArgumentParser(description="Collect release metrics from GitHub")
parser.add_argument("--user", type=str, default="fairagro", help="GitHub username")
parser.add_argument("--repo", type=str, required=True, help="GitHub repository name")

args = parser.parse_args()
user = args.user
repo = args.repo

base_url = f"https://api.github.com/repos/{user}/{repo}"
releases_url = f"{base_url}/releases"

client = requests.Session()

token = os.getenv("GITHUB_TOKEN")

if token:
    client.headers.update(
        {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
    )

res = client.get(releases_url)
if not res.ok:
    raise SystemExit(
        f"GitHub API error {res.status_code} for {releases_url}: {res.text}"
    )
content = res.json()

releases = jmespath.search(
    "[].{tag: tag_name, assets: assets[?ends_with(name, 'xz') || ends_with(name, 'zip') || ends_with(name, 'exe')|| ends_with(name, 'msi')|| ends_with(name, 'dmg')|| ends_with(name, 'gz')|| ends_with(name, 'AppImage')|| ends_with(name, 'deb')].{name: name, downloads: download_count}}",
    content,
)
print(json.dumps(releases, indent=2))
