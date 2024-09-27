from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from website.forms import ContactForm
from django.contrib import messages
from django.shortcuts import render
from blog.models import Rating
from blog.recommender import recommend_movies_for_user  # Import the recommender function
import pandas as pd # data processing

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




@login_required(login_url='accounts:login')
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Get user ratings
    user_ratings = Rating.objects.filter(user=request.user).select_related('movie')

    # Use the recommender to get recommended movies for the user
    recommended_movies = recommend_movies_for_user(request.user, num_recommendations=5)

    # Pass data to the template
    context = {
        'user_ratings': user_ratings,
        'recommended_movies': recommended_movies,  # List of recommended movie titles
    }

    return render(request, 'website/profile.html', context)