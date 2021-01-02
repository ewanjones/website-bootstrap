from django import shortcuts
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView

from application import accounts
from data.accounts import models

from . import forms

# Register/Login


class Login(LoginView):
    template_name = "accounts/login.html"
    success_url = settings.LOGIN_REDIRECT_URL


class Logout(LogoutView):
    redirect_url = settings.LOGOUT_REDIRECT_URL


class Register(FormView):
    template_name = "accounts/register.html"
    success_url = settings.LOGIN_REDIRECT_URL
    form_class = forms.Register
    success_url = "/accounts/register/success/"

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            accounts.register(
                full_name=data["full_name"],
                nickname=data["nickname"],
                email=data["email"],
                phone=data["phone"],
                password=data["password"],
                business_name=data["business_name"],
            )
        except accounts.UnableToRegister as e:
            form.add_error(None, e)
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


class RegisterSuccess(TemplateView):
    template_name = "accounts/register-success.html"


class ActivateAccount(TemplateView):
    template_name = "accounts/account-active.html"

    def dispatch(self, request, *args, **kwargs):
        user = shortcuts.get_object_or_404(
            models.User,
            pk=kwargs["user_id"],
            activation_code=kwargs["code"],
            is_active=False,
        )
        user.set_active()
        return super().dispatch(request, *args, **kwargs)


# Logged in


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["react_bundle_url"] = settings.REACT_BUNDLE_BASE_URL
        return context


class MyAccount(FormView):
    template_name = "accounts/my-account.html"
    success_url = "/accounts/settings/"
    form_class = forms.MyAccount

    def get_initial(self):
        user = self.request.user
        return {
            "full_name": user.full_name,
            "nickname": user.nickname,
            "email": user.email,
            "phone": user.phone,
        }

    def form_valid(self, form):
        form_data = form.cleaned_data
        password = form_data.pop("new_password")
        form_data.pop("confirm_password")
        changed_data = {k: v for k, v in form_data.items() if v}

        accounts.update_user(user=self.request.user, **changed_data, password=password)
        messages.success(self.request, "Account updated")

        return super().form_valid(form)


# Password reset


class PasswordResetRequest(FormView):
    template_name = "accounts/forgot-password.html"
    success_url = settings.LOGIN_REDIRECT_URL
    form_class = forms.ForgotPassword
    success_url = "/accounts/forgot/sent/"

    def form_valid(self, form):
        data = form.cleaned_data
        accounts.request_reset_password(email=data["email"])

        return HttpResponseRedirect(self.get_success_url())


class PasswordResetRequestSent(TemplateView):
    template_name = "accounts/forgot-password-sent.html"


class PasswordReset(FormView):
    template_name = "accounts/password-reset.html"
    form_class = forms.PasswordReset
    success_url = "/accounts/login/"

    def dispatch(self, request, *args, **kwargs):
        self.user = shortcuts.get_object_or_404(
            models.User, password_reset_code=kwargs["code"]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        accounts.reset_password(self.user, data["password"])

        return HttpResponseRedirect(self.get_success_url())
