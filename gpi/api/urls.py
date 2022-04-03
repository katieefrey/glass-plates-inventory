from django.urls import path
from rest_framework.schemas import get_schema_view

from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("docs/", include_docs_urls(title="GPI API")),
    path('archive/', views.archive, name="archive"),
    #path('gettest/', views.YourView.as_view(), name="YourView"),
    #path('test/', views.TrackView.as_view(), name="TrackView"),
    path('<str:archive>/', views.PlateArchive, name="PlateArchive"),
    path('<str:archive>/<str:identifier>/', views.GlassPlate, name="GlassPlate"),
]


# schema_view = get_schema_view(
#     title='Server Monitoring API',
#     url='https://www.example.org/api/',
#     urlconf='api.urls'
# )

# schema_url_patterns = [
#     path('api/', include('myproject.api.urls')),
# ]

# schema_view = get_schema_view(
#     title='Server Monitoring API',
#     url='https://www.example.org/api/',
#     patterns=schema_url_patterns,
# )