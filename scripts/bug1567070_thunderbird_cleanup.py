#!/usr/bin/env python3

'''

This script is used to remove the Thunderbird folder from locales, if the only
file present is "mail/messenger/aboutRights.ftl".

This file is created as result of a FTL2FTL migration in Thunderbird, but it
gets the file added for locales that don't localize Thunderbird at all.

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

    supported_formats = [
        '.dtd',
        '.ftl',
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
                file_list.append(filename)
    file_list.sort()

    return file_list


def main():
    p = argparse.ArgumentParser(
        description='Remove Thunderbird folder from non Thunderbird locales')

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
        locales = sorted([x for x in os.listdir(
            l10n_clones_path) if not x.startswith('.')])

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

        # Only look at the "mail" subfolder
        locale_mail_path = os.path.join(locale_path, 'mail')
        target_file_list = extractFileList(locale_mail_path)

        filename = 'messenger/aboutRights.ftl'
        if len(target_file_list) == 1 and target_file_list == [filename]:
            # The only file available is aboutRights.ftl, remove the folder
            if args.wetrun:
                os.remove(os.path.join(locale_mail_path, filename))
                need_commit = True

        if args.wetrun:
            if need_commit:
                # Commit changes
                subprocess.run([
                    'hg', '-R', locale_path, 'addremove'
                ])
                subprocess.run([
                    'hg', '-R', locale_path, 'commit', '-m',
                    'Remove migrated aboutRights.ftl from non Thunderbird locale'
                ])
                subprocess.run([
                    'hg', '-R', locale_path, 'push'
                ])
        else:
            print('(dry run)')

if __name__ == '__main__':
    main()
