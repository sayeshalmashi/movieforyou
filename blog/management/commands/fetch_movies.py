import requests
from blog.models import Movie , Comment, Category
def fetch_genres():
    api_key = 'YOUR_API_KEY'
    url = f'https://api.themoviedb.org/3/genre/movie/list'
    params = {'api_key': api_key, 'language': 'en-US'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        for genre in genres:
            Category.objects.get_or_create(name=genre['name'])
    else:
        print('Failed to fetch genres.')

def fetch_and_save_movies():
    api_key = 'YOUR_API_KEY'
    url = f'https://api.themoviedb.org/3/movie/popular'
    params = {'api_key': 'b346941d699868e0b62683a329a2496f', 'language': 'en-US', 'page': 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        movies = response.json().get('results', [])
        for movie in movies:
            new_movie, created = Movie.objects.get_or_create(
                title=movie['title'],
                defaults={
                    'content': movie['overview'],
                    'rate': movie['vote_average'],
                    'published_date': movie['release_date'],
                    'image': movie['poster_path'], # باید از یک URL کامل استفاده کنید
                    'status': True,  # مثلا فیلم‌هایی که در TMDB موجود هستند
                    'login_require': False  # مثلا برای همه کاربران نمایش داده شود
                }
            )
            if created:
                # اضافه کردن ژانرها به فیلم
                genre_ids = movie.get('genre_ids', [])
                for genre_id in genre_ids:
                    genre = Category.objects.filter(id=genre_id).first()
                    if genre:
                        new_movie.category.add(genre)
                new_movie.save()
    else:
        print('Failed to fetch movies.')
