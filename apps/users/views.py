from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetUserForm
from utils.email_send import send_register_email

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
           user = UserProfile.objects.get(Q(username=username) | Q(email=username) )
           if user.check_password(password):
                return user
        except Exception as e:
           return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
      def get(self, request):
          register_form = RegisterForm()
          return render(request, "register.html", {'register_form':register_form})
      def post(self, request):
          register_form = RegisterForm(request.POST)
          if register_form.is_valid():
              user_name = request.POST.get("email", "")
              if UserProfile.objects.filter(email=user_name):
                  return render(request, "register.html",{"register_form":register_form ,'msg':u"用户已经存在"})
              password = request.POST.get("password", "")
              user_profile = UserProfile()
              user_profile.username = user_name
              user_profile.email = user_name
              user_profile.password = make_password(password)
              user_profile.save()

              send_register_email(user_name, "register")
              return render(request, "login.html")
          else:
              return render(request, "register.html",{"register_form":register_form})


class LoginView(View):
      def get(self, request):
         return render(request, "login.html")

      def post(self, request):
         login_form = LoginForm(request.POST)
         if login_form.is_valid():
              user_name = request.POST.get("username", "")
              pass_word = request.POST.get("password", "")
              user = authenticate(username=user_name,password= pass_word)
              if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html",{"msg":"用户未激活"})

              else:
                  return render(request, "login.html",{"msg":"用户名或密码错误！"})
         else:
             return render(request, "login.html",{"login_form":login_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_password_form = ForgetPasswordForm()
        return render(request, "forget_password.html",{"forget_password_form":forget_password_form})
    def post(self, request):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forget_password.html", {"forget_password_form":forget_password_form})


class ResetUserView(View):
    def get(self, request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html",{"email":email})
        else:
            return render(request, "active_fail.html")
    def post(self, request):
        reset_user_form = ResetUserForm(request.POST)
        if reset_user_form.is_valid():
            email = request.POST.get("email","")
            password = request.POST.get("password","")
            password_check = request.POST.get("password_check","")
            if password == password_check:
               user = UserProfile.objects.get(email=email)
               user.password = make_password(password)
               user.save()
               return render(request, "login.html")
            else:
               return render(request, "password_reset.html",{"email":email, "msg":u"密码不一致"})


