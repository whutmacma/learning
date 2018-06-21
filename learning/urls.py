"""learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path( r'xadmin/', xadmin.site.urls),
    #path( r'', include('apps.message.urls')),
    #re_path(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
    path(r'', include('apps.mixapp.urls')),
    path(r'', include('apps.users.urls')),
    path(r'', include('apps.organization.urls')),
    path(r'', include('apps.courses.urls'))
]


