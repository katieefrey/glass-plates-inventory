from django.contrib import admin

from .models import Repository, PlatesInfo, GlassPlates, ExposureInfo

from mongoengine import Document, EmbeddedDocument, fields

# Register your models here.
admin.site.register(Repository)
admin.site.register(PlatesInfo)

admin.register(ExposureInfo)
admin.register(GlassPlates)