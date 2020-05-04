from django import forms
from expense_tracker.models import User_account,User_account_set_up


class UserExpenseCreateForm(forms.ModelForm):

    class Meta:
        model = User_account
        fields = [ 'account_type','balance']


class UserExpenseSetUpForm(forms.ModelForm):
    class Meta:
        model = User_account_set_up
        fields = [ 'default_view','fat_shamming']

