# _*_ encoding: utf-8
#用户管理相关表单过滤
#变量名要与表单key一致

from django import forms
from captcha.fields import CaptchaField

from users.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
     email = forms.EmailField(required=True)
     password = forms.CharField(required=True, min_length=5)
     captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetPasswordForm(forms.Form):
     email = forms.EmailField(required=True)
     captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ResetUserForm(forms.Form):
     password  = forms.CharField(required=True, min_length=5)
     password_check = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class ModifyPasswordForm(forms.Form):
     password1 = forms.CharField(required=True, min_length=5)
     password2 = forms.CharField(required=True, min_length=5)


class UserCenterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']





