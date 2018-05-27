from django.urls import re_path
from courses.views import CourseView, CourseDetailView, CourseVideoView, CourseCommentView

urlpatterns = [
    re_path(r'^course_list/$',CourseView.as_view(), name="course_list"),
    re_path(r'^course_list/(?P<course_id>\d+)/$',CourseDetailView.as_view(), name="course_detail"),
    re_path(r'^course_video/(?P<course_id>\d+)/$',CourseVideoView.as_view(), name="course_video"),
    re_path(r'^course_comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(), name="course_comment")
]

