from django.shortcuts import render

#from plates.models import Repository

import pymongo
from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
collection_name = dbname["glass"]

# Create your views here.

def index(request):

    repos = collection_name.distinct("repository")
    emulsion = collection_name.distinct("emulsion")
    # can i limit the emulsion to the selected repository?

    context = {
            "repositories": repos,
            "emulsion" : emulsion,
            }

    return render(request, "search/index.html", context)


def result(request):

    repo =  request.GET.getlist("repos")

    if repo[0] == "all":
        plates = list(collection_name.find({}).sort([("repository",pymongo.ASCENDING), ("identifier",pymongo.ASCENDING)]))
    else:
        plates = list(collection_name.find({"repository" : repo[0]}).sort([("identifier",pymongo.ASCENDING)]))
        
    context = {
        "query" : repo[0],
        "results" : plates
    }

    return render(request, "search/results.html", context)