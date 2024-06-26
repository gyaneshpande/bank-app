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
from django.contrib.auth import views as auth_views
from bank.views import CustomPasswordResetView
# from .admin import TransactionAdmin
# app_name = 'bank'

urlpatterns = [
    path('admin/analytics/', views.admin_analytics_view, name='admin_analytics'),
    path('admin/analytics1/', views.account_creation_graph, name='admin_analytics'),
    path('admin/', admin.site.urls),
    # path('bank/', include('bank.urls', namespace='bank')), 
    path('admin/transactions-per-month/', admin.site.urls, name='transactions_per_month'),
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
    path('transfer_money/', views.transfer_money, name='transfer_money'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset_form'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('add-money/<str:account_type>/', views.add_money_to_account, name='add_money_to_account'),
    path('add_insurance_information/', views.add_insurance_information, name='add_insurance_information'),
    path('view_insurance_information/', views.view_insurance_information, name='view_insurance_information'),
    path('admin/account-creation-graph/', views.account_creation_graph, name='account_creation_graph'),
]
