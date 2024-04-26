from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

def index_view(request):
  return render(request,'website/index.html')

def about_view(request):
  return render(request,'website/about.html')


def contact_view(request):
  return render(request, 'website/contacts.html')

def error_view(request):
  return render(request, 'website/404.html')

def interview_view(request):
  return render(request, 'website/interview.html')


def profile_view(request):
  return render(request, 'website/profile.html')



