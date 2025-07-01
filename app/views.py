from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import Post


class BaseHomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {
            'posts': posts,
        }
        return render(request, 'app/home.html', context)


class UserPageView(View):
    def get(self, request):
        return render(request, 'app/user_page.html')


class PostCreateView(View):
    def get(self, request):
        print(str(request.user))
        if str(request.user) == 'AnonymousUser':
            return render(request, 'app/login.html')
        return render(request, 'app/post_create.html')

    def post(self, request):
        author = User.objects.get(username=request.user)
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'image': request.POST.get('image'),
            'author': author,
        }
        post = Post(**data)
        post.save()
        return HttpResponse('<UNK>')






# Create your views here.
