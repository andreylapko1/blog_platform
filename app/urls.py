from django.urls import path

from app.views import BaseHomeView, UserPageView, PostCreateView, PostDetailView, UserDetailView

urlpatterns = [
    path('', BaseHomeView.as_view(), name='home_view'),
    path('user/', UserPageView.as_view(), name='user_page_view'),
    path('login/', UserPageView.as_view(), name='user_page_view'),
    path('post-create/', PostCreateView.as_view(), name='post_create_view'),
    path('post-detail/<int:post_id>', PostDetailView.as_view(), name='post_detail_view'),
    path('user-detail/', UserDetailView.as_view(), name='user_detail'),
]