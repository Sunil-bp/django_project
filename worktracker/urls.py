from django.urls import path
from . import views

urlpatterns = [
    path('', views.worktracker, name='worktracker-home'),
    path('test', views.test, name='test-home'),
]
