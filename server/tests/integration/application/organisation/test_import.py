import csv

from application import organisation
from data.organisation import models


def test_import_successfully(factory, fixture_path):
    path = fixture_path("test-data.csv")
    business = factory.Business()

    with open(path, "r") as f:
        rows = list(csv.reader(f))
        num_rows = len(rows) - 1
        f.seek(0)

        rows = csv.DictReader(f)
        organisation.import_organisation(business, rows)

        employees = models.Employee.objects.all()
        assert employees.count() == num_rows

        line_managers = [
            manager
            for manager in employees.values_list("line_manager", flat=True)
            if manager is not None
        ]
        assert len(list(line_managers))
