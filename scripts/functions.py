import os


def get_locale_folders(path):
    return sorted(
        [
            x
            for x in os.listdir(path)
            if os.path.isdir(os.path.join(path, x)) and not x.startswith(".")
        ]
    )
