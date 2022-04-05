# glass-plates-inventory

There are millions of astronomical photographic glass plates in various observatories, archives, and libraries around the world (Tsvetkov 2000), and recently there have been large efforts to digitize these plates and make their data available.  However, much of the focus of existing online databases have been on the astronomical uses of the plates, without thought to their historic, artistic, or intrinsic value.  Additionally, existing sites present their information using older web standards, such as full HTML table outputs on webpages, rather than using API and json formats.

My goal is to build an online inventory of astronomical photographic glass plates that puts the information into both a machine readable API and a human browsable interface.  The focus of the site will be on enhancing plate discoverability, both for astronomical and historical purposes.  I plan to build a proof-of-concept site, one that showcases these updated features and can handle a subset of a few thousand plates.  Scaling up the project to organize and maintain metadata on millions of plates is out of scope.  Instead, I plan to showcase what can be done using modern web application methods and build an application with an eye towards back end scalability.


API framework:
https://www.django-rest-framework.org/


* pip freeze > requirements.txt
* pip install -r requirements.txt


noSQL:
https://www.mongodb.com/compatibility/mongodb-and-django

https://www.djongomapper.com/

connection time out:
https://docs.atlas.mongodb.com/security/ip-access-list/



noSQL schema reading:

https://www.mongodb.com/unstructured-data/schemaless

https://www.mongodb.com/developer/article/mongodb-schema-design-best-practices/

https://www.compose.com/articles/mongodb-with-and-without-schemas/


https://www.linkedin.com/learning/advanced-nosql-for-data-science/index-data-with-document-databases?autoAdvance=true&autoSkip=true&autoplay=true&resume=false&u=2194065

index attributes usedin find, to speed things up

index_result = db.profiles.create_index([("age", pymongo.ASCENDING)], unique=False)

https://www.linkedin.com/learning/nosql-data-modeling-essential-training/creating-the-json-document?autoAdvance=true&autoSkip=true&autoplay=true&resume=false&u=2194065


WFPDB
output format: json
output verbosity: 3


IVOA:

UCDs
https://ivoa.net/documents/UCD1+/20180527/REC-UCDlist-1.3-20180527.pdf

VOTables
https://www.ivoa.net/documents/VOTable/20191021/REC-VOTable-1.4-20191021.html

Describing Catalogs w/XML
http://vizier.u-strasbg.fr/vizier/doc/astrores.htx

VOTables & Astropy
https://docs.astropy.org/en/stable/io/votable/index.html

openAPI schema

python manage.py generateschema --file openapi-schema.yml


https://swagger.io/tools/swagger-ui/

coreapi


https://medium.com/@vasjaforutube/django-mongodb-django-rest-framework-mongoengine-ee4eb5857b9a



https://docs.mongoengine.org/tutorial.html