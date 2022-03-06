from django.shortcuts import render

from .models import Repository

import pymongo
from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
collection_name = dbname["glass"]

# Create your views here.

def index(request):

    repos = collection_name.distinct("repository")

    repodetails = Repository.objects.all()

    context = {
            "repositories": repos,
            "details" : repodetails,
            }

    return render(request, "plates/collections.html", context)

def repo(request, repo_id):

    plates = collection_name.find({"repository" : repo_id}).limit(10)#.ToList()

    context = {
        "repo" : repo_id,
        "plates": plates
    }

    return render(request, "plates/repo.html", context)


def plate(request, repo_id, plate_id):

    plate = list(collection_name.find({"identifier" : plate_id.replace("%20", " ")}))

    context = {
        "repo" : repo_id,
        "plate": plate[0],
    }

    return render(request, "plates/plate.html", context)