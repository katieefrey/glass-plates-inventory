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
                #print("DASCH")            
                # word1 = " ".join(re.findall("[a-zA-Z]+", row[1]))
                # print(word1)
                # num = " ".join(re.findall("[0-9]+", row[1]))
                # print(num)
                #print (row[23])

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
                            "unit" : "minutes",
                            "center" : {
                                "ra" : {
                                "value" : row[3],
                                "format" : "hms"
                                },
                                "dec" : {
                                    "value" : row[4],
                                    "format": "daa"
                                },
                            },
                            "date" : {
                                "geocentric_date" : row[12],
                                "julian_date" : row[13],
                            },
                        },
                    ],
                    "observatory" : {
                        "name" : row[19],    
                        "location" : {
                            "latitude" : row[21],
                            "longitude" : row[22]
                        },
                    },
                    "telescope" : {
                        "name" : row[20],
                        "telescope_aperature" : {
                            "value" : row[23],
                            "unit" : "m"
                        },
                        "telescope_scale" : {
                            "value" : row[24],
                            "unit" : "arcsec/nm"
                        }
                    }
                }
        
                records.append(newrecord)


            elif row[0] == "Hamburg":
                print("Hamburg")

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "date" : row[10],
                    "center" : {
                        "ra" : {
                        "value" : row[3],
                        "format" : "hms" 
                        },
                        "dec" : {
                            "value" : row[4],
                            "format": "daa"
                        },
                    },
                    "exposure" : {
                        "time" : row[8],
                        "unit" : "minutes",
                    },
                    "multi_exposure" : row[7],
                    "emulsion" : row[16],
                    "telescope" : row[20]
                }
                
                records.append(newrecord)


            elif row[0] == "WFPDB" :
                print("WFPDB")

                newrecord = {
                    "identifier" : row[1],
                    "repository": row[0],
                    "instrument" : (row[1].split(" "))[0],
                    "number" : (row[1].split(" "))[1],

                    "center" : {
                        "ra" : {
                        "value" : row[5],
                        "format" : "degrees" 
                        },
                        "dec" : {
                            "value" : row[6],
                            "format": "degrees"
                        },
                    },
                    "exposure" : {   
                        "time" : row[9],
                        "unit" : "seconds",
                    },
                    "obs_epoch" : row[11],
                    "emulsion" : row[16],
                    "filter" : row[17],
                    "band" : row [18]
                }

                records.append(newrecord)


        output = json.dumps(records)
        print(output)

            


if __name__ == "__main__":
    convertData()
