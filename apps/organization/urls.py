from django.urls import re_path, include
from organization.views import OrganizationView

urlpatterns = [
    re_path(r'^org_list/$',OrganizationView.as_view(), name="org_list")
]
