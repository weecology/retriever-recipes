import argparse
import argcomplete

from recipes.lib.utils import get_script_version


script_list = []

script_version_list = get_script_version()
for script in script_version_list:
    script = script.split(',')[0]
    if script.endswith('.json'):
        script_list.append(('.'.join(script.split('.')[:-1])).replace('_', '-'))

parser = argparse.ArgumentParser(prog='retriever-recipes')

# ..............................................................
# Subparsers
# ..............................................................
subparsers = parser.add_subparsers(help='sub-command help', dest='command')
new_json_parser = subparsers.add_parser('new_json', help='CLI to create retriever datapackage.json script')
edit_json_parser = subparsers.add_parser('edit_json', help='CLI to edit retriever datapackage.json script')
delete_json_parser = subparsers.add_parser('delete_json', help='CLI to remove retriever datapackage.json script')
help_parser = subparsers.add_parser('help', help='')

# ..............................................................
# Subparsers With Arguments
# ..............................................................
edit_json_parser.add_argument('dataset', help='dataset name', choices=script_list)
delete_json_parser.add_argument('dataset', help='dataset name', choices=script_list)

argcomplete.autocomplete(parser)
