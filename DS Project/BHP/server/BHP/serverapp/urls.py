from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="api"),
    # path("get_api/", views.get_api, name="api"),
    path("get_loc/", views.get_locations, name="locations"),
    path("load-artifacts1/", views.load_saved_artifacts, name="load_artifacts"),
    path("load-artifacts2/", views.load_artifacts, name="load_artifacts"),
    path("get_price/", views.get_price, name="printprice"),
    path("main/", views.main, name="main"),
    path("predict_home_price/", views.predict_home_price, name="predict_home_price"),
    path("get_location_names/", views.get_location_names, name="get_location_names"),
]
