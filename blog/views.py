from django.shortcuts import render,get_object_or_404 , redirect 
from django.urls import reverse
from django.utils import timezone
from blog.models import Movie , Comment
from blog.forms import CommentForm
from django.core.paginator import Paginator , EmptyPage,PageNotAnInteger
from django.contrib import messages

def movies_view(request,**kwargs):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time).order_by('-id')
  if kwargs.get('cat_name')!=None:
    movies=movies.filter(status=1,category__name=kwargs['cat_name'])
  if kwargs.get('author_username')!=None:
    movies=movies.filter(status=1,author__username=kwargs['author_username'])
  
  movies=Paginator(movies,6)
  try:
    page_number=request.GET.get('page')
    movies=movies.get_page(page_number)
  except PageNotAnInteger:
    # return render(request,'path-to-your-404-template.html')
    movies=movies.get_page(1)
  except EmptyPage:
    movies=movies.get_page(1)
    
  context={'movies':movies}
  return render(request,'blog/movies.html',context)

def details_view(request,pid):
  if request.method == 'POST':
    form=CommentForm(request.POST)
    if form.is_valid():
      form.save()
      success_message = "you'r commet submited successfully"
      messages.add_message(request, messages.SUCCESS, success_message)
    else:
      error_message = "you'r comment didnt submited"
      messages.add_message(request, messages.ERROR, error_message)
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time)
  movie=get_object_or_404(movies,pk=pid)
  prev_post=Movie.objects.filter(pk__lt=movie.id,status=1,published_date__lte=current_time).order_by('-pk').first()
  next_post=Movie.objects.filter(pk__gt=movie.id,status=1,published_date__lte=current_time).order_by('pk').first()
  movie.count_views+=1
  movie.save()
  if request.user.is_authenticated:
    movie.login_require=True
    comments=Comment.objects.filter(movie=movie.id,approved=True)
    form=CommentForm() 
    context={'movie':movie,'comments':comments,'form':form,'prev_post':prev_post,'next_post':next_post,}
    return render(request,'blog/details.html',context)
  else:
    next_url=reverse('blog:details',kwargs={'pid':movie.id})
    return redirect(reverse('accounts:login') + '?next=' + next_url)

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