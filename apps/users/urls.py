from django.urls import re_path, include

from users.views import LoginView, ActiveUserView, RegisterView, ForgetPasswordView, ResetUserView


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name="login"),
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(), name="user_active"),
    re_path(r'^forget/$', ForgetPasswordView.as_view(), name="forget_password"),
    re_path(r'^reset/(?P<reset_code>.*)/$',ResetUserView.as_view(), name="reset_user"),
    re_path(r'^reset/$',ResetUserView.as_view(), name="reset_user")
]
