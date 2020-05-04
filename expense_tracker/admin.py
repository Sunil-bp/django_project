from django.contrib import admin

from expense_tracker.models import User_account,User_account_set_up
# Register your models here.

admin.site.register(User_account)
admin.site.register(User_account_set_up)
