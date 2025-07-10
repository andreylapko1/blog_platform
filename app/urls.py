from django.urls import path

from app.views import (BaseHomeView, UserPageView, PostCreateView, PostDetailView, UserDetailView, UserDetailInformationView, UserOtherView,
                       PostUpdateView, LikesView, PostDeleteView)

urlpatterns = [
    path('', BaseHomeView.as_view(), name='home_view'),
    path('user/', UserPageView.as_view(), name='user_page_view'),
    path('login/', UserPageView.as_view(), name='user_page_view'),
    path('user-view-other/<int:user_pk>', UserOtherView.as_view(), name='user_other_view'),
    path('post-create/', PostCreateView.as_view(), name='post_create_view'),
    path('post-update/<int:post_id>', PostUpdateView.as_view(), name='post_update_view'),
    path('post-delete/<int:post_id>', PostDeleteView.as_view(), name='post_delete_view'),
    path('post-detail/<int:post_id>', PostDetailView.as_view(), name='post_detail_view'),
    path('user-detail/', UserDetailView.as_view(), name='user_detail'),
    path('user-detail-information/', UserDetailInformationView.as_view(), name='user_detail-info'),
    path('likes', LikesView.as_view(), name='like_post'),
    path('likes', LikesView.as_view(), name='subscribe_view'),
]