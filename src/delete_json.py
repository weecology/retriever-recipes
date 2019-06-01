from __future__ import print_function

import os
import sys


def delete_json(script):
    json_file = script.replace('-', '_') + '.json'
    try:
        if os.path.exists(os.path.join('scripts', json_file)):
            os.remove(os.path.join('scripts', json_file))
    except OSError:
        print("Couldn't delete script.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception("no dataset specified.")
    script = sys.argv[1]
    delete_json(script)
