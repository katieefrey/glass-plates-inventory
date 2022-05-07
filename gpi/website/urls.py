from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='mainindex'),
    path('api/', views.api, name='api'),
    path('guides/', views.guides, name='guides'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    #account related
    # path("login", views.login_form, name="login_form"),
    # path("login_view", views.login_view, name="login_view"),
    # path("logout", views.logout_view, name="logout_view"),
    # path("account", views.account, name="account"),
    # path("register", views.register, name="register"),
    # path("registering", views.registering, name="registering"),

    #path('accounts/', include('django.contrib.auth.urls')),
]