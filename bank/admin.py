from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bank.models import Account, Customer, CheckingAccount, SavingAccount, LoanAccount, HomeInsurance, HomeLoan, StudentLoan, PersonalLoan, Insurance, University, StudentUniversity, CustomUser, Transaction
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from .models import Account
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_type', 'cust_id', 'analytics_link')
    
    def analytics_link(self, obj):
        url = reverse('admin_analytics')
        return format_html('<a href="{}" target="_blank">View Analytics</a>', url)

    analytics_link.short_description = 'Analytics'
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'first_name', 'last_name')
    
class LoanAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_no', 'loan_type')
    
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'first_name', 'last_name', 'analytics_link')

    def analytics_link(self, obj):
        url = reverse('admin_analytics')
        return format_html('<a href="{}" target="_blank">View Analytics</a>', url)

    analytics_link.short_description = 'Analytics'

# admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
admin.site.register(Customer, CustomUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CheckingAccount)
admin.site.register(SavingAccount)
admin.site.register(LoanAccount, LoanAdmin)
admin.site.register(HomeInsurance)
admin.site.register(HomeLoan)
admin.site.register(StudentLoan)
admin.site.register(PersonalLoan)
admin.site.register(Insurance)
admin.site.register(University)
admin.site.register(StudentUniversity)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Transaction)
