from django.db import models
#from djongo import models

# Create your models here.

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

class PlateInfo(EmbeddedDocument):
    #number = fields.IntField(required=True)
    #duration = fields.IntField(required=True)
    emulsion = fields.StringField(required=True)


class GlassPlates(Document):
    identifier = fields.StringField(required=True)
    repository = fields.StringField(required=True)
    #exposure_info = fields.ListField(fields.EmbeddedDocumentField(ExposureInfo))
    exposure_info = fields.ListField()
    obs_info = fields.DictField()
    plate_info = fields.DictField()
    #plate_info = fields.DictField(fields.EmbeddedDocumentField(PlateInfo))