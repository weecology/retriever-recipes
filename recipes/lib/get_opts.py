import argparse
import argcomplete

from recipes.lib.utils import get_script_version
from recipes.lib.defaults import SCRIPT_SEARCH_PATHS


script_list = []

script_version_list = get_script_version(SCRIPT_SEARCH_PATHS)
for script in script_version_list:
    script = script.split(',')[0]
    if script.endswith('.json'):
        script_list.append(('.'.join(script.split('.')[:-1])).replace('_', '-'))

parser = argparse.ArgumentParser(prog='retriever-recipes')

# ..............................................................
# Subparsers
# ..............................................................
subparsers = parser.add_subparsers(help='sub-command help', dest='command')
new_json_parser = subparsers.add_parser('new_json', help='CLI to create retriever json script')
edit_json_parser = subparsers.add_parser('edit_json', help='CLI to edit retriever json script')
delete_json_parser = subparsers.add_parser('delete_json', help='CLI to remove retriever json script')
help_parser = subparsers.add_parser('help', help='')

# ..............................................................
# Subparsers With Arguments
# ..............................................................
edit_json_parser.add_argument('dataset', nargs=1, help='dataset name', choices=script_list)
delete_json_parser.add_argument('dataset', nargs=1, help='dataset name', choices=script_list)

argcomplete.autocomplete(parser)
