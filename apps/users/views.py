#账户注册、登录、密码找回
#用户验证机制重构
#用户管理的所有逻辑
#
import  json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from users.models import UserProfile, EmailVerifyRecord
#表单过滤
from users.forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetUserForm, UploadImageForm, ModifyPasswordForm, UserCenterForm
from utils.email_send import send_register_email, send_pin_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserFavorite, UserCourse, UserMessage
from courses.models import Course, Teacher
from organization.models import CourseOrg


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
                    #course_organization =  CourseOrg.objects.all().order_by('click_nums')[:8]
                    #course_list = Course.objects.all().order_by('click_nums')[:7]
                    return HttpResponseRedirect(reverse('index'))
                    #render(request, "index.html", {
                    #    "organization_list":course_organization,
                    #    "course_list":course_list
                    #})
                else:
                    return render(request, "login.html",{"msg":"用户未激活"})

              else:
                  return render(request, "login.html",{"msg":"用户名或密码错误！"})
         else:
             return render(request, "login.html",{"login_form":login_form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html')


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


class UserCenterView(LoginRequiredMixin, View):
    def get(self, request):
        #if not request.user.is_authenticated:
        #   return render(reuqest, "login.html")
        return render(request, "usercenter.html")
    def post(self, request):
        userprofile_form = UserCenterForm(request.POST, instance=request.user)
        if userprofile_form.is_valid():
            request.user.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'fail', 'msg':userprofile_form.errors})



class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)#疑问？？？
        if image_form.is_valid():
            #image = image_form.cleaned_data['image']
            #request.user.image = image
            request.user.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'fail'})


class UpdatePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPasswordForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return JsonResponse({'status':'fail', 'msg':u'输入密码不一致'})

            request.user.password = make_password(password1)
            request.user.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'fail', 'msg':modify_form.errors})


class EmailPinView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({"status":"fail", "email":u"邮箱已经存在"})

        current_email = request.user.email
        send_pin_email(current_email, 'reset_email')

        return JsonResponse({'status':'success'})

class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        pin = request.POST.get("code","")
        current_email = request.POST.get("email","")

        if EmailVerifyRecord.objects.filter(code=pin):
            request.user.email = current_email
            request.user.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'fail', 'msg':u'验证错误或失效'})


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html' ,{
            "user_courses":user_courses
        })


class MyFavoriteCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list= []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav in favs:
            fav_id = fav.fav_id
            course = Course.objects.get(id=fav_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'user_fav_course':course_list
        })


class MyFavoriteTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list= []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav in favs:
            fav_id = fav.fav_id
            teacher = Teacher.objects.get(id=fav_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'user_fav_teacher':teacher_list
        })


class MyFavoriteOrganizationView(LoginRequiredMixin, View):
    def get(self, request):
        organization_list= []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav in favs:
            fav_id = fav.fav_id
            organization = CourseOrg.objects.get(id=fav_id)
            organization_list.append(organization)

        return render(request, 'usercenter-fav-org.html', {
            'user_fav_organization':organization_list
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id).order_by("-add_time")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 5, request=request)
        my_message = p.page(page)

        return render(request, 'usercenter-message.html', {
            "my_message":my_message
        })



