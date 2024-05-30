from django.contrib import admin
from blog.models import Movie , Category 
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
  date_hierarchy='create_date'
  empty_value_display='-empty-'
  list_display=('title','status','author','published_date','create_date','released_date',)
  list_filter=('status',) #topple akharesh ,
  ordering=['-create_date']
  search_fields=['title','content']
  # prepopulated_fields = {'slug': ('title',)}

admin.site.register(Movie,MovieAdmin)
admin.site.register(Category)
