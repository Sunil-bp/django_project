from home.models import Announcement

def add_variable_to_context(request):
    announcment = Announcement.objects.filter(current_announcement="True")
    if not  announcment:
        announcment = "nothing to be displayed"

    return {
        'announcment': announcment
    }