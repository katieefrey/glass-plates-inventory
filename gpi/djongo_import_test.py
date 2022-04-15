import json
import pymongo

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)

# First define the database name
dbname = my_client['plates']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["glass"]

f = open('hamburg_data_output.json', "r", encoding="utf-8") # load up json data
data = json.load(f)
f.close()

# Insert the documents
collection_name.insert_many(data)

# updating a whole section
# for x in data:
#     collection_name.update_one({"identifier": x["identifier"]}, {"$set": x}, upsert=True)

# updating parts of a section
# for x in data:
#     #print (type(x["plate_info"]))
#     if "condition" in x["plate_info"]:
#         print(x["plate_info"]["condition"])
#         collection_name.update_one({"identifier": x["identifier"]}, {"$set" : {"plate_info.condition" : x["plate_info"]["condition"]} }, upsert=False)

#     if "notes" in x["plate_info"]:
#         print(x["plate_info"]["notes"])
#         collection_name.update_one({"identifier": x["identifier"]}, {"$set" : {"plate_info.notes" : x["plate_info"]["notes"]} }, upsert=False)



print("data inserted")
