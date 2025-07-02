from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.base import View

from blog_platform import settings
from .models import Post, Profile
from .forms import UserUpdateProfileForm, PostCreateForm
from django.db import transaction
import os

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
    template_name = 'app/post_create.html'

    def get(self, request):
        if str(request.user) == 'AnonymousUser':
            return render(request, 'app/home.html')
        form = PostCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                new_post = Post()
                new_post.author = request.user
                new_post.title = form.cleaned_data.get('title')
                new_post.content = form.cleaned_data.get('text')
                if 'image' in form.cleaned_data and form.cleaned_data.get('image'):
                    new_post.image = form.cleaned_data.get('image')
                new_post.save()
                print(new_post.title)
            return redirect('home_view')
        else:
            return render(request, self.template_name, {'form': form})



class PostDetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        context = {
            'post': post,
        }
        return render(request, 'app/post_detail.html', context)


class UserDetailView(View):
    def get(self, request):
        user = User.objects.get(username=request.user)
        form_data = {
            'username': user.username,
            'email': user.email,
        }
        if hasattr(user, 'profile') and user.profile.profile_image:
            profile_picture_url = user.profile.profile_image.url
        else:
            profile_picture_url = settings.STATIC_URL + 'img/default_avatar.png'
        form = UserUpdateProfileForm(initial=form_data)
        context = {
            'form': form,
            'profile_image': profile_picture_url
        }
        return render(request, 'app/user_detail.html', context)

    def post(self, request):
        user = request.user
        if not hasattr(user, 'profile'):
            profile = Profile.objects.create(user=user)
        else:
            profile = user.profile


        form = UserUpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user.username = form.cleaned_data.get('username')
                user.email = form.cleaned_data.get('email')
                user.save()

                if 'profile_image' in form.cleaned_data and form.cleaned_data.get('profile_image'):
                    new_image = form.cleaned_data.get('profile_image')
                    if profile.profile_image:
                        old_image_path = profile.profile_image.path
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    profile.profile_image = new_image
                profile.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
        return redirect('user_page_view')



# Create your views here.
