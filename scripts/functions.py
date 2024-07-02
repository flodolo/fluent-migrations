import argparse
import os


def get_locale_folders(path):
    return sorted(
        [
            x
            for x in os.listdir(path)
            if os.path.isdir(os.path.join(path, x)) and not x.startswith(".")
        ]
    )


def get_cli_params(cmd_desc, threshold):
    p = argparse.ArgumentParser(description=cmd_desc)

    p.add_argument(
        "--no-updates",
        help="Do not pull from remote",
        action="store_true",
        dest="noupdates",
    )
    p.add_argument(
        "--wet-run",
        help="Commit local changes",
        action="store_true",
        dest="wetrun",
    )
    p.add_argument(
        "--push",
        help="Push changes to remote (imply --wet-run)",
        action="store_true",
    )
    p.add_argument(
        "--locale", help="Run on a specific locale", action="store", default=""
    )
    if threshold:
        p.add_argument(
            "--threshold",
            help="Minimum percentage of completion in completion under which locales are ignored",
            action="store",
            default="70",
        )

    return p.parse_args()
