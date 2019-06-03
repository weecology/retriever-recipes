"""Generates a configuration file containing the version number."""
from __future__ import absolute_import

import os

from src.utils import get_script_version


def write_version_file(scripts):
    """The function creates / updates version.txt with the script version numbers."""
    if os.path.isfile("version.txt"):
        os.remove("version.txt")

    with open("version.txt", "w") as version_file:
        version_file.write("Retriever Scripts Versions")
        for script in scripts:
            version_file.write('\n' + script)


def update_version_file():
    """Update version.txt."""
    scripts = get_script_version()
    write_version_file(scripts)
    print("Version.txt updated.")


if __name__ == '__main__':
    update_version_file()
