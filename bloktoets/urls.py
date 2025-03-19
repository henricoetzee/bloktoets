from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bt_api/", views.api, name="api")
]
