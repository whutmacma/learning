#账户注册、登录、密码找回
#用户验证机制重构
#用户管理的所有逻辑
#
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.models import UserProfile, EmailVerifyRecord
#表单过滤
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetUserForm
from utils.email_send import send_register_email


#重构用户验证机制
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:#Q 复杂数学运算 email与username均可作为登录用户名
           user = UserProfile.objects.get(Q(username=username) | Q(email=username) )
           if user.check_password(password):
                return user
        except Exception as e:
           return None


#激活账户
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


#注册逻辑
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
              user_profile.password = make_password(password)#密码加密
              user_profile.save()

              send_register_email(user_name, "register")#发送激活邮件
              return render(request, "login.html")
          else:
              return render(request, "register.html",{"register_form":register_form})


#登录机制
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


#密码找回
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


#用户属性重置
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


class UserCenterView(View):
    def get(self, request):
        return render(request, "usercenter.html")





