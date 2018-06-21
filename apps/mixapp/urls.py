from django.urls import re_path, include

from mixapp.views import IndexView

urlpatterns = [
    re_path(r'^index/$', IndexView.as_view(), name="index")
]

