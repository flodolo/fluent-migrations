#! /usr/bin/env bash

function interrupt_code()
# This code runs if user hits control-c
{
  printf "\n*** Operation interrupted ***\n"
  exit $?
}

# Trap keyboard interrupt (control-c)
trap interrupt_code SIGINT

function setupVirtualEnv() {
    # Create virtualenv folder if missing
    if [ ! -d $root_path/python-venv ]
    then
        echo "Setting up new virtualenv..."
        python3 -m venv $root_path/python-venv || exit 1
    fi

    # Install or update dependencies
    source $root_path/python-venv/bin/activate || exit 1
    pip install --upgrade --quiet pip
    pip install -r $script_path/requirements.txt --upgrade --quiet --use-pep517
    deactivate
}

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
    echo "To avoid pulling from repository, add no-updates"
    echo "(e.g. 'migration.sh no-updates' to run all locales without updates)."
    echo "---"
    echo "To push to repository, add push"
    echo "(e.g. 'migration.sh push' to run all locales and push changes)."
    echo "---"
    echo "To commit changes, add wet-run"
    echo "(e.g. 'migration.sh wet-run' to run all locales and commit migration changes)."
    echo "---"
    echo "To use the current checked out branch of the push repository instead of"
    echo "creating a new one for a wet-run, add current-branch"
    echo "(e.g. 'migration.sh wet-run current-branch' to do a wet-run on the current branch)."
    echo "---"
    echo "Multiple options can be combined. For example, for a prod migration:"
    echo "(e.g. 'migration.sh wet-run push' to run all locales, commit and push)."
}

# Set defaults
all_locales=true
pull_repository=true
push_repository=false
wet_run=false
create_branch=true

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
        current-branch)
            create_branch=false
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
echo "* Create new branch in push repository for wet-run: ${create_branch}"
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

cd ${l10n_path}
# Create the list of locales
if [ "${all_locales}" = true ]
then
    locale_list=(*/)
else
    locale_list=("${locale_code}")
fi

# Pull git repository
if [ "${pull_repository}" = true ]
then
    git -C ${l10n_path} pull
fi

# Set up virtualenv
setupVirtualEnv

# Activate virtualenv
source $root_path/python-venv/bin/activate || exit 1

for locale in ${locale_list[@]}
do
    # Remove trailing slash from $locale and $l10n_path
    locale=${locale%/}
    l10n_path=${l10n_path%/}
    echo "Locale: ${locale}"

    if [ "${wet_run}" = true ]
    then
        dry=""
        if [ "${create_branch}" = true ]
        then
            git -C ${l10n_path} switch -C ${branch_name}
        fi
    else
        dry="--dry-run"
    fi

    # Run migration
    migrate-l10n \
        --lang ${locale} \
        --reference-dir ${quarantine_path} \
        --localization-dir ${l10n_path}/${locale} \
        ${dry} ${recipes_list}
done

# Push git repository
if [ "${push_repository}" = true ]
then
    if [ "${create_branch}" = true ]
    then
        git -C ${l10n_path} push --set-upstream origin ${branch_name}
    else
        git -C ${l10n_path} push
    fi
fi
