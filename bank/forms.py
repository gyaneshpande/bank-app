# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from .models import CheckingAccount, SavingAccount, LoanAccount

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
    
class CheckingAccountForm(forms.ModelForm):
    class Meta:
        model = CheckingAccount
        fields = ['service_charge']  # Fields required to create a checking account

class SavingAccountForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = ['interest_rate']  # Fields required to create a checking account
        
class LoanAccountForm(forms.ModelForm):
    # LOAN_TYPE_CHOICES = (
    #     ('SL', 'Student Loan'),
    #     ('PL', 'Personal Loan'),
    #     ('HL', 'Home Loan'),
    # )

    # loan_type = forms.ChoiceField(choices=LOAN_TYPE_CHOICES)

    class Meta:
        model = LoanAccount
        fields = ['loan_type', 'loan_rate', 'loan_amount', 'loan_months']
    
    def __init__(self, *args, **kwargs):
        super(LoanAccountForm, self).__init__(*args, **kwargs)
        
        # Dynamically adjust form fields based on selected loan_type
        if 'loan_type' in self.data:
            loan_type = self.data.get('loan_type')
            if loan_type == 'PL':
                self.fields['loan_purpose'] = forms.CharField(label='Field for Personal Loan')
            elif loan_type == 'HL':
                self.fields['house_built_year'] = forms.CharField(label='Field for Home Loan')
            elif loan_type == 'SL':
                self.fields['field_for_student_loan'] = forms.CharField(label='Field for Student Loan')