from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns=[
  path('login',views.login_view,name='login'),
  # login
  path('logout',views.logout_view,name='logout'),
  # logout
  path('sign_up',views.signup_view,name='sign_up'),
  # registration/sign-up
  # path('change/password',views.ChangePasswordView.as_view(),name="change-password"),
  path('password_reset', views.PasswordReset.as_view(), name='password_reset'),
  path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
  path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]