import sys
from builtins import input

from recipes.lib.get_opts import parser
from recipes.lib.new_json import create_json
from recipes.lib.edit_json import edit_json
from recipes.lib.delete_json import delete_json


def main():
    """This function launches the retriever-recipes."""
    if len(sys.argv) == 1:
        # If no command line args are passed, show the help options
        parser.parse_args(['-h'])
    else:
        # Otherwise, parse them
        args = parser.parse_args()

        if args.command == 'new_json':
            # Create new JSON script
            create_json()
            return

        if args.command == 'edit_json':
            # Edit existing JSON script
            json_file = args.dataset.lower()
            edit_json(json_file)
            return

        if args.command == 'delete_json':
            # Delete existing JSON script
            confirm = input("Really remove " + args.dataset.lower() +
                            " and all its contents? (y/N): ")
            if confirm.lower().strip() in ['y', 'yes']:
                json_file = args.dataset.lower()
                delete_json(json_file)
            return

if __name__ == "__main__":
    main()
