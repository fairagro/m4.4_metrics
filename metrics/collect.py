import requests
import jmespath
import json
import os

user = "fairagro"
repo = "sciwin"
base_url = f"https://api.github.com/repos/{user}/{repo}"

releases_url = f"{base_url}/releases"

client = requests.Session()

token = os.getenv("GITHUB_TOKEN")

if token:
    client.headers.update(
        {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
    )

res = client.get(releases_url)
content = res.json()

releases = jmespath.search(
    "[].{tag: tag_name, assets: assets[?ends_with(name, 'xz') || ends_with(name, 'zip')].{name: name, downloads: download_count}}",
    content,
)
print(json.dumps(releases, indent=2))
