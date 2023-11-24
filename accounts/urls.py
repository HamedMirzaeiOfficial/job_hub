from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


app_name = 'accounts'


urlpatterns = [
     # --------------------------- Login/Logout/Password Change ------------------------
    path('login/', LoginView.as_view(), name="login"),
    path('login/sms/', sms_login_view, name="sms-login"),
    path('login/email/', email_login_view, name="email-login"),
    path('login/sms/verification/<str:phone>/', sms_login_verification_view, name="sms-login-verification"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", PasswordChangeView.as_view(), name="password-change"),

    # --------------------------- Users -----------------------------
    path('me/', ProfileView.as_view(), name="profile"),
    path('', UsersView.as_view(), name="users"),
    path('add/', AddUserView.as_view(), name="add-user"),
    path('<str:username>/', EditUserView.as_view(), name="edit-user"),
    path('<str:username>/delete/', DeleteUserView.as_view(), name="delete-user"),

    # --------------------------- User Verifcations -----------------------------
    path('verification/phone/', phone_verification, name='phone-verification'),
    path('verification/phone/check/', phone_verification_check, name='phone-verification-check'),
    path('verification/email/', email_verification, name='email-verification'),
    path('verification/email/check/', email_verification_check, name='email-verification-check'),
]