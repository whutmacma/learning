from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse

from operation.models import UserFavorite
from operation.forms import UserAskForm

# Create your views here.
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




