from django.urls import path
from .views import *


urlpatterns = [
    path('posts/', PostList.as_view(), name='Default'),
    path('<slug:slug>/', PostListDetail.as_view(),  name='detail'),
    path('posts/search/', PostSearch.as_view(), name="search_all_posts"),
    path('articles/create/', PostCreateArticles.as_view(), name='create_article'),
    path('news/create/', PostCreateNews.as_view(), name='create_news'),
    path('<slug:slug>/update', PostUpdate.as_view(), name='update_post'),
    path('articles/<slug:slug>/update', PostUpdate.as_view()),
    path('<slug:slug>/delete', PostDelete.as_view(), name='delete_post'),
    path('articles/<slug:slug>/delete', PostDelete.as_view()),
    path('posts/subscriptions/', subscribe, name='sub_scribe'),
]
