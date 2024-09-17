from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from website.forms import ContactForm
from django.contrib import messages
from django.shortcuts import render
from blog.models import Rating
from blog.recommender import recommend , similarity
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
    rated_movies = [rating.movie.title for rating in user_ratings]

    # Recommend movies based on user's rated movies
    recommended_movies = set()  # استفاده از set برای جلوگیری از موارد تکراری
    if rated_movies:
        for movie in rated_movies:
            recommendations = recommend(movie)
            if recommendations:  # اطمینان از اینکه تابع recommend نتیجه دارد
                recommended_movies.update(recommendations)

    # Pass data to the template
    context = {
        'user_ratings': user_ratings,
        'recommended_movies': list(recommended_movies),  # تبدیل set به list برای ارسال به قالب
    }

    return render(request, 'website/profile.html', context)