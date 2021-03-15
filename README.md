# Retriever-Recipes

[![Python package](https://github.com/weecology/retriever-recipes/actions/workflows/python-package.yml/badge.svg)](https://github.com/weecology/retriever-recipes/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/retriever/badge/?version=latest)](http://retriever.readthedocs.io/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/weecology/retriever](https://badges.gitter.im/weecology/retriever.svg)](https://gitter.im/weecology/retriever?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
<img alt="NumFOCUS"
   src="https://i0.wp.com/numfocus.org/wp-content/uploads/2019/06/AffiliatedProject.png" width="100" height="18">
</a>

The [Data Retriever](http://data-retriever.org) earlier used a simple CLI for developing new dataset scripts. This allowed users with no programming experience to quickly add most standard datasets to the [Retriever](https://github.com/weecology/retriever) by specifying the names and locations of the tables along with additional information about the configuration of the data. The script is saved as a JSON file, that follows the [DataPackage](http://specs.frictionlessdata.io/data-packages/) standards.

This functionality has been moved to this repository to separate the scripts from the core ``retriever`` functionalities to help with organization, maintenance, and testing. The `retriever-recipes` repository thus holds all the scripts which were earlier shipped with ``retriever`` and also all the script adding/editing functionalities.

To facilitate the use of recipes as a command-line utility, the user can simply clone the repository and install it. The installation steps are mentioned in the next section.

## Installation

```
    git clone https://www.github.com/weecology/retriever-recipes.git
    cd retriever-recipes
    python setup.py install

```

## Using the Command Line

To see the full list of command line options and datasets run `retriever-recipes --help`. The output will look like this:

```
    usage: retriever-recipes [-h] {new_json,edit_json,delete_json,help} ...

    positional arguments:
      {new_json,edit_json,delete_json,help}
                            sub-command help
        new_json            CLI to create retriever json script
        edit_json           CLI to edit retriever json script
        delete_json         CLI to remove retriever json script
        help

    optional arguments:
      -h, --help            show this help message and exit
```

### Examples

Some example usages of the CLI interface are:

1. Add a new JSON script: 

```
    retriever-recipes new_json
```

2. Delete an existing JSON script: 

```
    retriever-recipes delete_json dataset
```

3. Edit an existing JSON script: 

```
    retriever-recipes edit_json dataset`
```

## Website

For more information, see the [Data Retriever website](https://www.data-retriever.org/). 
