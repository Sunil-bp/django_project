from django.contrib import admin
from home.models import AppDetails ,Announcement
from django.contrib import messages
from django.contrib.auth.models import Permission
admin.site.register(Permission)
# Register your models here.
admin.site.register(AppDetails)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('author', 'announcement','date_created' ,'date_completed_by','completed','url' ,'current_announcement' )
    def save_model(self,request, obj, *args, **kwargs):
        no_of_current = Announcement.objects.filter(current_announcement="True")
        if len((no_of_current))<=2:
            messages.add_message(request, messages.INFO, f'Saving announcment  ')
            obj.save()
        else:
            obj.current_announcement = "False"
            obj.save()
            messages.add_message(request,messages.INFO, f'Cant have more than 3 active announcment ')
