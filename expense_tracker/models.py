from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=30, null=False, blank=False)
    balance = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.user.username} account : balance {self.balance}'

class User_account_set_up(models.Model):
    default_view_options = [
        ("daily", "daily"), ("weekly", "weekly"), ("monthly", "monthly"), ("yearly", "yearly"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_view = models.CharField(max_length=9,choices=default_view_options)
    fat_shamming = models.BooleanField(default=False)
    savings =  models.IntegerField(null=False, blank=False,default=0)


    def __str__(self):
        return f'{self.user.username} account : saving {self.savings}'
