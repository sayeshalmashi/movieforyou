from django.shortcuts import render

def error_400(request,exception):
  context={'exceptions':exception}
  response = render(request,'errors/400.html',context=context)
  response.status_code = 400
  return response

def error_403(request,exception):
  context={'exceptions':exception}
  response = render(request,'errors/403.html',context=context)
  response.status_code = 403
  return response

def error_404(request,exception):
  context={'exceptions':exception}
  response = render(request,'errors/404.html',context=context)
  response.status_code = 404
  return response

def error_500(request):
  response = render(request,'errors/500.html')
  response.status_code = 500
  return response