from django.urls import path
from blog.views import *
from blog.feeds import LatestEntriesFeed

app_name='blog'

urlpatterns = [
  path('',movies_view,name='index'),
  path('<int:pid>',details_view,name='details'),
  path('author/<str:author_username>',movies_view,name='author'),
  path('category/<str:cat_name>',movies_view,name='category'),
  path('search/',blog_search,name='search'),
  path('rss/feed/', LatestEntriesFeed()),
]