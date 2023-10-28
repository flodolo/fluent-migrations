# Fluent Migrations

This repository stores a copy of each migration module created for Gecko
strings, and a script to run the migrations.

## Set up the system

1. Create a virtual environment and install dependencies:

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install mercurial python-hglib fluent.migrate
```

2. Clone [gecko-strings-quarantine](https://hg.mozilla.org/users/axel_mozilla.com/gecko-strings-quarantine).

3. Clone all l10n repositories on your system. You can use [these
scripts](https://github.com/flodolo/scripts/tree/master/mozilla_l10n/clone_hgmo)
to automate the process.

4. Copy `config/config.dist` as `config`, and adapt the paths to your system.

5. Use `/scripts/migration.sh` to run the migration.

## Run migrations and organization of the recipes folder

In order to run a migration, recipes need to be stored directly in the
`recipes` folder. The script will look for any Python (`.py`) file starting
with `bug_`, allowing to run multiple recipes in one execution.

After running the migration on all l10n repositories, recipes need to be moved
in one of the `fx` subfolders. For example, if the migration landed in Firefox
77, recipes need to be moved to `fx77`. It’s then possible to use the utility
script `cleanup_migrations.py` to list all recipes landed in a specific version
of Firefox, and remove them from a local `mozilla-unified` clone.

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

Run `./scripts/migration.sh help` for help on all available command line options.

## Removing obsolete recipes from mozilla-central

Obsolete migration recipes need to be periodically removed from
`mozilla-central`. The script `cleanup_migrations.py` can be used for this
purpose.

For example, if you want to remove recipes for version 113, you can run this
command:

```
./scripts/cleanup_migrations.py 113 --bookmark
```

This will:
* Create a bookmark (`cleanrecipes_fx113`) in the `mozilla-unified` local clone.
* Check the recipes that are stored inside the `fx113` folder, and remove them
  from `mozilla-unified`.
* Provide a link to file the bug.

If you want to remove other versions in the same bug, you can run the command
without the `--bookmark` flag, and manually update the bug content with the text
printed in the console.

Once the bug is filed, move the corresponding fx folders (e.g. `fx113`) into the
`archive` folder.
