# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
import datetime

from astropy import units as u
from astropy.coordinates import SkyCoord


def convertData():


    records = []
    
    fp = open("mariamitchell_data.txt", "r", encoding="utf-8")

    mmap = (fp.read()).splitlines()

    for row in mmap:
        data = row.split(",")
        print (data)

        try:
            dates = data[5].split("_")
            x = datetime.datetime(1900+int(dates[0]), int(dates[1]), int(dates[2]))    
            thedate = x.strftime('%B %d, %Y')
        except:
            thedate = ""           

        if "." in data[2]:
            pieces = data[2].split(".")
            mins = pieces[0]
            secs = pieces[1]*60
            coords = SkyCoord(str(data[1]+":"+pieces[0]+":"+pieces[1]+" 0"), unit=(u.hourangle, u.deg))
        else:
            coords = SkyCoord(str(data[1]+":"+data[2]+":00 0"), unit=(u.hourangle, u.deg))
        
        decira = coords.ra.deg
        #decidec = coords.dec.deg


        if data[3] != "":
            deg = float(data[3])
        else:
            deg = None

        if data[6] == "":
            jd = None 
        elif data[6][0:2] == "24":
            jd = float(data[6])
        else: 
            jd = float("24"+data[6])

        newrecord = {
            "identifier" : data[0],
            "archive": "mmoapc",
            "obs_info" : {
                "instrument" : "7.5-inch Cooke/Clark refractor",
                "observatory" : "Maria Mitchell Observatory"      
            },
        }

        plate_info = {}
        exposure_info = [
            {
            "number": 0,
            "ra" : data[1]+":"+data[2]+":00",
            "ra_deg" : decira,
            "dec" : deg,
            "dec_deg" : deg
            }
        ]
        if data[7] != "":
            plate_info["emulsion"] = data[7]

        if data[8] != "":
            plate_info["notes"] = data[8]

        if data[5] != "":
            exposure_info[0]["calendar_date"] = thedate

        if data[6] != "":
            exposure_info[0]["jd2000"] = jd

        if data[4] != "":
            exposure_info[0]["duration"] = {
                "value" : data[4],
                "unit" : "min",
            }

        if plate_info != {}:
            newrecord["plate_info"] = plate_info

        if exposure_info != {}:
            newrecord["exposure_info"] = exposure_info   

        records.append(newrecord)


    with open('data_mm.json', 'w', encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
