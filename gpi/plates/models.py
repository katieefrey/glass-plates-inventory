from django.db import models
#from djongo import models

# Create your models here.

# class ArchiveField(models.Model):
#     name = models.CharField(null=True, max_length=200)
#     # email = models.EmailField(null=True)
    
#     class Meta:
#         abstract = True

class Repository(models.Model):
    abbr = models.CharField(max_length=500)
    name = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, null=True)
    desc = models.TextField(null=True)
    #fields = models.ArrayField(null=True, model_container=ArchiveField)

    def __str__(self):
        return f"{self.name}"


# this created a new database on MongoDB
# just a few sample records currently
class PlatesInfo(models.Model):
    identifier = models.CharField(max_length=500)
    repository = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.identifier}"




from mongoengine import Document, EmbeddedDocument, fields

class ExposureInfo(EmbeddedDocument):
    number = fields.IntField(required=True)
    duration = fields.IntField(required=True)
    duration_unit = fields.StringField(required=True)

class GlassPlates(Document):
    identifier = fields.StringField(required=True)
    repository = fields.StringField(required=True)
    #exposure_info = fields.ListField(fields.EmbeddedDocumentField(ExposureInfo))
    exposure_info = fields.ListField()
    obs_info = fields.DictField()
    plate_info = fields.DictField()


# import mongoengine
# from django.utils.crypto import get_random_string
# #from .apps import MongoengineAppConfig

# class RandomStringPKDocument(mongoengine.Document):
#     id = mongoengine.StringField(
#         primary_key=True,
#         max_length=12,
#         default=get_random_string,
#     )

#     # Meta abstract
#     meta = {'abstract': True}


# class GlassPlates(RandomStringPKDocument):
#     identifier = models.CharField(required=True, max_length=500)
#     repository = models.CharField(required=True, max_length=500)

#     # Meta collection name
#     meta = {'collection': f'{MongoengineAppConfig.name}_account'}


# # #observatories
# # """
# # - name
# # - general location
# # - lat
# # - long

# # """

# # class Observatory(models.Model):
# #     name = models.CharField(max_length=500)
# #     location = models.CharField(max_length=500, null=True)
# #     latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
# #     longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)

# #     def __str__(self):
# #         return f"{self.name}"


# # #telescopes (could be many telescopes at the same observatory)
# # # could have same telescope at 2 different locations (new entry for each?)
# # """
# # - name
# # - apature
# # - scale
# # """

# # class Telescope(models.Model):
# #     name = models.CharField(max_length=500)
# #     aperature = models.CharField(max_length=500, null=True)
# #     scale = models.DecimalField(max_digits=6, decimal_places=4, null=True)
# #     #obs = models.ForeignKey(Observatory, on_delete=models.CASCADE)

# #     def __str__(self):
# #         return f"{self.name}, at {self.obs}"

# # class Emulsion(models.Model):
# #     emulsion = models.CharField(max_length=500)

# #     def __str__(self):
# #         return f"{self.emulsion}"

# # class Filter(models.Model):
# #     filt = models.CharField(max_length=500)

# #     def __str__(self):
# #         return f"{self.filt}"

# # class Band(models.Model):
# #     band = models.CharField(max_length=500)

# #     def __str__(self):
# #         return f"{self.band}"

# # #plates
# # """
# # - telescope (which connects to which observatory)
# # - plate id
# # - RA
# # - Dec
# # - JD (if specific date is available, JD2000.0)
# # - looser date (if nothing better)
# # - Exposure time (seconds)
# # - multi exposuers on the plate
# # - emulsion
# # - filter
# # - band

# # import allows for
# # - JD, HJD, Geocentric Date, Heliocentric Date
# # - RA/Dec degrees/hh:mm:sec
# # and will auto convert to a standard format, probably decimals all around


# # """

# # class Plate(models.Model):
# #     series = models.CharField(max_length=3)
# #     number = models.IntegerField()
# #     # ra and dec, in decimal format
# #     ra = models.DecimalField(max_digits=8, decimal_places=5, null=True)
# #     dec = models.DecimalField(max_digits=8, decimal_places=5, null=True)
# #     # julian date
# #     jd = models.DecimalField(max_digits=13, decimal_places=5, null=True)
# #     # general date
# #     date = models.DateTimeField(null=True)
# #     # exposure time, seconds
# #     exptime = models.IntegerField(null=True)
# #     #emulsion = models.ForeignKey(Emulsion, on_delete=models.CASCADE, null=True)
# #     #filt = models.ForeignKey(Filter, on_delete=models.CASCADE, null=True)
# #     #band = models.ForeignKey(Band, on_delete=models.CASCADE, null=True)

# #     def __str__(self):
# #         return f"{self.series}{self.number}"
