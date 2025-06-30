from django.urls import path
from .views import BasePageView
urlpatterns = [
    path('', BasePageView.as_view(), name='base_home_view')
]