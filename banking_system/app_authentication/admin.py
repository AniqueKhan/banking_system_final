from django.contrib import admin
from app_authentication.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("account_name","education","self_employed","applicant_income","dependents")
    list_editable=("applicant_income","dependents")


# Register your models here.
admin.site.register(User,UserAdmin)