from django.urls import path

from . import views

urlpatterns = [
    path("about-us/", views.AboutUs.as_view(), name="about-us"),
    path("contact-us/", views.ContactUs.as_view(), name="contact-us"),
]
