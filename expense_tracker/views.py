from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from expense_tracker.models import User_account,User_account_set_up
from .forms import UserExpenseCreateForm,UserExpenseSetUpForm


# Create your views here.


@login_required
def profile(request):
    if request.method == 'POST':
        existing_user = User_account_set_up.objects.filter(user=request.user).first()
        if existing_user:
            print("user account is already there")
        else:
            print("crating user account for first time  ")
            existing_user = User_account_set_up(user=request.user)
        user_account = User_account(user=request.user)
        u_form = UserExpenseCreateForm(request.POST, instance=user_account)
        p_form = UserExpenseSetUpForm(request.POST,instance=existing_user)
        if u_form.is_valid() and p_form.is_valid():
            p_form.save()
            u_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('expense-tracker-home')
    else:
        # if existing then use the existing user account
        existing_user = User_account_set_up.objects.filter(user=request.user).first()
        existing_user_accounts = User_account.objects.filter(user=request.user)
        saving= None
        all_accounts = None
        if existing_user:
            print("user account is already there")
            saving = existing_user.savings
            all_accounts  = User_account.objects.filter(user=request.user)

        else:
            print("crating user account for first time  ")
            existing_user = User_account_set_up(user=request.user)
        user_account = User_account(user=request.user)
        #set up is just one  but account can be many
        u_form = UserExpenseCreateForm(instance=user_account)
        p_form = UserExpenseSetUpForm(instance=existing_user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'saving': saving,
        'all_account': all_accounts,

    }

    return render(request, 'expense_tracker/profile.html', context)

def expense_tracker(request):
    return render(request, 'expense_tracker/expense_home.html', {'title': 'expense profile'})
