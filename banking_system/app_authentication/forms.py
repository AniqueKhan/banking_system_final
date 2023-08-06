from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms 
from django.contrib.auth import authenticate
from bank_management.models import Branch, ACCOUNT_TYPES
from app_authentication.models import EDUCATION_CHOICES,DEPENDENTS_CHOICES,GENDER_CHOICES,PROPERTY_AREA_CHOICES,SELF_EMPLOYED_MARRIAGE_CHOICES
from app_authentication.models import User

def ForbiddenAccountName(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
                       'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_users:
        raise ValidationError(
            'This is an invalid account name, this is a reserverd word.')


def InvalidAccountName(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError(
            'This is an invalid account name, Do not user these chars: @ , - , + ')


def UniquePanNumber(value):
    if User.objects.filter(pan_number__iexact=value).exists():
        raise ValidationError('Account with this pan number already exists.')


def UniqueAccountName(value):
    if User.objects.filter(account_name__iexact=value).exists():
        raise ValidationError('Account with this account name already exists.')


class SignupForm(forms.Form):
    account_name = forms.CharField(max_length=20)

    # Pan Number Validator
    pan_number_regex = '^[A-Z]{3}P[A-Z][0-9]{4}K$'
    pan_number_validator = RegexValidator(pan_number_regex,'Pan Number must be in the format ABCPX1234K','invalid')
    pan_number = forms.CharField(validators=[pan_number_validator],max_length=11)

    # Phone Number Validator
    phone_regex = '^\+?1?\d{9,15}$'
    phone_validator = RegexValidator(phone_regex,'Phone number must be entered in the format: +999999999. Up to 15 digits allowed.','invalid')
    phone = forms.CharField(validators=[phone_validator],max_length=17,required=False)

    email = forms.EmailField()
    address = forms.CharField(max_length=100,required=False)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
    balance = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all())
    education = forms.ChoiceField(choices=EDUCATION_CHOICES,required=False)
    dependents = forms.ChoiceField(choices=DEPENDENTS_CHOICES,required=False)
    self_employed = forms.ChoiceField(choices=SELF_EMPLOYED_MARRIAGE_CHOICES,required=False)
    married = forms.ChoiceField(choices=SELF_EMPLOYED_MARRIAGE_CHOICES,required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,required=False)
    property_area = forms.ChoiceField(choices=PROPERTY_AREA_CHOICES,required=False)
    applicant_income = forms.DecimalField(max_digits=10,decimal_places=2)
    co_applicant_income = forms.DecimalField(max_digits=10,decimal_places=2,required=False)

    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    def __init__(self,*args,**kwargs):
        super(SignupForm,self).__init__(*args,**kwargs)
        self.fields['account_name'].validators.append(ForbiddenAccountName)
        self.fields['account_name'].validators.append(InvalidAccountName)
        self.fields['account_name'].validators.append(UniqueAccountName)
        self.fields['pan_number'].validators.append(UniquePanNumber) 

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords do not match. Try again'])
        return self.cleaned_data

class LoginForm(forms.Form):
    account_name = forms.CharField(max_length=30)
    pan_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)