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

    with open('sampledata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        records = []

        for row in csv_reader:
            #print(row)

            #original = row.copy()

            if row[0] == "DASCH":

                decira = convertRA(row[3])
                decidec = convertDEC(row[4])

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "plate_info" : {                    
                        "series" : " ".join(re.findall("[a-zA-Z]+", row[1])),
                        "number" : " ".join(re.findall("[0-9]+", row[1])),
                        "plate_class" : row[2],
                    },
                    "exposure_info" : [
                        {   
                            "number": 0,
                            "time" : {
                                "value" : row[8],
                                "unit" : "min",
                            },
                            "ra" : row[3],
                            "ra_deg" : decira,
                            "dec" : row[4],
                            "dec_deg" : decidec,
                            "date" : {
                                "value" : row[13],
                                "unit" : "JD2000",
                            },
                        },
                    ],
                    "obs_info" : {
                        "observatory" : row[19],    
                        "latitude" : row[21],
                        "longitude" : row[22],
                        "telescope" : row[20],
                        "aperature" : {
                            "value" : row[23],
                            "unit" : "m",
                        },
                        "scale" : {
                            "value" : row[24],
                            "unit" : "arcsec/nm"
                        },
                    }
                }
        
                records.append(newrecord)


            elif row[0] == "Hamburg":

                decira = convertRA(row[3])
                decidec = convertDEC(row[4])

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "plate_info" : {
                        "multi" : row[7],
                        "emulsion" : row[16],
                    },

                    "exposure_info" : [
                        {   
                            "number": 0,
                            "ra" : row[3],
                            "ra_deg" : decira,
                            "dec" : row[4],
                            "dec_deg" : decidec,
                            "time" : {
                                "value" : row[8],
                                "unit" : "min",
                            },
                            "date" : {
                                "value" : row[10],
                                "unit" : "JD2000",
                            },
                        }
                    ],
                    "obs_info" : {
                        "telescope" : row[20]
                    }
                }
                
                records.append(newrecord)
        
        with open('data_sample.json', 'w') as f:
            json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
