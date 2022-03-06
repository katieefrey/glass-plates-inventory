from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from astroquery.simbad import Simbad
import pymongo
import json

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
collection_name = dbname["glass"]


def index(request):

    repos = collection_name.distinct("repository")
    emulsion = collection_name.distinct("plate_info.emulsion")
   
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
        emulsion = collection_name.find({"repository": repo}).distinct("plate_info.emulsion")
    
    output = json.dumps(emulsion)

    return HttpResponse(output)


def result(request):

    repo =  request.GET.getlist("repos")
    emulsion = request.GET.getlist("emulsiondd")
    identifier = (request.GET["plateid"]).strip()
    obj = (request.GET["object"]).strip()
    radius = float((request.GET["radius"]).strip())/60
    ra = request.GET["ra"].strip()
    dec = request.GET["dec"].strip()

    query = {}

    # if plate identifer provided go straight there
    if identifier != "":
        
        try:
            plate = list(collection_name.find({"identifier" : identifier}))
            return redirect('/collections/'+plate[0]["repository"]+'/'+plate[0]["identifier"])
        except:
            return HttpResponse("plate not found")

    if repo[0] != "all":
        query["repository"] = repo[0]

    if emulsion[0] != "all":
        query["plate_info.emulsion"] = emulsion[0]

    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        result_table = Simbad.query_object(obj)
        ra = result_table['RA'][0]
        dec = result_table['DEC'][0]

    if ra != "" and dec != "":
        minra = round(convertRA(ra.replace(" ",":")) - radius*15,4)
        maxra = round(convertRA(ra.replace(" ",":")) + radius*15,4)

        mindec = round(convertDEC(dec.replace(" ",":")) - radius,4)
        maxdec = round(convertDEC(dec.replace(" ",":")) + radius,4)

        query["exposure_info.ra_deg"] = {"$gt" :  minra, "$lt" : maxra}
        query["exposure_info.dec_deg"] = {"$gt" :  mindec, "$lt" : maxdec}

    plates = list(collection_name.find(query).sort([("identifier",pymongo.ASCENDING)]))

    context = {
        "query" : query,
        "results" : plates,
    }

    return render(request, "search/results.html", context)



def convertRA(input_value):
    if input_value and ":" in str(input_value):
        ra = input_value.split(":")
        if float(ra[0]) >= 0:
            output_value = float(ra[0]) + float(ra[1])/60
            if len(ra) == 3:
                output_value += float(ra[2])/3600
        else:
            output_value = float(ra[0]) - float(ra[1])/60
            if len(ra) == 3:
                output_value -= float(ra[2])/3600

        output_value = output_value*15
    elif input_value:
        output_value = input_value
    else:
        return None

    return round(float(output_value),4)


def convertDEC(input_value):
    if input_value and ":" in str(input_value):
        ra = input_value.split(":")
        if float(ra[0]) >= 0:
            output_value = float(ra[0]) + float(ra[1])/60
            if len(ra) == 3:
                output_value += float(ra[2])/3600
        else:
            output_value = float(ra[0]) - float(ra[1])/60
            if len(ra) == 3:
                output_value -= float(ra[2])/3600
    else:
        output_value = input_value

    return round(float(output_value),4)
