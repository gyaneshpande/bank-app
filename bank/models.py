from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
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

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    street = models.CharField(max_length=30, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=2, null=False, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=10, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cust_id'], name='unique_customer')
        ]

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('S', 'Saving'),
        ('C', 'Checking'),
        ('L', 'Loan'),
    )
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=2, null=False, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=10, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cust_id', 'account_type'], name='unique_customer_account_type')
        ]
    
    def __str__(self):
        return f'Account id {self.id}, Account type {self.account_type}'

class SavingAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    account_no = models.AutoField(primary_key=True)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class CheckingAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    account_no = models.AutoField(primary_key=True)
    service_charge = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class LoanAccount(models.Model):
    LOAN_TYPE_CHOICES = (
        ('HL', 'Home Loan'),
        ('SL', 'Student Loan'),
        ('PL', 'Personal Loan'),
    )
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    account_no = models.AutoField(primary_key=True)
    loan_type = models.CharField(max_length=2, null=False, choices=LOAN_TYPE_CHOICES)
    loan_rate = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    loan_months = models.IntegerField(null=False)
    loan_payment = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date_opened = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('account_no', 'loan_type')
    
    def clean(self):
        # Check if the associated Account instance has the correct account type
        if self.account.account_type != 'L':
            raise ValidationError("The parent Account must have an account type of 'L' or 'Loan'.")

class PersonalLoan(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    pers_loan_id = models.AutoField(primary_key=True)
    loan_purpose = models.CharField(max_length=100, null=False)

class StudentLoan(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    stu_loan_id = models.AutoField(primary_key=True)

class University(models.Model):
    uni_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=50, null=False, unique=True)

class StudentUniversity(models.Model):
    STUDENT_TYPE_CHOICES = (
        ('U', 'Undergraduate'),
        ('G', 'Graduate'),
    )
    student_id = models.AutoField(primary_key=True)
    graduation_date = models.DateField(null=False) # handle month and  year
    student_type = models.CharField(max_length=1, null=False, choices=STUDENT_TYPE_CHOICES)
    uni_id = models.ForeignKey(University, on_delete=models.CASCADE)
    stu_loan_id = models.ForeignKey(StudentLoan, on_delete=models.CASCADE)

class Insurance(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, null=False)
    street = models.CharField(max_length=30, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=2, null=False, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=10, null=False)


class HomeLoan(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    home_loan_id = models.AutoField(primary_key=True)
    house_built_year = models.DateField(null=False) # handle for year

    def get_year(self):
        return self.house_built_year.year


class HomeInsurance(models.Model):
    home_ins_acc_no = models.AutoField(primary_key=True)
    yearly_ins_prem = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    company_id = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    home_loan_id = models.ForeignKey(HomeLoan, on_delete=models.CASCADE)
    
class CustomUser(AbstractUser):
    street = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=2, null=True, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=10, null=True)

    class Meta:
    # Add the unique_together constraint to ensure that usernames are unique
        unique_together = ('username',)

    # Define unique related_name attributes for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Provide a unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Provide a unique related_name
    )

@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            first_name=instance.first_name,
            last_name=instance.last_name,
            street=instance.street,
            city=instance.city,
            state=instance.state,
            zipcode=instance.zipcode
        )

