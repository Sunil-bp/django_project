from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('applist/', views.Applist.as_view(), name='App-list'),
    path('applist/<int:pk>/', views.ApplistDetail.as_view(), name='Applist-detail'),
    path('apphistory/', views.AppHistorylist.as_view(), name='AppHistorylist'),
    path('apphistory/<int:pk>/', views.AppHistoryDetail.as_view(), name='AppHistoryDetail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)