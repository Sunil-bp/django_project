from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime
from django.utils import timezone



class App_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=30, null=False, blank=False)
    def __str__(self):
        return f'name : {self.app_name} '


class App_history(models.Model):
    app_name = models.ForeignKey(App_list, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='app_log')
    tittle = models.CharField(max_length=30, null=True, blank=True)
    create_on = models.DateTimeField()
    notes = models.TextField(null=True, default=None, blank=True)

    def __str__(self):
        return f'name : {self.app_name} created {self.create_on}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 500:
            output_size = (400, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)