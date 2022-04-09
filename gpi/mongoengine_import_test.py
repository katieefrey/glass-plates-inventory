import django
django.setup()

#from myapp.models import MyModel

import json
import pymongo

import mongoengine

# from main.secrets import *

# from main.settings import *

# from mongoengine import Document, EmbeddedDocument, fields


from plates.models import ExposureInfo, GlassPlates


f = open('data_mm.json', "r", encoding="utf-8") # load up json data
data = json.load(f)

for x in data:
    print (x["identifier"])
    print (x["repository"])

    ross = GlassPlates(identifier=x["identifier"], repository=x["repository"]).save()

f.close()




print("data inserted")
