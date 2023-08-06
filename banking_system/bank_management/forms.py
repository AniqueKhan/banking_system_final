from django import forms
from django.core.validators import MinValueValidator
from app_authentication.models import User
from bank_management.models import LOAN_TYPES

class LoanRequestForm(forms.Form):
    account_name = forms.CharField(max_length=100)
    pan_number = forms.CharField(max_length=100)
    loan_amount = forms.IntegerField()
    loan_amount_term = forms.IntegerField()
    loan_type = forms.ChoiceField(choices=LOAN_TYPES,initial=LOAN_TYPES[0])

    def clean(self):
        cleaned_data = super().clean()
        account_name = cleaned_data.get('account_name')
        pan_number = cleaned_data.get('pan_number')

        # Check if user with the provided account name and number exists
        try:
            user = User.objects.get(account_name=account_name, pan_number=pan_number)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid account name or pan number')

        return cleaned_data

    def clean_loan_amount(self):
        loan_amount = self.cleaned_data.get('loan_amount')
        if loan_amount > 99999999:
            raise forms.ValidationError('Loan amount cannot be greater than 99999999')
        return loan_amount
