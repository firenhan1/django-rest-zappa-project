from django.urls import path, re_path
from .views import CreateDeviceAPI, GetDeviceAPI


urlpatterns = [
    re_path(r"^devices/?$", CreateDeviceAPI.as_view(), name="create_device"),
    path("devices/id<pk>/", GetDeviceAPI.as_view(), name="get_device"),
]
