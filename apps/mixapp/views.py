from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response


from users.models import Banner
from courses.models import Course
from organization.models import CourseOrg
# Create your views here.

class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all().order_by('index')[:5]

        course_organization =  CourseOrg.objects.all().order_by('-click_nums')[:8]
        course_list = Course.objects.all().order_by('-click_nums')[:15]
        return render(request, 'index.html', {
            "banners":banners,
            "organization_list":course_organization,
            "course_list":course_list
        })



def page_not_found(self):
    #response = render_to_response('404.html', {})
    #response.status_code = 404
    response = 1
    return response #render_to_response('405.html', {})


