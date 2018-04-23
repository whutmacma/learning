# _*_ encoding:utf-8 _*_

import xadmin


from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
	search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']


xadmin.site.register(Course, CourseAdmin)

