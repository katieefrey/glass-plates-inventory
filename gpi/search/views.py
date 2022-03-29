from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from astroquery.simbad import Simbad
from astropy import units as u
from astropy.coordinates import SkyCoord

import pymongo
import json

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
glass = dbname["glass"]
repos = dbname["plates_repository"]


def index(request):

    archives = repos.distinct("abbr")
    #emulsion = glass.distinct("plate_info.emulsion")

    sortlist = [
        # {
        #     "name" : "identifier",
        #     "field": "identifier"
        # },
        {
            "name" : "Archive",
            "field": "repository"
        },
        {
            "name" : "Right Ascension",
            "field": "exposure_info.ra_deg"
        },
    ]
   
    context = {
            "repositories": archives,
            #"emulsion" : emulsion,
            "sortlist" : sortlist
            }

    return render(request, "search/search.html", context)



def find_emulsions(request):

    repo = request.POST["repo"]

    if repo == "all":
        emulsion = glass.distinct("emulsion")
    else:
        emulsion = glass.find({"repository": repo}).distinct("plate_info.emulsion")
    
    output = json.dumps(emulsion)

    return HttpResponse(output)

def result(request):

    repo =  request.GET.getlist("repos")
    #emulsion = request.GET.getlist("emulsion")
    identifier = (request.GET["plateid"]).strip()
    obj = (request.GET["object"]).strip()
    radius = float((request.GET["radius"]).strip())/60
    ra = request.GET["ra"].strip()
    dec = request.GET["dec"].strip()
    freetext = (request.GET["freetext"]).strip()
    user = (request.GET["user"]).strip()
    sortlist = request.GET.getlist("sortlist")

    try:
        num_skip = int(request.GET["num_skip"].strip())
    except:
        num_skip = 0

    try:
        num_results = int(request.GET["num_results"].strip())
    except:
        num_results = 50

    query = {}

    # if plate identifer provided go straight there
    if identifier != "":
        query["identifier"] = { "$regex" : identifier, "$options" : "i"}

    if repo[0] != "all":
        query["repository"] = repo[0]


    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        coords = SkyCoord.from_name(obj)
        ra = coords.ra.deg
        dec = coords.dec.deg

    if ra != "":
        if ":" in str(ra):
            coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
            ra = coords.ra.deg
        
        minra = round(float(ra) - radius*15, 4)
        maxra = round(float(ra) + radius*15, 4)
        query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}

    if dec != "":
        if ":" in str(dec):
            coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
            dec = coords.dec.deg
        
        mindec = round(float(dec) - radius, 4)
        maxdec = round(float(dec) + radius, 4)
        query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}

    if ra != "" and dec != "":
        del query["exposure_info"]
        query["$and"] = [
            {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
            {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
        ]

    if freetext != "":
        
        query["$or"] = [
            {"plate_info.availability_note" : { "$regex" : freetext, "$options" : "i"}},
            {"plate_info.digitization_note" : { "$regex" : freetext, "$options" : "i"}},
            {"plate_info.quality" : { "$regex" : freetext, "$options" : "i"}},
            {"plate_info.notes" : { "$regex" : freetext, "$options" : "i"}},
            {"plate_info.observer" : { "$regex" : freetext, "$options" : "i"}},
            {"obs_info.instrument" : { "$regex" : freetext, "$options" : "i"}},
            {"obs_info.observatory" : { "$regex" : freetext, "$options" : "i"}},
            {"exposure_info.target" : { "$regex" : freetext, "$options" : "i"}},
            {"plate_info.emulsion" : { "$regex" : freetext, "$options" : "i"}}
        ]
    
    if user != "":
        query["$or"] = [
            {"plate_info.observer" : { "$regex" : user, "$options" : "i"}},
        ]

    # execute the full query
    plates = (
        (
        glass.find(query)
             .sort([(sortlist[0],pymongo.ASCENDING)])
             .collation({"locale": "en_US", "numericOrdering": True})
        )
        .skip(num_skip)
        .limit(num_results)
    )

    results_count = plates.count()
    context = {
        "query" : query,
        "results" : plates,
        "results_count" : results_count,
        "num_start": num_skip + 1,
        "num_end" : num_skip + num_results,
        "num_results"  : num_results,
    }

    # also need to write a no results returned page
    return render(request, "search/results.html", context)