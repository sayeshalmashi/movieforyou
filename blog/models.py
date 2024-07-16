from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
  name=models.CharField(max_length=255)
  def __str__(self):
    return self.name
  
class Movie(models.Model):
  title=models.CharField(max_length=255)
  content=models.TextField()
  image=models.ImageField(upload_to='blog/',default='blog/default.jpg')
  rate=models.IntegerField()
  category=models.ManyToManyField(Category)
  status=models.BooleanField(default=False)
  count_views=models.IntegerField(default=0)
  published_date=models.DateTimeField(null=True)
  create_date=models.DateTimeField(auto_now_add=True)
  update_date=models.DateTimeField(auto_now=True)
  released_date=models.DateTimeField(null=True)
  author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  login_require=models.BooleanField(default=False)
  class Meta:
    ordering=['-create_date']
    
  def __str__(self):
   return "{}-{}".format(self.title,self.id)
  def get_absolute_url(self):
   return reverse('blog:details',kwargs={'pid':self.id})
  


class Comment(models.Model):
  movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
  name=models.CharField(max_length=255)
  email=models.EmailField()
  subject=models.CharField(max_length=255)
  message=models.TextField()
  approved=models.BooleanField(default=False)
  created_date=models.DateTimeField(auto_now_add=True)
  updated_date=models.DateTimeField(auto_now=True)
  class Meta:
    ordering=['-created_date']
    
  def __str__(self):
     return self.name