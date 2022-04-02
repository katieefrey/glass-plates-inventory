from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from bson.json_util import dumps

from astropy import units as u
from astropy.coordinates import SkyCoord

import pymongo
import json

from main.secrets import connect_string

my_client = pymongo.MongoClient(connect_string)
dbname = my_client['plates']
glassplates = dbname["glass"]
repos = dbname["plates_repository"]


sort_list = [
    {
        "name" : "Identifier",
        "nickname" :"identifier",
        "field": "identifier"
    },
    {
        "name" : "Archive",
        "nickname" :"archive",
        "field": "repository"
    },
    {
        "name" : "Right Ascension",
        "nickname" : "ra",
        "field": "exposure_info.ra_deg"
    },
]


# Create your views here.
@api_view(['GET'])
def root(request):

    try:
        identifier = (request.GET["identifier"]).strip()
    except:
        identifier = ""

    try:
        obj = (request.GET["object"]).strip()
    except:
        obj = ""

    try:
        radius = float((request.GET["radius"]).strip())/60
    except:
        radius = 10/60

    try:
        ra = request.GET["ra"].strip()
    except:
        ra = ""

    try:
        dec = request.GET["dec"].strip()
    except:
        dec = ""

    try:
        text = (request.GET["text"]).strip()
    except:
        text = ""

    try:
        observer = (request.GET["observer"]).strip()
    except:
        observer = ""

    try:
        sort_order = request.GET["sort_order"].strip()
        for x in sort_list:
            if x["nickname"] == sort_order:
                sortfield = x["field"]
    except:
        sortfield = "identifier"

    try:
        archive = request.GET["archive"].strip()
    except:
        archive = "all"

    try:
        num_skip = int(request.GET["num_skip"].strip())
    except:
        num_skip = 0

    try:
        num_results = int(request.GET["num_results"].strip())
    except:
        num_results = 50

    query = {}
    
    if identifier != "":
        query["identifier"] = { "$regex" : identifier, "$options" : "i"}

    if archive != "all":
        query["repository"] = { "$regex" : archive, "$options" : "i"}

    # if plate identifer and ardchive provided, attempt to go straight there
    if identifier != "" and archive != "all":
        try:
            plate = list(glassplates.find({"identifier" : identifier}))
            return redirect('/collections/'+plate[0]["repository"]+'/'+plate[0]["identifier"])
        except:
            pass

    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        try:
            coords = SkyCoord.from_name(obj)
            ra = coords.ra.deg
            dec = coords.dec.deg
        except:
            pass

    if ra != "":
        try:
            if ":" in str(ra):
                coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
                ra = coords.ra.deg
            minra = round(float(ra) - radius*15, 4)
            maxra = round(float(ra) + radius*15, 4)
            query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}

        except:
            pass

    if dec != "":
        try:
            if ":" in str(dec):
                coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
                dec = coords.dec.deg
            mindec = round(float(dec) - radius, 4)
            maxdec = round(float(dec) + radius, 4)
            query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}
        except:
            pass

    if ra != "" and dec != "":
        del query["exposure_info"]
        query["$and"] = [
            {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
            {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
        ]

    if text != "":
        
        query["$or"] = [
            {"plate_info.availability_note" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.digitization_note" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.quality" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.notes" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.observer" : { "$regex" : text, "$options" : "i"}},
            {"obs_info.instrument" : { "$regex" : text, "$options" : "i"}},
            {"obs_info.observatory" : { "$regex" : text, "$options" : "i"}},
            {"exposure_info.target" : { "$regex" : text, "$options" : "i"}},
            {"plate_info.emulsion" : { "$regex" : text, "$options" : "i"}}
        ]
    
    if observer != "":
        query["$or"] = [
            {"plate_info.observer" : { "$regex" : observer, "$options" : "i"}},
        ]

    # execute the full query
    plates = (
        (
        glassplates.find(query)
             .sort([(sortfield,pymongo.ASCENDING)])
             .collation({"locale": "en_US", "numericOrdering": True})
        )
        .skip(num_skip)
        .limit(num_results)
    )

    plates_out = json.loads(dumps(plates))

    results_count = plates.count()

    results = {
        "total_results" : results_count,
        "num_results" : num_results,
        "num_skip" : num_skip,
        "results" : plates_out,
    }

    if plates == None:
        return Response(results, status=status.HTTP_204_NO_CONTENT)
            
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
def archive(request):
    archives = json.loads(dumps(repos.find({})))
    return Response(archives)


# @api_view(['GET', 'POST'])
# def glasspost(request):
#     if request.method == 'GET':
#         archives = repos.distinct("abbr")
#     elif request.method =='POST':
#         print (request.data)
#         repos.insert(request.data)
#         archives = repos.distinct("abbr")
#         #pass
#     return Response(archives)


# plates in archive
@api_view(['GET'])
def PlateArchive(request, archive):

    try:
        num_skip = int(request.GET["num_skip"].strip())
    except:
        num_skip = 0

    try:
        num_results = int(request.GET["num_results"].strip())
    except:
        num_results = 50

    query = {}
    query["repository"] = { "$regex" : archive, "$options" : "i"}

    plates = (
            (
                glassplates.find(query)
                    .sort([('identifier',pymongo.ASCENDING)])
                    .collation({"locale": "en_US", "numericOrdering": True})
                )
                .skip(num_skip)
                .limit(num_results)
            )
    
    plates_out = json.loads(dumps(plates))
    
    results_count = plates.count()

    results = {
        "total_results" : results_count,
        "num_results" : num_results,
        "num_skip" : num_skip,
        "results" : plates_out,
    }

    # if plates == None:
    #     return Response(results, status=status.HTTP_204_NO_CONTENT)
            
    return Response(results, status=status.HTTP_200_OK)

# specific plate
@api_view(['GET'])
def GlassPlate(request, archive, identifier):

    query = {}
    query["repository"] = { "$regex" : archive, "$options" : "i"}
    query["identifier"] = { "$regex" : '^'+identifier+'$', "$options" : "i"}

    plates = json.loads(dumps(glassplates.find_one(query)))
    
    # if plates == None:
    #     return Response({"results" : plates}, status=status.HTTP_204_NO_CONTENT)
            
    return Response({"results" : plates}, status=status.HTTP_200_OK)



