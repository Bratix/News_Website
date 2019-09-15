from django.urls import path
from django.conf.urls import url
from . import views

app_name = "News"

urlpatterns = [
    #home page
    path('', views.IndexView.as_view(), name = "index"),
    #category articles
    path('view/category/<pk>', views.ArticlesbyCategoryView.as_view(), name = "category_detail"),
    #SEARCH articles
    path('arctiles/search', views.SearchArticles.as_view(), name = "article_search"),

    #create profile
    path('create/userprofile', views.UserProfileCreate.as_view(), name = "create_profile"),
    #edit profile
    path('<pk>/userprofile', views.UserProfileEdit.as_view(), name = "edit_profile"),


    #view articles
    path('article/<pk>', views.ArticleDetail.as_view(), name = "article_detail"),
    #create articles
    path('article_create', views.ArticleCreate.as_view(), name = "article_create"),
    #create articles
    path('article_edit/<pk>', views.ArticleEdit.as_view(), name = "article_edit"),

    #create comment
    path('comment/<pk>', views.CommentCreate.as_view(), name = "comment_create"),
    #edit comment
    path('comment/edit/<pk>', views.CommentUpdate.as_view(), name = "comment_edit"),
    #delete comment
    path('comment/delete/<pk>', views.CommentDelete.as_view(), name = "comment_delete"),
]
