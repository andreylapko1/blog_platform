from django.urls import path

from app.views import BaseHomeView, UserPageView, PostCreateView

urlpatterns = [
    path('', BaseHomeView.as_view(), name='home_view'),
    path('user/', UserPageView.as_view(), name='user_page_view'),
    path('post-create/', PostCreateView.as_view(), name='post_create_view'),
]