from unittest import mock

import pytest
from tests import fake

from application.organisation import _import


@mock.patch.object(_import, "models")
class TestImportValidation:
    @fake.database_transaction()
    def test_required_headers_not_provided_shows_column_names(self, mock_models):
        business = mock.Mock()
        rows = [{"wrong_column": None}]

        with pytest.raises(_import.UnableToImport, match="department"):
            _import.import_organisation(business, rows)

    @fake.database_transaction()
    def test_name_column_not_provided(self, mock_models):
        business = mock.Mock()
        rows = [{"department": "Tech", "level": "A", "role": "Manager"}]

        with pytest.raises(_import.UnableToImport, match="name"):
            _import.import_organisation(business, rows)

    @fake.database_transaction()
    def test_deparment_column_not_provided(self, mock_models):
        business = mock.Mock()
        rows = [{"name": "Sam", "level": "A", "role": "Manager"}]

        with pytest.raises(_import.UnableToImport, match="department"):
            _import.import_organisation(business, rows)


@pytest.mark.parametrize(
    "value,expected_currency,expected_salary",
    [
        ("$10,000", "$", 10000),
        ("10000", "", 10000),
        ("£10,000.00", "£", 10000),
        ("NA", "", None),
        ("", "", None),
        (None, "", None),
    ],
)
def test_salary_parsing(value, expected_currency, expected_salary):
    currency, salary = _import._parse_salary(value)
    assert currency == expected_currency
    assert salary == expected_salary
