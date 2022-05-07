# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
from datetime import datetime

from astropy import units as u
from astropy.coordinates import SkyCoord

def convertData():

    records = []
    
    fp = open("dasch_data.json", "r", encoding="utf-8")
    dasch = json.load(fp)

    prev = "a0"

    for row in dasch["data"]:

        coords = SkyCoord(str(row[4]+" "+row[5]), unit=(u.hourangle, u.deg))
        decira = coords.ra.deg
        decidec = coords.dec.deg

        current = row[0]+str(row[1])

        if current != prev:

            newrecord = {
                "identifier" : row[0]+str(row[1]),
                "archive": "hco",
                "plate_info" : {                    
                    "series" : row[0],
                    "number" : row[1],
                },
                "exposure_info" : [
                    {   
                        "number": row[2],
                        "duration" : {
                            "value" : row[3],
                            "unit" : "min",
                        },
                        "ra" : row[4],
                        "ra_deg" : decira,
                        "dec" : row[5],
                        "dec_deg" : decidec,
                        "jd2000" : row[6]
                    },
                ]
            }

            records.append(newrecord)

        else:
            newrecord["exposure_info"].append({
                "number": row[2],
                "duration" : {
                    "value" : row[3],
                    "unit" : "min",
                },
                "ra" : row[4],
                "ra_deg" : decira,
                "dec" : row[5],
                "dec_deg" : decidec,
                "jd2000" : row[6]
            })

            records = records[:-1]
            records.append(newrecord)

        prev = row[0]+str(row[1])


    with open('dasch_data_output.json', 'w', encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
