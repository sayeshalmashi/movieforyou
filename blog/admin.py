from django.contrib import admin
from blog.models import Movie , Category ,Comment
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
  date_hierarchy='release_date'
  empty_value_display='-empty-'
  list_display=('title','vote_count','release_date','login_require',)
  list_filter=('release_date',) #topple akharesh ,
  ordering=['-release_date']
  search_fields=['title','overview']


class CommentAdmin(admin.ModelAdmin):
  date_hierarchy='created_date'
  empty_value_display='-empty-'
  list_display=('name','movie','approved','created_date')
  list_filter=('movie','approved',) #topple akharesh ,
  ordering=['-created_date']
  search_fields=['name','movie']

admin.site.register(Comment,CommentAdmin)
admin.site.register(Movie,MovieAdmin)
admin.site.register(Category)
