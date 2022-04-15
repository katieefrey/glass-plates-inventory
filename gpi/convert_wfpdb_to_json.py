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
    
    fp = open("wfpdb_data.json", "r", encoding="utf-8")

    wfpdb = json.load(fp)

    for row in wfpdb["data"]:


        if row[3] != None:
            if ":" not in str(row[3]):
                decira = row[3]
                decidec = row[4]
            else:
                coords = SkyCoord(str(row[3]+" "+str(row[4])), unit=(u.hourangle, u.deg))
                decira = coords.ra.deg
                decidec = coords.dec.deg
        
        else:
            decira =  ""
            decidec = ""


        newrecord = {
            "identifier" : row[2],
            "archive": "wfpdb"
        }

        plate_info = {}
        exposure_dict = {}
        exposure_info = []
        obs_info = {}

        if row[12] != None:
            plate_info["emulsion"] = row[12]

        if row[10] != None:
            plate_info["type"] = row[10]

        if row[13] != None:
            plate_info["filter"] = row[13]

        if row[14] != None:
            plate_info["band"] = row[14]


        if row[15] != None:
            plate_info["width"] = {
                "value" : row[15],
                "unit" : "cm"
            }
        if row[16] != None:
            plate_info["height"] = {
                "value" : row[16],
                "unit" : "cm",
            }

        if row[17] != None:
            plate_info["observer"] = row[17]

        if row[18] != None:
            plate_info["notes"] = row[18]

        if row[19] != None:
            plate_info["quality"] = row[19]

        if row[20] != "":
            plate_info["availability_note"] = row[20]

        if row[21] != None:
            plate_info["digitization_note"] = row[21]

        if row[1] != "":
            obs_info["instrument"] = row[1]

        exposure_dict = {
            "number": 0
        }

        if row[3] != None:
            exposure_dict["ra"] = row[3]
            exposure_dict["ra_deg"] = decira

        if row[4] != None:
            exposure_dict["dec"] = row[4]
            exposure_dict["dec_deg"] = decidec

        if row[5] != None:
            exposure_dict["coord_quality"] = row[5]

        if row[6] != None:
            exposure_dict["jd2000"] = row[6]

        if row[7] != None:
            exposure_dict["date_quality"] = row[7]

        if row[11] != None:
            exposure_dict["duration"] = {
                "value" : row[11],
                "unit" : "sec",
            }

        if row[8] != None and row[8] != "":
            exposure_dict["target"] = row[8]
        
        if row[9] != None:
            exposure_dict["target_type"] = row[9]

        if exposure_dict != {}:
            exposure_info.append(exposure_dict)

        
        if plate_info != {}:
            newrecord["plate_info"] = plate_info

        if exposure_info != []:
            newrecord["exposure_info"] = exposure_info

        if obs_info != {}:
            newrecord["obs_info"] = obs_info


        records.append(newrecord)


    with open('wfpdb_data_output.json', 'w', encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
