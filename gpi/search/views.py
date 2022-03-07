from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from astroquery.simbad import Simbad
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
   
    context = {
            "repositories": archives,
            #"emulsion" : emulsion,
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


def archive_specific(request):

    repo = request.POST["repo"]


    fieldlist = (list(repos.find({"abbr": repo})))
    print (fieldlist[0]["fields"])

    formstring = ""

    for x in fieldlist[0]["fields"]:

        print (x["name"])
        field = (x["name"].split("."))[1]
        print(field)

        print(x["type"])

        

        if x["type"] == "text":
            formstring += """
            <div class='mb-3 row'>
                <label for='astronomer' class='col-sm-4 col-form-label cap'>"""+field+"""</label>
                <div class='col-sm-7'>
                    <input type='text' class='form-control' name='"""+field+"""' id='"""+field+"""'>
                </div>
            </div>
            """

        if x["type"] == "number":
            formstring += """
            <div class='mb-3 row'>
                <label for='astronomer' class='col-sm-4 col-form-label cap'>"""+field+"""</label>
                <div class='col-sm-7'>
                    <input type='number' class='form-control' name='"""+field+"""' id='"""+field+"""'>
                </div>
            </div>
            """

        if x["type"] == "dropdown":
            emulsion = glass.find({"repository": repo}).distinct("plate_info.emulsion")

            formstring += """
            <div class="mb-3 row">
                <label for="emulsion" class="col-sm-4 col-form-label">Emulsion</label>
                <div class="col-sm-7">
                    <select id="emulsion" name="emulsion" class="form-select" aria-label="Default select example">
                        <option value="all" selected>(select an emulsion)</option>
            """
            
            for y in emulsion:
                print (y)
                formstring += "<option value='"+str(y)+"'>"+str(y)+"</option>"

            formstring+= """         
                    </select>
                </div>
            </div>
            """

    """
    DASCH:
        observatory
            lat/long
        telescope
        plate mentioned in notebook
        number of exposures

    Hamburg:
        emulsion
        telescope
        number of exposuers
        plate size

    WFPDB:
        emulsion
        filter
        band
        observer

    """

    # if repo == "all":
    #     emulsion = glass.distinct("emulsion")
    # else:
    #     emulsion = glass.find({"repository": repo}).distinct("plate_info.emulsion")
    
    #output = json.dumps(fieldlist)
    output = json.dumps({"test" : "test1"})
    return HttpResponse(formstring)

def result(request):

    repo =  request.GET.getlist("repos")
    emulsion = request.GET.getlist("emulsion")
    identifier = (request.GET["plateid"]).strip()
    obj = (request.GET["object"]).strip()
    radius = float((request.GET["radius"]).strip())/60
    ra = request.GET["ra"].strip()
    dec = request.GET["dec"].strip()
    num_skip = int(request.GET["num_skip"].strip())
    num_results = int(request.GET["num_results"].strip())

    query = {}

    # if plate identifer provided go straight there
    if identifier != "":
        try:
            plate = list(glass.find({"identifier" : identifier}))
            return redirect('/collections/'+plate[0]["repository"]+'/'+plate[0]["identifier"])
        except:
            # need to write a plate not found page
            return HttpResponse("plate not found")

    if repo[0] != "all":
        query["repository"] = repo[0]

    if emulsion[0] != "all":
        query["plate_info.emulsion"] = emulsion[0]

    # if object was queried, this overwrites any ra and dec that might have been queried
    if obj != "":
        result_table = Simbad.query_object(obj)
        ra = (result_table['RA'][0]).replace(" ",":")
        dec = (result_table['DEC'][0]).replace(" ",":")

    if ra != "":
        minra = round(convertRA(ra) - radius*15,4)
        maxra = round(convertRA(ra) + radius*15,4)
        query["exposure_info"] = {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}

    if dec != "":
        mindec = round(convertDEC(dec) - radius,4)
        maxdec = round(convertDEC(dec) + radius,4)
        query["exposure_info"] = {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}

    if ra != "" and dec != "":
        del query["exposure_info"]
        query["$and"] = [
            {"exposure_info": {"$elemMatch": {"dec_deg": {"$gt": mindec, "$lt": maxdec}}}},
            {"exposure_info": {"$elemMatch": {"ra_deg": {"$gt": minra, "$lt": maxra}}}}
        ]
    
    # execute the full query
    plates = (glass.find(query).sort([("identifier",pymongo.ASCENDING)]).collation({"locale": "en_US", "numericOrdering": True})).skip(num_skip).limit(num_results)

    context = {
        "query" : query,
        "results" : plates,
    }

    # also need to write a no results returned page
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
