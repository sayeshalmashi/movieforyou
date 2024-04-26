from django.urls import path
from blog.views import *
app_name='blog'

urlpatterns = [
  path('',catalog_view,name='index'),
  path('category/<str:cat_name>',catalog_view,name='category'),
  path('details/<str:cat_name>',details_view,name='category'),
]