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

    return render(request, "plates/index.html", context)