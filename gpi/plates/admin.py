from django.contrib import admin

from .models import Repository, PlatesInfo

# Register your models here.
admin.site.register(Repository)
admin.site.register(PlatesInfo)