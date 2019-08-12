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
import pytest
from distutils.version import LooseVersion

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from recipes.lib.utils import get_script_version

import retriever as rt

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
    pgdb_host = "pgdb_recipes"

global_modified_scripts = []

spatial_datasets = [
        "forest-inventory-analysis",
        "prism-climate",
        "vertnet",
        "NPN",
        "mammal-super-tree"
    ]
spatial_datasets_list = [dataset.lower() for dataset in spatial_datasets]


def setup_module():
    """Make sure that you are in the source main directory.

    This ensures that scripts obtained are from the scripts directory
    and not the .retriever's script directory.
    """
    os.chdir(retriever_recipes_root_dir)
    if os.path.exists("test_modified"):
        subprocess.call(['rm', '-r', 'test_modified'])
    get_modified_scripts()
    os.makedirs("test_modified")
    os.chdir("test_modified")


def teardown_module():
    """Cleanup temporary output files and return to root directory."""
    os.chdir("..")
    subprocess.call(['rm', '-r', 'test_modified'])


def get_modified_scripts():
    """Get modified script list, using version.txt in repo and master upstream"""
    global global_modified_scripts
    modified_list = []
    version_file = requests.get(
        "https://raw.githubusercontent.com/weecology/retriever-recipes/retriever-recipes-dev/version.txt")
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
        elif LooseVersion(local_version) > upstream_versions[local_script]:
            script_name = os.path.basename(local_script).split('.')[0]
            script = script_name.replace('_', '-')
            modified_list.append(script)
    global_modified_scripts = modified_list


@pytest.mark.skipif('IN_TRAVIS' in os.environ, reason="Does not run on travis")
def test_install_csv():
    """Installs modified scripts using csv engine"""
    errors = []
    for script in global_modified_scripts:
        if script not in spatial_datasets_list:
            try:
                rt.install_csv(script, table_name='{db}_{table}.csv', debug=True)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                errors.append(("csv", script, e))
    assert errors == []


@pytest.mark.skipif('IN_TRAVIS' in os.environ, reason="Does not run on travis")
def test_install_xml():
    """Installs modified scripts using xml engine"""
    errors = []
    for script in global_modified_scripts:
        if script not in spatial_datasets_list:
            try:
                rt.install_xml(script, table_name='{db}_{table}.xml', debug=True)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                errors.append(("xml", script, e))
    assert errors == []


@pytest.mark.skipif('IN_TRAVIS' in os.environ, reason="Does not run on travis")
def test_install_json():
    """Installs modified scripts using json engine"""
    errors = []
    for script in global_modified_scripts:
        if script not in spatial_datasets_list:
            try:
                rt.install_json(script, table_name='{db}_{table}.json', debug=True)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                errors.append(("json", script, e))
    assert errors == []


@pytest.mark.skipif('IN_TRAVIS' in os.environ, reason="Does not run on travis")
def test_install_sqlite():
    """Installs modified scripts using sqlite engine"""
    dbfile = os.path.normpath(os.path.join(os.getcwd(), 'testdb_retriever.sqlite'))

    errors = []
    for script in global_modified_scripts:
        if script not in spatial_datasets_list:
            try:
                rt.install_sqlite(script, file=dbfile, table_name='{db}_{table}', debug=True)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                errors.append(("sqlite", script, e))
    assert errors == []


@pytest.mark.skipif('IN_TRAVIS' in os.environ, reason="Does not run on travis")
def test_install_postgres():
    """Installs modified scripts using postgres engine"""
    errors = []
    for script in global_modified_scripts:
        if script in spatial_datasets_list:
            args = {'user': 'postgres',
                    'password': os_password,
                    'host': pgdb_host,
                    'port': 5432,
                    'database': testdb_retriever,
                    'database_name': 'testschema',
                    'table_name': '{db}.{table}',
                    'debug': True}
            cmd = 'psql -U postgres -d ' + testdb_retriever +' -h ' + pgdb_host + ' -w -c \"DROP SCHEMA IF EXISTS testschema CASCADE\"'
            subprocess.call(shlex.split(cmd))
            try:
                rt.install_postgres(script, **args)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                errors.append(("postgres", script, e))
            continue
    assert errors == []
