#!/usr/bin/env python3

"""
Pass a version number like 65 to
- Get the list of recipes from the fluent migrations landed in that version
- Remove the recipes from the mozilla-unified repository
"""

import argparse
import os
import sys

def main():

    # Get absolute path of the repository's root from the script location
    root_folder = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    config_file = os.path.join(root_folder, 'config', 'config')

    if not os.path.exists(config_file):
        print('ERROR: config file is missing')
        sys.exit(1)

    # Try importing the mozilla-unified path from config/config
    with open(config_file, 'r') as cfg:
        lines = cfg.readlines()
        for line in lines:
            if line.startswith("mozilla_unified_path"):
                mozilla_unified_path = line.split('=')[1].strip().strip('"')

    try:
        mozilla_unified_path
    except NameError:
        print('mozilla_unified_path is not defined in the config file')
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('version_number', help='Version number, e.g. 65')
    args = parser.parse_args()

    # Get the list of recipes
    recipes_path = os.path.join(root_folder, 'recipes', 'fx{}')
    recipes_path = recipes_path.format(args.version_number)
    hg_path = os.path.join(
        mozilla_unified_path, 'python', 'l10n', 'fluent_migrations')

    for root, dirs, files in os.walk(recipes_path, followlinks=True):
        # Exclude hidden folders and files
        recipes = [f for f in files if not f[0] == '.']
    try:
        recipes.sort()
        print('Affected bugs:')
        for recipe in recipes:
            print('- Bug {}'.format(recipe.split('_')[1]))
            # Remove the files from mozilla-unified
            os.remove(os.path.join(hg_path, recipe))
    except NameError:
        print('No recipes found')


if __name__ == '__main__':
    main()
