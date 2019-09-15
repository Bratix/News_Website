from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    picture = models.FileField(null = True, blank = True) 
    bio = models.TextField()
    username = models.CharField(max_length = 30)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("News:edit_profile", kwargs={"pk": self.pk}) 

class Category(models.Model):
    name = models.CharField(max_length = 30)
    picture = models.FileField(null = True, blank = True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    title = models.CharField(max_length = 120)
    text = models.TextField()
    picture = models.FileField(null = True, blank = True)
    creation_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("News:article_detail", kwargs={"pk": self.pk}) 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length = 3000)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse("News:article_detail", kwargs={"pk": self.article.pk}) 

    