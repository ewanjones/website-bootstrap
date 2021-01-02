import os

import django_webtest
import pytest
from django.urls import reverse

from tests import factories


def pytest_collection_modifyitems(config, items):
    """
    Add marks to test automagically.
    """
    for item in items:
        path = os.path.relpath(item.fspath)
        if "functional" in path:
            item.add_marker(pytest.mark.django_db)
        if "integration" in path:
            item.add_marker(pytest.mark.django_db)


# FIXTURES


class WebtestAppWrapper(object):
    """
    Wrapper class for the Webtest client to add some convenience methods.
    """

    OK = "200 OK"
    FOUND = "302 Found"
    UNAUTHORIZED = "401 Unauthorized"
    BAD_REQUEST = "400 Bad Request"
    FORBIDDEN = "403 Forbidden"
    NOT_FOUND = "404 Not Found"

    # We keep a property reference to the user that we are masquerading as
    user = None

    def __init__(self, app):
        self.app = app

    def get(self, url_name=None, url_kwargs=None, **kwargs):
        if url_name is not None:
            url = reverse(url_name, kwargs=url_kwargs)
        else:
            url = kwargs.pop("url")

        return self.app.get(url, **kwargs)

    def post(self, url_name=None, body={}, url_kwargs=None, **kwargs):
        if url_name is not None:
            url = reverse(url_name, kwargs=url_kwargs)
        else:
            url = kwargs.pop("url")
        return self.app.post(url, body, **kwargs)

    def post_json(self, url_name=None, url_kwargs=None, **kwargs):
        if url_name is not None:
            url = reverse(url_name, kwargs=url_kwargs)
        else:
            url = kwargs.pop("url")
        return self.app.post_json(url, **kwargs)

    def set_user(self, user, password):
        self.user = user
        self.app.set_user(user)
        self.app.authorization = ("Basic", (user.email, password))


@pytest.fixture
def anon_webapp():
    """
    Provide an API to interact with Django views.
    """
    app = django_webtest.DjangoTestApp()
    return WebtestAppWrapper(app)


@pytest.fixture
def auth_webapp():
    user = factories.User(password="test")
    app = django_webtest.DjangoTestApp()
    webapp = WebtestAppWrapper(app)
    webapp.set_user(user, "test")
    return webapp


@pytest.fixture
def factory():
    """
    Provide a fixture to allow easy access to factories.
    """
    return factories


@pytest.fixture
def fixture_path():
    """
    Return the path to a fixture given a relative path.
    """

    def _get_fixture_filepath(filepath):
        return os.path.join(os.path.dirname(__file__), "fixtures", filepath)

    return _get_fixture_filepath
