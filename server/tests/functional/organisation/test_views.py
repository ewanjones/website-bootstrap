import csv
from unittest import mock

from application import organisation
from data.organisation import models


class TestCreateBusiness:
    def test_not_logged_in_denied(self, anon_webapp):
        response = anon_webapp.post("create-business", status=401)

        assert response.status == anon_webapp.UNAUTHORIZED

    def test_business_created_successfully(self, auth_webapp):
        name = "My Business"
        description = "This is the business description"

        response = auth_webapp.post(
            url_name="create-business",
            body={"name": name, "description": description},
            user=auth_webapp.user,
        )

        business = models.Business.objects.get(name=name)
        assert response.status == auth_webapp.OK
        assert response.json == {
            "business": {
                "id": business.id,
                "user_id": str(auth_webapp.user.id),
                "user_name": auth_webapp.user.nickname,
                "name": name,
                "description": description,
                "departments": [],
                "levels": [],
            },
            "message": "success",
        }


class TestListBusinesses:
    def test_not_logged_in_denied(self, anon_webapp):
        response = anon_webapp.post("list-businesses", status=401)
        assert response.status == anon_webapp.UNAUTHORIZED

    def test_only_shows_user_businesses(self, factory, auth_webapp):
        business = factory.Business(user=auth_webapp.user)
        level = factory.Level(business=business)
        department = factory.Department(business=business)

        # This business shouldn't be returned
        other_user = factory.User(email="other@example.com", password="test")
        factory.Business(user=other_user)

        response = auth_webapp.get(url_name="list-businesses", user=auth_webapp.user)

        assert response.status == auth_webapp.OK
        assert response.json == {
            "businesses": [
                {
                    "id": business.id,
                    "user_id": str(auth_webapp.user.id),
                    "user_name": auth_webapp.user.nickname,
                    "name": business.name,
                    "description": business.description,
                    "departments": [
                        {
                            "name": department.name,
                            "description": department.description,
                            "num_line_managers": 0,
                            "average_direct_reports": None,
                            "num_employees": 0,
                            "operating_cost": None,
                        }
                    ],
                    "levels": [{"name": level.name, "description": level.description}],
                }
            ],
            "message": "success",
        }


class TestListEmployees:
    def test_returns_successfully(self, factory, auth_webapp):
        business = factory.Business(user=auth_webapp.user)
        level = factory.Level(business=business)
        department = factory.Department(business=business)
        role = factory.Role(level=level, department=department)
        employee = factory.Employee(role_id=role.id)

        response = auth_webapp.get(
            url_name="list-employees",
            url_kwargs={"pk": business.id},
            user=auth_webapp.user,
        )

        assert response.status == auth_webapp.OK
        assert response.json == {
            "employees": [
                {
                    "id": employee.id,
                    "name": employee.name,
                    "salary": employee.salary,
                    "role": employee.role.name,
                    "gender": employee.gender,
                    "department": employee.role.department.name,
                    "num_direct_reports": 0,
                    "level": employee.role.level.name,
                    "start_date": employee.start_date.strftime("%Y-%m-%d"),
                    "end_date": None,
                }
            ],
            "message": "success",
        }


class TestOrgImport:
    def test_upload_file(self, factory, fixture_path, auth_webapp):
        business = factory.Business(user=auth_webapp.user)
        filepath = fixture_path("test-data.csv")
        with open(filepath, "r") as f:
            rows = list(csv.reader(f))
            # exclude the head in the number of rows
            num_rows = len(rows) - 1

            f.seek(0)
            response = auth_webapp.post(
                "import-organisation",
                url_kwargs={"pk": business.id},
                body=f.read(),
                user=auth_webapp.user,
                headers={
                    "Content-Type": "application/csv;",
                    "Content-Disposition": "attachment; filename=file.csv",
                },
            )

        assert response.status == auth_webapp.OK
        assert models.Employee.objects.count() == num_rows
        roles = models.Role.objects.all()
        assert roles.exists()
        assert all([role.department for role in roles])
        assert all([role.level for role in roles])

    @mock.patch("interfaces.organisation.views.organisation")
    def test_upload_failed(self, mock_app, factory, fixture_path, auth_webapp):
        mock_app.UnableToImport = organisation.UnableToImport
        mock_app.import_organisation.side_effect = mock_app.UnableToImport

        business = factory.Business(user=auth_webapp.user)
        filepath = fixture_path("test-data.csv")

        with open(filepath, "r") as f:
            f.seek(0)
            response = auth_webapp.post(
                "import-organisation",
                url_kwargs={"pk": business.id},
                body=f.read(),
                user=auth_webapp.user,
                headers={
                    "Content-Type": "application/csv;",
                    "Content-Disposition": "attachment; filename=file.csv",
                },
                status=400,
            )

        assert response.status == auth_webapp.BAD_REQUEST


class TestEmployeeHierarchy:
    def test_returns_successfully(self, factory, auth_webapp):
        # Set up business modelsj
        business = factory.Business(user=auth_webapp.user)
        department = factory.Department(business=business)
        level = factory.Level(business=business)
        role = factory.Role(name="Some Role", department=department, level=level)
        # Now create the employee network
        ceo = factory.Employee(name="Rohan", role=role)
        factory.Employee(name="Ewan", role=role)
        manager = factory.Employee(name="Lucy", line_manager=ceo, role=role)
        factory.Employee(name="Luke", line_manager=manager, role=role)

        response = auth_webapp.get(
            "employee-hierarchy",
            url_kwargs={"pk": business.id},
            user=auth_webapp.user,
            headers={
                "Content-Type": "application/csv;",
                "Content-Disposition": "attachment; filename=file.csv",
            },
        )

        assert response.status == auth_webapp.OK
