from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("error/", views.holding, name="holding"),
    path("result/", views.result, name="result"),
    #path("find_emulsions", views.find_emulsions, name="find_emulsions"),
    # path("archive_specific", views.archive_specific, name="archive_specific"),
    # path("add_plate", views.add_plate, name="add_plate"),
    # path("no_plate", views.no_plate, name="no_plate"),
    # path("remove_plate", views.remove_plate, name="remove_plate"),
    # path("plateseries/", views.browse_series, name="browse_series"),
    # path("plateseries/<series_id>", views.browse_plates, name="browse_plates"),
    # path("plate/<plate_id>", views.plate, name="plate"),
    # path("notebooks/", views.notebooks, name="notebooks"),
    # path("notebook/<phaedra_id>/", views.phaedra, name="phaedra"),
    # path("notebook/<phaedra_id>/<int:page>/", views.page, name="page"),
    # path("search", views.search, name="search"),
    # path("testview", views.testview, name="testview"),
]
