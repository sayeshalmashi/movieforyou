from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout ,views as auth_views
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm , PasswordResetForm
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm , LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
# from django.contrib.auth import  get_user_model
from django.contrib.auth.views import (PasswordChangeView,PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import reverse_lazy
from .forms import *

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            userinput = request.POST['username']
            try:
                username = User.objects.get(email=userinput).username
            except User.DoesNotExist:
                username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.add_message(request,messages.SUCCESS,'Login was successful')
                return redirect('/')
            else:
                 messages.add_message(request,messages.ERROR,'The desired person was not found')
        return render(request, "registration/login.html")
    else:
          return redirect('/')

@login_required
def logout_view(request):
  logout(request)
  return redirect('/')

def signup_view(request):
  if request.method=='POST':
    form=RegistrationForm(request.POST)
    if form.is_valid():
      user= form.save()
      login(request,user)
      return redirect('/')
  else:
    form= RegistrationForm()
  
  context={'form': form}
  return render(request,'registration/sign_up.html',context)


# Customized password change and reset views

# class ChangePasswordView(PasswordChangeView):
#     template_name = 'registration/change_password.html'
#     success_url = reverse_lazy('account:user-setting')
#     form_class = ChangePasswordForm


class PasswordReset(PasswordResetView):
    template_name="registration/password_reset_form.html"
    success_url=reverse_lazy("accounts:password_reset_done")

class PasswordResetDone(PasswordResetDoneView):
    template_name="registration/password_reset_done.html"
    success_url=reverse_lazy("accounts:password_reset_confirm")

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name="registration/password_reset_confirm.html"
    success_url=reverse_lazy("accounts:password_reset_complete")

class PasswordResetComplete(PasswordResetCompleteView):
    template_name="registration/password_reset_complete.html"
    