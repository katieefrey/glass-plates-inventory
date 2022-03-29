# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
import datetime


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
            thedate = "No Date"           

        decira = convertRA(data[1]+":"+data[2]+":00")
        #decidec = convertDEC(row[4])

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
            "repository": "mmoapc",
            "plate_info" : {
                "emulsion" : data[7],
                #"type" : row[10],
                #"filter" : row[13],
                #"band" : row[14],
                #"width" : {
                #    "value" : row[15],
                #    "unit" : "cm"
                #},
                #"height" : {
                #    "value" : row[16],
                #    "unit" : "cm",
                #},
                #"observer" : row[17],
                "notes" : data[8],
                #"quality" : row[19],
                #"availability_note" : availnote,
                #"digitization_note" : row[21]
            },
            "obs_info" : {
                "instrument" : "7.5-inch Cooke/Clark refractor",
                "observatory" : "Maria Mitchell Observatory"      
            },
            "exposure_info" : [
                {
                    "number": 0,
                    "ra" : data[1]+":"+data[2]+":00",
                    "ra_deg" : decira,
                    "dec" : deg,
                    "dec_deg" : deg,
                    #"coord_quality" : row[5],
                    "date" : {
                        "value" : jd,
                        "unit" : "JD2000",
                    },
                    "calendar_date" : thedate,
                    #"date_quality" : row[7],
                    "time" : {
                        "value" : data[4],
                        "unit" : "min",
                    },
                    #"target" : target,
                    #"target_type": row[9],
                }
            ]          
        }

        records.append(newrecord)


    with open('data_mm.json', 'w', encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
