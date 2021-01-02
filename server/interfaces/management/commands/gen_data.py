from .screens.main_screen import MainScreen
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Interactive command for generating data for the database or CSV output"
    max = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        MainScreen().handle_choice()

    