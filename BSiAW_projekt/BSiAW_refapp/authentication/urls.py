from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#from .views import CustomPasswordResetView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('enable-otp/', views.enable_otp, name='enable_otp'),
    path('dashboard/', views.role_based_redirect, name='role_redirect'),
    path('judge-dashboard/', views.judge_dashboard, name='judge_dashboard'),
    path('committee-dashboard/', views.committee_dashboard, name='committee_dashboard'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('manage-otp/', views.manage_otp, name='manage_otp'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]