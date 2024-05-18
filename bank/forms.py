# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from .models import CheckingAccount, SavingAccount, LoanAccount, Transaction, Account, StudentLoan, PersonalLoan, HomeLoan, Insurance
from django.forms.widgets import Select
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)
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
            # elif loan_type == 'SL':
            #     self.fields['field_for_student_loan'] = forms.CharField(label='Field for Student Loan')
                
                
class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source_account_type', 'destination_account', 'destination_account_type', 'amount', 'recepient_first_name', 'recepient_last_name']
        
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'readonly': False})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'readonly': False})
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the old password field
        del self.fields['old_password']
    
class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)

class StateSelectWidget(Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = str(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return '<option value="%s"%s>%s</option>' % (
            conditional_escape(option_value), selected_html,
            conditional_escape(str(option_label)))
class InsuranceForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=100)
    street = forms.CharField(label='Street', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100, widget=StateSelectWidget(choices=STATE_CHOICES))
    zipcode = forms.CharField(label='Zipcode', max_length=100)
    yearly_ins_prem = forms.DecimalField(label='Yearly Insurance premium', max_digits=10, decimal_places=2)
    
    def save(self):
        company_name = self.cleaned_data['company_name']
        street = self.cleaned_data['street']
        city = self.cleaned_data['city']
        state = self.cleaned_data['state']
        zipcode = self.cleaned_data['zipcode']
        
        insurance_company = Insurance.objects.create(company_name=company_name, street=street, city=city, state=state, zipcode=zipcode)
        return insurance_company
    # Add more fields as necessary