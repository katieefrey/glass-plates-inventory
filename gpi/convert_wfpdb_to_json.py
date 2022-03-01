# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
from datetime import datetime

from wfpdb_data_sample import *


def convertData():


    records = []
    
    fp = open("wfpdb_data.json", "r")

    wfpdb = json.load(fp)

    for row in wfpdb["data"]:

        if row[20] == "":
            availnote = None 
        else:
            availnote = row[20]

        if row[8] == "":
            target = None 
        else:
            target = row[8]

        newrecord = {
            "identifier" : row[2],
            "repository": "WFPDB",
            "instrument" : (row[1]),            
            "method" : row[10],
            "exposures" : [
                {
                    "number": 0,
                    "ra" : row[3],
                    "ra_format" : "degrees",
                    "dec" : row[4],
                    "dec_format" : "degrees",
                    "coord_quality" : row[5],
                    "date" : row[6],
                    "date_epoch" : "JD2000",
                    "date_quality" : row[7],
                    "time" : row[11],
                    "time_unit" : "seconds",
                    "target" : target,
                    "target_type": row[9],
                }
            ],
            "emulsion" : row[12],
            "filter" : row[13],
            "band" : row [14],
            "width" : row[15],
            "height" : row[16],
            "width_unit" : "cm",
            "height_unit" : "cm",
            "observer" : row[17],
            "notes" : row[18],
            "quality" : row[19],
            "availability_note" : availnote,
            "digitization_note" : row[21]
        }

        records.append(newrecord)


    with open('data.json', 'w') as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
