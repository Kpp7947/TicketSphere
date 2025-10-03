from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput, EmailInput

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"})
    )
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "first_name": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "last_name": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "email": EmailInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            # "password1": PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            # "password2": PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
        # label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
        # label="New Password"
    )
    new_password2 = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
        # label="Confirm New Password"
    )
