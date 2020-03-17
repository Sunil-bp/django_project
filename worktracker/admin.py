from django.contrib import admin
from worktracker.models import Login_data,Task,Userstat,Lunch,Break,Rules
# Register your models here.

admin.site.register(Login_data)
admin.site.register(Task)
admin.site.register(Userstat)
admin.site.register(Lunch)
admin.site.register(Break)
admin.site.register(Rules)
