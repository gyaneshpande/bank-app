# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from .models import CheckingAccount, SavingAccount, LoanAccount, Transaction, Account, StudentLoan, PersonalLoan, HomeLoan

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
        fields = ['service_charge', 'balance']  # Fields required to create a checking account

class SavingAccountForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = ['interest_rate', 'balance']  # Fields required to create a checking account
        
class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = ['loan_type', 'loan_rate', 'loan_amount', 'loan_months']
    
    def __init__(self, *args, **kwargs):
        super(LoanAccountForm, self).__init__(*args, **kwargs)
        
        # Dynamically adjust form fields based on selected loan_type
        if 'loan_type' in self.data:
            loan_type = self.data.get('loan_type')
            if loan_type == 'PL':
                self.fields['loan_purpose'] = forms.CharField(label='Purpose for Personal Loan')
            elif loan_type == 'HL':
                self.fields['house_built_year'] = forms.CharField(label='House built year')
            elif loan_type == 'SL':
                self.fields['field_for_student_loan'] = forms.CharField(label='Field for Student Loan')
                
# class PersonalLoanForm(forms.ModelForm):
#     class Meta:
#         model = PersonalLoan
#         fields = ['loan_purpose']  # Add fields specific to Personal Loan

# class HomeLoanForm(forms.ModelForm):
#     class Meta:
#         model = HomeLoan
#         fields = ['house_built_year',]  # Add fields specific to Home Loan

# class StudentLoanForm(forms.ModelForm):
#     class Meta:
#         model = StudentLoan
        # fields = ['']  # Add fields specific to Student Loan
                
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source_account_type', 'destination_account', 'destination_account_type', 'amount', 'recepient_first_name', 'recepient_last_name']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the old password field
        del self.fields['old_password']