from django.urls import re_path, include

from users.views import LoginView, ActiveUserView, RegisterView, ForgetPasswordView, ResetUserView, UserCenterView, UploadImageView, UpdatePasswordView, EmailPinView, UpdateEmailView, MyCourseView, MyFavoriteCourseView, MyFavoriteTeacherView, MyFavoriteOrganizationView, MyMessageView


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name="login"),
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(), name="user_active"),
    re_path(r'^forget/$', ForgetPasswordView.as_view(), name="forget_password"),
    re_path(r'^reset/(?P<reset_code>.*)/$',ResetUserView.as_view(), name="reset_user"),
    re_path(r'^reset/$',ResetUserView.as_view(), name="reset_user"),
    re_path(r'^usercenter/$',UserCenterView.as_view(), name="usercenter"),
    re_path(r'^usercenter/image/upload/$',UploadImageView.as_view(), name="upload_image"),
    re_path(r'^usercenter/password/update/$',UpdatePasswordView.as_view(), name="update_password"),
    re_path(r'^usercenter/email_pin/send/$',EmailPinView.as_view(), name="email_pin"),
    re_path(r'^usercenter/email/update/$',UpdateEmailView.as_view(), name="update_email"),
    re_path(r'^usercenter/my_course/$',MyCourseView.as_view(), name="my_course"),
    re_path(r'^usercenter/favorite/course/$',MyFavoriteCourseView.as_view(), name="my_fav_course"),
    re_path(r'^usercenter/favorite/teacher/$',MyFavoriteTeacherView.as_view(), name="my_fav_teacher"),
    re_path(r'^usercenter/favorite/organization/$',MyFavoriteOrganizationView.as_view(), name="my_fav_organization"),
    re_path(r'^usercenter/my_message/$',MyMessageView.as_view(), name="my_message")
]
