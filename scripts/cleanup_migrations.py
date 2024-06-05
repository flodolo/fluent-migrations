#!/usr/bin/env python3

"""
Pass a version number like 65 to:
- Get the list of recipes from the fluent migrations landed in that version
- Remove the recipes from the mozilla-unified repository
- Get a link to file a bug in Bugzilla
"""

import argparse
import os
import subprocess

import local_config


def main():
    bug_template = "https://bugzilla.mozilla.org/enter_bug.cgi?assigned_to=nobody%40mozilla.org&bug_ignored=0&bug_severity=normal&bug_status=NEW&bug_type=task&cc=francesco.lodolo%40gmail.com&cf_fx_iteration=---&cf_fx_points=---&comment=Remove%20migration%20recipes%20for%20Firefox%20{version}.%0D%0A%0D%0A{bugs}&component=Fluent%20Migration&contenttypemethod=list&contenttypeselection=text%2Fplain&defined_groups=1&filed_via=standard_form&flag_type-4=X&flag_type-607=X&flag_type-800=X&flag_type-803=X&flag_type-936=X&form_name=enter_bug&maketemplate=Remember%20values%20as%20bookmarkable%20template&op_sys=Unspecified&priority=--&product=Localization%20Infrastructure%20and%20Tools&rep_platform=Unspecified&short_desc=Remove%20Fluent%20migration%20recipes%20for%20Firefox%20{version}&target_milestone=---&version=unspecified"

    # Get absolute path of the repository's root from the script location
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # Read paths from config file
    [mozilla_unified_path] = local_config.read_config(["mozilla_unified_path"])

    parser = argparse.ArgumentParser()
    parser.add_argument("version_number", help="Version number, e.g. 65")
    parser.add_argument(
        "--bookmark", help="Create bookmark in mozilla-unified", action="store_true"
    )
    args = parser.parse_args()

    # Get the list of recipes
    version_number = args.version_number
    recipes_path = os.path.join(root_folder, "recipes", f"fx{version_number}")
    hg_path = os.path.join(mozilla_unified_path, "python", "l10n", "fluent_migrations")

    for root, dirs, files in os.walk(recipes_path, followlinks=True):
        # Exclude hidden folders and files
        recipes = [f for f in files if not f[0] == "."]
    try:
        recipes.sort()
        output = []
        output.append(f"Affected bugs ({version_number}):")
        for recipe in recipes:
            # Remove the files from mozilla-unified
            try:
                recipe_path = os.path.join(hg_path, recipe)
                os.remove(recipe_path)
                output.append("- Bug {}".format(recipe.split("_")[1]))
            except FileNotFoundError:
                print(f"File {recipe_path} doesn't exist")

        print("\n".join(output))

        if args.bookmark:
            # Create hg bookmark and addremove files
            subprocess.run(
                [
                    "hg",
                    "-R",
                    mozilla_unified_path,
                    "bookmark",
                    f"cleanrecipes_fx{version_number}",
                ]
            )
        subprocess.run(["hg", "-R", mozilla_unified_path, "addremove"])

        # Print link to bug template
        encoded_output = [line.replace(" ", "%20") for line in output]
        print("\nBug template:\n")
        print(
            bug_template.format(
                version=args.version_number, bugs="%0D%0A".join(encoded_output)
            )
        )
    except NameError:
        print("No recipes found")


if __name__ == "__main__":
    main()
