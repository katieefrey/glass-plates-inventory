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

    plates = list(collection_name.find({"repository" : repo_id}))

    context = {
        "repo" : repo_id,
        "plates": plates
    }

    return render(request, "plates/repo.html", context)

def plate(request, repo_id, plate_id):

    plate = list(collection_name.find({"identifier" : plate_id}))

    quality_flag = 0
    target_flag = 0
    target_type_flag = 0
    time_flag = 0


    for x in plate[0]["exposures"]:
        try:
            if x["coord_quality"] != None:
                quality_flag = 1
        except:
            pass

        try:
            if x["target"] != None:
                target_flag = 1
                print("==> "+x["target"])
        except:
            pass

        try:
            if x["target_type"] != None:
                target_type_flag = 1
        except:
            pass

        try:
            if x["time"] != None:
                time_flag = 1
        except:
            pass

    context = {
        "repo" : repo_id,
        "plate": plate[0],
        "quality_flag" : quality_flag,
        "target_flag" : target_flag,
        "target_type_flag" : target_type_flag,
        "time_flag" : time_flag
    }

    return render(request, "plates/plate.html", context)