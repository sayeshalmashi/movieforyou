from django.shortcuts import render,get_object_or_404


def catalog_view(request,**kwargs):
  
  return render(request,'blog/catalog.html')

def category_view(request,pid):
  return render(request,'blog/category.html')

def details_view(request,pid):
  return render(request,'blog/details.html')
