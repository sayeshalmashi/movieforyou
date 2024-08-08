from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
DEFAULT_DATE='2000-01-01'

class Category(models.Model):
    genre_id = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    genres = models.ManyToManyField(Category, related_name='movies')
    movie_id = models.IntegerField(unique=True, null=True)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(default=DEFAULT_DATE)
    title = models.CharField(max_length=255)
    video = models.BooleanField(default=False)
    trailer_url = models.URLField(null=True, blank=True)
    vote_average = models.FloatField()
    login_require = models.BooleanField(default=False)
    vote_count = models.IntegerField()
    status = models.BooleanField(default=True)


    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return "{}-{}".format(self.title, self.id)

    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'pid': self.id})
 
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    class Meta:
        unique_together = ('movie', 'user')
 
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