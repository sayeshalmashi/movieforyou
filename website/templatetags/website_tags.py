from django import template
from django.utils import timezone
from blog.models import Movie ,Category

register = template.Library()

@register.inclusion_tag('website/latestmovie.html')
def latestmovie(arg=8):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1).order_by('-release_date')[:arg]
  return {'movies':movies}


@register.inclusion_tag('blog/moviecategory.html')
def postcategory():
  movies=Movie.objects.filter(status=1)
  categories=Category.objects.all()
  cat_dict={}
  for name in categories:
    cat_dict[name]=movies.filter(category=name).count()
  return {'categories':cat_dict}