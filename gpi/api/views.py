from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from bson.json_util import dumps

from astropy import units as u
from astropy.coordinates import SkyCoord

import pymongo
import json
import re

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


# gltest
# https://stackoverflow.com/a/31649061

# might want to look at this more
# https://stackoverflow.com/questions/41424053/how-to-use-django-rest-filtering-with-mongoengine-for-list-filtering

# from rest_framework_mongoengine import generics
# from .serializers import GlassPlatesSerializer
# from plates.models import GlassPlates
# from rest_framework.response import Response
# from rest_framework import status 

# # my_filter_fields = ['identifier', 'repository', 'emulsion', 'radius', 'plate_info__notes','ra', 'dec', 'obj']

# class GlassPlatesList(generics.ListAPIView):

#     # do i need this line?
#     #queryset = GlassPlates.objects.all()

#     serializer_class = GlassPlatesSerializer
#     #my_filter_fields = ['identifier', 'repository', 'emulsion', 'test', 'radius', 'plate_info__notes','ra', 'dec', 'obj']
    
#     def get_filters():
#         my_filter_fields = ['identifier', 'repository', 'emulsion', 'radius', 'plate_info__notes','ra', 'dec', 'obj']
#         return my_filter_fields

#     def get_kwargs_for_filtering(self):
#         radius = 10/60

#         filtering_kwargs = {} 
#         # iterate over the filter fields
#         for field in GlassPlatesList.get_filters():#my_filter_fields: 
#             # get the value of a field from request query parameter

#             if field == "radius":
#                 field_value = self.request.query_params.get(field)
#                 if field_value:
#                     try:
#                         radius = float(field_value)/60
#                     except:
#                         pass

#             elif field == "ra":
#                 ra = self.request.query_params.get(field)
#                 if ra:
#                     try:
#                         if ":" in str(ra):
#                             coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
#                             ra = coords.ra.deg
#                         minra = round(float(ra) - radius*15, 4)
#                         maxra = round(float(ra) + radius*15, 4)
#                         filtering_kwargs["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}
#                     except:
#                         filtering_kwargs["exposure_info"] = {"$elemMatch": {"ra_deg": ra}}

#             elif field == "dec":
#                 dec = self.request.query_params.get(field)
#                 if dec:
#                     try:
#                         if ":" in str(dec):
#                             coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
#                             dec = coords.dec.deg
#                         mindec = round(float(dec) - radius, 4)
#                         maxdec = round(float(dec) + radius, 4)
#                         filtering_kwargs["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}
#                     except:
#                         filtering_kwargs["exposure_info"] = {"$elemMatch": {"dec_deg": dec}}

#             elif field == "obj":
#                 obj = self.request.query_params.get(field)
#                 if obj:
#                     coords = SkyCoord.from_name(obj)
#                     ra = coords.ra.deg
#                     dec = coords.dec.deg

#                     minra = round(float(ra) - radius*15, 4)
#                     maxra = round(float(ra) + radius*15, 4)
#                     filtering_kwargs["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}

#                     mindec = round(float(dec) - radius, 4)
#                     maxdec = round(float(dec) + radius, 4)
#                     filtering_kwargs["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}

#             # elif field == "text":
#             #     text = self.request.query_params.get(field)
#             #     from mongoengine.queryset.visitor import Q

#             #     if text:

#             #         filtering_kwargs["$or"] = [
#             #             {"plate_info.availability_note" : { "$regex" : text, "$options" : "i"}},
#             #             {"plate_info.digitization_note" : { "$regex" : text, "$options" : "i"}},
#             #             {"plate_info.quality" : { "$regex" : text, "$options" : "i"}},
#             #             {"plate_info.notes" : { "$regex" : text, "$options" : "i"}},
#             #             {"plate_info.observer" : { "$regex" : text, "$options" : "i"}},
#             #             {"obs_info.instrument" : { "$regex" : text, "$options" : "i"}},
#             #             {"obs_info.observatory" : { "$regex" : text, "$options" : "i"}},
#             #             {"exposure_info.target" : { "$regex" : text, "$options" : "i"}},
#             #             {"plate_info.emulsion" : { "$regex" : text, "$options" : "i"}}
#             #         ]

