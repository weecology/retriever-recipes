from __future__ import print_function

import os
import sys
import json
from time import sleep

from utils import clean_input


def edit_dict(obj, tabwidth=0):
    """
    Recursive helper function for edit_json() to edit a datapackage.JSON script file.
    """
    for key, val in obj.copy().items():
        print('\n' + "  " * tabwidth + "->" + key + " (", type(val), ") :\n")
        if isinstance(val, list):
            for v in val:
                print("  " * tabwidth + str(v) + '\n\n')
        elif isinstance(val, dict):
            for item in val.items():
                print("  " * tabwidth + str(item) + '\n\n')
        else:
            print("  " * tabwidth + str(val) + '\n\n')

        while True:
            try:
                if isinstance(val, dict):
                    if val != {}:
                        print("    '" + key + "' has the following keys:\n" +
                              str(obj[key].keys()) + "\n")
                        do_edit = clean_input(
                            "Edit the values for these sub-keys of " + key + "? (y/N): ")

                        if do_edit.lower() in ['y', 'yes']:
                            edit_dict(obj[key], tabwidth + 1)

                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Add an item")
                    print("2. Modify an item")
                    print("3. Delete an item")
                    print("4. Remove from script")
                    print("5. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        add_key = clean_input('Enter new key: ')
                        add_val = clean_input('Enter new value: ')
                        obj[key][add_key] = add_val

                    elif selection == '2':
                        mod_key = clean_input('Enter the key: ')
                        if mod_key not in val:
                            print("Invalid input! Key not found.")
                            continue
                        mod_val = clean_input('Enter new value: ')
                        obj[key][mod_key] = mod_val

                    elif selection == '3':
                        del_key = clean_input('Enter key to be deleted: ')
                        if del_key not in val:
                            print("Invalid key: Not found")
                            continue
                        print("Removed " + str(del_key) +
                              " : " + str(obj[key].pop(del_key)))

                    elif selection == '4':
                        do_remove = clean_input(
                            "Are you sure "
                            "(completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)
                    elif selection == '5' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")

                elif isinstance(val, list):

                    for i in range(len(val)):
                        print(i + 1, '. ', str(val[i]))
                        if isinstance(val[i], dict):
                            do_edit = clean_input(
                                "\nEdit this dict in '" + key + "'? (y/N): ")

                            if do_edit.lower() in ['y', 'yes']:
                                edit_dict(obj[key][i], tabwidth + 2)

                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Add an item")
                    print("2. Delete an item")
                    print("3. Remove from script")
                    print("4. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        add_val = clean_input('Enter new value: ')
                        obj[key].append(add_val)

                    elif selection == '2':
                        del_val = clean_input('Enter value to be deleted: ')

                        if del_val not in obj[key]:
                            print("Invalid value: Not found.")
                            continue
                        obj[key].remove(del_val)
                        print("Removed " + str(del_val))

                    elif selection == '3':
                        do_remove = clean_input(
                            "Are you sure "
                            "(completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)

                    elif selection == '4' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")

                else:
                    print("Select one of the following for the key '" + key + "': \n")
                    print("1. Modify value")
                    print("2. Remove from script")
                    print("3. Continue (no changes)\n")

                    selection = clean_input("\nYour choice: ")

                    if selection == '1':
                        new_val = clean_input('Enter new value: ')
                        obj[key] = new_val

                    elif selection == '2':
                        do_remove = clean_input(
                            "Are you sure (completely remove this entry)? (y/n): ")

                        if do_remove.lower() in ['y', 'yes']:
                            obj.pop(key)
                            print("Removed " + key + " from script.\n")
                        else:
                            print("Aborted.")
                            sleep(1)
                    elif selection == '3' or selection == "":
                        pass
                    else:
                        raise RuntimeError("Invalid input!")
                break
            except RuntimeError:
                continue


def edit_json(script):
    """
    Edit existing datapackage.JSON script.

    Usage: retriever edit_json <script_name>
    Note: Name of script is the dataset name.
    """
    json_file = script.replace('-', '_') + '.json'
    try:
        contents = json.load(
            open(os.path.join('scripts', json_file), 'r'))
    except (IOError, OSError):
        print("Script not found.")
        return

    edit_dict(contents, 1)

    file_name = contents['name'] + ".json"
    file_name = file_name.replace('-', '_')
    with open(os.path.join('scripts', file_name), 'w') as output_file:
        json.dump(contents,
                  output_file,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))
        output_file.write('\n')
        print("\nScript written to " + os.path.join('scripts', file_name))
        output_file.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception("no dataset specified.")
    script = sys.argv[1]
    edit_json(script)
