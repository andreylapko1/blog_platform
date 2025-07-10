import json
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Comment, UserInformation
from blog_platform import settings
from .models import Post, Profile
from .forms import UserUpdateProfileForm, PostCreateForm, CommentCreateForm, UserInformationForm
from django.db import transaction
import os

class BaseHomeView(ListView):
    paginate_by = 9
    model = Post
    template_name = 'app/home.html'
    context_object_name = 'posts'

    # def get(self, request):
    #     posts = Post.objects.all()
    #     context = {
    #         'posts': posts,
    #     }
    #     return render(request, 'app/home.html', context)


class UserPageView(View):
    def get(self, request):
        return render(request, 'app/user_page.html', )

class PostCreateView(View):
    template_name = 'app/post_create.html'

    def get(self, request):
        if str(request.user) == 'AnonymousUser':
            return redirect('home_view')
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
            return redirect('home_view')
        else:
            return render(request, self.template_name, {'form': form})



class PostDetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = CommentCreateForm()
        comments = Comment.objects.filter(post=post)
        comments_data = list(comments.values('id', 'author__username', 'text', 'created_at'))
        comments_json = json.dumps(comments_data, default=str)
        context = {
            'post': post,
            'comments_json': comments_json,
            'user': request.user,
            'form': form,
            'comments': comments
        }
        return render(request, 'app/post_detail.html', context)

    def post(self, request, post_id):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Неверный формат JSON в запросе.'}, status=400)
            form = CommentCreateForm(data)
            if form.is_valid():
                post = get_object_or_404(Post, pk=post_id)
                author = request.user
                if not author.is_authenticated:
                    return JsonResponse({'success': False, 'message': 'Пользователь не авторизован.'}, status=401)

                comment_text = form.cleaned_data.get('text')
                comment = Comment(text=comment_text, post=post, author=author)
                comment.save()
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.pk,
                        'author': comment.author.username,
                        'text': comment.text,
                         'created_at': comment.created_at.strftime("%d.%m.%Y %H:%M")

                    }
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            form = CommentCreateForm(request.POST)
            if form.is_valid():
                post = Post.objects.get(pk=post_id)
                author = request.user
                comment_text = form.cleaned_data.get('text')
                comment = Comment(text=comment_text, post=post, author=author)
                comment.save()
                return redirect('post_detail_view', post_id)
            else:
                return redirect('post_detail_view', post_id)


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
        return redirect('user_page_view')



class UserDetailInformationView(View):
    def get(self, request):
        try:
            user_info = request.user.userinformation
        except UserInformation.DoesNotExist:
            user_info = UserInformation.objects.create(user=request.user)
        initial_data = {
            'first_name': user_info.first_name,
            'last_name': user_info.last_name,
            'date_of_birth': user_info.date_of_birth,
            'about_user': user_info.about_user,
            'phone': user_info.phone,
            'inst': user_info.inst,
            'hobbies': user_info.hobbies,
            'web_site': user_info.web_site,
            'geo': user_info.geo,
            'profession': user_info.profession,
        }
        form = UserInformationForm(initial=initial_data)
        return render(request, 'app/user_detail_info.html', {'form': form})

    def post(self, request):
        try:
            user_info = request.user.userinformation
        except UserInformation.DoesNotExist:
            user_info = UserInformation.objects.create(user=request.user)
        form = UserInformationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_info.first_name = cleaned_data.get('first_name')
            user_info.last_name = cleaned_data.get('last_name')
            user_info.date_of_birth = cleaned_data.get('date_of_birth')
            user_info.about_user = cleaned_data.get('about_user')
            user_info.phone = cleaned_data.get('phone')
            user_info.inst = cleaned_data.get('inst')
            user_info.hobbies = cleaned_data.get('hobbies')
            user_info.web_site = cleaned_data.get('web_site')
            user_info.geo = cleaned_data.get('geo')
            user_info.profession = cleaned_data.get('profession')
            user_info.save()
        return redirect('user_page_view')

class UserOtherView(View):
    def get(self, request, user_pk):
        user = User.objects.get(pk=user_pk)
        return render(request, 'app/user_page.html', {'user': user})


class PostUpdateView(View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        initial_data = {
            'title': post.title,
            'text': post.content,
            'image': post.image,
        }
        form = PostCreateForm(initial=initial_data)
        return render(request, 'app/post_update.html', {'form': form, 'post': post})


    def post(self, request, post_id):
        form = PostCreateForm(request.POST, request.FILES)
        post = Post.objects.get(pk=post_id)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['text']
            if not form.cleaned_data['image']:
                post.image = post.image
            else:
                post.image = form.cleaned_data['image']
            post.save()
            return redirect('user_page_view')
        else:
            return redirect('user_page_view')



class LikesView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        param = request.POST.get('action')
        if not post_id or not param:
            return JsonResponse({'status': 'error', 'message': 'Отсутствует ID поста или действие'}, status=400)
        try:
            post = get_object_or_404(Post, id=post_id)
            session_liked_posts = request.session.get('liked_posts', [])
            with transaction.atomic():
                if param == 'like':
                    if post.id not in session_liked_posts:
                        post.total_likes += 1
                        session_liked_posts.append(post.id)
                elif param == 'unlike':
                    if post.id in session_liked_posts:
                        if post.total_likes > 0:
                            post.total_likes -= 1
                        session_liked_posts.remove(post.id)
                post.save()
                request.session['liked_posts'] = session_liked_posts
                request.session.modified = True
                return JsonResponse({'status': 'ok', 'total_likes': post.total_likes}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post does not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'{e}'}, status=400)



# Create your views here.
