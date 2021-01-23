from django import forms
from data.accounts import validators


class Register(forms.Form):
    nickname = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(
        max_length=15, required=False, validators=[validators.is_phone]
    )
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())


class ForgotPassword(forms.Form):
    email = forms.CharField(max_length=100)


class PasswordReset(forms.Form):
    password = forms.CharField(max_length=100)
    repeat_password = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["repeat_password"]:
            raise forms.ValidationError("Passwords do not match")


class MyAccount(forms.Form):
    nickname = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)

    new_password = forms.CharField(
        max_length=30, widget=forms.PasswordInput(), required=False
    )
    confirm_password = forms.CharField(
        max_length=30, widget=forms.PasswordInput(), required=False
    )

    def clean(self):
        data = self.cleaned_data
        if (data["new_password"] or data["confirm_password"]) and not (
            data["new_password"] and data["confirm_password"]
        ):
            raise forms.ValidationError("Please enter both password fields")
