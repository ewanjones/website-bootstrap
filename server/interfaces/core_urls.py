from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from interfaces.accounts import views


"""
Core URLs

The frontend requires an 'api/' prefix to ajax endpoints.
"""


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("interfaces.accounts.urls")),
    path("", include("interfaces.info.urls")),
    path("", views.Home.as_view(), name="home"),
    #  path("api/organisation/", include("interfaces.organisation.urls")),
]
