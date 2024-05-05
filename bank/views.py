# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from .models import CustomUser  # Import your custom user model
from .forms import RegistrationForm, LoginForm, CheckingAccountForm, SavingAccountForm, LoanAccountForm, TransferForm, AddMoneyForm, InsuranceForm
from django.urls import reverse_lazy
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, CheckingAccount, SavingAccount, LoanAccount, Account, StudentLoan, PersonalLoan, HomeLoan, Transaction, HomeInsurance, Insurance
from django.utils import timezone
from django.core.cache import cache
import random
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from datetime import datetime
from django.db import transaction
from decimal import Decimal

# Constants for OTP generation
OTP_LENGTH = 6
OTP_EXPIRY_SECONDS = 180  # 3 minutes
def generate_otp():
    """Generate a random OTP."""
    return ''.join(random.choices('0123456789', k=OTP_LENGTH))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect(reverse_lazy('login'))
        # else:
        #     print(form.errors)
    else:
        # print(form.errors)
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or homepage
                print("login success!")
                messages.success(request, 'Login successful!')
                return redirect('user_account')
                # return render(request, 'user_account.html', {'user': user})
            else:
                # Authentication failed
                print("Error in login")
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            otp = request.POST.get('otp')
            if otp is None:
                otp_value = generate_otp()
                cache_key = f"password_reset_otp_{request.user.id}"
                cache.set(cache_key, otp_value, OTP_EXPIRY_SECONDS)
                messages.success(request, "Your otp is: "+otp_value+" It is valid for 180 seconds")
                return render(request, 'registration/forgot_password.html', {'show_otp': True, 'otp_value': otp_value})
            submitted_otp = request.POST.get('otp', '')
            print("submitted otp is "+ submitted_otp)
            cache_key = f"password_reset_otp_{request.user.id}"
            cached_otp = cache.get(cache_key)
            # print("Cached opt is" + cached_otp)
            if cached_otp is None or submitted_otp != cached_otp:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('forgot_password')  # Redirect back to transfer page

            if request.method == 'POST':
                form = PasswordChangeForm(user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  # Important to update the session
                    messages.success(request, 'Your password has been changed successfully.')
                    return redirect('login')
            else:
                form = PasswordChangeForm(request.user)
            return render(request, 'registration/password_change_form.html', {'form': form})
        else:
            messages.error(request, 'Email address not found.')
            return redirect('forgot_password')
    else:
        return render(request, 'registration/forgot_password.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    print("Logout Success")
    messages.success(request, 'Logout successful!')
    return redirect('home')  # Redirect to the home page after logout

@login_required
def user_account(request):
    user = request.user
    # Query Customer model to get the corresponding customer
    try:
        customer = CustomUser.objects.get(id=user.id)
    except Customer.DoesNotExist:
        # Handle the case where customer doesn't exist
        return render(request, 'error.html', {'message': 'Customer data not found for this user.'})

    # Check if the user already has checking, savings, and loan accounts
    has_checking_account = Account.objects.filter(cust_id_id=user.id, account_type='C').exists()
    has_saving_account = Account.objects.filter(cust_id_id=user.id,account_type='S').exists()
    has_loan_account = Account.objects.filter(cust_id_id=user.id, account_type='L').exists()

    # Render the user account page with options to create missing accounts
    return render(request, 'user_account.html', {
        'customer': customer,
        'has_checking_account': has_checking_account,
        'has_saving_account': has_saving_account,
        'has_loan_account': has_loan_account
    })

@login_required
def create_checking_account(request):
    account_exists = False  # Flag to indicate if account exists

    # Check if the account already exists for the logged-in user
    try:
        account = Account.objects.get(cust_id=request.user, account_type='C')
        account_exists = True
    except Account.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = CheckingAccountForm(request.POST)
        if form.is_valid():
            # Get or create the Account object for the logged-in user with account_type 'C'
            # customer = CustomUser.objects.get(cust_id=request.user.id)
            user = CustomUser.objects.get(id=request.user.id)
            print(user)
            # street = user.street
            city = user.city
            state = user.state
            zipcode = user.zipcode
            if not account_exists:
                account= Account.objects.create(cust_id_id=request.user.id, account_type='C', city=city, state=state, zipcode=zipcode)
                print(account)
                # Create a CheckingAccount record linked to the created or retrieved Account object
                checking_account = form.save(commit=False)
                checking_account.account = account
                checking_account.save()
            
                return redirect('user_account')  # Redirect to user account page after creating the account
    else:
        form = CheckingAccountForm()
    return render(request, 'create_account.html', {
        'form': form,
        'account_exists': account_exists,
        'account': account if account_exists else None,
    })

def create_saving_account(request):
    account_exists = False  # Flag to indicate if account exists

    # Check if the account already exists for the logged-in user
    try:
        account = Account.objects.get(cust_id=request.user, account_type='S')
        account_exists = True
    except Account.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = SavingAccountForm(request.POST)
        if form.is_valid():
            # Get or create the Account object for the logged-in user with account_type 'S'
            # customer = CustomUser.objects.get(cust_id=request.user.id)
            user = CustomUser.objects.get(id=request.user.id)
            print(user)
            # street = user.street
            city = user.city
            state = user.state
            zipcode = user.zipcode
            if not account_exists:
                account = Account.objects.create(cust_id_id=request.user.id, account_type='S', city=city, state=state, zipcode=zipcode)
                print(account)
                # Create a CheckingAccount record linked to the created or retrieved Account object
                saving_account = form.save(commit=False)
                saving_account.account = account
                saving_account.save()
            
                return redirect('user_account')  # Redirect to user account page after creating the account
    else:
        form = SavingAccountForm()
    return render(request, 'create_account.html', {
        'form': form,
        'account_exists': account_exists,
        'account': account if account_exists else None,
    })

def create_loan_account(request):
    # Logic to create a loan account for the user
    # Redirect back to user account page after creation
    return redirect('user_account')

@login_required
def checking_account_details(request):
    # Logic to fetch and display checking account details
    print(request.user.id)
    account = Account.objects.get(cust_id_id=request.user.id, account_type='C')
    print(account)
    checking_account = CheckingAccount.objects.get(account_id = account.id)
    print(checking_account.service_charge)
    return render(request, 'account_details.html', {'account': account,'checking_account': checking_account})

def saving_account_details(request):
    print(request.user.id)
    account = Account.objects.get(cust_id_id=request.user.id, account_type='S')
    savings_account = SavingAccount.objects.get(account_id = account.id)
    return render(request, 'account_details.html', {'account': account, 'saving_account': savings_account})

def loan_account_details(request):
    print(request.user.id)
    account = Account.objects.get(cust_id_id=request.user.id, account_type='L')
    loan_account = LoanAccount.objects.get(account_id = account.id)
    home_loan_account = HomeLoan.objects.get(account_id = account.id)
    has_insurance = HomeInsurance.objects.filter(home_loan_id_id=home_loan_account.home_loan_id).exists()
    return render(request, 'account_details.html', {'account': account, 'loan_account': loan_account, 'insurance_exists': has_insurance})

@transaction.atomic
def apply_loan_account(request):
    if request.method == 'POST':
        # loan_type = request.POST.get('loan_type')
        # print(loan_type)
        # if loan_type == 'SL':  # Student Loan
        #     form1 = LoanAccountForm(request.POST)
        # elif loan_type == 'PL':  # Personal Loan
        #     form1 = PersonalLoanForm(request.POST)
        # elif loan_type == 'HL':  # Home Loan
        #     form1 = HomeLoanForm(request.POST)
        # else:
        #     form1 = None
        form = LoanAccountForm(request.POST)
        print(form)
        account, _ = Account.objects.get_or_create(
                cust_id=request.user,
                account_type='L',
                city=request.user.city,
                state=request.user.state,
                zipcode=request.user.zipcode
            )
        print(account)
        if form.is_valid():
            loan_type = form.cleaned_data['loan_type']
            form_data = form.save(commit=False)

            # Create an entry in the loan_account table linked to the created account
            loan_amount = form.cleaned_data['loan_amount']
            interest_rate = form.cleaned_data['loan_rate']
            loan_months = form.cleaned_data['loan_months']

            monthly_interest_rate = (interest_rate / 100) / 12
            loan_payment = loan_amount * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_months)
            loan_account, _ = LoanAccount.objects.get_or_create(
                account=account,
                loan_type=form_data.loan_type,
                loan_rate=form_data.loan_rate,
                loan_amount=form_data.loan_amount,
                loan_months=form_data.loan_months,
                loan_payment=loan_payment
            )

            # Create an entry in the corresponding loan table
            if loan_type == 'SL':  # Student Loan
                student_loan = StudentLoan.objects.create(account=account)
                # Perform additional actions specific to student loan if needed
            elif loan_type == 'PL':  # Personal Loan
                loan_purpose = form.cleaned_data['loan_purpose']
                personal_loan = PersonalLoan.objects.create(account=account, loan_purpose=loan_purpose)
                # Perform additional actions specific to personal loan if needed
            elif loan_type == 'HL':  # Home Loan
                house_built_year = int(form.cleaned_data['house_built_year'])
                year_datetime = datetime(year=house_built_year, month=1, day=1)
                home_loan = HomeLoan.objects.create(account=account, house_built_year=year_datetime)
                # Perform additional actions specific to home loan if needed

            return redirect('user_account')  # Redirect to user account page after creating the account
    else:
        form = LoanAccountForm()
    return render(request, 'apply_loan.html', {'form': form})

def get_full_account_type(abbreviated_type):
            if abbreviated_type == 'C':
                return 'Checking'
            elif abbreviated_type == 'S':
                return 'Savings'
            elif abbreviated_type == 'L':
                return 'Loan'
            else:
                return abbreviated_type  # Return the same value if not 'C', 'S', or 'L'

def fetch_account(cust_id, account_type):
    try:
        account_id = Account.objects.get(cust_id_id=cust_id, account_type=account_type)
        account = None
        if account_type == 'C':
            account = CheckingAccount.objects.get(account_id=account_id.id)
        elif account_type == 'S':
            account = SavingAccount.objects.get(account_id=account_id.id)
        elif account_type == 'L':
            account = LoanAccount.objects.get(account_id=account_id.id)
        return account
    except Exception as e:
        print(f"Error fetching account: {e}")
        return None

@login_required
def transfer_money(request):
    form = TransferForm()  # Instantiate form at the beginning of the function
    user = request.user

    # Get the user's accounts
    source_accounts = Account.objects.filter(cust_id_id=user)

    # Get unique account types
    source_account_types = source_accounts.values_list('account_type', flat=True).distinct()
    source_account_types = [account_type for account_type in source_account_types if account_type != 'L']
    # print(source_accounts)
    account_types = [
        {'value': 'C', 'label': 'Checking'},
        {'value': 'S', 'label': 'Savings'},
        {'value': 'L', 'label': 'Loan'},
    ]
    form_data = {
        'source_account_type': request.POST.get('source_account_type', ''),
        'destination_account': request.POST.get('destination_account', ''),
        'destination_account_type': request.POST.get('destination_account_type', ''),
        'amount': request.POST.get('amount', ''),
        'recepient_first_name': request.POST.get('recepient_first_name', ''),
        'recepient_last_name': request.POST.get('recepient_last_name', ''),
    }
    account_type_mapping = {account_type: get_full_account_type(account_type) for account_type in source_account_types}
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            source_account_type = transfer.source_account_type
            source_account = fetch_account(request.user, source_account_type)
            transfer.source_account_id = request.user.id
            destination_account_number = transfer.destination_account
            amount = transfer.amount
            first_name = transfer.recepient_first_name.lower()
            last_name = transfer.recepient_last_name.lower()
            # Get source and destination account types
            destination_account_type = transfer.destination_account_type
            # print(type(destination_account_number))
            # destination_account = CustomUser.objects.get(destination_account_number)
            dest_account = fetch_account(destination_account_number.cust_id_id, destination_account_type)
            
            if dest_account is None:
                form.add_error('destination_account', "Destination account does not exist.")
                return render(request, 'transfer_money.html', {'form': form, 'account_type_mapping': account_type_mapping, 'account_types': account_types, 'form_data': form_data})
            custom_user = CustomUser.objects.get(id=destination_account_number.cust_id_id)
            if custom_user.first_name.lower() != first_name or custom_user.last_name.lower() != last_name:
                form.add_error('destination_account', "Recepient Name doesn't match")
                return render(request, 'transfer_money.html', {'form': form, 'account_type_mapping': account_type_mapping, 'account_types': account_types, 'form_data': form_data})    
            # check otp
            otp = request.POST.get('otp')
            print(otp)
            if otp is None:
                otp_value = generate_otp()
                cache_key = f"money_transfer_otp_{request.user.id}"
                cache.set(cache_key, otp_value, OTP_EXPIRY_SECONDS)
                messages.success(request, "Your otp is: "+otp_value+" It is valid for 180 seconds")
                return render(request, 'transfer_money.html', {'form': form, 'account_type_mapping': account_type_mapping, 'account_types': account_types,'show_otp': True, 'otp_value': otp_value, 'form_data': form_data})
            # print(otp)
            # messages.error(request, 'Your otp is ' + otp)
            # print(otp)
            submitted_otp = request.POST.get('otp', '')
            print("submitted otp is "+ submitted_otp)
            cache_key = f"money_transfer_otp_{request.user.id}"
            cached_otp = cache.get(cache_key)
            # print("Cached opt is" + cached_otp)
            if cached_otp is None or submitted_otp != cached_otp:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('transfer_money')  # Redirect back to transfer page
            
            # Check if source account has sufficient balance
            if source_account.balance >= amount:
                # Update account balances
                source_account.balance -= amount
                dest_account.balance += amount
                source_account.save()
                dest_account.save()
                
                # Record the transaction
                transfer.source_account_type = source_account_type
                transfer.destination_account_type = destination_account_type
                transfer.save()
                messages.success(request, 'Transaction completed successfully!')
                return redirect('user_account')  # Redirect to accounts page
            else:
                # Insufficient balance
                form.add_error(None, "Insufficient balance.")
    else:
        # Assuming you have a logged-in user
        

        print(user)

    context = {
        'form': form,
        'account_type_mapping': account_type_mapping,
        'account_types': account_types,
        'form_data': form_data
    }

    return render(request, 'transfer_money.html', context)

def transaction_history(request):
    user = request.user
    print(user)
    transactions = Transaction.objects.filter(source_account_id=user.id).order_by('-timestamp')
    return render(request, 'transaction_history.html', {'transactions': transactions})

def add_money_to_account(request, account_type):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        print(request.user.id)
        if amount < 0:
            messages.error(request, "Value cannot be less than 0")
            return redirect('user_account')
        account = Account.objects.get(cust_id=request.user, account_type=account_type)
        if account_type == 'C':
            checking_account = CheckingAccount.objects.get(account_id=account.id)
            checking_account.balance += amount
            checking_account.save()
        elif account_type == 'S':
            saving_account = SavingAccount.objects.get(account_id=account.id)
            saving_account.balance += amount
            saving_account.save()
        # Add more conditions for other account types if needed

        # Redirect to account details page after adding money
        messages.success(request, "Amount added successfully!")
        return redirect('user_account')  # Update with the correct URL name for account details page
    else:
        # Redirect to the homepage if the request method is not POST
        return redirect('home')  # Update with the correct URL name for the homepage
    
def add_insurance_information(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST)
        if form.is_valid():
            # Process the form data and save to database
            # For example:
            print(request.user.id)
            
            account = Account.objects.get(cust_id=request.user, account_type='L')
            home_loan = HomeLoan.objects.get(account_id=account.id)
            yearly_ins_prem = form.cleaned_data['yearly_ins_prem']
            ins_company = form.save()
            HomeInsurance.objects.create(yearly_ins_prem=yearly_ins_prem, home_loan_id_id=home_loan.home_loan_id, company_id_id=ins_company.company_id)
            # Save to database here

            # Redirect to a success page or back to account details page
            return redirect('view_insurance_information')  # Replace with your URL name for account details page
    else:
        form = InsuranceForm()
    
    return render(request, 'add_insurance_information.html', {'form': form})

def view_insurance_information(request):
    # Retrieve insurance information from the database
    account = Account.objects.get(cust_id=request.user, account_type='L')
    home_loan = HomeLoan.objects.get(account_id=account.id)
    insurance_info = HomeInsurance.objects.get(home_loan_id_id=home_loan.home_loan_id)
    company_info = Insurance.objects.get(company_id=insurance_info.company_id_id)

    # Render the template with the insurance information
    return render(request, 'view_insurance_information.html', {'insurance_info': insurance_info, 'company_info': company_info, 'home_loan': home_loan, 'account': account})

