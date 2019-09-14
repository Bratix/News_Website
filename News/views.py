from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Category, Article, UserProfile
from django.core import serializers
from django.http import JsonResponse
import facebook
import requests
import urllib
from optparse import OptionParser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.db.models import Count

class IndexView(View):
    def get(self, request):
        context = {'all_categories': Category.objects.order_by('name'),'futured_articles': Article.objects.order_by('-creation_date')[:9],'popular_news': Article.objects.annotate(count=Count('comment')).order_by('-count')[:7]}
        return render(request, 'News/index.html',context)

class ArticlesbyCategoryView(generic.ListView):
    template_name = 'News/category_articles.html'

    def get_queryset(self):
        current_category = Category.objects.get(id=self.kwargs['pk'])
        return Article.objects.filter(category = current_category).order_by('-creation_date')

class SearchArticles(generic.ListView):
    template_name = 'News/search.html'

    def get_queryset(self):
        wanted = self.request.GET.get('search')
        return Article.objects.filter(title__contains=wanted).distinct()

class UserProfileCreate(CreateView):
    model = UserProfile
    fields = ['username','picture','bio']
    template_name = "News/create_profile.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserProfileCreate, self).form_valid(form)

class ArticleCreate(CreateView):
    model = Article
    fields = ['title','text','picture','category']
    template_name = "News/article_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreate, self).form_valid(form)

class ArticleEdit(UpdateView):
    model = Article
    fields = ['title','text','picture','category']
    template_name = "News/article_update.html"

class UserProfileEdit(UpdateView):
    model = UserProfile
    fields = ['username','picture','bio']
    template_name = "News/edit_profile.html"

    def get_success_url(self):
        return reverse('News:index')


class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'News/single_post.html'
