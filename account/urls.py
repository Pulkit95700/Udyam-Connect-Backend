from django.contrib import admin
from django.urls import path, include
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, CompanyListView, CompanyDetailView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('changepassword/', UserChangePasswordView.as_view(), name="change_password"),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name="send_reset_email"),
    path('reset-password/<uid>/<token>', UserPasswordResetView.as_view(), name="send_reset_email"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('companies', CompanyListView.as_view(), name="company_list"),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name="company_detail")

]   
