from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User_account,User_account_set_up



@receiver(post_save, sender=User_account)
def update_user_set_up(sender, instance, **kwargs):
    existing_user = User_account_set_up.objects.filter(user=instance.user).first()
        # update(saving=self.instance.balance)
    existing_user.savings +=instance.balance
    existing_user.save()
