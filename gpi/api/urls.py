from django.urls import path

from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path('archive/', views.archive, name="archive"),
    path('<str:archive>/', views.PlateArchive, name="PlateArchive"),
    path('<str:archive>/<str:identifier>/', views.GlassPlate, name="GlassPlate"),

]
