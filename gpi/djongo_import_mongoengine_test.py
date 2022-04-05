import json
import pymongo

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)

# First define the database name
dbname = my_client['plates']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["plates_glassplates"]

f = open('data_mm.json', "r", encoding="utf-8") # load up json data
data = json.load(f)
f.close()

# Insert the documents
collection_name.insert_many(data)

# for x in data:
#     collection_name.update_one({"identifier": x["identifier"]}, {"$set": x}, upsert=True)

print("data inserted")
