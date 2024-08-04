from django.core.management.base import BaseCommand
from blog.views import fetch_movies


class Command(BaseCommand):
    help = 'fetch and save popular movies from TMDB'
    def handle(self , *args , **options):
        fetch_movies()
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved'))