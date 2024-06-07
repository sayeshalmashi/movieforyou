from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from blog.models import Movie

def movies_view(request,**kwargs):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time).order_by('-id')
  if kwargs.get('cat_name')!=None:
    movies=movies.filter(status=1,category__name=kwargs['cat_name'])
  if kwargs.get('author_username')!=None:
    movies=movies.filter(status=1,author__username=kwargs['author_username'])
  
  context={'movies':movies}
  return render(request,'blog/movies.html',context)

def details_view(request,pid):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time)
  movie=get_object_or_404(movies,pk=pid)
  # prev_post=Movie.objects.filter(pk__lt=movie.id,status=1,published_date__lte=current_time).order_by('-pk').first()
  # next_post=Movie.objects.filter(pk__gt=movie.id,status=1,published_date__lte=current_time).order_by('pk').first()
  # # post.count_views+=1
  # movie.save()
  context={'movie':movie}
  return render(request,'blog/details.html',context)


# def blog_category(request,cat_name):
#   movies=Movie.objects.filter(status=1,category__name=cat_name)
#   context={'movies':movies}
#   return render(request,'blog/movies.html',context)

def blog_search(request):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time).order_by('-id')
  if request.method=='GET':
    if s:= request.GET.get('s'): # agar request.GET.get('s') ro rikhte toye s
      movies=movies.filter(title__contains=s)
  context={'movies':movies}
  return render(request,'blog/movies.html',context)