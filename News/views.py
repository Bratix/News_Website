from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Category, Article, UserProfile, Comment
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Count

class IndexView(View):
    def get(self, request):
        context = {'all_categories': Category.objects.order_by('name'),'futured_articles': Article.objects.order_by('-creation_date')[:9],'popular_news': Article.objects.annotate(count=Count('comment')).order_by('-count')[:7]}
        return render(request, 'News/index.html',context)

class ContactUs(View):
    def get(self, request):
        return render(request, 'News/contact_us.html')
    def post(self, request):
        subject = self.request.POST.get('subject')
        text = self.request.POST.get('my_textarea')
        print(subject,text)
        send_mail(
        subject,
        text,
        self.request.user.userprofile.username,
        ['amarrbratic@gmail.com'],
        fail_silently=False,
        )
        return redirect('News:index')


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

class ArticleDelete(DeleteView):
    model = Article

    def get_success_url(self):
        return reverse_lazy('News:index')

class UserProfileEdit(UpdateView):
    model = UserProfile
    fields = ['username','picture','bio']
    template_name = "News/edit_profile.html"

    def get_success_url(self):
        return reverse('News:index')


class ArticleDetail(generic.DetailView):
    model = Article
    template_name = 'News/single_post.html'


class CommentCreate(CreateView):
    model = Comment
    fields = ['comment_text']

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
        
    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(id=self.kwargs['pk'])
        response = super(CommentCreate, self).form_valid(form)

        if self.request.is_ajax():
            data = {
                'pk' : self.object.pk,
                'comment_text' : self.object.comment_text,
                'user' : str(self.object.user.userprofile.username),
                'creation_date' : self.object.creation_date,
                'comment_count' : self.object.article.comment_set.count(),
                'picture_url' : self.object.user.userprofile.picture.url,
            }
            return JsonResponse(data)
        else:
            return response

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['comment_text']

class CommentDelete(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('News:article_detail',kwargs = {'pk': Comment.objects.get(id=self.kwargs['pk']).article.id})
