"""
URL configuration for banking_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bank import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', views.user_account, name='user_account'), 
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_checking_account/', views.create_checking_account, name='create_checking_account'),
    path('create_saving_account/', views.create_saving_account, name='create_saving_account'),
    path('apply_loan_account/', views.apply_loan_account, name='apply_loan_account'),
    path('create_checking_account/', views.create_checking_account, name='create_checking_account'),
    path('checking_account_details/', views.checking_account_details, name='checking_account_details'),
    path('saving_account_details/', views.saving_account_details, name='saving_account_details'),
    path('loan_account_details/', views.loan_account_details, name='loan_account_details'),
]
