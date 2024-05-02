#!/usr/bin/env python3

"""

This script is used to remove obsolete strings and reformat files accordingly
to the source content (en-US).

By default, the script runs on all locales, pulls from the repository but
doesn't commit local changes. To commit:

./remove_obsolete_strings.py --wetrun

See "./remove_obsolete_strings.py --help" for other options.

"""

from compare_locales.parser import getParser
from compare_locales.serializer import serialize
import argparse
import local_config
import os
import subprocess


def extractFileList(repository_path):
    """
    Extract the list of supported files. Store the relative path and ignore
    specific folders for products we don't want to modify (e.g. SeaMonkey).
    """

    supported_formats = [
        ".dtd",
        ".properties",
        ".ftl",
    ]

    excluded_folders = (
        ".hg",
        "calendar",
        "chat",
        "editor",
        "extensions",
        "other-licenses",
    )

    excluded_files = ("region.properties",)

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Ignore excluded folders
        if root == repository_path:
            dirs[:] = [d for d in dirs if d not in excluded_folders]

        for filename in files:
            if (
                os.path.splitext(filename)[1] in supported_formats
                and filename not in excluded_files
            ):
                filename = os.path.relpath(
                    os.path.join(root, filename), repository_path
                )
                file_list.append(filename)
    file_list.sort()

    return file_list


def main():
    p = argparse.ArgumentParser(
        description="Remove obsolete strings and reformat files in localized repositories"
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
    args = p.parse_args()

    # Read paths from config file
    [l10n_clones_path, quarantine_path] = local_config.read_config(
        ["l10n_clones_path", "quarantine_path"]
    )

    if args.locale:
        locales = [args.locale]
    else:
        locales = [x for x in os.listdir(l10n_clones_path) if not x.startswith(".")]
        # Exclude locales still working on Mercurial directly
        excluded_locales = [
            "ja",
            "ja-JP-mac",
        ]
        locales = sorted([x for x in locales if x not in excluded_locales])

    # Get a list of supported files in the source repository
    source_file_list = extractFileList(quarantine_path)

    for locale in locales:
        print("Locale: {}".format(locale))
        locale_path = os.path.join(l10n_clones_path, locale)

        # Update locale repository, unless --noupdates was called explicitly
        if not args.noupdates:
            print("Updating repository...")
            subprocess.run(["hg", "-R", locale_path, "pull", "-u"])

        # Create list of target files
        target_file_list = extractFileList(locale_path)

        # Ignore files in locale that are not available in the source
        target_file_list = [f for f in target_file_list if f in source_file_list]

        # Read source and target and write the output overwriting the existing
        # localized file
        for filename in target_file_list:
            source_filename = os.path.join(quarantine_path, filename)
            target_filename = os.path.join(locale_path, filename)
            with open(source_filename) as f:
                source_content = f.read()
                source_parser = getParser(filename)
                source_parser.readUnicode(source_content)
                reference = list(source_parser.walk())
            with open(target_filename) as f:
                target_content = f.read()
                target_parser = getParser(filename)
                target_parser.readUnicode(target_content)
                target = list(target_parser.walk())

            output = serialize(filename, reference, target, {})

            """
            # zh-CN has an extra string that needs to be kept (start page)
            if (
                locale == "zh-CN"
                and filename == "browser/chrome/browser/browser.properties"
            ):
                output += b"\n# DO NOT REMOVE: this string is used to set up the home page for zh-CN\n"
                output += b"browser.startup.homepage = https://start.firefoxchina.cn\n"
            """

            with open(target_filename, "wb") as f:
                f.write(output)

        if args.wetrun:
            # Commit changes
            subprocess.run(["hg", "-R", locale_path, "addremove"])
            subprocess.run(
                [
                    "hg",
                    "-R",
                    locale_path,
                    "commit",
                    "-m",
                    "Remove obsolete strings and reformat files",
                ]
            )
            subprocess.run(["hg", "-R", locale_path, "push"])
        else:
            print("(dry run)")


if __name__ == "__main__":
    main()
