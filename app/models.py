from django.db import models

class Post(models.Model):
    title = models.CharField(verbose_name='post title', max_length=255, default=None)
    text = models.TextField(verbose_name='post text', null=True ,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)


class User(models.Model):
    firs_name = models.CharField(verbose_name='name user', max_length=120, null=False ,blank=False)
    last_name = models.CharField(verbose_name='last name user', max_length=120, null=False ,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.TextField(verbose_name='comment text', null=False ,blank=False)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)













# Create your models here.
