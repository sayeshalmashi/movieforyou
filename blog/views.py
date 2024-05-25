from django.shortcuts import render,get_object_or_404


def movies_view(request):
  return render(request,'blog/movies.html')

def details_view(request):
  return render(request,'blog/details.html')
