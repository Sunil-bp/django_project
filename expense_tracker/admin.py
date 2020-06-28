from django.contrib import admin
from expense_tracker.models import Subcategory,Category,FinanceProfile,Account,\
    AccountCategory,AccountSubcategory,ExpenseRecord,ExpenseTransfer
# Register your models here.

admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(FinanceProfile)
admin.site.register(Account)
admin.site.register(AccountCategory)
admin.site.register(AccountSubcategory)
admin.site.register(ExpenseRecord)
admin.site.register(ExpenseTransfer)