from __future__ import print_function

import os
import io
import sys
import imp
import json
from os.path import join, exists
from collections import OrderedDict

ENCODING = 'ISO-8859-1'


def is_empty(val):
    """Check if a variable is an empty string or an empty list."""
    return val == "" or val == []


def clean_input(prompt="", split_char='', ignore_empty=False, dtype=None):
    """Clean the user-input from the CLI before adding it."""
    while True:
        val = input(prompt).strip()
        # split to list type if split_char specified
        if split_char != "":
            val = [v.strip() for v in val.split(split_char) if v.strip() != ""]
        # do not ignore empty input if not allowed
        if not ignore_empty and is_empty(val):
            print("\tError: empty input. Need one or more values.\n")
            continue
        # ensure correct input datatype if specified
        if not is_empty(val) and dtype is not None:
            try:
                if not type(eval(val)) == dtype:
                    print("\tError: input doesn't match required type ", dtype, "\n")
                    continue
            except:
                print("\tError: illegal argument. Input type should be ", dtype, "\n")
                continue
        break
    return val


def open_fr(file_name, encoding=ENCODING, encode=True):
    """Open file for reading respecting Python version and OS differences.

    Sets newline to Linux line endings on Windows and Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if os.name == 'nt':
            file_obj = io.open(file_name, 'r', newline='', encoding=encoding)
        else:
            if encode:
                file_obj = io.open(file_name, "r", encoding=encoding)
            else:
                file_obj = io.open(file_name, "r")
    else:
        file_obj = io.open(file_name, "r", encoding=encoding)
    return file_obj


def read_json(json_file):
    """Read Json dataset package files

    Load each json and get the appropriate encoding for the dataset
    Reload the json using the encoding to ensure correct character sets
    """
    json_object = OrderedDict()
    json_file_encoding = None

    try:
        file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        if "encoding" in json_object:
            json_file_encoding = json_object['encoding']
        file_obj.close()
    except ValueError:
        pass

    # Reload json using encoding if available
    try:
        if json_file_encoding:
            file_obj = open_fr(json_file, encoding=json_file_encoding)
        else:
            file_obj = open_fr(json_file)
        json_object = json.load(file_obj)
        file_obj.close()
    except ValueError:
        pass

    if type(json_object) is dict and "version" in json_object.keys():
        return json_object["version"]
    return None


def read_py(script_name, search_path):
    file, pathname, desc = imp.find_module(script_name, [search_path])
    try:
        new_module = imp.load_module(script_name, file, pathname, desc)
        if hasattr(new_module.SCRIPT, "version"):
            return new_module.SCRIPT.version
    except:
        pass
    return None


def get_script_version():
    """This function gets the version number of the scripts and returns them in array form."""
    search_path = 'scripts'
    loaded_files = []
    scripts = []
    if exists(search_path):
        data_packages = [file_i for file_i in os.listdir(search_path) if file_i.endswith(".json")]
        for script in data_packages:
            script_name = '.'.join(script.split('.')[:-1])
            script_version = read_json(os.path.join(search_path, script))
            if script_name not in loaded_files and script_version:
                scripts.append(','.join([script, str(script_version)]))
                loaded_files.append(script_name)

        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 ('#retriever' in
                  ' '.join(open_fr(join(search_path, file), encoding=ENCODING).readlines()[:2]).lower())
                 ]
        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            script_version = read_py(script_name, search_path)
            if script_name not in loaded_files and script_version:
                scripts.append(','.join([script, str(script_version)]))
                loaded_files.append(script_name)
    else:
        print("No")
    scripts = sorted(scripts, key=str.lower)
    return scripts
