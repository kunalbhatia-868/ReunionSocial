from django.urls import path
from accounts.views import UserDetail,AuthenticateView,Follow,UnFollow

urlpatterns = [
    path("authenticate/",AuthenticateView.as_view(),name="authenticate"),
    path('user/',UserDetail.as_view(),name="user_detail"),
    path('follow/<uuid:user_id>',Follow.as_view(),name="follow"),
    path('unfollow/<uuid:user_id>',UnFollow.as_view(),name="unfollow"),
]
