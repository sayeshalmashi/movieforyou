from django.contrib.syndication.views import Feed
from django.urls import reverse
from blog.models import Movie
from django.utils import timezone

class LatestEntriesFeed(Feed):
    title = "blog newst posts"
    link = "/rss/feed"
    description = "best blog ever"
    
    def items(self):
        current_time=timezone.now()
        return Movie.objects.filter(status=True,published_date__lte=current_time)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]
 