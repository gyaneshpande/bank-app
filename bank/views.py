# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser  # Import your custom user model
from .forms import RegistrationForm, LoginForm, CheckingAccountForm, SavingAccountForm, LoanAccountForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, CheckingAccount, SavingAccount, LoanAccount, Account, StudentLoan, PersonalLoan, HomeLoan

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

def home(request):
    return render(request, 'base.html')

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
    return render(request, 'account_details.html', {'account': account, 'loan_account': loan_account})

def apply_loan_account(request):
    if request.method == 'POST':
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

            # Create an entry in the accounts table with account_type 'L'
            # account = Account.objects.create(
            #     cust_id=request.user,
            #     account_type='L',
            #     city=request.user.city,
            #     state=request.user.state,
            #     zipcode=request.user.zipcode
            # )

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
                personal_loan = PersonalLoan.objects.create(account=account, **form_data.__dict__)
                # Perform additional actions specific to personal loan if needed
            elif loan_type == 'HL':  # Home Loan
                home_loan = HomeLoan.objects.create(account=account, **form_data.__dict__)
                # Perform additional actions specific to home loan if needed

            return redirect('user_account')  # Redirect to user account page after creating the account
    else:
        form = LoanAccountForm()
    return render(request, 'apply_loan.html', {'form': form})

