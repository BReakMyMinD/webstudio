from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Your Username")
    password1 = forms.CharField(label="Your Password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label="Repeat Your Password", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email Address")
    first_name = forms.CharField(label="Name")
    last_name = forms.CharField(label="Surname")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            return user


class OrderForm(forms.Form):
    info = forms.CharField(label=False, widget=forms.Textarea, required=False)

    def get_info(self):
        return self.cleaned_data["info"]
