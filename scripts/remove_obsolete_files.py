#!/usr/bin/env python3

"""

This script is used to remove:
- Obsolete files (available in the locale but not in quarantine).
- Empty files, i.e. files with only comments.

Fluent files need to be ignored, since we add empty files to avoid falling
back to English.

By default, the script runs on all locales, pulls from the repository but
doesn't commit local changes. To commit:

./remove_obsolete_files.py --wet-run

To commit and push use --push instead of --wet-run.

See "./remove_obsolete_files.py --help" for other options.

"""

import os
import subprocess

import local_config

from compare_locales import parser
from functions import get_locale_folders, get_cli_params


def extractFileList(repository_path):
    """
    Extract the list of supported files. Store the relative path and ignore
    specific paths.
    """

    excluded_paths = ()

    supported_formats = [
        ".dtd",
        ".inc",
        ".ini",
        ".properties",
    ]

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Exclude hidden folders and files
        files = [f for f in files if not f[0] == "."]
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for filename in files:
            if os.path.splitext(filename)[1] in supported_formats:
                filename = os.path.relpath(
                    os.path.join(root, filename), repository_path
                )
                # Ignore excluded folders
                if filename.startswith(excluded_paths):
                    continue
                file_list.append(filename)
    file_list.sort()

    return file_list


def findEmptyFiles(repository_path):
    """
    Find empty files
    """

    empty_files_list = []
    file_list = extractFileList(repository_path)

    for file_path in file_list:
        file_parser = parser.getParser(os.path.splitext(file_path)[1])
        file_parser.readFile(os.path.join(repository_path, file_path))
        try:
            empty_file = True
            entities = file_parser.parse()
            for entity in entities:
                # Ignore Junk
                if isinstance(entity, parser.Junk):
                    continue
                empty_file = False

            if empty_file:
                empty_files_list.append(file_path)
        except Exception as e:
            print("Error parsing file: {}".format(file_path))
            print(e)

    return empty_files_list


def main():
    args = get_cli_params(
        cmd_desc="Remove obsolete and empty files in localized repositories",
        threshold=False,
    )
    # Commit changes for both --wet-run and --push
    commit_changes = args.wetrun or args.push

    # Read paths from config file
    [l10n_path, quarantine_path] = local_config.read_config(
        ["l10n_path", "quarantine_path"]
    )

    # Get the list of locales
    locales = [args.locale] if args.locale else get_locale_folders(l10n_path)

    # Store the list of files in quarantine
    source_file_list = extractFileList(quarantine_path)

    # Update l10n repository, unless --noupdates was called explicitly
    if not args.noupdates:
        print("Updating repository...")
        subprocess.run(["git", "-C", l10n_path, "pull"])

    for locale in locales:
        print("Locale: {}".format(locale))
        need_commit = False
        locale_path = os.path.join(l10n_path, locale)

        target_file_list = extractFileList(locale_path)

        # Remove obsolete files (file in the locale, but not available in quarantine)
        obsolete_files_list = []
        for filename in target_file_list:
            if filename not in source_file_list:
                obsolete_files_list.append(filename)
                if commit_changes:
                    os.remove(os.path.join(locale_path, filename))
                    need_commit = True

        obsolete_files_list.sort()
        if obsolete_files_list:
            print("Obsolete files:")
            print("\n".join(obsolete_files_list))

        # Find files containing no strings
        empty_files_list = []
        empty_files_list = findEmptyFiles(locale_path)
        if empty_files_list:
            if commit_changes:
                for filename in empty_files_list:
                    os.remove(os.path.join(locale_path, filename))
                need_commit = True
            print("Empty files:")
            print("\n".join(empty_files_list))

        if commit_changes:
            if need_commit:
                # Commit changes
                subprocess.run(["git", "-C", l10n_path, "add", locale])
                subprocess.run(
                    [
                        "git",
                        "-C",
                        l10n_path,
                        "commit",
                        "-m",
                        "Bug 1443175 - Remove obsolete and empty files",
                    ]
                )
        else:
            print("(dry run)")

    if args.push:
        subprocess.run(["git", "-C", l10n_path, "push"])


if __name__ == "__main__":
    main()
