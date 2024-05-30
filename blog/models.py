from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
  name=models.CharField(max_length=255)
  def __str__(self):
    return self.name
  

class Movie(models.Model):
  title=models.CharField(max_length=255)
  content=models.TextField()
  rate=models.IntegerField()
  category=models.ManyToManyField(Category)
  status=models.BooleanField(default=False)
  published_date=models.DateTimeField(null=True)
  create_date=models.DateTimeField(auto_now_add=True)
  update_date=models.DateTimeField(auto_now=True)
  released_date=models.DateTimeField(null=True)
  # director=models.ManyToManyField()
  author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  # slug = models.SlugField(unique=False,blank=True)
  class Meta:
    ordering=['-create_date']
    
  def __str__(self):
   return "{}-{}".format(self.title,self.id)
  
  # def save(self, *args, **kwargs):
  #     if not self.slug:
  #         self.slug = slugify(self.title)
  #     super(Movie, self).save(*args, **kwargs)