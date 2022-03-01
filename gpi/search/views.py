from django.shortcuts import render
from django.http import HttpResponse
import json

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
   
    context = {
            "repositories": repos,
            "emulsion" : emulsion,
            }

    return render(request, "search/search.html", context)



def find_emulsions(request):

    repo = request.POST["repo"]

    if repo == "all":
        emulsion = collection_name.distinct("emulsion")
    else:
        emulsion = collection_name.find({"repository": repo}).distinct("emulsion")
    
    output = json.dumps(emulsion)

    return HttpResponse(output)


def result(request):

    repo =  request.GET.getlist("repos")
    emulsion = request.GET.getlist("emulsiondd")

    query = {}

    if repo[0] != "all":
        query["repository"] = repo[0]

    if emulsion[0] != "all":
        query["emulsion"] = emulsion[0]

    plates = list(collection_name.find(query).sort([("identifier",pymongo.ASCENDING)]))
        
    context = {
        "query" : query,
        "results" : plates
    }

    return render(request, "search/results.html", context)