from django import template
from django.utils import timezone
from blog.models import Movie ,Category

register = template.Library()

@register.inclusion_tag('website/latestmovie.html')
def latestmovie(arg=8):
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time).order_by('-released_date')[:arg]
  return {'movies':movies}


@register.inclusion_tag('blog/moviecategory.html')
def postcategory():
  current_time=timezone.now()
  movies=Movie.objects.filter(status=1,published_date__lte=current_time)
  categories=Category.objects.all()
  cat_dict={}
  for name in categories:
    cat_dict[name]=movies.filter(category=name).count()
  return {'categories':cat_dict}