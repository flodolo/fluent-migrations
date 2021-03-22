"""
This code is imported from other scripts to read paths from the
configuration file.
"""

import os
import sys


def read_config(params):
    # Get absolute path of the repository's root from the script location
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    config_file = os.path.join(root_folder, "config", "config")

    # Abort if config file is missing
    if not os.path.exists(config_file):
        sys.exit("ERROR: config file is missing")

    # Read all available paths in the config file
    paths = {}
    with open(config_file, "r") as cfg_file:
        for line in cfg_file:
            line = line.strip()
            # Ignore comments and empty lines
            if line == "" or line.startswith("#"):
                continue
            paths[line.split("=")[0]] = line.split("=")[1].strip('"')

    results = []
    for param in params:
        if param not in paths:
            sys.exit("{} is not defined in the config file".format(param))
        else:
            if not os.path.exists(paths[param]):
                sys.exit(
                    "Path defined for {} ({}) does not exist".format(
                        param, paths[param]
                    )
                )
        results.append(paths[param])

    return results
