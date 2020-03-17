from django.urls import path
from . import views
from .views import (
    AppListView,
    AppDetailView,
    AppCreateView,
    AppUpdateView,
    AppDeleteView
)


urlpatterns = [
    path('', AppListView.as_view(), name='main-home'),

    path('app/<int:pk>/', AppDetailView.as_view(), name='app-detail'),
    path('app/new/', AppCreateView.as_view(), name='app-create'),
    path('app/<int:pk>/update/', AppUpdateView.as_view(), name='app-update'),
    path('app/<int:pk>/delete/', AppDeleteView.as_view(), name='app-delete'),
    path('about/', views.about, name='home-about'),
    path('advice/', views.advice, name='advice'),
]
