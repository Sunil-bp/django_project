from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from expense_tracker.models import Subcategory,Category,FinanceProfile,Account,\
    AccountCategory,AccountSubcategory,ExpenseRecord,ExpenseTransfer
from django.contrib.auth.models import User
from users.models import Profile

from expense_tracker.serializers  import SubcategorySerializer,CategorySerializer,FinanceProfileSerializer,AccountSerializer,\
    AccountCategorySerializer,AccountSubcategorySerializer,ExpenseRecordSerializer,ExpenseTransferSerializer,UserSerializer,UserLoginSerializer,ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

##auth jwt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

#Create your views here.


class ProfileImage(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = Profile.objects.filter(user=user)
        print(">>>>>>>>>>>>")
        print(profile)
        return profile
    serializer_class = ProfileSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return ExpenseRecord.objects.filter(profile = profile)
    serializer_class = ExpenseRecordSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte','exact'],
                        "amount":['gte', 'lte','exact'],
                        'account':['exact'],
                        'category': ['exact'],
                        'sub_category': ['exact'],
                        }
    search_fields =['note',]
    ordering_fields ='__all__'
    ordering = ['-create_on']
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        profile = FinanceProfile.objects.get(user=user)
        return ExpenseRecord.objects.filter(profile=profile)
    queryset = ExpenseRecord.objects.all()
    serializer_class = ExpenseRecordSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryList(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SubcategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountSubcategorySerializer
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return AccountSubcategory.objects.filter(profile = profile)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryAccountList(generics.ListCreateAPIView):
    serializer_class = AccountCategorySerializer
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return AccountCategory.objects.filter(profile = profile)

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class AccountList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return Account.objects.filter(profile = profile)
    serializer_class = AccountSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return Account.objects.filter(profile = profile)
    serializer_class = AccountSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseTransferList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return ExpenseTransfer.objects.filter(profile = profile)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'create_on': ['gte', 'lte', 'exact'],
                        "amount": ['gte', 'lte', 'exact'],

                        }
    search_fields = ['note', ]
    ordering_fields = '__all__'
    ordering = ['-create_on']
    serializer_class = ExpenseTransferSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ExpenseTransferDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.get(user=user)
        return ExpenseTransfer.objects.filter(profile = profile)
    serializer_class = ExpenseTransferSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProfileList(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.filter(user=user)
        return profile
    serializer_class = FinanceProfileSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user = self.request.user
        profile  = FinanceProfile.objects.filter(user=user)
        return profile
    serializer_class = FinanceProfileSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class UserList(generics.ListCreateAPIView):
    def get_queryset(self):
        user  = User.objects.filter(username=self.request.user.username)
        return user
    serializer_class = UserSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# @login_required
# def profile(request):
#     return render(request, 'expense_tracker/profile.html')
#
def angular(request):
    return render(request, 'expense_tracker/expense_home.html', {'title': 'expense profile'})

def expense_tracker(request):
    return render(request, 'expense_tracker/index.html')