from django.contrib import admin

# Register your models here.


from app_log.models import App_list,App_history


admin.site.register(App_list)
admin.site.register(App_history)