from django.urls import path
from blog.views import *
app_name='blog'

urlpatterns = [
  path('',catalog_view,name='index'),
  path('category',category_view,name='categorys'),
  path('details',details_view,name='single_category'),
]