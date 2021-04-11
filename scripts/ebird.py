# -*- coding: UTF-8 -*-
#retriever

import os
import sys
from tqdm import tqdm

from retriever.lib.models import Table
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION

    try:
        from retriever.lib.tools import open_fr, open_fw, open_csvw
    except ImportError:
        from retriever.lib.scripts import open_fr, open_fw, open_csvw
except ImportError:
    from retriever import open_fr, open_fw, VERSION, open_csvw


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "eBird Observation Dataset"
        self.name = "ebird"
        self.encoding = "utf-8"
        self.retriever_minimum_version = "2.1.dev"
        self.urls = {
            "ebird_data": "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/EOD_CLO_2016.csv.gz"
        }
        self.version = "2.0.0"
        self.ref = "https://ebird.org/home"
        self.citation = (
            "Sullivan, B.L., C.L. Wood, M.J. Iliff, R.E. Bonney, D. Fink, "
            "and S. Kelling. 2009. eBird: a citizen-based bird observation "
            "network in the biological sciences. "
            "Biological Conservation 142: 2282-2292."
        )
        self.description = (
            "A collection of observations from birders through "
            "portals managed and maintained by local partner "
            "conservation organizations"
        )
        self.keywords = [
            "bird distribution",
            "abundance",
            "habitat",
            "trends",
            "bird",
            "avian",
            "observation",
            "international",
            "location", "latitude",
            "longitude",
            "date",
            "spatial",
        ]

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)

        original_file_name = "EOD_CLO_2016.csv"
        new_data_file = "new_EOD_CLO_2016.csv"

        print("Extraction of ~ 100 gb raw data, this may take some minutes..")
        self.engine.download_files_from_archive(
            self.urls["ebird_data"],
            [original_file_name],
            archive_type="gz", archive_name="EOD_CLO_2016.csv.gz"
        )
        print("Done with extraction. preprocessing data for installation...")
        sys.stdout.flush()
        number_of_records = 361429888
        table = Table("bird_observations",
                      delimiter=",",
                      do_not_bulk_insert=True,
                      csv_extend_size=True,
                      number_of_records=number_of_records)
        table.columns = [
            ("basisofrecord", ("char", 16)),
            ("institutioncode", ("char", 3)),
            ("collectioncode", ("char", 14)),
            ("catalognumber", ("char", 12)),
            ("occurrenceid", ("char", 43)),
            ("recordedby", ("char", 10)),
            ("year", ("int",)),
            ("month", ("int",)),
            ("day", ("int",)),
            ("publishingcountry", ("char", 2)),
            ("country", ("char", 43)),
            ("stateprovince", ("char", 48)),
            ("county", ("char", 40)),
            ("decimallatitude", ("double",)),
            ("decimallongitude", ("double",)),
            ("locality", ("char", 220)),
            ("kingdom", ("char", 8)),
            ("phylum", ("char", 8)),
            ("classes", ("char", 4)),
            ("ordered", ("char", 19)),
            ("family", ("char", 18)),
            ("genus", ("char", 18)),
            ("specificepithet", ("char", 21)),
            ("scientificname", ("char", 33)),
            ("vernacularname", ("char", 33)),
            ("individualcount", ("int",)),
        ]
        self.engine.table = table
        self.engine.create_table()

        old_path = self.engine.format_filename(original_file_name)
        new_path = self.engine.format_filename(new_data_file)

        # Clean up the data and enforce encording
        p_desc = 'Cleaning source file {}'.format(original_file_name)
        pbar = tqdm(desc=p_desc, total=number_of_records, unit='rows')

        csv_file = open_fw(new_path)
        csv_writer = open_csvw(csv_file)

        with open_fr(old_path, encoding="utf-8") as infile:
            for line in infile:
                if line:
                    k = bytes(line.strip(), 'utf-8').decode("utf-8")
                    csv_writer.writerow(k.split(","))
                    pbar.update(1)
        if csv_file:
            csv_file.close()

        # Remove original file to save space(~100gb)
        os.remove(old_path)
        sys.stdout.flush()
        self.engine.insert_data_from_file(new_path)


SCRIPT = main()
