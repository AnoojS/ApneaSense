from django import forms
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username=forms.CharField(
        required=True,
        help_text=None,
    )

    password=forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=None,
    )

    class Meta:
        model = User
        fields = ('username', 'password')