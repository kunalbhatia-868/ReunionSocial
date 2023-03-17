from django.urls import path
from social.views import (PostCreateView,
PostDetailDeleteView,
AllPostView,
CommentCreateView,
UnLikeView,
LikeView,
)
urlpatterns = [
    path("posts/<uuid:post_id>/",PostDetailDeleteView.as_view(),name="post_detail_delete"),
    path('posts/',PostCreateView.as_view(),name="create_post"),
    path('all_posts/',AllPostView.as_view(),name='all_posts'),
    path('comment/<uuid:post_id>/',CommentCreateView.as_view(),name="create_comment"),
    path('like/<uuid:post_id>/',LikeView.as_view(),name="like"),
    path('unlike/<uuid:post_id>/',UnLikeView.as_view(),name="unlike"),


    
]
