# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name','street', 'city', 'state', 'zipcode']
    
    
    def clean(self):
        # Add any additional custom validation logic here, e.g., checking for unique emails, etc.
        # If validation fails, raise forms.ValidationError with appropriate message
        cleaned_data = super(RegistrationForm, self).clean()
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
