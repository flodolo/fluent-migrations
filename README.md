# Fluent Migrations

This repository stores a copy of each migration module created for Gecko
strings, and a script to run the migration.

## Running Migrations

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
