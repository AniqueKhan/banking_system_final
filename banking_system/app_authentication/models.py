from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, account_name, password=None, **extra_fields):
        if not account_name:
            raise ValueError('The Account Name field must be set')
        user = self.model(account_name=self.normalize_email(
            account_name), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(account_name, password, **extra_fields)

SELF_EMPLOYED_MARRIAGE_CHOICES = [('yes', 'Yes'),('no', 'No'),]
GENDER_CHOICES = [('male', 'Male'),('female', 'Female'),]
PROPERTY_AREA_CHOICES = [('urban', 'Urban'),('semi-urban', 'Semiurban'),('rural', 'Rural'),]
DEPENDENTS_CHOICES = [(0, '0'),(1, '1'),(2, '2'),(3, '3'),(4, '4'),]
EDUCATION_CHOICES = [('graduated', 'Graduate'),('not_graduated', 'Not Graduate'),]

class User(AbstractBaseUser, PermissionsMixin):
    account_name = models.CharField(max_length=30, unique=True)
    pan_number_regex = '^[A-Z]{3}P[A-Z][0-9]{4}K$'
    pan_number_validator = RegexValidator(pan_number_regex,'Account Number must be in the format ABCP1X1234K','invalid')
    pan_number = models.CharField(validators=[pan_number_validator],max_length=11,unique=True,null=False,blank=False)
    phone_regex = '^\+?1?\d{9,15}$'
    phone_validator = RegexValidator(phone_regex,'Phone number must be entered in the format: +999999999. Up to 15 digits allowed.','invalid')
    phone = models.CharField(validators=[phone_validator],max_length=17,null=True,blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    self_employed = models.CharField(max_length=3, choices=SELF_EMPLOYED_MARRIAGE_CHOICES,default=SELF_EMPLOYED_MARRIAGE_CHOICES[0])
    married = models.CharField(max_length=3, choices=SELF_EMPLOYED_MARRIAGE_CHOICES,default=SELF_EMPLOYED_MARRIAGE_CHOICES[0])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,default=GENDER_CHOICES[0])
    dependents = models.IntegerField(choices=DEPENDENTS_CHOICES,default=DEPENDENTS_CHOICES[0][0])
    education = models.CharField(max_length=13, choices=EDUCATION_CHOICES,default=EDUCATION_CHOICES[0])
    applicant_income = models.FloatField()
    co_applicant_income = models.FloatField(blank=True,null=True)
    property_area = models.CharField(max_length=10,choices=PROPERTY_AREA_CHOICES,default=PROPERTY_AREA_CHOICES[0])
    email = models.EmailField(blank=True,null=True)
    
    USERNAME_FIELD = 'account_name'
    REQUIRED_FIELDS = ['pan_number','applicant_income']

    objects = UserManager()

    def __str__(self):
        return self.account_name
