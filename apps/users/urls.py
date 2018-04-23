from django.urls import re_path, include
from users.views import LoginView, RegisterView


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name="login"),
    re_path(r'^register/$', RegisterView.as_view(), name="register"),
    re_path(r'^captcha/', include('captcha.urls'))
]
