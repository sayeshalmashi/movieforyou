from django.contrib import admin
from blog.models import Movie , Category ,Comment
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
  date_hierarchy='create_date'
  empty_value_display='-empty-'
  list_display=('title','status','author','published_date','create_date','released_date','login_require',)
  list_filter=('status',) #topple akharesh ,
  ordering=['-create_date']
  search_fields=['title','content']


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
