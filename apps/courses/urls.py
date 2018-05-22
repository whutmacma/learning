from django.urls import re_path
from courses.views import CourseView, CourseDetailView

urlpatterns = [
    re_path(r'^course_list/$',CourseView.as_view(), name="course_list"),
    re_path(r'^course_list/(?P<course_id>\d+)/$',CourseDetailView.as_view(), name="course_detail")
]

