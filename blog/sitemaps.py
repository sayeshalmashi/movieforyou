from django.contrib.sitemaps import Sitemap
from blog.models import Movie
from django.utils import timezone

class BlogSitemap(Sitemap):
    
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        current_time=timezone.now()
        return Movie.objects.filter(status=1,published_date__lte=current_time)

    def lastmod(self, obj):
        return obj.published_date