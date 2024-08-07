from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from blog.models import Movie, Comment, Category , Rating
from blog.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Count
from datetime import datetime
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = '5903757e800fec82004573c343c707d5'
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_and_save_movies():
    total_movies = 0
    page = 1

    while total_movies < 800:
        # Define the endpoint and parameters
        url = f'{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}'

        # Make the request
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error fetching data: {response.status_code}')
            return

        data = response.json()
        movies = data.get('results', [])

        if not movies:
            break

        for movie_data in movies:
            release_date = movie_data.get('release_date')
            if release_date:
                release_date = datetime.strptime(release_date, '%Y-%m-%d')
            else:
                release_date = None

            # Get or create movie
            movie, created = Movie.objects.get_or_create(
                movie_id=movie_data['id'],
                defaults={
                    'adult': movie_data['adult'],
                    'backdrop_path': movie_data.get('backdrop_path'),
                    'original_language': movie_data['original_language'],
                    'original_title': movie_data['original_title'],
                    'overview': movie_data['overview'],
                    'popularity': movie_data['popularity'],
                    'poster_path': movie_data.get('poster_path'),
                    'release_date': release_date,
                    'title': movie_data['title'],
                    'video': movie_data['video'],
                    'vote_average': movie_data['vote_average'],
                    'vote_count': movie_data['vote_count'],
                }
            )

            # Process genres
            genre_ids = movie_data['genre_ids']
            for genre_id in genre_ids:
                genre_data = fetch_genre_by_id(genre_id)
                genre, _ = Category.objects.get_or_create(
                    genre_id=genre_data['id'],
                    defaults={'name': genre_data['name']}
                )
                movie.genres.add(genre)

            # Fetch and save the trailer
            trailer_url = fetch_trailer_url(movie_data['id'])
            if trailer_url:
                movie.trailer_url = trailer_url

            movie.save()

        total_movies += len(movies)
        page += 1

def fetch_trailer_url(movie_id):
    # Define the endpoint and parameters
    url = f'{BASE_URL}/movie/{movie_id}/videos'
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }

    # Make the request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f'Error fetching trailer data: {response.status_code}')
        return None

    videos = response.json().get('results', [])
    
    # Filter for trailers
    for video in videos:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f'https://www.youtube.com/watch?v={video["key"]}'

    return None

def fetch_genre_by_id(genre_id):
    # Define the endpoint and parameters
    url = f'{BASE_URL}/genre/movie/list'
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }

    # Make the request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f'Error fetching genre data: {response.status_code}')
        return {}

    genres = response.json().get('genres', [])
    for genre in genres:
        if genre['id'] == genre_id:
            return genre

    return {}


def movies_view(request, **kwargs):
    current_time = timezone.now()
    movies = Movie.objects.filter(status=True, release_date__lte=current_time).order_by('-movie_id')
    
    # Filter movies by category name
    if 'cat_name' in kwargs:
        movies = movies.filter(genres__name__iexact=kwargs['cat_name'])
    categories=Category.objects.annotate(movie_count=Count('movies')).filter(movie_count__gt=0)
    # Pagination
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    try:
        movies = paginator.get_page(page_number)
    except PageNotAnInteger:
        movies = paginator.get_page(1)
    except EmptyPage:
        movies = paginator.get_page(paginator.num_pages)
# Custom pagination logic for displaying 5-page ranges
    def get_page_range(current_page, total_pages, max_range=5):
        start = max(current_page - max_range // 2, 1)
        end = min(start + max_range - 1, total_pages)
        start = max(end - max_range + 1, 1)
        return range(start, end + 1)

    page_range = get_page_range(movies.number, paginator.num_pages)

    context = {
        'movies': movies,
        'categories': categories,
        'page_range': page_range,
    }
    return render(request, 'blog/movies.html', context)


# Define details_view function
def details_view(request, pid):
    movie = get_object_or_404(Movie, pk=pid, status=True)
    categories=movie.genres.all()
    similar_movies =Movie.objects.filter(genres__in=categories).exclude(id=movie.id).distinct()[:10]
    if request.user.is_authenticated:
        comments = Comment.objects.filter(movie=movie, approved=True)
        form = CommentForm()
        
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.movie = movie
                comment.save()
                messages.success(request, "Your comment was submitted successfully.")
            else:
                messages.error(request, "There was an error submitting your comment.")
        
        context = {
            'movie': movie,
            'categories':categories,
            'comments': comments,
            'form': form,
            'similar_movies':similar_movies ,
        }
        return render(request, 'blog/details.html', context)
    else:
        next_url = reverse('blog:details', kwargs={'pid': movie.id})
        return redirect(f"{reverse('accounts:login')}?next={next_url}")


@csrf_exempt
def rate_movie(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        
        if not movie_id or not rating:
            return JsonResponse({'message': 'Invalid data'}, status=400)
        
        movie = Movie.objects.get(pk=movie_id)
        # فرض بر این است که هر کاربر می‌تواند فقط یک بار امتیاز بدهد
        rating_obj, created = Rating.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={'rating': rating}
        )
        
        return JsonResponse({'message': 'Rating submitted successfully'})
    return JsonResponse({'message': 'Invalid method'}, status=405)
# Define blog_search function
def blog_search(request):
    current_time = timezone.now()
    movies = Movie.objects.filter(status=True, release_date__lte=current_time).order_by('-movie_id')
    
    if 's' in request.GET:
        s = request.GET.get('s')
        movies = movies.filter(title__icontains=s)
    
    context = {'movies': movies}
    return render(request, 'blog/movies.html', context)