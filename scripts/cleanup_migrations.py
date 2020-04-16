#!/usr/bin/env python

"""
Pass a version number like 65 to
- Get the list of recipes from the fluent migrations landed in that version
- Remove the recipes from the mozilla-unified repository
"""

import argparse
import os


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('version_number', help='Version number, e.g. 65')
    args = parser.parse_args()

    # Get the list of recipes
    recipes_path = '/Users/flodolo/github/fluent-migrations/recipes/fx{}'.format(args.version_number)
    hg_path = '/Users/flodolo/mozilla/mercurial/mozilla-unified/python/l10n/fluent_migrations'

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
