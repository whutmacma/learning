from django.urls import re_path, include
from organization.views import OrganizationView, AddFavoriteView, AddUserAskView, OrganizationHomeView, OrganizationCourseListView, OrganizationTeacherListView, OrganizationDescriptView, TeacherListView, TeacherDetailView

urlpatterns = [
    re_path(r'^org_list/$',OrganizationView.as_view(), name="org_list"),
    re_path(r'^org_list/add_ask/$',AddUserAskView.as_view(), name="add_ask"),
    re_path(r'^org_list/home/(?P<organization_id>\d+)/$',OrganizationHomeView.as_view(), name="org_home"),
    re_path(r'^org_list/course_list/(?P<organization_id>\d+)/$',OrganizationCourseListView.as_view(), name="org_course_list"),
    re_path(r'^org_list/teacher_list/(?P<organization_id>\d+)/$',OrganizationTeacherListView.as_view(), name="org_teacher_list"),
    re_path(r'^org_list/descript/(?P<organization_id>\d+)/$',OrganizationDescriptView.as_view(), name="org_descript"),
    re_path(r'^add_fav/$', AddFavoriteView.as_view(), name="add_favorite"),

    re_path(r'^teacher_list/$', TeacherListView.as_view(), name="teacher_list"),
    re_path(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name="teacher_detail" )
]
