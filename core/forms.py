from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Surname"}),
    )
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("You need to provide username!")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken!")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        conf_pass = self.cleaned_data.get("confirm_password")
        # strong pass validation can be applied.
        # for now, I skip this one. Will only check matching
        if not password and not conf_pass:
            raise ValidationError(
                "You need to povide both, password and confirm password!"
            )
        if password != conf_pass:
            raise ValidationError("Password does not match!")
        return conf_pass
