from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.Register.as_view(), name="register"),
    path("register/success/", views.RegisterSuccess.as_view(), name="register-success"),
    path(
        "<int:user_id>/activate/<str:code>",
        views.ActivateAccount.as_view(),
        name="account-activate",
    ),
    path(
        "forgot/", views.PasswordResetRequest.as_view(), name="password-reset-request"
    ),
    path(
        "forgot/sent/",
        views.PasswordResetRequestSent.as_view(),
        name="password-reset-sent",
    ),
    path(
        "forgot/reset/<str:code>", views.PasswordReset.as_view(), name="password-reset"
    ),
    path("settings/", views.MyAccount.as_view(), name="my-account"),
]
