#! /usr/bin/env bash

function interrupt_code()
# This code runs if user hits control-c
{
  printf "\n*** Operation interrupted ***\n"
  exit $?
}

# Trap keyboard interrupt (control-c)
trap interrupt_code SIGINT

script_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_path="$(dirname "${script_path}")"

# Import config
if [ ! -f "${root_path}/config/config" ]
then
    echo "ERROR: ${root_path}/config/config is missing"
    exit
fi
source "${root_path}/config/config"

# Add recipes to $PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${root_path}/recipes/"

function echo_manual() {
    echo "Run 'migration.sh' without parameters to make a dry-run on all locales."
    echo "Run 'migration.sh help' to display this manual."
    echo "---"
    echo "To run only one locale, add the locale code as first parameter"
    echo "(e.g. 'migration.sh it' to run only Italian)."
    echo "---"
    echo "To avoid pulling from repositories, add no-updates"
    echo "(e.g. 'migration.sh no-updates' to run all locales without updates)."
    echo "---"
    echo "To push to repositories, add push"
    echo "(e.g. 'migration.sh push' to run all locales and push changes)."
    echo "---"
    echo "To commit changes, add wet-run"
    echo "(e.g. 'migration.sh wet-run' to run all locales and commit migration changes)."
    echo "---"
    echo "Multiple options can be combined. For example, for a prod migration:"
    echo "(e.g. 'migration.sh wet-run push' to run all locales, commit and push)."
}

# Set defaults
all_locales=true
pull_repository=true
push_repository=false
wet_run=false

# Check command parameters
while [[ $# -gt 0 ]]
do
    case $1 in
        help)
            echo_manual
            exit
        ;;
        no-updates)
            pull_repository=false
        ;;
        push)
            push_repository=true
        ;;
        wet-run)
            wet_run=true
        ;;
        *)
            all_locales=false
            locale_code=$1
        ;;
    esac
    shift
done

echo "Request summary:"
echo "* Pull from repositories: ${pull_repository}"
echo "* Push changes to repositories: ${push_repository}"
echo "* Commit migration changes: ${wet_run}"
if [ "$all_locales" = true ]
then
    echo "* Elaborate all locales: ${all_locales}"
else
    echo "* Elaborate locale: ${locale_code}"
fi

read -p "Continue (y/N)?" -n 1 choice
if [[ ! ${choice} =~ ^[Yy]$ ]]
then
    printf "\nMigration aborted\n"
    exit
fi

# Create the list of available migration recipes.
cd "${root_path}/recipes/"
recipes=(bug*.py)
recipes_list=""
for recipe in ${recipes[@]}
do
    recipes_list="${recipes_list} ${recipe%.py}"
done
echo

cd ${l10n_clones_path}
# Create the list of locales
if [ "${all_locales}" = true ]
then
    locale_list=(*/)
else
    locale_list=("${locale_code}")
fi

for locale in ${locale_list[@]}
do
    # Remove trailing slash from $locale
    locale=${locale%/}
    echo "Locale: ${locale}"

    # Pull from hg server
    if [ "${pull_repository}" = true ]
    then
        hg --cwd ${l10n_clones_path}/${locale} pull -u -r default
    fi

    if [ "${wet_run}" = true ]
    then
        dry=""
    else
        dry="--dry-run"
    fi

    # Run migration
    # -B is to avoid creating .pyc files for each migration recipe
    python -B ${fluent_migration_path}/fluent/migrate/tool.py \
        --lang ${locale} \
        --reference-dir ${quarantine_path} \
        --localization-dir ${l10n_clones_path}/${locale} \
        ${dry} ${recipes_list}

    # Push to hg server
    if [ "${push_repository}" = true ]
    then
        hg --cwd ${l10n_clones_path}/${locale} push
    fi
done
