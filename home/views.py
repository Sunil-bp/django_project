from django.shortcuts import render,redirect
from home.models import AppDetails
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.http import HttpResponse
# def home(request):
#
#     context = {'apps' : AppDetails.objects.all()}
#     return render(request,'home/home.html',context )



def about(request):
    return render(request,'home/about.html',{'title':'about home'})

def user_check(user):
    return user.username in ["sunil","test"]

@login_required
@user_passes_test(user_check,login_url='/unauthorised_page/')
def advice(request):
    text ="[11:36 PM, 1/13/2020] Pikachu: Don't wait 4 anyone ever again\n\
            [11:36 PM, 1/13/2020] Pikachu: She has taken you 4 granted\n\
            [11:36 PM, 1/13/2020] Sunil: I need perspectives.   What is she feeling. .\n\
            [11:36 PM, 1/13/2020] Pikachu: And that is bad\n\
            [11:36 PM, 1/13/2020] Pikachu: Shut up\n\
            [11:37 PM, 1/13/2020] Pikachu: Dimag khrab hogya h yera\n\
            [11:37 PM, 1/13/2020] Pikachu: Ghar gya h na\n\
            [11:37 PM, 1/13/2020] Pikachu: Uske bare m mat soch"
    text_line  = text.split("\n")
    dict_send = {"chat_data":text_line}
    return render(request, "home/chat_advice.html",context=dict_send)

class AppListView(ListView):
    model = AppDetails
    template_name = 'home/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'apps'
    ordering = ['-date_created']


class AppDetailView(DetailView):
    model = AppDetails
    template_name = 'home/app_detail.html'


class AppCreateView(LoginRequiredMixin, CreateView):
    model = AppDetails
    fields = ['app_name', 'why']
    template_name = 'home/post_app.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AppUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AppDetails
    fields = ['app_name', 'why']
    template_name = 'home/post_app.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Your Blog has been updated ')
        return super().form_valid(form)

    def test_func(self):
        AppDetails = self.get_object()
        if self.request.user == AppDetails.author:
            return True
        return False


class AppDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AppDetails
    success_url = '/'

    def test_func(self):
        AppDetails = self.get_object()
        if self.request.user == AppDetails.author:
            return True
        return False
