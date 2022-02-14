## using example from https://www.mongodb.com/compatibility/mongodb-and-django

import pymongo

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)

# First define the database name
dbname = my_client['plates']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["glass"]

# Check the count
count = collection_name.count()
print("total documents: "+str(count))
print(" ")

# Read the documents
details = collection_name.find({})
# Print on the terminal
for r in details:
    print(r["identifier"])



# # Update one document
# update_data = collection_name.update_one({'medicine_id':'RR000123456'}, {'$set':{'common_name':'Paracetamol 500'}})

# # Delete one document
# delete_data = collection_name.delete_one({'medicine_id':'RR000123456'})


