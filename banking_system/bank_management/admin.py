from django.contrib import admin
from bank_management.models import *
# Register your models here.
class LoanAdmin(admin.ModelAdmin):
    list_display = ("availed_by","due_at","paid","paid_at","loan_status")
    list_editable=("paid",)
admin.site.register(Loan,LoanAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ("hold_by","balance")
    list_editable=("balance",)

admin.site.register(Account,AccountAdmin)
admin.site.register((Branch,Transaction,Notification))