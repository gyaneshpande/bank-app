# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser  # Import your custom user model
from .forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages

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
                return redirect(reverse_lazy('home'))
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

