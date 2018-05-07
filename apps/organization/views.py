from django.shortcuts import render
from django.views.generic import View


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg, CityDict

# Create your views here.


class OrganizationView(View):
    def get(self, request):
        all_organizations = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_organizations =  all_organizations.filter(city_id=int(city_id))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_organizations, 1, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_organizations":orgs,
            "all_citys":all_citys,
            "city_id":city_id
        })


