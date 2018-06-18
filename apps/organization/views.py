from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from organization.models import CourseOrg, CityDict, Teacher
from organization.forms import UserAskForm
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


class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
        #   return HttpResponse("{'status':'scucess'}", content_type='application/json')
            return JsonResponse({'status':'success'})
        else:
            return  JsonResponse({'status':'fail', 'msg':userask_form.errors })
        #   return HttpResponse("{'status':'fail','msg':'添加出错'}", content_type='application/json')


class AddFavoriteView(View):
    def post(self,request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated:
            return  JsonResponse({'status':'fail', 'msg':'用户未登录'})

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            return  JsonResponse({'status':'success', 'msg':'收藏'})
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save();
                #   return HttpResponse("{'status':'scucess'}", content_type='application/json')
                return JsonResponse({'status':'success', 'msg':'已收藏'})
            else:
                return  JsonResponse({'status':'fail', 'msg':'收藏失败'})




class OrganizationHomeView(View):
    def get(self, request, organization_id):
        current_page = 'home'
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_courses = course_organization.course_set.all()[:3]#外键
        all_teachers = course_organization.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html',{
            'organization':course_organization,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'current_page':current_page
        })


class OrganizationCourseListView(View):
    def get(self, request, organization_id):
        current_page = 'course_list'
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_courses = course_organization.course_set.all()#外键
        return render(request, 'org-course-list.html',{
            'organization':course_organization,
            'all_courses':all_courses,
            'current_page':current_page
        })


class OrganizationTeacherListView(View):
    def get(self, request, organization_id):
        current_page = 'teacher_list'
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        all_teachers = course_organization.teacher_set.all()#外键
        return render(request, 'org-teacher-list.html',{
            'organization':course_organization,
            'all_teachers':all_teachers,
            'current_page':current_page
        })


class OrganizationDescriptView(View):
    def get(self, request, organization_id):
        current_page = 'descript'
        course_organization = CourseOrg.objects.get(id=int(organization_id))
        return render(request, 'org-descript.html',{
            'organization':course_organization,
            'current_page':current_page
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

        return render(request, 'teacher-detail.html', {
            "teacher_detail":teacher_detail,
            "course_list":course_list,
            "hot_teacher":organization_hot_teacher,
            "has_fav_teacher":has_fav_teacher,
            "has_fav_organization":has_fav_organization
        })






