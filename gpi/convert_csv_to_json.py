# standard lib packages
import sys
import os
import re
import os.path
import json
import csv
from datetime import datetime

def convertData():

    with open('sampledata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        records = []

        for row in csv_reader:
            #print(row)

            #original = row.copy()

            if row[0] == "DASCH":

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "series" : " ".join(re.findall("[a-zA-Z]+", row[1])),
                    "number" : " ".join(re.findall("[0-9]+", row[1])),
                    "plate_class" : row[2],
                    "exposures" : [
                        {   
                            "number": 0,
                            "time" : row[8],
                            "time_unit" : "minutes",
                            "ra" : row[3],
                            "ra_format" : "hms",
                            "dec" : row[4],
                            "dec_format": "daa",
                            "date" : row[13],
                            "date_epoch" : "JD2000",
                        },
                    ],
                    "observatory" : {
                        "name" : row[19],    
                        "latitude" : row[21],
                        "longitude" : row[22]
                    },
                    "telescope" : {
                        "name" : row[20],
                        "aperature" : row[23],
                        "aperature_unit" : "m",
                        "scale" : row[24],
                        "scale_unit" : "arcsec/nm"
                    }
                }
        
                records.append(newrecord)


            elif row[0] == "Hamburg":
                print("Hamburg")

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "exposures" : [
                        {   
                            "number": 0,
                            "ra" : row[3],
                            "ra_format" : "hms",
                            "dec" : row[4],
                            "dec_format": "daa",
                            "time" : row[8],
                            "time_unit" : "minutes",
                            "date" : row[10],
                            "date_epoch" : "JD2000",
                        }
                    ],
                    "multi" : row[7],
                    "emulsion" : row[16],
                    "telescope" : row[20]
                }
                
                records.append(newrecord)
        
        with open('data_sample.json', 'w') as f:
            json.dump(records, f, ensure_ascii=False)

if __name__ == "__main__":
    convertData()
