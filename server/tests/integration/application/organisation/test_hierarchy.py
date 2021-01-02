from application import organisation
from data.organisation import models


def test_create_employee_hierarchy(factory):
    # Set up business modelsj
    business = factory.Business()
    department = factory.Department(business=business)
    level = factory.Level(business=business)
    role = factory.Role(name="Some Role", department=department, level=level)
    # Now create the employee network
    ceo = factory.Employee(name="Rohan", role=role)
    factory.Employee(name="Ewan", role=role)
    manager = factory.Employee(name="Lucy", line_manager=ceo, role=role)
    factory.Employee(name="Luke", line_manager=manager, role=role)

    employees = models.Employee.objects.all()
    results = organisation.create_employee_hierarchy(employees)

    assert len(results) == 2
    assert results[0]["direct_reports"][0]["name"] == "Lucy"
    assert results[0]["direct_reports"][0]["direct_reports"][0]["name"] == "Luke"
