from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

class AppDetails(models.Model):
    app_name = models.CharField(max_length=30)
    why = models.TextField()
    date_created = models.DateField(default = timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.app_name

    def get_absolute_url(self):
        return reverse('app-detail', kwargs={'pk': self.id})

class Announcement(models.Model):
    work_done = (
        ('True', 'Work completed'),
        ('False', 'Work not done'),
    )
    current_value = (
        ('True', 'displayed'),
        ('False', 'not displayed'),
    )
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    announcement = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    date_completed_by = models.DateField()
    completed =models.CharField(max_length=5, choices=work_done)
    url = models.CharField(max_length=50)
    current_announcement = models.CharField(max_length=5, choices=current_value,default = "False")
    def __str__(self):
        return self.announcement

