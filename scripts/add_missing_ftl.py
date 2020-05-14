#!/usr/bin/env python3

'''
This script is used to add missing FTL files to locales that are above
a certain threshold of completion in Pontoon.

This is used to avoid falling back to English in the UI when a file in a
Fluent bundle is missing.
'''

import json
import local_config
import os
import subprocess
import sys
from urllib.parse import quote as urlquote
from urllib.request import urlopen


def extractFileList(repository_path):
    '''Extract the list of FTL files.'''

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

        for file_name in files:
            if os.path.splitext(file_name)[1] == '.ftl':
                file_name = os.path.relpath(
                    os.path.join(root, file_name),
                    repository_path
                )
                file_list.append(file_name)
    file_list.sort()

    return file_list


def main():
    # Read paths from config file
    try:
        [l10n_clones_path, quarantine_path] = local_config.read_config(
            ['l10n_clones_path', 'quarantine_path'])
    except Exception as e:
        print('Error reading paths from config')
        print(e)

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
    locales.sort()

    # Get a list of FTL files in the source repository
    complete_source_files = extractFileList(quarantine_path)

    # Manual list of stand-alone files that's not useful to add
    ignored_files = [
        'browser/browser/aboutCertError.ftl',
        'browser/browser/aboutConfig.ftl',
        'browser/browser/aboutLogins.ftl',
        'browser/browser/aboutPolicies.ftl',
        'browser/browser/aboutPrivateBrowsing.ftl',
        'browser/browser/aboutRestartRequired.ftl',
        'browser/browser/aboutRobots.ftl',
        'browser/browser/aboutSessionRestore.ftl',
        'browser/browser/aboutTabCrashed.ftl',
        'browser/browser/newInstallPage.ftl',
        'browser/browser/newtab/asrouter.ftl',
        'browser/browser/newtab/newtab.ftl',
        'browser/browser/newtab/onboarding.ftl',
        'browser/browser/policies/policies-descriptions.ftl',
        'browser/browser/preferences/fxaPairDevice.ftl',
        'browser/browser/protections.ftl',
        'browser/browser/touchbar/touchbar.ftl',
        'devtools/client/aboutdebugging.ftl',
        'devtools/client/accessibility.ftl',
        'devtools/client/application.ftl',
        'devtools/client/tooltips.ftl',
        'devtools/startup/aboutDevTools.ftl',
        'security/manager/security/certificates/certManager.ftl',
        'security/manager/security/certificates/deviceManager.ftl',
        'toolkit/crashreporter/aboutcrashes.ftl',
        'toolkit/toolkit/about/aboutAbout.ftl',
        'toolkit/toolkit/about/aboutAddons.ftl',
        'toolkit/toolkit/about/aboutCompat.ftl',
        'toolkit/toolkit/about/aboutConfig.ftl',
        'toolkit/toolkit/about/aboutNetworking.ftl',
        'toolkit/toolkit/about/aboutPerformance.ftl',
        'toolkit/toolkit/about/aboutPlugins.ftl',
        'toolkit/toolkit/about/aboutProfiles.ftl',
        'toolkit/toolkit/about/aboutRights.ftl',
        'toolkit/toolkit/about/aboutServiceWorkers.ftl',
        'toolkit/toolkit/about/aboutSupport.ftl',
        'toolkit/toolkit/about/aboutTelemetry.ftl',
        'toolkit/toolkit/about/certviewer.ftl',
        'toolkit/toolkit/about/url-classifier.ftl',
        'toolkit/toolkit/global/processTypes.ftl',
        'toolkit/toolkit/pictureinpicture/pictureinpicture.ftl',
    ]
    source_files = [f for f in complete_source_files if f not in ignored_files]

    # Get completion stats for locales from Pontoon
    query = '''
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
'''
    pontoon_stats = {}
    try:
        print("Reading Pontoon stats...")
        url = 'https://pontoon.mozilla.org/graphql?query={}'.format(
            urlquote(query))
        response = urlopen(url)
        json_data = json.load(response)
        for project, project_data in json_data['data'].items():
            for element in project_data['localizations']:
                locale = element['locale']['code']
                pontoon_stats[locale] = round(
                    (float(element['totalStrings'] - element['missingStrings'])
                     ) / element['totalStrings'] * 100,
                    2)
    except Exception as e:
        print(e)

    ignored_locales = {
        'missing': [],
        'incomplete': [],
    }
    threshold = 70

    files_total = 0
    out_log = []
    for locale in locales:
        # Ignore a locale if it's not in Pontoon or is below 60%
        if locale not in pontoon_stats and locale not in ['ja-JP-mac']:
            ignored_locales['missing'].append(locale)
            continue

        if locale not in ['ja-JP-mac'] and pontoon_stats[locale] < threshold:
            ignored_locales['incomplete'].append(locale)
            continue

        l10n_repo = os.path.join(l10n_clones_path, locale)

        # Update locale repository
        subprocess.run([
            'hg', '-R', l10n_repo, 'pull', '-u'
        ])

        # Create list of files
        locale_files = extractFileList(l10n_repo)

        added_files = 0
        for file_name in source_files:
            if file_name not in locale_files:
                full_file_name = os.path.join(l10n_repo, file_name)
                with open(full_file_name, 'w') as f:
                    f.write(
                        '# This Source Code Form is subject to the terms of the Mozilla Public\n'
                        '# License, v. 2.0. If a copy of the MPL was not distributed with this\n'
                        '# file, You can obtain one at http://mozilla.org/MPL/2.0/.\n'
                    )
                added_files += 1

        if added_files > 0:
            out_log.append('{}: added {} files'.format(locale, added_files))
            files_total += added_files
            subprocess.run([
                'hg', '-R', l10n_repo, 'addremove'
            ])
            subprocess.run([
                'hg', '-R', l10n_repo, 'commit', '-m',
                'Bug 1586984 - Add empty FTL files to repository to avoid English fallback'
            ])
            subprocess.run([
                'hg', '-R', l10n_repo, 'push'
            ])

    print('Total files added: {}'.format(files_total))
    print('\n'.join(out_log))

    if ignored_locales['missing']:
        print('Locales not available in Pontoon ({}):'.format(
            len(ignored_locales['missing'])))
        print(', '.join(ignored_locales['missing']))

    if ignored_locales['incomplete']:
        print('Locales below {}% ({}):'.format(
            threshold,
            len(ignored_locales['incomplete'])))
        print(', '.join(ignored_locales['incomplete']))


if __name__ == '__main__':
    main()
