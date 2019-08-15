import os
import platform
import subprocess

from setuptools import setup, find_packages

from recipes.lib.defaults import RETRIEVER_HOME_DIR

current_platform = platform.system().lower()

if os.path.exists(".git/hooks"):  # check if we are in git repo
    subprocess.call("cp hooks/pre-commit .git/hooks/pre-commit", shell=True)
    subprocess.call("chmod +x .git/hooks/pre-commit", shell=True)


def read(*names, **kwargs):
    return open(
        os.path.join(os.path.dirname(__file__), *names),
    ).read()


setup(
    name='retriever-recipes',
    version='0.0.1',
    description='Retriever Recieps',
    long_description='{a}'.format(a=read('README.md')),
    long_description_content_type='text/markdown',
    author='Harshit Bansal, Apoorva Pandey, Ben Morris, Shivam Negi, Akash Goel, Andrew Zhang, Henry Senyondo, Ethan White',
    author_email='ethan@weecology.org',
    url='https://github.com/weecology/retriever-recipes',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Database',
    ],
    packages=find_packages(
        exclude=['hooks',
                 'docs',
                 'tests',
                 'scripts',
                 'docker',
                 ".cache"]),
    entry_points={
        'console_scripts': [
            'retriever-recipes = recipes.__main__:main',
        ],
    },
    install_requires=[
        'future',
        'argcomplete'
    ],
    setup_requires=[],
)

# windows doesn't have bash. No point in using bash-completion
if current_platform != "windows":
    # if platform is OS X use "~/.bash_profile"
    if current_platform == "darwin":
        bash_file = "~/.bash_profile"
    # if platform is Linux use "~/.bashrc
    elif current_platform == "linux":
        bash_file = "~/.bashrc"
    # else write and discard
    else:
        bash_file = "/dev/null"

    argcomplete_command = 'eval "$(register-python-argcomplete retriever-recipes)"'
    with open(os.path.expanduser(bash_file), "a+") as bashrc:
        bashrc.seek(0)
        # register retriever for arg-completion if not already registered
        # whenever a new shell is spawned
        if argcomplete_command not in bashrc.read():
            bashrc.write(argcomplete_command + "\n")
            bashrc.close()
    os.system("activate-global-python-argcomplete")
    # register for the current shell
    os.system(argcomplete_command)

if os.path.exists(RETRIEVER_HOME_DIR):
    retriever_recipes_path = os.getcwd()
    with open(os.path.join(RETRIEVER_HOME_DIR, "retriever_recipes_path.txt"), "w+") as f:
        f.write(retriever_recipes_path)
