from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Category(models.Model):
    category = [
        ("income", "income"), ("expense", "expense"),
    ]
    category_name = models.CharField(max_length=30, null=False, blank=False)
    type = models.CharField(max_length=9,choices=category)
    pre_add = models.BooleanField(default=False)
    icon = models.CharField(max_length=20,default="home")
    def __str__(self):
        return str(self.category_name) + " : "+ str(self.pre_add)

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=30, null=False, blank=False)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    pre_add = models.BooleanField(default=False)
    def __str__(self):
        return str(self.subcategory_name) + " : "+ str(self.parent.category_name)+ " : "+ str(self.pre_add)

class FinanceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    create_on = models.DateField(default=datetime.date.today)
    def __str__(self):
        return f'{self.user} account {self.user.username}'


class Account(models.Model):
    profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=30, null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.profile.user} account  {self.account_name} : balance {self.balance}'


class ExpenseRecord(models.Model):
    record_type = [
        ("income", "income"), ("expense", "expense"),
    ]
    profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE)
    account =  models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    create_on = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=7, choices=record_type)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.account}  : {self.amount} :  {self.note}'




class ExpenseTransfer(models.Model):
    profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField(null=False, blank=False)
    from_account = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True,related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True,related_name='to_account')
    note = models.CharField(max_length=30, null=False, blank=False)



    def __str__(self):
        return f'{self.profile} :  {self.amount} :   {self.from_account}  {self.to_account}'


class AccountCategory(models.Model):
    profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user}   {self.category} '


class AccountSubcategory(models.Model):
    profile = models.ForeignKey(FinanceProfile, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user}  {self.subcategory} '


