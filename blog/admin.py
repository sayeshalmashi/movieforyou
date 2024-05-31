from django.contrib import admin
from blog.models import Movie
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
  date_hierarchy='create_date'
  empty_value_display='-empty-'
  list_display=('title','status','published_date','create_date','released_date',)
  list_filter=('status',) #topple akharesh ,
  ordering=['-create_date']
  search_fields=['title','content']

admin.site.register(Movie,MovieAdmin)