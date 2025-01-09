from django.db import models
from app_authentication.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name

LOAN_TYPES = (('personal', 'Personal Loan'),('home', 'Home Loan'),('auto', 'Auto Loan'),('student', 'Student Loan'),('business', 'Business Loan'),('line_of_credit', 'Line of Credit'),)

class Loan(models.Model):
    loan_type = models.CharField(max_length=15, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    availed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    interest_rate = models.PositiveIntegerField(default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    paid_at = models.DateTimeField(blank=True,null=True)
    loan_status = models.CharField(max_length=15,blank=True,null=True)
    credited = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan for {self.availed_by} of amount {self.amount}"

    def get_credit_history(self):
        user = self.availed_by
        user_due_loans = Loan.objects.filter(due_at__lte=timezone.now(),availed_by=user,paid=False)
        if len(user_due_loans)==0:
            return 1
        return 0
        
    def get_loan_amount_term(self):
        return (self.due_at - self.created_at).days

    def get_pay_loan_button(self):
        account = Account.objects.filter(hold_by=self.availed_by).first()
        total_amount = self.amount + (self.amount * self.interest_rate / 100)

        if not self.paid and account:
            return account.balance >= total_amount
        
        return False
    
    def update_loan_status(self):
        user = self.availed_by
        account = Account.objects.filter(hold_by=self.availed_by).first()
        total_amount = self.amount + (self.amount * self.interest_rate / 100)
        user_pending_loans =  Loan.objects.filter(due_at__gte=timezone.now(),availed_by=user,paid=False)
        user_due_loans =  Loan.objects.filter(due_at__lte=timezone.now(),availed_by=user,paid=False)

        # The factors considered for approving the loans for the machine learning testing part are , 
        # 1 ) The account balance must be greater than the loan amount with interest
        # 2 ) The user must be self.employed and graduated
        # 3 ) The user must have zero due loans and less than two pending loans
        # 4 ) The dependents on the users must be 3 or less and his/her income should be greater than 40000

        if (account.balance >= total_amount and 
            user.self_employed and user.applicant_income >= 40000 and 
            user.dependents <=3 and len(user_due_loans) == 0 and
            len(user_pending_loans) <= 50 and user.education == "graduated"):
            self.loan_status = "Approved" # Approved
        else:
            self.loan_status = "Rejected" # Rejected
        

    def save(self, *args, **kwargs):
        if self.loan_status=="Approved" and not self.credited:
            account = Account.objects.filter(hold_by=self.availed_by)[0]
            account.balance+=self.amount
            account.save()
            self.credited=True
        super().save(*args, **kwargs)

    def clean(self):
        if self.due_at<=self.created_at:
            raise ValidationError("Due Date must be greater than created date")
        
    



ACCOUNT_TYPES = (('checking', 'Checking'),('savings', 'Savings'),('money_market', 'Money Market'),('cd', 'Certificate of Deposit'),('credit', 'Credit Card'),('loan', 'Loan'),)

class Account(models.Model):
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    hold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hold_by}"

TRANSACTION_TYPES = (('DEPOSIT', 'Deposit'),('WITHDRAWAL', 'Withdrawal'),('TRANSFER', 'Transfer'))

class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    sent_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    sent_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    description = models.CharField(max_length=255,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sent_by.hold_by.account_name} sent {self.amount} to {self.sent_to.hold_by.account_name} from {self.branch.name}'

    def save(self,*args,**kwargs):
        if self.sent_by.balance < self.amount:
            raise ValidationError(f"Insufficient Balance in {self.sent_by} account")
        self.sent_by.balance-=self.amount
        self.sent_to.balance+=self.amount
        self.sent_by.save()
        self.sent_to.save()
        super().save(*args,**kwargs)


class Notification(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=90,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}"


def create_notification_on_loan_creation(sender, instance, created, **kwargs):
    if created:
        loan = instance
        user = loan.availed_by
        message = f"You took a loan of amount \u20B9{loan.amount} from {loan.branch}. The due date is {loan.due_at.date()}."
        email_subject="Loan Request Approved"

        if loan.loan_status=="Rejected":
            message=f"Whoops! Your request for a loan of amount \u20B9{loan.amount} from {loan.branch} was rejected."
            email_subject="Loan Request Rejected"
        
        Notification.objects.create(loan=loan, user=user, message=message)

        # if user.email:
        #     send_mail(subject=email_subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

post_save.connect(create_notification_on_loan_creation, sender=Loan)

def create_notification_on_loan_payment(sender,instance,created,**kwargs):
    loan = instance
    if not created and loan.paid:
        user = loan.availed_by
        message = f"Your loan of \u20B9{loan.amount} from {loan.branch} has been paid off!"
        Notification.objects.create(loan=loan,user=user,message=message)
        if user.email:
            email_subject = "Loan Payed Off!"
            # send_mail(subject=email_subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
post_save.connect(create_notification_on_loan_payment, sender=Loan)