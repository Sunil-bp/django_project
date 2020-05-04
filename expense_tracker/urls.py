from django.urls import path
from . import views



urlpatterns = [
    path('', views.expense_tracker, name='expense-tracker-home'),
    path('profile/', views.profile, name='expense-tracker-profile'),
]