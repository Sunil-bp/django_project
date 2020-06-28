from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path(r'token-auth/', obtain_jwt_token),
    path('auth/', views.UserLoginAPIView.as_view(), name='expense-tracker-auth'),
    path('expense/', views.ExpenseList.as_view(), name='expense-tracker-list'),
    path('expense/<int:pk>/', views.ExpenseDetail.as_view(), name='expense-tracker-detail'),
    path('category/', views.CategoryList.as_view(), name='expense-tracker-category'),
    path('subcategory/', views.SubcategoryList.as_view(), name='expense-tracker-subcategory'),
    path('categoryaccount/', views.CategoryAccountList.as_view(), name='expense-tracker-category-account'),
    path('subcategoryaccount/', views.SubcategoryAccountList.as_view(), name='expense-tracker-subcategory-account'),
    path('account/', views.AccountList.as_view(), name='expense-tracker-account'),
    path('account/<int:pk>/', views.AccountDetail.as_view(), name='expense-tracker-account-details'),
    path('expensetransfer/', views.ExpenseTransferList.as_view(), name='expense-tracker-tansfer'),
    path('expensetransfer/<int:pk>/', views.ExpenseTransferDetail.as_view(), name='expense-tracker-transfer-details'),
    path('profile/', views.ProfileList.as_view(), name='expense-tracker-profile'),
    path('user/', views.UserList.as_view(), name='expense-tracker-user'),
    path('user-image/', views.ProfileImage.as_view(), name='expense-tracker-user-image'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='expense-tracker-profile-details'),
]
urlpatterns = format_suffix_patterns(urlpatterns)