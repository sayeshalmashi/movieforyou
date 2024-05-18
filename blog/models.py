from django.db import models


# Create your models here.

class Movie(models.Model):
  title=models.CharField(max_length=255)
  content=models.TextField()
  rate=models.IntegerField()
  status=models.BooleanField(default=False)
  published_date=models.DateTimeField(null=True)
  create_date=models.DateTimeField(auto_now_add=True)
  update_date=models.DateTimeField(auto_now=True)
  class Meta:
    ordering=['-create_date']
    
  def __str__(self):
   return "{}-{}".format(self.title,self.id)