from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
           "placeholder": "Password", "type": "password", 
        }),required=True
    )
    password2 = forms.CharField(
        label="Password Confirm",
        widget=forms.PasswordInput(attrs={
           "placeholder": "Password Confirm", "type": "password",
        }),required=True
    )

    teamID = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={
            "type":"hidden"
        }),
        required=False,
        )
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'teamID']
        widgets = {
            'username': forms.TextInput(attrs={
                "placeholder": "Username", "type": "text",
            }),
            'email': forms.EmailInput(attrs={
                "placeholder": "Email Address", "type": "email",
            }),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "type": "text", }), required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "type": "password"}),required=True
    )
    error_messages = {
        'invalid_login': "Either password or username is wrong or both.",
    }

    