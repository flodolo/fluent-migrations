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

## Command Line Options

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
