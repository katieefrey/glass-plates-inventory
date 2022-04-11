import pymongo
from django.shortcuts import render
from main.secrets import connect_string

from django.http import HttpResponse

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']

glass = dbname["glass"]
repos = dbname["plates_repository"]

def index(request):

    repodetails = repos.find({})

    context = {
            "details" : repodetails,
            }

    return render(request, "plates/collections.html", context)

def repo(request, repo_id):

    plates = glass.find({"repository" : repo_id}).sort([("identifier",pymongo.ASCENDING)]).collation({"locale": "en_US", "numericOrdering": True}).limit(10)

    context = {
        "repo" : repo_id,
        "plates": plates
    }

    return render(request, "plates/repo.html", context)


def plate(request, repo_id, plate_id):

    newid = plate_id.replace("%2520", " ")

    plate = list(glass.find({"identifier" : newid}))
    
    context = {
        "repo" : repo_id,
        "plate": plate[0],
    }

    return render(request, "plates/plate.html", context)