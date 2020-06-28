from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from app_log.serializers  import AppListserializers,Apphistoryserializers
from app_log.models import App_list,App_history


class Applist(generics.ListCreateAPIView):
    serializer_class = AppListserializers
    queryset = App_list.objects.all()

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ApplistDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = App_list.objects.all()
    serializer_class = AppListserializers
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class AppHistorylist(generics.ListCreateAPIView):
    serializer_class = Apphistoryserializers
    queryset = App_history.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte', 'exact'],
                        'app_name': ['exact'],
                        }
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class AppHistoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = App_history.objects.all()
    serializer_class = Apphistoryserializers
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
