#!/usr/bin/env python3

'''
This script is used to remove obsolete strings from all locales,
and reformat files accordingly to the source content (en-US).
'''

from compare_locales.parser import getParser
from compare_locales.serializer import serialize
import os
import subprocess
import sys


def extractFileList(repository_path):
    '''
        Extract the list of supported files. Store the relative path and ignore
        specific folders for products we don't want to modify (e.g. SeaMonkey).
    '''

    supported_formats = [
        '.dtd',
        '.properties',
        '.ftl',
    ]

    excluded_folders = (
        '.hg',
        'calendar',
        'chat',
        'editor',
        'extensions',
        'mail',
        'other-licenses',
        'suite',
    )

    file_list = []
    for root, dirs, files in os.walk(repository_path, followlinks=True):
        # Ignore excluded folders
        if root == repository_path:
            dirs[:] = [d for d in dirs if not d in excluded_folders]

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
    # Get absolute path of the repository's root from the script location
    root_folder = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    config_file = os.path.join(root_folder, 'config', 'config')

    if not os.path.exists(config_file):
        print('ERROR: config file is missing')
        sys.exit(1)

    # Try importing the path to l10n clones from config/config
    with open(config_file, 'r') as cfg:
        lines = cfg.readlines()
        for line in lines:
            if line.startswith("l10n_clones_path"):
                l10n_clones_path = line.split('=')[1].strip().strip('"')
            if line.startswith("quarantine_path"):
                quarantine_path = line.split('=')[1].strip().strip('"')

    # Make sure paths are set correctly
    try:
        l10n_clones_path
    except NameError:
        print('l10n_clones_path is not defined in the config file')
        sys.exit(1)
    try:
        quarantine_path
    except NameError:
        print('quarantine_path is not defined in the config file')
        sys.exit(1)

    locales = [x for x in os.listdir(
        l10n_clones_path) if not x.startswith('.')]
    # Exclude locales still working on Mercurial directly
    excluded_locales = [
        'da', 'it', 'ja', 'ja-JP-mac',
    ]
    locales = [l for l in locales if not l in excluded_locales]
    locales.sort()

    # Get a list of supported files in the source repository
    source_file_list = extractFileList(quarantine_path)

    for locale in locales:
        print('Updating: {}'.format(locale))
        locale_path = os.path.join(l10n_clones_path, locale)

        # Update locale repository
        subprocess.run([
            'hg', '-R', locale_path, 'pull', '-u'
        ])

        # Create list of target files
        target_file_list = extractFileList(locale_path)

        # Ignore files in locale that are not available in the source
        target_file_list = [
            f for f in target_file_list if f in source_file_list]

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

            # zh-CN has an extra string that needs to be kept (start page)
            if locale == 'zh-CN' and filename == 'browser/chrome/browser/browser.properties':
                output += b'\n# DO NOT REMOVE: this string is used to set up the home page for zh-CN\n'
                output += b'browser.startup.homepage = https://start.firefoxchina.cn\n'

            with open(target_filename, 'wb') as f:
                f.write(output)

        # Commit changes
        subprocess.run([
            'hg', '-R', locale_path, 'addremove'
        ])
        subprocess.run([
            'hg', '-R', locale_path, 'commit', '-m',
            'Remove obsolete files and reformat files'
        ])
        subprocess.run([
            'hg', '-R', locale_path, 'push'
        ])


if __name__ == '__main__':
    main()
