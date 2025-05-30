# Fluent Migrations

This repository stores a copy of each migration recipe created for
`mozilla-central`, a script to run the migrations, as well as other support
scripts.

## Set up the system

1. Make sure that Python 3 is installed. The bash script will create a virtual
env in `python-venv` and install the required packages.

2. Clone [firefox-l10n-source](https://github.com/mozilla-l10n/firefox-l10n-source)
and switch to the `update` branch.

3. Clone [firefox-l10n](https://github.com/mozilla-l10n/firefox-l10n-source).

4. Copy `config/config.dist` as `config`, and adapt the paths to your system.

5. Use `/scripts/migration.sh` to run the migration.

## Run migrations and organization of the `recipes` folder

In order to run a migration, the recipe needs to be available in the `recipes`
folder. The script will look for any Python (`.py`) file starting with `bug_`,
allowing to run multiple recipes in one execution.

After running the migration, recipes need to be moved in one of the `fx`
subfolders. For example, if the migration landed in Firefox 77, recipes need to
be moved to `fx77`. It’s then possible to use the utility script
`cleanup_migrations.py` to list all recipes landed in a specific version of
Firefox, and remove them from the local clone of
[mozilla-firefox/firefox](https://github.com/mozilla-firefox/firefox).

The `no_train` folder is used for recipes that never landed in
`mozilla-central`.

## Command line options

To dry-run all locales use:

```
$ ./scripts/migration.sh no-updates
```

To run one locale without pushing:

```
$ ./scripts/migration.sh it wet-run
```

For running migrations on all locales and push to repository, use:

```
$ ./scripts/migration.sh wet-run push
```

To use the current checked out branch instead of creating a new branch for wet-runs, use:

```
$ ./scripts/migration.sh wet-run current-branch
```

> [!CAUTION]
> The script assumes your local clone of `firefox-l10n` is already on the
> correct branch, and that the value of `push.default` in Git’s configuration
> allows to push without an explicit remote or branch if you have not created
> a new branch.

Run `./scripts/migration.sh help` for help on all available command line options.

## Removing obsolete recipes from `mozilla-central`

Obsolete migration recipes need to be periodically removed from
`mozilla-central`. The script `cleanup_migrations.py` can be used for this
purpose.

For example, if you want to remove recipes for version 113, you can run this
command:

```
./scripts/cleanup_migrations.py 113 --branch
```

This will:
* Create a branch (`cleanrecipes_fx113`) in the `mozilla-firefox/firefox` local clone.
* Check the recipes that are stored inside the `fx113` folder, and remove them
  from the repository.
* Provide a link to file the bug with pre-populated text.

If you want to remove other versions in the same bug, you can run the command
without the `--branch` flag, and manually update the bug content with the text
printed in the console.

Once the bug is filed, move the corresponding fx folders (e.g. `fx113`) into the
`archive` folder.

# Other scripts

This repository includes other Python scripts that should be run within the
virtual environment created by the main bash script (to activate it run `source
python-venv/bin/activate`):
* `remove_obsolete_files.py`: removes obsolete files from locales. By default,
  `.ftl` files are ignored, given the fallback issue. To clean up `.ftl` files,
  you can add `.ftl` to the list `supported_formats`, then run
  `add_missing_ftl.py` to add files that are still relevant.
* `remove_obsolete_strings.py`: removes obsolete strings from files, and
  reformats them. This should be run sparingly (e.g. after the removal of an ESR
  branch), as it requires a resource intensive sync in Pontoon (it’s
  advised to use a larger Heroku worker for the first sync).
