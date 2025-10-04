from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from django.core.exceptions import ValidationError

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
        }
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "first_name": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "last_name": TextInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
            "email": EmailInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        # print("username: ", username)
        # print(User.objects.exclude(pk=self.instance.pk))
        # print(User.objects.exclude(id=self.instance.id))
        # print(User.objects.exclude(pk=self.instance.pk).filter(username=username))
        if (User.objects.exclude(id=self.instance.id).filter(username=username).exists()):
            raise ValidationError("This username is already exists.")
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
    )
    new_password1 = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
    )
    new_password2 = forms.CharField(
        widget=PasswordInput(attrs={"class": "border rounded-lg px-3 py-2 w-full text-black"}),
    )

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        # print("new_password1: ", new_password1)
        # print("password: ", self.user.password)
        # print("password: ", self.user.check_password(new_password1))
        if self.user.check_password(new_password1):
            raise ValidationError("New password cannot be the same as the old password.")
        return new_password1