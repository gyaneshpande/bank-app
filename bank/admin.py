from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bank.models import Account, Customer, CheckingAccount, SavingAccount, LoanAccount, HomeInsurance, HomeLoan, StudentLoan, PersonalLoan, Insurance, University, StudentUniversity, CustomUser

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_type', 'cust_id')
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'first_name', 'last_name')
    
class LoanAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_no', 'loan_type')
    
# Register your models here.
admin.site.register(Customer, CustomerAdmin)
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
