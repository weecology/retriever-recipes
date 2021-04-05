"""Retriever script for direct download of data data"""

from __future__ import print_function
from pkg_resources import parse_version

import retriever
from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "West Nile virus in California, 2003–2018: A persistent threat"
        self.name = "west-nile-virus-in-ca"
        self.ref = "https://doi.org/10.1371/journal.pntd.0008841"
        self.urls = {"WNVC": "https://ndownloader.figshare.com/files/25525537"}
        self.citation = "Snyder, Robert E.; Feiszli, Tina; Foss, Leslie; Messenger, Sharon; Fang, Ying; Barker, Christopher M.;"\
                        "et al. (2020): West Nile virus in California, 2003–2018: A persistent threat."
        self.licenses = [{"name": "CC0-4.0"}]
        self.keywords = ['West Nile virus', 'U.S','Annual enzootic detection']
        self.retriever_minimum_version = "2.0.dev"
        self.version = "1.4.5"
        self.description = "Demographic characteristics of human West Nile virus (WNV)" \
                           "disease cases (n = 6,909) and asymptomatic infections (n = 730) reported to" \
                            "the California Department of Public Health, 2003–2018."

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(correct_invalid_value,
                                              nulls=['NA'])
        else:
            self.cleanup_func_table = Cleanup(correct_invalid_value,
                                              missing_values=['NA'])
            self.encoding = "latin-1"

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # files are nested in another baad_data folder
        # important files considered (baad_data.csv,baad_methods.csv)
        # relevant files can be added in the same manner

        file_names = ["table.csv"
                      ]
        engine.download_files_from_archive(self.urls["WNVC"], file_names)

        # creating data from baad_data.csv
        if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
            filename = "Table1.csv"
            engine.auto_create_table(Table("data",
                                           cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))
        else:
            filename = "Table1.csv"
            engine.auto_create_table(Table("data",
                                           cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))

        # creating methods from baad_methods.csv
        

SCRIPT = main()