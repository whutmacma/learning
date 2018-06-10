from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from courses.models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by("-click_nums")[:4]

        sort = request.GET.get('sort','')
        if sort == "student_nums":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        search = request.GET.get('keywords','')
        all_courses = all_courses.filter(Q(name__icontains=search)|Q(desc__icontains=search)|Q(detail__icontains=search)|Q(category__icontains=search))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 99999999, request=request)
        courses = p.page(page)


        return render(request, 'course-list.html',{
            "sort": sort,
            "all_courses":courses,
            "hot_courses":hot_courses
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))

        #lesson_nums = course_detail.get_lesson_nums()
        #learn_users = course_detail.get_learn_users()
        course_detail.click_nums += 1
        course_detail.save()

        has_fav_course=has_fav_organization=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.course_organization.id, fav_type=2):
                has_fav_organization = True

        tag = course_detail.tag
        relate_courses =""
        if tag:
            relate_courses =  Course.objects.filter(tag=tag)[:1]
        return render(request, 'course-detail.html', {
            "course_detail":course_detail,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_organization":has_fav_organization
        })


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course_detail.id)

        user_courses = UserCourse.objects.filter(user=request.user, course=course_detail)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()
            course_detail.students +=1
            course_detail.save()

        user_courses = UserCourse.objects.filter(course_id=course_id)
        user_ids = [ user.user_id for user in user_courses ]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [ course.course_id for course in all_user_courses]
        course_names = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html',{
            "course_detail":course_detail,
            "all_resources":all_resources,
            "relate_courses":course_names
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course_detail = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course_detail.id)
        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(course_id=course_id)
        user_ids = [ user.user_id for user in user_courses ]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [ course.course_id for course in all_user_courses]
        course_names = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]


        return render(request, 'course-comment.html', {
            "course_detail":course_detail,
            "all_resources":all_resources,
            "all_comments":all_comments,
            "relate_courses":course_names
        })
    def post(self, request, course_id):
        if not request.user.is_authenticated:
            return  JsonResponse({'status':'fail', 'msg':'用户未登录'})

        comment = request.POST.get('comments','')
        if comment != "":
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.comments = comment
            course_comment.save()
            return JsonResponse({'status':'success'})
        return JsonResponse({'status':'fail','msg':'评论失败'})


