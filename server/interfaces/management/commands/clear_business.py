from django.core.management.base import BaseCommand
from django.db.models.deletion import ProtectedError

from data.organisation import models


class Command(BaseCommand):
    help = "Clear a business of all levels, departments, roles and employees"

    def add_arguments(self, parser):
        parser.add_argument("--business", help="The business ID to clear")

    def handle(self, *args, **options):
        business = models.Business.objects.get(pk=options["business"])

        print("Deleting employees")
        while models.Employee.objects.count():
            employees = models.Employee.objects.filter(
                role__department__business=business, direct_reports__isnull=True
            )
            employees.delete()

        print("Deleting roles")
        roles = models.Role.objects.filter(department__business=business)
        roles.delete()

        print("Deleting departments")
        business.departments.all().delete()

        print("Deleting levels")
        business.levels.all().delete()
