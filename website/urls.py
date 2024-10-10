from django.urls import path,include
from website.views import *
app_name='website'

urlpatterns = [
  path('',index_view,name='index'),
  path('about',about_view,name='about'),
  path('contact',contact_view, name='contact'),
  path('interview',interview_view, name='interview'),
  path('error',error_view, name='error'),
  path('interview',interview_view, name='interview'),
  path('profile',profile_view, name='profile'),
  path('document',document_view, name='document'),
]