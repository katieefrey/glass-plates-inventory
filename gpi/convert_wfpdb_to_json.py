# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
from datetime import datetime


def convertRA(input_value):
    if input_value and ":" in str(input_value):
        ra = input_value.split(":")
        if float(ra[0]) >= 0:
            output_value = float(ra[0]) + float(ra[1])/60
            if len(ra) == 3:
                output_value += float(ra[2])/3600
        else:
            output_value = float(ra[0]) - float(ra[1])/60
            if len(ra) == 3:
                output_value -= float(ra[2])/3600

        output_value = output_value*15
    elif input_value:
        output_value = input_value
    else:
        return None

    return round(output_value,4)


def convertDEC(input_value):
    if input_value and ":" in str(input_value):
        ra = input_value.split(":")
        if float(ra[0]) >= 0:
            output_value = float(ra[0]) + float(ra[1])/60
            if len(ra) == 3:
                output_value += float(ra[2])/3600
        else:
            output_value = float(ra[0]) - float(ra[1])/60
            if len(ra) == 3:
                output_value -= float(ra[2])/3600
    elif input_value:
        output_value = input_value
    else:
        return None

    return round(output_value,4)

def convertData():


    records = []
    
    fp = open("wfpdb_data.json", "r", encoding="utf-8")

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

        decira = convertRA(row[3])
        decidec = convertDEC(row[4])

        newrecord = {
            "identifier" : row[2],
            "repository": "WFPDB",
            "plate_info" : {
                "emulsion" : row[12],
                "type" : row[10],
                "filter" : row[13],
                "band" : row[14],
                "width" : {
                    "value" : row[15],
                    "unit" : "cm"
                },
                "height" : {
                    "value" : row[16],
                    "unit" : "cm",
                },
                "observer" : row[17],
                "notes" : row[18],
                "quality" : row[19],
                "availability_note" : availnote,
                "digitization_note" : row[21]
            },
            "obs_info" : {
                "instrument" : (row[1]),            
            },
            "exposure_info" : [
                {
                    "number": 0,
                    "ra" : row[3],
                    "ra_deg" : decira,
                    "dec" : row[4],
                    "dec_deg" : decidec,
                    "coord_quality" : row[5],
                    "date" : {
                        "value" : row[6],
                        "unit" : "JD2000",
                    },
                    "date_quality" : row[7],
                    "time" : {
                        "value" : row[11],
                        "unit" : "sec",
                    },
                    "target" : target,
                    "target_type": row[9],
                }
            ]          
        }

        records.append(newrecord)


    with open('data.json', 'w', encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
