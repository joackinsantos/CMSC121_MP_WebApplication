from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput, PasswordInput, CharField

class CreateUserForm(UserCreationForm):
    attrs1={'class': 'form-control', 'placeholder': 'Password', 'required': True,}
    attrs2={'class': 'form-control', 'placeholder': 'Confirm Password', 'required': True,}
    password1 = CharField(widget=PasswordInput(attrs=attrs1))
    password2 = CharField(widget=PasswordInput(attrs=attrs2))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True,}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True,}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': True,}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True,})
        }
