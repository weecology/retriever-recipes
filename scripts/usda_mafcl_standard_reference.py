#retriever
# Data types for the tables are included in the zip

import csv
import os

from pkg_resources import parse_version
from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw
except ImportError:
    from retriever import open_fr, open_fw, VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "Nutrient Data Laboratory. USDA National Nutrient Database for Standard Reference, Release 28 "
        self.name = "usda-mafcl-standard-reference"
        self.retriever_minimum_version = "2.1.dev"
        self.urls = {
            "full_version": "https://www.ars.usda.gov/ARSUserFiles/80400535/DATA/SR/sr28/dnload/sr28asc.zip",
            "abbreviated_version": "https://www.ars.usda.gov/ARSUserFiles/80400535/DATA/SR/sr28/dnload/sr28abbr.zip",
        }
        self.version = "1.0.0"
        self.ref = "https://www.ars.usda.gov/northeast-area/beltsville-md-bhnrc/beltsville-human-nutrition-research-center/methods-and-application-of-food-composition-laboratory/mafcl-site-pages/sr17-sr28/"
        self.citation = "US Department of Agriculture, Agricultural Research Service. 2016. Nutrient Data Laboratory. USDA National Nutrient Database for Standard Reference, Release 28 (Slightly revised). Version Current: May 2016. http://www.ars.usda.gov/nea/bhnrc/mafcl"
        self.description = "The dataset contains nutrient data for Standard Reference"
        self.keywords = ["Nutrient", "Food", "Agriculture"]
        self.encoding = "utf-8"
        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine

        # Download both full and abbreviated versions and extract the data files
        abbrev_version = ["ABBREV.txt"]
        full_version = [
            "DERIV_CD.txt", "FOOTNOTE.txt", "NUTR_DEF.txt", "WEIGHT.txt", "DATA_SRC.txt",
            "FD_GROUP.txt", "LANGDESC.txt", "NUT_DATA.txt", "DATSRCLN.txt",
            "FOOD_DES.txt", "LANGUAL.txt", "SRC_CD.txt"
        ]

        self.engine.download_files_from_archive(
            self.urls["full_version"], archive_type="zip", file_names=full_version
        )
        self.engine.download_files_from_archive(
            self.urls["abbreviated_version"],
            archive_type="zip",
            file_names=abbrev_version,
        )

        # Convert original txt to csv
        convert_to_csv(self.engine.format_data_dir())

        # FOOD_DES table
        new_file_name = "food_des.csv"
        table = Table("food_des", delimiter=",", header_rows=0)
        table.columns = [
            ("ndb_no", ("int",)),
            ("fdgrp_cd", ("int",)),
            ("long_desc", ("char", "205")),
            ("shrt_desc", ("char", "65")),
            ("comname", ("char", "105")),
            ("manufacname", ("char", "70")),
            ("survey", ("char", "1")),
            ("ref_desc", ("char", "140")),
            ("refuse", ("double",)),
            ("sciname", ("char", "67")),
            ("n_factor", ("double",)),
            ("pro_factor", ("double",)),
            ("fat_factor", ("double",)),
            ("cho_factor", ("double",)),
        ]
        self.create_and_install(new_file_name, table)

        # FdGrp_Cd table
        new_file_name = "fd_group.csv"
        table = Table("fd_group", delimiter=",", header_rows=0)
        table.columns = [("fdgrp_cd", ("int",)), ("fdgrp_desc", ("char", "65"))]
        self.create_and_install(new_file_name, table)

        # LANGUAL table
        new_file_name = "langual.csv"
        table = Table("langual", delimiter=",", header_rows=0)
        table.columns = [("ndb_no", ("int",)), ("factor_code", ("char", "5"))]
        self.create_and_install(new_file_name, table)

        # LANGDESC Table
        new_file_name = "langdesc.csv"
        table = Table("langdesc", delimiter=",", header_rows=0)
        table.columns = [
            ("factor_code", ("char", "5")),
            ("description", ("char", "145")),
        ]
        self.create_and_install(new_file_name, table)

        # NUT_DATA table
        new_file_name = "nut_data.csv"
        missingValues = [
            "Unnamed: 6", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9", "Unnamed: 10",
            "Unnamed: 11", "Unnamed: 12", "Unnamed: 13", "Unnamed: 14", "Unnamed: 15",
            "Unnamed: 17"
        ]
        table = Table(
            "nut_data",
            delimiter=",",
            header_rows=0,
            missingValues=missingValues,
            do_not_bulk_insert=True,
        )
        table.columns = [
            ("ndb_no", ("int",)),
            ("nutr_no", ("int",)),
            ("nutr_val", ("double",)),
            ("num_data_pts", ("int",)),
            ("std_error", ("double",)),
            ("src_cd", ("int",)),
            ("deriv_cd", ("char", "12")),
            ("ref_ndb_no", ("double",)),
            ("add_nutr_mark", ("char", "12")),
            ("num_studies", ("double",)),
            ("min", ("double",)),
            ("max", ("double",)),
            ("df", ("double",)),
            ("low_eb", ("double",)),
            ("up_eb", ("double",)),
            ("stat_cmt", ("char", "12")),
            ("addmod_date", ("char", "12")),
            ("cc", ("char", "12")),
        ]
        self.create_and_install(new_file_name, table)

        # NUTR_DEF table
        new_file_name = "nutr_def.csv"
        table = Table("nutr_def", delimiter=",", header_rows=0)
        table.columns = [
            ("nutr_no", ("int",)),
            ("units", ("char", "10")),
            ("tagname", ("char", "25")),
            ("nutrdesc", ("char", "60")),
            ("num_dec", ("int",)),
            ("sr_order", ("int",)),
        ]
        self.create_and_install(new_file_name, table)

        # SRC_CD table
        new_file_name = "src_cd.csv"
        table = Table("src_cd", delimiter=",", header_rows=0)
        table.columns = [("src_cd", ("int",)), ("srccd_desc", ("char", "65"))]
        self.create_and_install(new_file_name, table)

        # DERIV_CD table
        new_file_name = "deriv_cd.csv"
        table = Table("deriv_cd", delimiter=",", header_rows=0)
        table.columns = [("deriv_cd", ("char", "5")), ("deriv_desc", ("char", "130"))]
        self.create_and_install(new_file_name, table)

        # WEIGHT table
        new_file_name = "weight.csv"
        table = Table(
            "weight",
            delimiter=",",
            header_rows=0,
            missingValues=["Unnamed: 5", "Unnamed: 6"],
        )
        table.columns = [
            ("ndb_no", ("int",)),
            ("seq", ("int",)),
            ("amount", ("double",)),
            ("msre_desc", ("char", "130")),
            ("gm_wgt", ("double",)),
            ("num_data_pts", ("double",)),
            ("std_dev", ("double",)),
        ]
        self.create_and_install(new_file_name, table)

        # FOOTNOTE table
        new_file_name = "footnote.csv"
        table = Table(
            "footnote", delimiter=",", header_rows=0, missingValues=["Unnamed: 3"]
        )
        table.columns = [
            ("ndb_no", ("int",)),
            ("footnt_no", ("int",)),
            ("footnt_typ", ("char", "2")),
            ("nutr_no", ("double",)),
            ("footnt_txt", ("char", "200")),
        ]
        self.create_and_install(new_file_name, table)

        # DATSRCLN table
        new_file_name = "datsrcln.csv"
        table = Table("datsrcln", delimiter=",", header_rows=0)
        table.columns = [
            ("ndb_no", ("int",)),
            ("nutr_no", ("int",)),
            ("datasrc_id", ("char", "7")),
        ]

        self.create_and_install(new_file_name, table)

        # DATA_SRC table
        new_file_name = "data_src.csv"
        table = Table("data_src", delimiter=",", header_rows=0)
        table.columns = [
            ("datasrc_id", ("char", "7")),
            ("authors", ("char", "257")),
            ("title", ("char", "257")),
            ("year", ("char", "5")),
            ("journal", ("char", "137")),
            ("vol_city", ("char", "17")),
            ("issue_state", ("char", "5")),
            ("start_page", ("char", "5")),
            ("end_page", ("char", "5")),
        ]
        self.create_and_install(new_file_name, table)

        # ABBREV table
        new_file_name = "abbrev.csv"
        table = Table("abbrev", delimiter=",", header_rows=0)
        table.columns = [
            ("ndb_no", ("char", "7")),
            ("shrt_desc", ("char", "60")),
            ("water", ("double",)),
            ("energ_kcal", ("int",)),
            ("protein", ("double",)),
            ("lipid_tot", ("double",)),
            ("ash", ("double",)),
            ("carbohydrt", ("double",)),
            ("fiber_td", ("double",)),
            ("sugar_tot", ("char", "6")),
            ("calcium", ("int",)),
            ("iron", ("double",)),
            ("magnesium", ("int",)),
            ("phosphorus", ("int",)),
            ("potassium", ("int",)),
            ("sodium", ("int",)),
            ("zinc", ("double",)),
            ("copper", ("double",)),
            ("manganese", ("double",)),
            ("selenium", ("double",)),
            ("vit_c", ("double",)),
            ("thiamin", ("double",)),
            ("riboflavin", ("double",)),
            ("niacin", ("double",)),
            ("panto_acid", ("double",)),
            ("vit_b6", ("double",)),
            ("folate_tot", ("int",)),
            ("folic_acid", ("int",)),
            ("food_folate", ("int",)),
            ("folate_dfe", ("int",)),
            ("choline_tot", ("double",)),
            ("vit_b12", ("double",)),
            ("vit_a_iu", ("int",)),
            ("vit_a_rae", ("int",)),
            ("retinol", ("int",)),
            ("alpha_carot", ("int",)),
            ("beta_carot", ("int",)),
            ("beta_crypt", ("int",)),
            ("lycopene", ("int",)),
            ("lut_zea", ("int",)),
            ("vit_e", ("double",)),
            ("vit_d_mcg", ("double",)),
            ("vit_d_iu", ("int",)),
            ("vit_k", ("double",)),
            ("fa_sat", ("double",)),
            ("fa_mono", ("double",)),
            ("fa_poly", ("double",)),
            ("cholestrl", ("int",)),
            ("gmwt_1", ("double",)),
            ("gmwt_desc1", ("char", "80")),
            ("gmwt_2", ("double",)),
            ("gmwt_desc2", ("char", "80")),
            ("refuse_pct", ("int",)),
        ]
        self.create_and_install(new_file_name, table)

    def create_and_install(self, new_file_name, table):
        data_path = self.engine.format_filename(new_file_name)
        self.engine.auto_create_table(table, filename=new_file_name)
        self.engine.insert_data_from_file(data_path)


def convert_to_csv(dir_name):
    """Change the file delimiter to comma delimiter"""
    for file_name in os.listdir(dir_name):
        file_path = os.path.join(dir_name, file_name)
        if file_path.endswith(".txt"):
            csv_file_name = file_name.replace(".txt", ".csv").lower()
            output_file = os.path.join(dir_name, csv_file_name)
            with open_fr(file_path, encoding="latin-1") as read_object, open_fw(
                output_file
            ) as outputfw:
                fr = csv.reader(read_object, delimiter="^", quotechar="~")
                fw = csv.writer(outputfw, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                for line in fr:
                    if line:
                        fw.writerow(line)
            # delete the text files
            os.remove(file_path)


SCRIPT = main()
