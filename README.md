# glass-plates-inventory

There are millions of astronomical photographic glass plates in various observatories, archives, and libraries around the world (Tsvetkov 2000), and recently there have been large efforts to digitize these plates and make their data available.  However, much of the focus of existing online databases have been on the astronomical uses of the plates, without thought to their historic, artistic, or intrinsic value.  Additionally, existing sites present their information using older web standards, such as full HTML table outputs on webpages, rather than using API and json formats.

My goal is to build an online inventory of astronomical photographic glass plates that puts the information into both a machine readable API and a human browsable interface.  The focus of the site will be on enhancing plate discoverability, both for astronomical and historical purposes.  I plan to build a proof-of-concept site, one that showcases these updated features and can handle a subset of a few thousand plates.  Scaling up the project to organize and maintain metadata on millions of plates is out of scope.  Instead, I plan to showcase what can be done using modern web application methods and build an application with an eye towards back end scalability.


API framework:
https://www.django-rest-framework.org/


* pip freeze > requirements.txt
* pip install -r requirements.txt


noSQL:
https://www.mongodb.com/compatibility/mongodb-and-django