from django.shortcuts import render
from django.views.generic.base import View


class BaseHomeView(View):
    def get(self, request):
        return render(request, 'app/base_home.html')


class UserPageView(View):
    def get(self, request):
        return render(request, 'app/user_page.html')


class PostCreateView(View):
    def get(self, request):
        return render(request, 'app/post_create.html')







# Create your views here.
