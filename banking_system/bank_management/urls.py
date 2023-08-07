from django.urls import path
from bank_management.views import *

urlpatterns = [
    # path("",index,name="index"),
    path("my-profile",my_profile,name='my-profile'),
    path("branches",branches,name='branches'),
    path("branch/<int:pk>",branch_detail,name='branch-detail'),
    path("add-balance",add_balance,name='add-balance'),
    path('loans/<int:loan_pk>/pay_loan/', pay_loan, name='pay-loan'),
    path("",loans,name='loans'),
    path("loan-request",loan_request,name='loan-request'),
    path("notifications",notifications,name='notifications'),
    path("notifications/<notification_id>/delete",delete_notification,name='delete-notification'),
]