import html
import sys
import json
from pathlib import Path
import shutil

REMOTE_REPO: Path = Path.cwd()
LOCAL_REPO: Path = REMOTE_REPO.parent.joinpath(sys.argv[2])

REMOTE_REPO.joinpath("apk").mkdir(parents=True, exist_ok=True)
REMOTE_REPO.joinpath("icon").mkdir(parents=True, exist_ok=True)

to_delete: list[str] = json.loads(sys.argv[1])

for module in to_delete:
    apk_name = f"aniyomi-{module}-v*.*.apk"
    icon_name = f"eu.kanade.tachiyomi.animeextension.{module}.png"
    for file in REMOTE_REPO.joinpath("apk").glob(apk_name):
        print(file.name)
        file.unlink(missing_ok=True)
    for file in REMOTE_REPO.joinpath("icon").glob(icon_name):
        print(file.name)
        file.unlink(missing_ok=True)

if LOCAL_REPO.joinpath("apk").exists():
    shutil.copytree(src=LOCAL_REPO.joinpath("apk"), dst=REMOTE_REPO.joinpath("apk"), dirs_exist_ok=True)
if LOCAL_REPO.joinpath("icon").exists():
    shutil.copytree(src=LOCAL_REPO.joinpath("icon"), dst=REMOTE_REPO.joinpath("icon"), dirs_exist_ok=True)

remote_index_path = REMOTE_REPO.joinpath("index.json")
if remote_index_path.exists():
    with remote_index_path.open() as remote_index_file:
        remote_index = json.load(remote_index_file)
else:
    remote_index = []

local_index_path = LOCAL_REPO.joinpath("index.min.json")
if local_index_path.exists():
    with local_index_path.open() as local_index_file:
        local_index = json.load(local_index_file)
else:
    local_index = []
index = [
    item for item in remote_index
    if not any(item["pkg"].endswith(f".{module}") for module in to_delete)
]
index.extend(local_index)
index.sort(key=lambda x: x["pkg"])

with REMOTE_REPO.joinpath("index.json").open("w", encoding="utf-8") as index_file:
    json.dump(index, index_file, ensure_ascii=False, indent=2)

for item in index:
    for source in item["sources"]:
        source.pop("versionId", None)

with REMOTE_REPO.joinpath("index.min.json").open("w", encoding="utf-8") as index_min_file:
    json.dump(index, index_min_file, ensure_ascii=False, separators=(",", ":"))
repo_meta = {
    "name": "Dou",
    "shortName": "DOU",
    "website": "https://github.com/wdinrev/dou-source",
    "signingKeyFingerprint": "af1193f39628878e5a23796ffd06aa7541996f85555dcfaf5f14a21078d5a960",
}
with REMOTE_REPO.joinpath("repo.json").open("w", encoding="utf-8") as repo_file:
    json.dump(repo_meta, repo_file, ensure_ascii=False, indent=2)

with REMOTE_REPO.joinpath("index.html").open("w", encoding="utf-8") as index_html_file:
    index_html_file.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>apks</title>\n</head>\n<body>\n<pre>\n')
    for entry in index:
        apk_escaped = 'apk/' + html.escape(entry["apk"])
        name_escaped = html.escape(entry["name"])
        index_html_file.write(f'<a href="{apk_escaped}">{name_escaped}</a>\n')
    index_html_file.write('</pre>\n</body>\n</html>\n')