#             elif field == "emulsion":
#                 field_value = self.request.query_params.get(field)
#                 if field_value: 
#                     filtering_kwargs["plate_info__"+field] = { "$regex" : field_value, "$options" : "i"}

#             else:
#                 field_value = self.request.query_params.get(field) 
#                 if field_value: 
#                     filtering_kwargs[field] = { "$regex" : field_value, "$options" : "i"}

#         print (filtering_kwargs)

#         return filtering_kwargs 

#     def get_queryset(self):

#         queryset = GlassPlates.objects.all() 
#         # get the fields with values for filtering 
#         filtering_kwargs = self.get_kwargs_for_filtering() 

#         if filtering_kwargs:
#             # filter the queryset based on 'filtering_kwargs'
#             queryset = GlassPlates.objects.filter(**filtering_kwargs)

#         return queryset


# # print(GlassPlatesList.get_filters())

# # gtest
# # https://medium.com/@vasjaforutube/django-mongodb-django-rest-framework-mongoengine-ee4eb5857b9a
# from rest_framework_mongoengine import viewsets
# from .serializers import GlassPlatesSerializer
# from plates.models import GlassPlates

# class GlassPlatesViewSet(viewsets.ModelViewSet):
#     serializer_class = GlassPlatesSerializer
#     def get_queryset(self):
#         return GlassPlates.objects.all()




# my custom API build
# this needs documentation
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
            print(ra)
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

    if ra != "":
        try:
            if ":" in str(ra):
                coords = SkyCoord(ra+" 0", unit=(u.hourangle, u.deg))
                ra = coords.ra.deg
            minra = round(float(ra) - radius*15, 4)
            maxra = round(float(ra) + radius*15, 4)
            query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

    if dec != "":
        try:
            if ":" in str(dec):
                coords = SkyCoord("0 "+dec, unit=(u.hourangle, u.deg))
                dec = coords.dec.deg
            mindec = round(float(dec) - radius, 4)
            maxdec = round(float(dec) + radius, 4)
            query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}
        except:
            results = {
                "total_results" : 0,
                "num_results" : 0,
                "results": {}
            }
            return Response(results, status=status.HTTP_404_NOT_FOUND)

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
        "start" : num_skip+1,
    }

    if num_skip + num_results >= results_count:
        results["end"] = results_count
    else:
        results["end"] = num_skip + num_results

    # find next page
    if num_skip + num_results <= results_count:
        if "num_skip" in request.build_absolute_uri():
            results["next_page"] = re.sub(r"num_skip=\d+", "num_skip="+str(num_skip+num_results), request.build_absolute_uri())
        elif "?" in request.build_absolute_uri():
            results["next_page"] = request.build_absolute_uri()+"&num_skip="+str(num_skip + num_results)
        else:
            results["next_page"] = request.build_absolute_uri()+"?num_skip="+str(num_skip + num_results)

    # find previous page
    if num_skip+1 - num_results >= 0:
        if "num_skip" in request.build_absolute_uri():
            results["previous_page"] = re.sub(r"num_skip=\d+", "num_skip="+str(num_skip-num_results), request.build_absolute_uri())
        elif "?" in request.build_absolute_uri():
            results["previous_page"] = request.build_absolute_uri()+"&num_skip="+str(num_skip-num_results)
        else:
            results["previous_page"] = request.build_absolute_uri()+"?num_skip="+str(num_skip-num_results)

    results["results"] = plates_out
    

    # print(request)

    # print (request.build_absolute_uri())
    # print("this one?" + request.build_absolute_uri('?'))
    # print(request.build_absolute_uri('/')[:-1].strip("/"))
    # print(request.build_absolute_uri('/').strip("/"))
    # if plates == None:
    #     return Response(results, status=status.HTTP_204_NO_CONTENT)
            
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
def archive(request):
    archives = json.loads(dumps(repos.find({})))
    return Response(archives)

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



