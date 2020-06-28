from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.


class Login_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(default=timezone.now)
    login_time = models.DateTimeField()
    log_out = models.DateTimeField(null=True, blank=True, default=None)


class Task(models.Model):
    all_prio = [
        (1,1),(2,2),(3,3),(4,4),(5,5),
    ]
    all_type =[
        ("work","work"),("project","project"),("life","life"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)
    tittle = models.CharField(max_length=30,null=False,blank=False)
    priority = models.IntegerField(choices=all_prio)
    type = models.CharField(max_length=7, choices=all_type)
    description = models.TextField(null=True, default=None, blank=True)
    notes = models.TextField(null=True, default=None, blank=True)
    ending = models.TextField(null=True, default=None, blank=True)
    tags = models.TextField(null=True, default=None, blank=True)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(blank=True, null=True)
    isparent = models.IntegerField(default=0)
    timetaken = models.DurationField(null=True, blank=True)
    temp_start = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.tittle =="":
            print("tittle is blank not saved ")
        else:
            super().save()

    def __str__(self):
        return str(self.user.username) +" : " +  str(self.tittle)

class Rules(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.CharField(max_length=30, null=False, blank=False)
    rule_no = models.IntegerField()
    notes = models.TextField(null=True, default=None, blank=True)



class Lunch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunch_in = models.DateTimeField(auto_now_add=True)
    lunch_out = models.DateTimeField(null=True, default=None, blank=True)
    create_on = models.DateField(    default=datetime.date.today)
    notes = models.TextField(null=True, default=None, blank=True)

class Break(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    break_in = models.DateTimeField(auto_now_add=True)
    break_out = models.DateTimeField(null=True, default=None, blank=True)
    create_on = models.DateField(default=datetime.date.today)
    break_tittle = models.TextField(null=True, default=None)


class Userstat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_task = models.ForeignKey(Task, on_delete=models.CASCADE,null=True)
    is_running = models.BooleanField(default=False)
    current_side_track = models.TextField(null=True, default="show_sidetrack_list")
    def __str__(self):
        return str(self.current_task)


