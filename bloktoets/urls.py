from django.urls import path

from . import views, utils

urlpatterns = [
    path("", views.index, name="index"),
    path("bt_api/", views.api, name="api"),
    path("bt_api/update_pricing/", utils.extenal_product_price_update, name="api_price_update")
]
