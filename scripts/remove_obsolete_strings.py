#!/usr/bin/env python3

"""

This script is used to remove obsolete strings and reformat files accordingly
to the source content (en-US).

By default, the script runs on all locales, pulls from the repository but
doesn't commit local changes. To commit:

./remove_obsolete_strings.py --wet-run

To commit and push use --push instead of --wet-run.

See "./remove_obsolete_strings.py --help" for other options.

"""

import os
import subprocess

import local_config

from compare_locales.parser import getParser
from compare_locales.serializer import serialize
from functions import get_locale_folders, get_cli_params


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
        ".git",
        "extensions",
    )

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Ignore excluded and hidden folders
        if root == repository_path:
            dirs[:] = [d for d in dirs if d[0] != "." and d not in excluded_folders]

        for filename in files:
            if os.path.splitext(filename)[1] in supported_formats:
                filename = os.path.relpath(
                    os.path.join(root, filename), repository_path
                )
                file_list.append(filename)
    file_list.sort()

    return file_list


def main():
    args = get_cli_params(
        cmd_desc="Remove obsolete strings and reformat files in localized repositories",
        threshold=False,
    )
    # Commit changes for both --wet-run and --push
    commit_changes = args.wetrun or args.push

    # Read paths from config file
    [l10n_path, quarantine_path] = local_config.read_config(
        ["l10n_path", "quarantine_path"]
    )

    locales = [args.locale] if args.locale else get_locale_folders(l10n_path)
    # Exclude locales still working on Mercurial directly
    excluded_locales = [
        "ja",
        "ja-JP-mac",
    ]
    locales = sorted([x for x in locales if x not in excluded_locales])

    # Get a list of supported files in the source repository
    source_file_list = extractFileList(quarantine_path)

    # Update l10n repository, unless --noupdates was called explicitly
    if not args.noupdates:
        print("Updating repository...")
        subprocess.run(["git", "-C", l10n_path, "pull"])

    for locale in locales:
        print("Locale: {}".format(locale))
        locale_path = os.path.join(l10n_path, locale)

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

        if commit_changes:
            # Commit changes
            subprocess.run(["git", "-C", l10n_path, "add", locale])
            subprocess.run(
                [
                    "git",
                    "-C",
                    l10n_path,
                    "commit",
                    "-m",
                    "Remove obsolete strings and reformat files",
                ]
            )
        else:
            print("(dry run)")

    if args.push:
        subprocess.run(["git", "-C", l10n_path, "push"])


if __name__ == "__main__":
    main()
