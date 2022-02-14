# standard lib packages
import sys
import os
import os.path
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE','dasch.settings')

import django
django.setup()

from hco.models import Notebook, Page, Plate, PagePlate, Items


def add_Notebookdata(data1, data2, data3, data4):
    d, created = Notebook.objects.get_or_create(phaenum=data1, title=data2,xmlfile=data3, bibcode=data4)
    return d


def add_Images(data1, data2, data3, data4):

    notesbook = Notebook.objects.get(phaenum=data1)
    try:
        pg = Page.objects.get(notebook_id=notesbook.id, pgnum=data2,imgurl=data3)
        pg.zooid = data4
        pg.save()
        return pg
    except:
        d, created = Page.objects.get_or_create(notebook_id=notesbook.id, pgnum=data2,imgurl=data3, zooid=data4)
        return d

def add_Plate(data1, data2):

    try:
        d, created = Plate.objects.get_or_create(series=data1, number=data2)
        return d
    except ValueError:
        return "error"

def add_PagePlate(data1, data2):
    d, created = PagePlate.objects.get_or_create(pg=data1, plate=data2)

    return d


def addData(wr):

    with open('leavitt_2-3-2022.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            print(row)

            original = row.copy()

            row.pop(0)
            row.pop(0)

            phaedraid = row[0]
            anotebook = Items.objects.get(item_id=phaedraid)

            anotebook.title
            anotebook.bibcode

            row.pop(0)

            pgid = row[0]
            row.pop(0)

            zooid = row[0]
            row.pop(0)

            print(zooid)

            while("" in row):
                row.remove("")

            add_Notebookdata(phaedraid, anotebook.title, "NULL", anotebook.bibcode)
            page = add_Images(phaedraid, pgid, "NULL", zooid)

            for i in row:
                #print(i)
                try:
                    if i[0].isalpha():
                        if i[1].isnumeric():
                            plate = add_Plate(i[0],i[1:])
                        else:
                            # print(i)
                            # print (i[:2])
                            # print (i[2:])
                            plate = add_Plate(i[:2],i[2:])
                    else:
                        plate = "error"
                except:
                    plate = "error"


                if plate == "error":
                    wr.writerow(original)
                else:
                    add_PagePlate(page, plate)
        

def populate():

    with open('items.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            data1 = row[0]
            data2 = row[1]
            data3 = row[2]
            data4 = row[3]

            add_Notebookdata(data1, data2, data3, data4)

    folder = 'imgurls'

    for dirName, subdirList, fileList in os.walk(folder):

        for file in fileList:
            textfile = open(dirName+'/'+file, 'r')
            contents = textfile.read()
            lines = contents.splitlines()
            phaedraid = file[0:11]
            data1 = phaedraid

            for x in range(0,len(lines)):
                data2 = x+1
                data3 = lines[x]

                add_Images(data1, data2, data3)

    print ("finished")


if __name__ == "__main__":
    #populate()

    timestamp = datetime.now().strftime("%Y_%m%d_%H%M")
    resultFile = open("errors"+timestamp+".csv",'w', encoding='utf-8', newline='')
    wr = csv.writer(resultFile,quoting=csv.QUOTE_ALL)
    addData(wr)
    resultFile.close()