from django.urls import re_path, include
from operation.views import AddFavoriteView, AddUserAskView
urlpatterns = [
    re_path(r'^add_fav/$', AddFavoriteView.as_view(), name="add_favorite"),
    re_path(r'^add_user_ask/$', AddUserAskView.as_view(), name="add_user_ask")

]
