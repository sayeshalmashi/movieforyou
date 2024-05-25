from django.urls import path
from blog.views import *
app_name='blog'

urlpatterns = [
  path('',movies_view,name='index'),
  path('details',details_view,name='single_category'),
]