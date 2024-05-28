from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from blog.models import Movie

def movies_view(request):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time).order_by('-id')
  
  context={'movies':movies}
  return render(request,'blog/movies.html',context)

def details_view(request):
  return render(request,'blog/details.html')
