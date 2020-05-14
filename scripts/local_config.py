#!/usr/bin/env python3

"""
This code is imported from other scripts to read paths from the
configuration file.
"""

import os
import sys


def read_config(params):
    # Get absolute path of the repository's root from the script location
    root_folder = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    config_file = os.path.join(root_folder, 'config', 'config')

    # Abort if config file is missing
    if not os.path.exists(config_file):
        print('ERROR: config file is missing')
        sys.exit(1)

    # Read all available paths in the config file
    paths = {}
    with open(config_file, 'r') as cfg:
        lines = cfg.readlines()
        # Ignore comments and empty lines
        lines[:] = [l.strip() for l in lines if l.strip() != '' and not l.startswith('#')]

        for line in lines:
            paths[line.split('=')[0]] = line.split('=')[1].strip('"')

    results = []
    for param in params:
        if not param in paths:
            print('{} is not defined in the config file'.format(param))
            sys.exit(1)
        else:
            if not os.path.exists(paths[param]):
                print('Path defined for {} ({}) does not exist'.format(
                    param, paths[param]))
                sys.exit(1)
        results.append(paths[param])

    return results

if __name__ == '__main__':
    main()
