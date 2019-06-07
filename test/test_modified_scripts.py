"""This module, when run, attempts to install datasets for modified Retriever
scripts in the /scripts folder
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import shlex
import subprocess
import requests
from imp import reload
from distutils.version import LooseVersion

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils import get_script_version

ENCODING = 'ISO-8859-1'

reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding(ENCODING)

file_location = os.path.dirname(os.path.realpath(__file__))
retriever_recipes_root_dir = os.path.abspath(os.path.join(file_location, os.pardir))

os_password = ""
pgdb_host = "localhost"
testdb_retriever = "testdb_retriever"
testschema = "testschema_retriever"

if os.name == "nt":
    os_password = "Password12!"

docker_or_travis = os.environ.get("IN_DOCKER")
if docker_or_travis == "true":
    os_password = 'Password12!'
    pgdb_host = "pgdb_retriever"


def setup_module():
    """Make sure that you are in the source main directory.

    This ensures that scripts obtained are from the scripts directory
    and not the .retriever's script directory.
    """
    os.chdir(retriever_recipes_root_dir)


def get_modified_scripts():
    """Get modified script list, using version.txt in repo and master upstream"""
    modified_list = []
    version_file = requests.get(
        "https://raw.githubusercontent.com/harshitbansal05/retriever-recipes/master/version.txt")
    local_repo_scripts = get_script_version()

    upstream_versions = {}
    version_file = version_file.text.splitlines()[1:]
    for line in version_file:
        master_script_name, master_script_version = line.lower().strip().split(",")
        upstream_versions[master_script_name] = master_script_version

    for item in local_repo_scripts:
        local_script, local_version = item.lower().split(",")
        # check for new scripts or a change in versions for present scripts
        # repo script versions compared with upstream.
        if local_script not in upstream_versions.keys():
            script_name = os.path.basename(local_script).split('.')[0]
            script = script_name.replace('_', '-')
            modified_list.append(script)
        elif LooseVersion(local_version) != upstream_versions[local_script]:
            script_name = os.path.basename(local_script).split('.')[0]
            script = script_name.replace('_', '-')
            modified_list.append(script)
    print("List: ", modified_list)
    return modified_list


def install_modified():
    """Installs modified scripts and returns any errors found"""
    try:
        import retriever as rt
    except ImportError:
        print("Retriever is not installed. Skipping tests...")
        return

    setup_module()

    spatial_datasets = [
        "forest-inventory-analysis",
        "bioclim",
        "prism-climate",
        "vertnet",
        "NPN",
        "mammal-super-tree"
    ]
    spatial_datasets_list = [dataset.lower() for dataset in spatial_datasets]

    modified_scripts = get_modified_scripts()
    if modified_scripts is None:
        print("No new scripts found. Database is up to date.")
        sys.exit()
    else:
        print(modified_scripts)
    if os.path.exists("test_modified"):
        subprocess.call(['rm', '-r', 'test_modified'])
    os.makedirs("test_modified")
    os.chdir("test_modified")
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb_retriever.sqlite'))

    engine_test = {
        rt.install_xml: ["xml", {'table_name': '{db}_{table}.xml', 'debug': True}],

        rt.install_json: ["json", {'table_name': '{db}_{table}.json', 'debug': True}],

        rt.install_csv: ["csv", {'table_name': '{db}_{table}.csv', 'debug': True}],

        rt.install_sqlite: ["sqlite", {'file': dbfile,
                            'table_name': '{db}_{table}', 'debug': True}]
    }
    
    errors = []
    for script in modified_scripts:
        if script in spatial_datasets_list:
            args = {'user': 'postgres',
                    'password': os_password,
                    'host': pgdb_host,
                    'port': 5432,
                    'database': testdb_retriever,
                    'database_name': 'testschema',
                    'table_name': '{db}.{table}',
                    'debug': True}
            print("Args:")
            print(args)
            cmd = 'psql -U postgres -d ' + testdb_retriever +' -h ' + pgdb_host + ' -w -c \"DROP SCHEMA IF EXISTS testschema CASCADE\"'
            subprocess.call(shlex.split(cmd))
            try:
                rt.install_postgres(script, **args)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("ERROR.")
                errors.append(("postgres", script, e))
            continue
        for install_function in engine_test:
            args = engine_test[install_function]
            try:
                install_function(script, **(args[1]))
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("ERROR.")
                errors.append((args[0], script, e))

    os.chdir("..")
    subprocess.call(['rm', '-r', 'test_modified'])

    if errors:
        print("Engine, Dataset, Error")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("All tests passed. All scripts are updated to latest version.")
        exit(0)

if __name__ == "__main__":
    install_modified()
