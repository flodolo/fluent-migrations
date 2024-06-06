#!/usr/bin/env python3

"""
This script is used to add missing FTL files to locales that are above
a certain threshold of completion in Pontoon.

This is used to avoid falling back to English in the UI when a file in a
Fluent bundle is missing.

By default, the script runs on all locales, pulls from the repository but
doesn't commit local changes. To commit:

./add_missing_ftl.py --wetrun

See "./add_missing_ftl.py --help" for other options.
"""

import argparse
import json
import os
import subprocess

from urllib.parse import quote as urlquote
from urllib.request import urlopen

import local_config

from functions import get_locale_folders


def extractFileList(repository_path):
    """Extract the list of FTL files."""

    excluded_folders = (
        ".hg",
        "calendar",
        "chat",
        "editor",
        "extensions",
        "mail",
        "other-licenses",
        "suite",
    )

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Ignore excluded folders
        if root == repository_path:
            dirs[:] = [d for d in dirs if d not in excluded_folders]

        for file_name in files:
            if os.path.splitext(file_name)[1] == ".ftl":
                file_name = os.path.relpath(
                    os.path.join(root, file_name), repository_path
                )
                file_list.append(file_name)
    file_list.sort()

    return file_list


def main():
    p = argparse.ArgumentParser(
        description="Add missing FTL files in localized repositories"
    )

    p.add_argument("--noupdates", help="Do not pull from remote", action="store_true")
    p.add_argument(
        "--wetrun",
        help="Commit local changes and push them to remote",
        action="store_true",
    )
    p.add_argument(
        "--locale", help="Run on a specific locale", action="store", default=""
    )
    p.add_argument(
        "--threshold",
        help="Minimum percentage of completion in completion under which locales are ignored",
        action="store",
        default="70",
    )
    args = p.parse_args()

    # Read paths from config file
    [l10n_path, quarantine_path] = local_config.read_config(
        ["l10n_path", "quarantine_path"]
    )

    # Get the list of locales
    locales = [args.locale] if args.locale else get_locale_folders(l10n_path)

    # Get a list of FTL files in the source repository
    complete_source_files = extractFileList(quarantine_path)

    # Manual list of stand-alone files that's not useful to add
    ignored_files = [
        "devtools/client/aboutdebugging.ftl",
        "devtools/client/accessibility.ftl",
        "devtools/client/application.ftl",
        "devtools/client/tooltips.ftl",
        "devtools/startup/aboutDevTools.ftl",
    ]
    source_files = [f for f in complete_source_files if f not in ignored_files]

    # Get completion stats for locales from Pontoon
    query = """
{
  firefox: project(slug: "firefox") {
    localizations {
        locale {
            code
        },
        missingStrings,
        totalStrings
    }
  }
}
"""
    pontoon_stats = {}
    try:
        print("Reading Pontoon stats...")
        url = "https://pontoon.mozilla.org/graphql?query={}".format(urlquote(query))
        response = urlopen(url)
        json_data = json.load(response)
        for project, project_data in json_data["data"].items():
            for element in project_data["localizations"]:
                locale = element["locale"]["code"]
                pontoon_stats[locale] = round(
                    (float(element["totalStrings"] - element["missingStrings"]))
                    / element["totalStrings"]
                    * 100,
                    2,
                )
    except Exception as e:
        print(e)

    ignored_locales = {
        "missing": [],
        "incomplete": [],
    }
    threshold = int(args.threshold)

    files_total = 0
    out_log = []

    # If a locale is not available in Pontoon, but it's been requested
    # explicitly, fake stats to run the commands anyway.
    requested_locale = args.locale
    if requested_locale and requested_locale not in pontoon_stats:
        print(
            "Locale {} is not available in Pontoon but was requested explicitly. Assuming completion at 100%".format(
                requested_locale
            )
        )
        pontoon_stats[requested_locale] = 100

    # Update l10n repository, unless --noupdates was called explicitly
    if not args.noupdates:
        subprocess.run(["git", "-C", l10n_path, "pull"])

    for locale in locales:
        # Ignore a locale if it's not in Pontoon or is below 60%
        if locale not in pontoon_stats and locale not in ["ja-JP-mac"]:
            ignored_locales["missing"].append(locale)
            continue

        if locale not in ["ja-JP-mac"] and pontoon_stats[locale] < threshold:
            ignored_locales["incomplete"].append(locale)
            continue

        l10n_repo = os.path.join(l10n_path, locale)

        # Create list of files
        locale_files = extractFileList(l10n_repo)

        added_files = 0
        for file_name in source_files:
            if file_name not in locale_files:
                full_file_name = os.path.join(l10n_repo, file_name)
                file_path = os.path.dirname(full_file_name)
                if not os.path.isdir(file_path):
                    # Create missing folder
                    print(
                        "Creating missing folder: {}".format(
                            os.path.relpath(file_path, l10n_repo)
                        )
                    )
                    os.makedirs(file_path)

                with open(full_file_name, "w") as f:
                    f.write(
                        "# This Source Code Form is subject to the terms of the Mozilla Public\n"
                        "# License, v. 2.0. If a copy of the MPL was not distributed with this\n"
                        "# file, You can obtain one at http://mozilla.org/MPL/2.0/.\n"
                    )
                added_files += 1

        if added_files > 0:
            out_log.append("{}: added {} files".format(locale, added_files))
            files_total += added_files
            if args.wetrun:
                subprocess.run(["git", "-C", l10n_path, "add", locale])
                subprocess.run(
                    [
                        "git",
                        "-C",
                        l10n_path,
                        "commit",
                        "-m",
                        "Bug 1586984 - Add empty FTL files to repository to avoid English fallback",
                    ]
                )

    if args.wetrun:
        subprocess.run(["git", "-C", l10n_path, "push"])
    else:
        print("*** DRY RUN ***")
    print("Total files added: {}".format(files_total))
    print("\n".join(out_log))

    if ignored_locales["missing"]:
        print(
            "Locales not available in Pontoon ({}):".format(
                len(ignored_locales["missing"])
            )
        )
        print(", ".join(ignored_locales["missing"]))

    if ignored_locales["incomplete"]:
        print(
            "Locales below {}% ({}):".format(
                threshold, len(ignored_locales["incomplete"])
            )
        )
        print(", ".join(ignored_locales["incomplete"]))


if __name__ == "__main__":
    main()
