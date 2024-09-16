from django.contrib import admin
from blog.models import Movie , Category ,Comment, Rating
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
  date_hierarchy='release_date'
  empty_value_display='-empty-'
  list_display=('title','vote_count','trailer_url','release_date','login_require',)
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
  
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'rated_at')
    list_filter = ('user', 'movie', 'rating') 
    search_fields = ('user__username', 'movie__title')

admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Movie,MovieAdmin)
admin.site.register(Category)