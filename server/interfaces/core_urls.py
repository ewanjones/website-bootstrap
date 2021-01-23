from django.contrib import admin
from django.urls import include, path

from interfaces.accounts import views


"""
Core URLs

The frontend react app requires an 'api/' prefix to ajax endpoints.
"""


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("interfaces.accounts.urls")),
    path("", include("interfaces.info.urls")),
    path("", views.Home.as_view(), name="home"),
]
