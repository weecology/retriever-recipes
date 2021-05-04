"""Retriever script for direct download of data"""


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
        self.title = "Real-time decision-making during emergency disease outbreaks"
        self.name = "decision-making-during-outbreaks-uk"
        self.ref = "https://figshare.com/collections/Data_from_Real-time_decision-making_during_emergency_disease_outbreaks/4178165"
        self.urls = {"DMDE": "https://ndownloader.figshare.com/files/12523310"}
        self.citation = "Probert, William J. M.; Jewell, Chris P.; Werkman, Marleen; J. Fonnesbeck, Christopher; Goto,"\ 
                        "Yoshitaka; C. Runge, Michael; et al. (2018)"
        self.licenses = [{"name": "CC0-0.0"}]
        self.keywords = ['decision-making', 'UK','epidemics']
        self.retriever_minimum_version = "2.0.dev"
        self.version = "1.4.5"
        self.description = "These data include parameter estimates and simulation output for outbreak"\ 
                           "of foot-and-mouth disease (FMD): the outbreak in UK in 2001. Parameters are"\
                           " estimated at several time points throughout both outbreaks." \
                           "of several control interventions from these time points onwards was also performed and the" \
                           "simulated total number of culled livestock is recorded."

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

        # files are nested in another data folder
        # important files considered (parameters_uk.csv,simulation_output_uk.csv)
        # relevant files can be added in the same manner

        file_names = ["data/parameters_uk.csv",
                      "data/simulation_output_uk.csv"]
        engine.download_files_from_archive(self.urls["DMDE"], file_names)

        # creating data from parameters_uk.csv
        if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
            filename = "data/parameters_uk.csv"
            engine.auto_create_table(Table("parameters",
                                           cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))
        else:
            filename = "parameters_uk.csv"
            engine.auto_create_table(Table("parameters",
                                           cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))
        # creating methods from simulation_output_uk.csv

        if parse_version(VERSION).__str__() >= parse_version("2.1.dev").__str__():
            filename = "data/simulation_output_uk.csv"
            engine.auto_create_table(Table("output", cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))
        else:
            filename = "simulation_output_uk.csv"
            engine.auto_create_table(Table("output", cleanup=self.cleanup_func_table),
                                     filename=filename)
            engine.insert_data_from_file(engine.format_filename(filename))
      
        
        

SCRIPT = main()