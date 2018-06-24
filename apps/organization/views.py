from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from organization.models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.


class OrganizationView(View):
    def get(self, request):
        all_organizations = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_organizations = all_organizations.order_by("-click_nums")[:3]

        city_id = request.GET.get('city', '')
        if city_id:
            all_organizations =  all_organizations.filter(city_id=int(city_id))
        category = request.GET.get('ct','')
        if category:
            all_organizations = all_organizations.filter(category=category)
        sort = request.GET.get('sort','')
        if sort:
            if sort == "student_nums":
                all_organizations = all_organizations.order_by("-student_nums")
            if sort == "course_nums":
                all_organizations = all_organizations.order_by("-course_nums")
        search = request.GET.get('keywords','')
        all_organizations = all_organizations.filter( Q(desc__icontains=search)|Q(name__icontains=search)|Q(address__icontains=search))

        organization_nums = all_organizations.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_organizations, 5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_organizations":orgs,
            "all_citys":all_citys,
            "organization_nums":organization_nums,
            "city_id":city_id,
            "category":category,
            "sort":sort,
            "hot_organizations":hot_organizations
        })


class OrganizationHomeView(View):
    def get(self, request, organization_id):
        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_type=2, fav_id=int(organization_id), user=request.user):
                is_favorite = True
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_courses = course_organization.course_set.all()[:3]#外键
        all_teachers = course_organization.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html',{
            'organization':course_organization,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'is_favorite':is_favorite
        })


class OrganizationCourseListView(View):
    def get(self, request, organization_id):
        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_type=2, fav_id=int(organization_id), user=request.user):
                is_favorite = True
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_courses = course_organization.course_set.all()#外键
        return render(request, 'org-course-list.html',{
            'organization':course_organization,
            'all_courses':all_courses,
            'is_favorite':is_favorite
        })


class OrganizationTeacherListView(View):
    def get(self, request, organization_id):
        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_type=2, fav_id=int(organization_id), user=request.user):
                is_favorite = True
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_teachers = course_organization.teacher_set.all()#外键
        return render(request, 'org-teacher-list.html',{
            'organization':course_organization,
            'all_teachers':all_teachers,
            'is_favorite':is_favorite
        })


class OrganizationDescriptView(View):
    def get(self, request, organization_id):
        is_favorite = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_type=2, fav_id=int(organization_id), user=request.user):
                is_favorite = True
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        return render(request, 'org-descript.html',{
            'organization':course_organization,
            'is_favorite':is_favorite
        })



class TeacherListView(View):
    def get(self, request):
        teacher_list = Teacher.objects.all()
        hot_teacher_list = teacher_list.order_by("-click_nums")[:5]

        sort = request.GET.get('sort','')
        if sort == 'hot':
            teacher_list = teacher_list.order_by('-click_nums')
        search = request.GET.get('keywords','')
        teacher_list = teacher_list.filter(Q(name__icontains=search)|Q(points__icontains=search))

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teacher_list, 5, request=request)
        teacher_desc_list = p.page(page)

        return render(request, 'teachers-list.html', {
            "teacher_desc_list":teacher_desc_list,
            "hot_teacher_list":hot_teacher_list,
            "sort":sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id ):

        teacher_detail = Teacher.objects.get(id=int(teacher_id))
        course_list = teacher_detail.get_course()
        organization_hot_teacher = teacher_detail.org.get_teacher().order_by('-click_nums')[:5]

        has_fav_teacher = has_fav_organization = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_type=3, fav_id=int(teacher_id)):
                has_hav_teacher = True
            if UserFavorite.objects.filter(fav_type=2, fav_id=teacher_detail.org_id):
                has_fav_organization = True
        teacher_detail.click_nums += 1
        teacher_detail.save()

        return render(request, 'teacher-detail.html', {
            "teacher_detail":teacher_detail,
            "course_list":course_list,
            "hot_teacher":organization_hot_teacher,
            "has_fav_teacher":has_fav_teacher,
            "has_fav_organization":has_fav_organization
        })






