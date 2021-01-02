from django.views.generic import TemplateView


class AboutUs(TemplateView):
    template_name = "about-us.html"


class ContactUs(TemplateView):
    template_name = "contact-us.html"
