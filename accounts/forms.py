from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.forms import (PasswordChangeForm,
                                       ReadOnlyPasswordHashField)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (PasswordChangeForm,
                                       ReadOnlyPasswordHashField)
from django.core.exceptions import ValidationError
# from .models import User
from django.core import validators

class RegistrationForm(UserCreationForm):
  email=forms.EmailField(required=True)
  class Meta:
    model=User
    fields=['username','email','password1','password2']

    
class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput({'placeholder': "گذرواژه فعلی", 'id': "old_password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput({'placeholder': "گذرواژه جدید", 'id': "new_password1"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput({'placeholder': "تکرار گذرواژه", 'id': "new_password2"}))

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("گذرواژه فعلی تان اشتباه وارد شد. لطفا دوباره تلاش کنید")
        return old_password


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'is_active', 'is_superuser','is_staff')