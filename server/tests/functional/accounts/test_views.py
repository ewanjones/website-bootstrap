from django.conf import settings
from django.core import mail

from data.accounts import models as account_models


class TestLogin:
    def test_no_user_redirects_to_about_us(self, anon_webapp):
        response = anon_webapp.get("home")

        assert response.status == anon_webapp.FOUND
        assert "about-us" in response.url

    def test_user_can_login(self, anon_webapp, factory):
        user = factory.User()
        user.set_password("test")

        login_page = anon_webapp.get("login")
        form = login_page.form
        form["username"] = user.email
        form["password"] = "test"
        response = form.submit()

        # Assert we are redirected to home
        assert response.status == anon_webapp.OK
        assert response.url == b""

    def test_incorrect_credentials(self, anon_webapp, factory):
        user = factory.User()
        user.set_password("test")

        login_page = anon_webapp.get("login")
        form = login_page.form
        form["username"] = user.email
        form["password"] = "wrongpassword"
        response = form.submit()

        # Assert we are redirected to home
        assert response.status == anon_webapp.OK
        assert b"Please enter a correct email and password" in response.content


class TestRegister:
    def test_register_account_successfully(self, factory, anon_webapp):
        register_page = anon_webapp.get("register")
        form = register_page.form

        form["full_name"] = "someone"
        form["nickname"] = "someone"
        form["email"] = "someone@example.com"
        form["phone"] = "07123456789"
        form["password"] = "320dwekljrh3"
        form["business_name"] = "sell stuff"
        response = form.submit()

        assert response.status == anon_webapp.FOUND
        assert "/" in response.url
        user = account_models.User.objects.get(
            full_name="someone", email="someone@example.com"
        )
        assert user.businesses.count() == 1

        login_page = anon_webapp.get("login")
        form = login_page.form
        form["username"] = user.email
        form["password"] = "test"
        response = form.submit()

        assert response.url == b""
        user.refresh_from_db()
        assert user.nickname == "someone"
        assert user.email == "someone@example.com"
        assert user.is_active is False
        assert len(mail.outbox) == 1

    def test_register_missing_password(self, factory, anon_webapp):
        register_page = anon_webapp.get("register")
        form = register_page.form

        form["full_name"] = "someone"
        form["nickname"] = "someone"
        form["email"] = "someone@example.com"
        form["phone"] = "07123456789"
        form["password"] = ""
        form["business_name"] = "sell stuff"
        response = form.submit()

        assert response.status == anon_webapp.OK

    def test_user_already_exists(self, factory, anon_webapp):
        user = factory.User()

        register_page = anon_webapp.get("register")
        form = register_page.form

        form["full_name"] = user.full_name
        form["nickname"] = user.nickname
        form["email"] = user.email
        form["phone"] = user.phone
        form["password"] = "something"
        form["business_name"] = "sell stuff"
        response = form.submit()

        assert response.status == anon_webapp.OK


class TestActivate:
    def test_activate_successfully(self, factory, anon_webapp):
        user = factory.User(is_active=False, activation_code="test")

        response = anon_webapp.get(
            "account-activate",
            url_kwargs={"user_id": user.id, "code": user.activation_code},
        )

        assert response.status == anon_webapp.OK
        user.refresh_from_db()
        assert user.is_active is True

    def test_account_already_active_returns_404(self, factory, anon_webapp):
        user = factory.User(is_active=True, activation_code="test")

        response = anon_webapp.get(
            "account-activate",
            status=404,
            url_kwargs={"user_id": user.id, "code": user.activation_code},
        )

        assert response.status == anon_webapp.NOT_FOUND


class TestLogout:
    def test_logout_sucessfully(self, factory, auth_webapp):
        response = auth_webapp.get("logout")

        assert response.status == auth_webapp.FOUND
        assert response.url == settings.LOGIN_URL


class TestResetPassword:
    def test_password_reset(self, factory, anon_webapp):
        user = factory.User()
        old_password = user.password

        page = anon_webapp.get("password-reset-request")
        form = page.form

        form["email"] = user.email
        response = form.submit()

        assert response.status == anon_webapp.FOUND
        assert len(mail.outbox) == 1
        user.refresh_from_db()
        assert user.password_reset_code

        reset_page = anon_webapp.get(
            "password-reset", url_kwargs={"code": user.password_reset_code}
        )
        form = reset_page.form
        form["password"] = "newpassword"
        form["repeat_password"] = "newpassword"
        response = form.submit()

        assert response.status == anon_webapp.FOUND
        user.refresh_from_db()
        assert user.password != old_password
