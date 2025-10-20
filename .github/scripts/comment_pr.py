#!/usr/bin/env python3
import os
import sys

from typing import Dict

import requests


def get_token() -> str | None:
    return os.environ.get("REPO_TOKEN", "").strip()


def gh_get(session: requests.Session, url: str, **params):
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def gh_post(session: requests.Session, url: str, json_data: Dict):
    r = session.post(url, json=json_data, timeout=30)
    r.raise_for_status()
    return r.json()


def find_open_target_pr(session: requests.Session) -> str:
    url = "https://api.github.com/repos/mozilla-l10n/firefox-l10n-source/pulls"
    prs = gh_get(session, url, state="open", per_page=100)
    open_prs = [pr for pr in prs if pr.get("title") == "Update messages"]

    if len(open_prs) > 1:
        sys.exit("ERROR: More than one open PR with title 'Update messages'. Aborting.")

    return open_prs[0].get("number")


def comment_if_needed(session: requests.Session, pr_number: str) -> None:
    comments_url = f"https://api.github.com/repos/mozilla-l10n/firefox-l10n-source/issues/{pr_number}/comments"
    comment_marker = "[fluent-recipes-bot]"
    existing = gh_get(session, comments_url, per_page=100)
    for c in existing:
        if comment_marker in (c.get("body") or ""):
            return

    body = f"{comment_marker} There are pending migrations in https://github.com/flodolo/fluent-migrations"
    gh_post(session, comments_url, {"body": body})


def main():
    token = get_token()
    if not token:
        sys.exit("ERROR: No token found. Set REPO_TOKEN.")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
    }

    with requests.Session() as s:
        s.headers.update(headers)
        pr_number = find_open_target_pr(s)
        if pr_number:
            comment_if_needed(s, pr_number)
        else:
            sys.exit("ERROR: No open PRs with title 'Update messages'.")


if __name__ == "__main__":
    main()
