from django.shortcuts import render
from django.views.generic import View


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from courses.models import Course
# Create your views here.


class CourseView(View):
    def get(self, request):
        template_category = "course_list"
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by("-click_nums")[:4]

        sort = request.GET.get('sort','')
        if sort == "student_nums":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 1, request=request)
        courses = p.page(page)


        return render(request, 'course-list.html',{
            "template_category":template_category,
            "sort": sort,
            "all_courses":courses,
            "hot_courses":hot_courses
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        template_category = "course_list"
        course_detail = Course.objects.get(id=int(course_id))

        #lesson_nums = course_detail.get_lesson_nums()
        #learn_users = course_detail.get_learn_users()
        course_detail.click_nums += 1
        course_detail.save()
        return render(request, 'course-detail.html', {
            "template_category":template_category,
            "course_detail":course_detail,
        })




