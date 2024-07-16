from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from website.forms import ContactForm
from django.contrib import messages

def index_view(request):
  return render(request,'website/index.html')

def about_view(request):
  return render(request,'website/about.html')


def contact_view(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      form.save()
      success_message = "you'r ticket submited successfully"
      messages.add_message(request, messages.SUCCESS, success_message)
    else:
      error_message = "you'r ticket didnt submited"
      messages.add_message(request, messages.ERROR, error_message)
  form = ContactForm()
  return render(request, 'website/contacts.html', {'form': form})

def error_view(request):
  return render(request, 'website/404.html')

def interview_view(request):
  return render(request, 'website/interview.html')

@login_required(login_url='accounts/login')
def profile_view(request):
  return render(request, 'website/profile.html')

