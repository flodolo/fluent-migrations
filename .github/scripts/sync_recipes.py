#!/usr/bin/env python3
import os
import re

from pathlib import Path
from typing import Dict, List, Set

import requests


def get_token() -> str:
    return os.environ.get("REPO_TOKEN", "")


def check_recipes_dir() -> Path:
    script_dir = Path(__file__).resolve().parent
    recipes_dir = script_dir.parents[1] / "recipes"
    recipes_dir.mkdir(parents=True, exist_ok=True)
    return recipes_dir


def find_local_bug_files(recipes_dir: Path) -> Set[str]:
    return {p.name for p in recipes_dir.rglob("bug_*.py") if p.is_file()}


def fetch_remote_bug_files(session: requests.Session) -> List[Dict]:
    url = "https://api.github.com/repos/mozilla-firefox/firefox/contents/python/l10n/fluent_migrations"
    recipe_pattern = re.compile(r"^bug_.*\.py$")
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    items = resp.json()
    if not isinstance(items, list):
        raise RuntimeError(f"Unexpected response for contents API: {items!r}")

    return [
        it
        for it in items
        if it.get("type") == "file" and recipe_pattern.match(it.get("name", ""))
    ]


def download_missing(
    files: List[Dict],
    missing_names: Set[str],
    dest_dir: Path,
    session: requests.Session,
) -> List[str]:
    downloaded = []
    files_by_name = {f["name"]: f for f in files}
    for name in sorted(missing_names):
        info = files_by_name.get(name)
        if not info:
            continue
        url = info.get("download_url")
        if not url:
            continue
        r = session.get(url, timeout=30)
        r.raise_for_status()
        target = dest_dir / name
        target.write_bytes(r.content)
        downloaded.append(name)
        print(f"Downloaded {name} -> {target}")
    return downloaded


def main():
    recipes_dir = check_recipes_dir()
    local = find_local_bug_files(recipes_dir)

    headers = {"Accept": "application/vnd.github+json"}
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with requests.Session() as s:
        s.headers.update(headers)
        remote_items = fetch_remote_bug_files(s)
        remote_names = {it["name"] for it in remote_items}

        missing = remote_names - local
        print(
            f"Local count: {len(local)} | Remote count: {len(remote_names)} | Missing: {len(missing)}"
        )

        downloaded = download_missing(remote_items, missing, recipes_dir, s)

    print(f"Downloaded {len(downloaded)} files.")


if __name__ == "__main__":
    main()
