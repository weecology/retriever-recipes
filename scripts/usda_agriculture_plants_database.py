#retriever
from __future__ import absolute_import
from __future__ import print_function

import csv

from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fw, open_csvw, to_str, open_fr
    except ImportError:
        from retriever.lib.scripts import open_fw, open_csvw, to_str, open_fr
except ImportError:
    from retriever import HOME_DIR, open_fr, open_fw, open_csvw, to_str, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "U.S. Department of Agriculture's PLANTS Database"
        self.name = "usda-agriculture-plants-database"
        self.retriever_minimum_version = "2.1.dev"
        self.version = "1.0.0"
        self.ref = "https://plants.sc.egov.usda.gov/download.html"
        self.citation = ""
        self.description = "U.S. Department of Agriculture's PLANTS Database"
        self.keywords = ["plants", "agriculture"]
        self.encoding = "latin-1"

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # Complete Plants Checklist
        file_name = "complete_plant_checklist.csv"
        table_name = "complete_plant_checklist"
        complete_plant_url = "https://plants.sc.egov.usda.gov/java/downloadData?fileName=plantlst.txt&static=true"
        self.engine.download_file(complete_plant_url, filename=file_name)
        data_path = self.engine.format_filename(file_name)
        table = Table(table_name, delimiter=",")
        table.columns = [
            ("symbol", ("char", "7")),
            ("synonym_symbol", ("char", "7")),
            ("scientific_name_with_author", ("char", "183")),
            ("common_name", ("char", "42")),
            ("family", ("char", "30")),
        ]
        self.engine.auto_create_table(table, filename=file_name)
        self.engine.insert_data_from_file(data_path)

        # Symbols for Unknown Plants
        file_name = "symbols_unknown_plants.csv"
        table_name = "unknown_plants"
        unknown_plants_url = "https://plants.sc.egov.usda.gov/Data/unknown_plants.txt"
        self.engine.download_file(unknown_plants_url, filename=file_name)
        data_path = self.engine.format_filename(file_name)
        table = Table(table_name, delimiter=",")
        table.columns = [("symbol", ("char", "7")),
                         ("common_name", ("char", "56"))]
        self.engine.auto_create_table(table, filename=file_name)
        self.engine.insert_data_from_file(data_path)

        # State PLANTS Checklist
        base_url = "https://plants.sc.egov.usda.gov/"
        state_plant_checklist_base_url = "{base}java/stateDownload?statefips={id}"
        state_plant_checklist_file = "all_state_plant_checklist.csv"
        table_name = "state_plant_checklist"
        state_plant_checklist = [
            ("US01", "Alabama", "US"),
            ("US02", "Alaska", "US"),
            ("US05", "Arkansas", "US"),
            ("US04", "Arizona", "US"),
            ("US06", "California", "US"),
            ("US08", "Colorado", "US"),
            ("US09", "Connecticut", "US"),
            ("US10", "Delaware", "US"),
            ("US11", "District of Columbia", "US"),
            ("US12", "Florida", "US"),
            ("US13", "Georgia", "US"),
            ("US15", "Hawaii", "US"),
            ("US16", "Idaho", "US"),
            ("US17", "Illinois", "US"),
            ("US18", "Indiana", "US"),
            ("US19", "Iowa", "US"),
            ("US20", "Kansas", "US"),
            ("US21", "Kentucky", "US"),
            ("US22", "Louisiana", "US"),
            ("US23", "Maine", "US"),
            ("US24", "Maryland", "US"),
            ("US25", "Massachusetts", "US"),
            ("US26", "Michigan", "US"),
            ("US27", "Minnesota", "US"),
            ("US28", "Mississippi", "US"),
            ("US29", "Missouri", "US"),
            ("US30", "Montana", "US"),
            ("US31", "Nebraska", "US"),
            ("US32", "Nevada", "US"),
            ("US33", "New Hampshire", "US"),
            ("US34", "New Jersey", "US"),
            ("US35", "New Mexico", "US"),
            ("US36", "New York", "US"),
            ("US37", "North Carolina", "US"),
            ("US38", "North Dakota", "US"),
            ("US39", "Ohio", "US"),
            ("US40", "Oklahoma", "US"),
            ("US41", "Oregon", "US"),
            ("US42", "Pennsylvania", "US"),
            ("US44", "Rhode Island", "US"),
            ("US45", "South Carolina", "US"),
            ("US46", "South Dakota", "US"),
            ("US47", "Tennessee", "US"),
            ("US48", "Texas", "US"),
            ("US49", "Utah", "US"),
            ("US50", "Vermont", "US"),
            ("US51", "Virginia", "US"),
            ("US53", "Washington", "US"),
            ("US54", "West Virginia", "US"),
            ("US55", "Wisconsin", "US"),
            ("US56", "Wyoming", "US"),
            ("US72", "Puerto Rico", "US"),
            ("US78", "Virgin Islands", "US"),
            ("CA01", "Alberta", "Canada"),
            ("CA02", "British Columbia", "Canada"),
            ("CA03", "Manitoba", "Canada"),
            ("CA04", "New Brunswick", "Canada"),
            ("CALB", "Labrador", "Canada"),
            ("CANF", "Newfoundland", "Canada"),
            ("CA13", "Northwest Territories", "Canada"),
            ("CA07", "Nova Scotia", "Canada"),
            ("CA14", "Nunavut", "Canada"),
            ("CA08", "Ontario", "Canada"),
            ("CA09", "Prince Edward Island", "Canada"),
            ("CA10", "Québec", "Canada"),
            ("CA11", "Saskatchewan", "Canada"),
            ("CA12", "Yukon", "Canada"),
            ("GL", "Greenland", "Denmark"),
            ("SB", "St. Pierre and Miquelon", "France"),
        ]

        with open_fw(engine.format_filename(state_plant_checklist_file)) as write_object:
            csv_writer = open_csvw(write_object)
            for state_info in state_plant_checklist:
                file_name = state_info[1].replace(".", "").replace(" ", "_").lower() + ".csv"
                file_name = "old_state_plant_checklist_" + file_name
                state_url = state_plant_checklist_base_url.format(base=base_url, id=state_info[0])
                self.engine.download_file(state_url, filename=file_name)
                with open_fr(engine.format_filename(file_name)) as read_object:
                    # Read state file and only write the data minus header
                    next(read_object)
                    for row in csv.reader(read_object, delimiter=","):
                        csv_writer.writerow([state_info[2]] + [state_info[1]] + row)

        data_path = self.engine.format_filename(state_plant_checklist_file)
        table = Table(table_name, delimiter=",", header_rows=0)
        table.columns = [
            ("country", ("char", "7")),
            ("state", ("char", "23")),
            ("symbol", ("char", "7")),
            ("synonym_symbol", ("char", "7")),
            ("scientific_name_with_author", ("char", "183")),
            ("national_common_name", ("char", "42")),
            ("family", ("char", "17")),
        ]
        self.engine.auto_create_table(table, filename=state_plant_checklist_file)
        self.engine.insert_data_from_file(data_path)

        # NRCS State GSAT Lists
        base_url = "https://www.plants.usda.gov/"
        nrcs_state_gsat_base_url = "{base}java/gsatDownload?gsatid={id}"
        nrcs_state_gsat_file = "all_nrcs_state_gsat.csv"
        table_name = "nrcs_state_gsat"
        nrcs_state_gsat = [
            ("Alabama", "2"),
            ("Alaska", ""),
            ("Arkansas", ""),
            ("Arizona", "2"),
            ("California", ""),
            ("Colorado", ""),
            ("Connecticut", ""),
            ("Delaware", ""),
            ("Florida", ""),
            ("Georgia", ""),
            ("Hawaii", ""),
            ("Idaho", "9"),
            ("Illinois", ""),
            ("Indiana", ""),
            ("Iowa ", ""),
            ("Kansas", "6"),
            ("Kentucky", ""),
            ("Louisiana", "16"),
            ("Maine", ""),
            ("Maryland", ""),
            ("Massachusetts", ""),
            ("Michigan", ""),
            ("Minnesota", "11"),
            ("Mississippi", ""),
            ("Missouri", "14"),
            ("Montana", ""),
            ("Nebraska", "17"),
            ("Nevada", "4"),
            ("New Hampshire", ""),
            ("New Jersey ", ""),
            ("New Mexico", "1"),
            ("New York", ""),
            ("Noth Carolina", ""),
            ("North Dakota", "5"),
            ("Ohio", ""),
            ("Oklahoma", "12"),
            ("Oregon", "3"),
            ("Pennsylvania", "15"),
            ("Rhode Island", ""),
            ("South Carolina", ""),
            ("South Dakota", "7"),
            ("Tennessee", ""),
            ("Texas", "13"),
            ("Utah", ""),
            ("Vermont ", ""),
            ("Virginia", ""),
            ("Washington", "8"),
            ("West Virginia", ""),
            ("Wisconsin", ""),
            ("Wyoming", "10"),
        ]

        with open_fw(engine.format_filename(nrcs_state_gsat_file)) as write_object:
            for state_info in nrcs_state_gsat:
                if state_info[1]:
                    # skip states with no data ("state", ""),
                    file_name = state_info[0].replace(" ", "_").replace(".", "").lower() + ".csv"
                    file_name = "old_nrcs_state_gsat_" + file_name
                    state_url = nrcs_state_gsat_base_url.format(base=base_url, id=state_info[1])
                    self.engine.download_file(state_url, filename=file_name)
                    with open_fr(engine.format_filename(file_name)) as read_object:
                        # Read state file and only write the data minus header
                        next(read_object)
                        state_quoted = '"{state}",'.format(state=state_info[0])
                        for line in read_object:
                            write_object.write(state_quoted + line)

        data_path = self.engine.format_filename(nrcs_state_gsat_file)
        table = Table(table_name, delimiter=",", header_rows=0)
        table.columns = [
            ("state", ("char", "12")),
            ("symbol", ("char", "7")),
            ("scientific_name_with_author", ("char", "183")),
            ("gsat_common_name", ("char", "93")),
        ]
        self.engine.auto_create_table(table, filename=nrcs_state_gsat_file)
        self.engine.insert_data_from_file(data_path)

        base_url = "https://plants.sc.egov.usda.gov/"
        nrcs_state_plant_lists_url = "{base}java/nrcsStateDownload?statefips={id}"
        nrcs_state_plant_file = "all_nrcs_state_plant.csv"
        table_name = "nrcs_state_plant"
        nrcs_state_plant_lists = [
            ("01", "Alabama"),
            ("02", "Alaska"),
            ("05", "Arkansas"),
            ("04", "Arizona"),
            ("06", "California"),
            ("08", "Colorado"),
            ("09", "Connecticut"),
            ("10", "Delaware"),
            ("12", "Florida"),
            ("13", "Georgia"),
            ("15", "Hawaii"),
            ("16", "Idaho"),
            ("17", "Illinois"),
            ("18", "Indiana"),
            ("19", "Iowa"),
            ("20", "Kansas"),
            ("21", "Kentucky"),
            ("22", "Louisiana"),
            ("23", "Maine"),
            ("24", "Maryland"),
            ("25", "Massachusetts"),
            ("26", "Michigan"),
            ("27", "Minnesota"),
            ("28", "Mississippi"),
            ("29", "Missouri"),
            ("30", "Montana"),
            ("31", "Nebraska"),
            ("32", "Nevada"),
            ("33", "New Hampshire"),
            ("34", "New Jersey"),
            ("35", "New Mexico"),
            ("36", "New York"),
            ("37", "North Carolina"),
            ("38", "North Dakota"),
            ("39", "Ohio"),
            ("40", "Oklahoma"),
            ("41", "Oregon"),
            ("42", "Pennsylvania"),
            ("44", "Rhode Island"),
            ("45", "South Carolina"),
            ("46", "South Dakota"),
            ("47", "Tennessee"),
            ("48", "Texas"),
            ("49", "Utah"),
            ("50", "Vermont"),
            ("51", "Virginia"),
            ("53", "Washington"),
            ("54", "West Virginia"),
            ("55", "Wisconsin"),
            ("56", "Wyoming"),
            ("72", "Puerto Rico"),
            ("78", "Virgin Islands"),
        ]

        with open_fw(engine.format_filename(nrcs_state_plant_file)) as write_object:
            for state_info in nrcs_state_plant_lists:
                file_name = state_info[1].replace(" ", "_").replace(".", "").lower() + ".csv"
                file_name = "old_nrcs_state_plant_" + file_name
                state_url = nrcs_state_plant_lists_url.format(base=base_url, id=state_info[0])
                self.engine.download_file(state_url, filename=file_name)
                with open_fr(engine.format_filename(file_name)) as read_object:
                    # Read state file and only write the data minus header
                    next(read_object)
                    state_quoted = '"{state}",'.format(state=state_info[1])
                    for line in read_object:
                        write_object.write(state_quoted + line)

        data_path = self.engine.format_filename(nrcs_state_plant_file)
        table = Table(table_name, delimiter=",", header_rows=0)
        table.columns = [
            ("state", ("char", "17")),
            ("symbol", ("char", "7")),
            ("synonym_symbol", ("char", "7")),
            ("scientific_name_with_author", ("char", "183")),
            ("state_common_name", ("char", "42")),
            ("family", ("char", "17")),
        ]
        self.engine.auto_create_table(table, filename=nrcs_state_plant_file)
        self.engine.insert_data_from_file(data_path)


SCRIPT = main()
