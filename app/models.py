from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(verbose_name='post content', null=False)
    image = models.ImageField(upload_to='posts_img/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

class Comment(models.Model):
    text = models.TextField(null=False, blank=False, verbose_name='comment text')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.text}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile_pic/')

    def __str__(self):
        return f'{self.user}'


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'



class UserInformation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, )
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True,)
    about_user = models.TextField(null=True, blank=True)




# Create your models here.
