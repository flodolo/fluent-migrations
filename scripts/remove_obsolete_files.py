#!/usr/bin/env python3

'''

This script is used to remove empty files, i.e. files with only comments.

Fluent files need to be ignored, since we add empty files to avoid falling
back to English.

'''

from compare_locales import parser
import argparse
import local_config
import os
import subprocess


def extractFileList(repository_path):
    '''
        Extract the list of supported files. Store the relative path and ignore
        specific paths.
    '''

    excluded_paths = (
        'dom/chrome/netErrorApp.dtd',
        'extensions/irc/',
        'other-licenses/branding/sunbird/',
        'suite/',
    )

    excluded_files = (
        'region.properties',
    )

    supported_formats = [
        '.dtd',
        '.inc',
        '.ini',
        '.properties',
    ]

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Exclude hidden folders and files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            if os.path.splitext(filename)[1] in supported_formats:
                filename = os.path.relpath(
                    os.path.join(root, filename),
                    repository_path
                )
                # Ignore excluded_folders
                if filename.startswith(excluded_paths):
                    continue
                # Ignore some files
                if filename.endswith(excluded_files):
                    continue
                file_list.append(filename)
    file_list.sort()

    return file_list


def findEmptyFiles(repository_path):
    '''
        Find empty files
    '''

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
            print('Error parsing file: {}'.format(file_path))
            print(e)

    return empty_files_list


def main():
    p = argparse.ArgumentParser(
        description='Remove empty files in localized repositories')

    p.add_argument(
        '--noupdates',
        help='Do not pull from remote',
        action='store_true'
    )
    p.add_argument(
        '--wetrun',
        help='Commit local changes and push them to remote',
        action='store_true'
    )
    p.add_argument(
        '--locale',
        help='Run on a specific locale',
        action='store',
        default=''
    )
    args = p.parse_args()

    # Read paths from config file
    [l10n_clones_path, quarantine_path] = local_config.read_config(
        ['l10n_clones_path', 'quarantine_path'])

    # Get the list of locales
    if args.locale:
        locales = [args.locale]
    else:
        locales = [x for x in os.listdir(
            l10n_clones_path) if not x.startswith('.')]
        locales.sort()

    # Store the list of files in quarantine
    source_file_list = extractFileList(quarantine_path)

    for locale in locales:
        print('Locale: {}'.format(locale))
        need_commit = False
        locale_path = os.path.join(l10n_clones_path, locale)

        # Update locale repository, unless --noupdates was called explicitly
        if not args.noupdates:
            print('Updating repository...')
            subprocess.run([
                'hg', '-R', locale_path, 'pull', '-u'
            ])

        target_file_list = extractFileList(locale_path)

        # Remove obsolete files (file in the locale, but not available in quarantine)
        obsolete_files_list = []
        for filename in target_file_list:
            if filename not in source_file_list:
                obsolete_files_list.append(filename)
                if args.wetrun:
                    os.remove(os.path.join(locale_path, filename))
                    need_commit = True

        obsolete_files_list.sort()
        if obsolete_files_list:
            print('Obsolete files:')
            print('\n'.join(obsolete_files_list))

        # Find files containing no strings
        empty_files_list = []
        empty_files_list = findEmptyFiles(locale_path)
        if empty_files_list:
            if args.wetrun:
                for filename in empty_files_list:
                    os.remove(os.path.join(locale_path, filename))
                need_commit = True
            print('Empty files:')
            print('\n'.join(empty_files_list))

        if args.wetrun and need_commit:
            # Commit changes
            subprocess.run([
                'hg', '-R', locale_path, 'addremove'
            ])
            subprocess.run([
                'hg', '-R', locale_path, 'commit', '-m',
                'Bug 1443175 - Remove obsolete and empty files'
            ])
            subprocess.run([
                'hg', '-R', locale_path, 'push'
            ])
        else:
            print('(dry run)')


if __name__ == '__main__':
    main()
