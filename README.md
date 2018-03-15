# Fluent Migrations

This repository stores a copy of each migration module created for Gecko
strings, and a script to run the migration.

## Running Migrations

1. Create a virtual environment and install dependencies:

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install mercurial python-hglib
```

2. Clone both [python-fluent](https://github.com/projectfluent/python-fluent)
and [compare-locales](https://hg.mozilla.org/l10n/compare-locales/) on your
system. Install both libraries running `pip install -e .` from the root of each
repository.

3. Clone [gecko-strings-quarantine](https://hg.mozilla.org/users/axel_mozilla.com/gecko-strings-quarantine).

4. Clone all l10n repositories on your system. You can use [this
script](https://github.com/flodolo/scripts/blob/master/mozilla_l10n/update_locales.py)
to generate a list of supported repositories, and [this
script](https://github.com/flodolo/scripts/blob/master/mozilla_l10n/clone.sh) to
clone them.

5. Copy `config/config.dist` as `config`, and adapt the paths to your system.

6. Use `/scripts/migration.sh` to run the migration.

## Command Line Options

To dry-run all locales use:

```
$ migration.sh no-updates
```

To run one locale without pushing:

```
$ migration.sh it wet-run
```

For running migrations on all locales and push to repository, use:

```
$ migration.sh wet-run push
```

Run `/scripts/migration.sh help` for help on all available command line options.
