from __future__ import print_function

import os
import re
import json
from os.path import join, exists

from utils import clean_input, is_empty, open_fr, ENCODING


def short_names():
    search_path = 'scripts'
    shortnames = set()
    if exists(search_path):
        data_packages = [file_i for file_i in os.listdir(search_path) if file_i.endswith(".json")]
        for script in data_packages:
            script_name = '.'.join(script.split('.')[:-1])
            script_name = script_name.replace('_', '-')
            shortnames.add(script_name)
        files = [file for file in os.listdir(search_path)
                 if file[-3:] == ".py" and file[0] != "_" and
                 ('#retriever' in
                  ' '.join(open_fr(join(search_path, file), encoding=ENCODING).readlines()[:2]).lower())
                 ]
        for script in files:
            script_name = '.'.join(script.split('.')[:-1])
            script_name = script_name.replace('_', '-')
            shortnames.add(script_name)
    return list(shortnames)


def get_replace_columns(dialect):
    """Get the replace values for columns from the user."""
    val = clean_input("replace_columns (separated by "
                      "';', with comma-separated values) "
                      "(press return to skip): ",
                      split_char=';', ignore_empty=True)
    if val == "" or val == []:
        # return and don't add key to dialect dict if empty val
        return
    dialect['replace_columns'] = []
    for v in val:
        try:
            pair = v.split(',')
            dialect['replace_columns'].append((pair[0].strip(), pair[1].strip()))
        except IndexError:
            continue


def get_nulls(dialect):
    """Get list of strings that denote missing value in the dataset."""
    val = clean_input(
        "missing values (separated by ';') (press return to skip): ",
        split_char=';',
        ignore_empty=True
    )
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['missingValues'] = val
    # change list to single value if size == 1
    if len(dialect['missingValues']) == 1:
        dialect['missingValues'] = dialect['missingValues'][0]


def get_delimiter(dialect):
    """Get the string delimiter for the dataset file(s)."""
    val = clean_input("delimiter (press return to skip): ", ignore_empty=True)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['delimiter'] = val


def get_do_not_bulk_insert(dialect):
    """Set do_not_bulk_insert property."""
    val = clean_input(
        "do_not_bulk_insert (bool = True/False) (press return to skip): ",
        ignore_empty=True,
        dtype=bool
    )
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['do_not_bulk_insert'] = val


def get_contains_pk(dialect):
    """Set contains_pk property."""
    val = clean_input(
        "contains_pk (bool = True/False) (press return to skip): ",
        ignore_empty=True,
        dtype=bool
    )
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['contains_pk'] = val


def get_fixed_width(dialect):
    """Set fixed_width property."""
    val = clean_input(
        "fixed_width (bool = True/False) (press return to skip): ",
        ignore_empty=True,
        dtype=bool
    )
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['fixed_width'] = val


def get_header_rows(dialect):
    """Get number of rows considered as the header."""
    val = clean_input("header_rows (int) (press return to skip): ",
                      ignore_empty=True, dtype=int)
    if val == "" or val == []:
        # return and dont add key to dialect dict if empty val
        return
    dialect['header_rows'] = val


def create_json():
    """
    Creates datapackage.JSON script.
    http://specs.frictionlessdata.io/data-packages/#descriptor-datapackagejson
    Takes input from user via command line.
    """
    contents = {}
    tableurls = {}

    invalid_name = True
    script_exists = True
    while script_exists or invalid_name:
        contents['name'] = clean_input("name (a short unique identifier;"
                                       " only lowercase letters and - allowed): ")
        invalid_name = re.compile(r'[^a-z-]').search(contents['name'])
        if invalid_name:
            print("name can only contain lowercase letters and -")
            continue
        script_exists = contents['name'].lower() in short_names()
        if script_exists:
            print("Dataset already available. Check the list or try a different name")

    contents['title'] = clean_input("title: ", ignore_empty=True)
    contents['description'] = clean_input("description: ", ignore_empty=True)
    contents['citation'] = clean_input("citations (separated by ';'): ",
                                       split_char=';', ignore_empty=True)
    contents['homepage'] = clean_input("homepage (for the entire dataset): ", ignore_empty=True)
    contents['keywords'] = clean_input("keywords (separated by ';'): ",
                                       split_char=';', ignore_empty=True)
    contents['resources'] = []
    contents['retriever'] = "True"
    contents['retriever_minimum_version'] = "2.0.dev"
    contents['encoding'] = clean_input("encoding: ", ignore_empty=True)
    if is_empty(clean_input("encoding: ", ignore_empty=True)):
        contents['encoding'] = ENCODING
    contents['version'] = "1.0.0"

    # Add tables
    while True:
        addtable = clean_input("\nAdd Table? (y/N): ")
        if addtable.lower() in ["n", "no"]:
            break
        elif addtable.lower() not in ["y", "yes"]:
            print("Not a valid option\n")
            continue
        else:
            table = dict()
            table['name'] = clean_input("table-name: ")
            table['url'] = clean_input("table-url: ")
            table['dialect'] = {}
            tableurls[table['name']] = table['url']

            # get table properties (dialect)
            # refer retriever.lib.table.Table
            get_replace_columns(table['dialect'])
            get_nulls(table['dialect'])
            get_delimiter(table['dialect'])
            get_do_not_bulk_insert(table['dialect'])
            get_contains_pk(table['dialect'])
            get_fixed_width(table['dialect'])
            get_header_rows(table['dialect'])

            # set table schema
            table['schema'] = {}
            table['schema']["fields"] = []
            print("Enter columns [format = name, type, (optional) size] (press return to skip):\n\n")
            while True:
                # get column list (optional)
                try:
                    col_list = clean_input("", split_char=',', ignore_empty=True)
                    if not col_list:
                        break
                    if not isinstance(col_list, list):
                        raise Exception

                    col_list = [c.strip() for c in col_list]
                    col_obj = dict()  # dict to store column data
                    col_obj["name"] = col_list[0]
                    col_obj["type"] = col_list[1]

                    if len(col_list) > 2:
                        if type(eval(col_list[2])) != int:
                            raise Exception
                        col_obj["size"] = col_list[2]
                    table["schema"]["fields"].append(col_obj)
                except:
                    print("Exception occured. Check the input format again.\n")
                    pass

            isCT = clean_input(
                "Add crosstab columns? (y,N): ", ignore_empty=True)
            if isCT.lower() in ["y", "yes"]:
                ct_column = clean_input("Crosstab column name: ")
                ct_names = []
                print("Enter names of crosstab column values (Press return after each name):\n")
                name = clean_input()
                while name != "":
                    ct_names.append(name)
                    name = clean_input()

                table['schema']['ct_column'] = ct_column
                table['schema']['ct_names'] = ct_names

            contents['resources'].append(table)
    give_message = clean_input(
        "Would you like to add a Message? (y,N): ", ignore_empty=True)
    if give_message.lower() in ["y", "yes"]:
        contents['message'] = clean_input("Provide your Message: ", ignore_empty=True)
    contents['urls'] = tableurls
    file_name = contents['name'] + ".json"
    file_name = file_name.replace('-', '_')
    with open(os.path.join('scripts', file_name), 'w') as output_file:
        json.dump(contents,
                  output_file,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))
        output_file.write('\n')
        print("\nScript written to " + file_name)
        output_file.close()


if __name__ == '__main__':
    create_json()
