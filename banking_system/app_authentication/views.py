from django.shortcuts import render,redirect
from app_authentication.forms import SignupForm
from app_authentication.models import User
from bank_management.models import Account
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
# Create your views here.


def signup(request):
    if request.method =="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account_name = form.cleaned_data.get("account_name")
            pan_number = form.cleaned_data.get("pan_number")
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            co_applicant_income = form.cleaned_data.get('co_applicant_income')
            applicant_income = form.cleaned_data.get('applicant_income')
            property_area = form.cleaned_data.get('property_area')
            gender = form.cleaned_data.get('gender')
            married = form.cleaned_data.get('married')
            self_employed = form.cleaned_data.get('self_employed')
            dependents = form.cleaned_data.get('dependents')
            education = form.cleaned_data.get('education')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            # User Creation
            user = User.objects.create_user(
                account_name=account_name,
                pan_number=pan_number,
                self_employed=self_employed,
                married=married,
                education=education,
                gender=gender,
                applicant_income=applicant_income,
                property_area=property_area,
                dependents=dependents,
                password=password)
            
            if phone:user.phone=phone
            if email:user.email=email
            if address:user.address=address
            if co_applicant_income:user.co_applicant_income=co_applicant_income

            user.save()

            # Account Creation
            branch = form.cleaned_data.get('branch')
            balance = form.cleaned_data.get('balance')
            account_type = form.cleaned_data.get('account_type')

            account = Account.objects.create(account_type=account_type,branch=branch,hold_by=user)

            if balance:account.balance=balance

            account.save()
            login(request, user)
            return redirect("loans")


    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            account_name = form.cleaned_data['account_name']
            password = form.cleaned_data['password']
            pan_number = form.cleaned_data['pan_number']
            queryset = User.objects.filter(account_name=account_name,pan_number=pan_number)
            if len(queryset)==0:
                form.add_error(None, 'Invalid login credentials')
            else:
                login(request,queryset[0])
                return redirect('loans')
            
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect("index")
#     if request.method=="POST":
#         account_name = request.POST.get("account_name")
#         pan_number = request.POST.get("pan_number")
#         password = request.POST.get("password")
#         user = authenticate(request,account_name=account_name,pan_number=pan_number,password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("core:home")
#         else:
#             context = {
#                 "error":"Invalid Credentials"
#             }
#             return render(request, "login.html",context)
#     else:
#         return render(request, "login.html")
