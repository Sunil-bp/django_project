from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from expense_tracker.models import Subcategory,Category,FinanceProfile\
    ,Account,AccountCategory,AccountSubcategory,ExpenseRecord,ExpenseTransfer


@receiver(post_save, sender=FinanceProfile)
def update_user_set_up(sender, instance, **kwargs):
    category_querry = Category.objects.filter(pre_add=True)
    for category in category_querry:
        ac = AccountCategory.objects.create(profile= instance,category=category)
        ac.save()
    sub_category_querry = Subcategory.objects.filter(pre_add=True)
    for sub_category in sub_category_querry:
        sac = AccountSubcategory.objects.create(profile=instance, subcategory=sub_category)
        sac.save()



@receiver(pre_save, sender=ExpenseRecord)
def add_expense(sender, instance, **kwargs):
    ac = Account.objects.get(profile= instance.profile,account_name=instance.account.account_name)
    if instance.type=="income":
        ac.balance += instance.amount
    else:
        ac.balance -= instance.amount
    ac.save()

@receiver(post_save, sender=ExpenseTransfer)
def expense_tranfer(sender, instance, **kwargs):
    ac = Account.objects.get(profile= instance.profile,account_name=instance.from_account.account_name)
    ac.balance -= instance.amount
    ac.save()

    ac = Account.objects.get(profile=instance.profile, account_name=instance.to_account.account_name)
    ac.balance += instance.amount
    ac.save()
