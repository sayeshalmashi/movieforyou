from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from blog.models import Movie, Comment, Category
from blog.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

TMDB_API_KEY='5903757e800fec82004573c343c707d5'
# Define fetch_movies function
def fetch_movies(api_key, page=1):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}'
    response = requests.get(url)
    print(f"API Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"API Response Data: {data}")  # چاپ داده‌های دریافت‌شده
        return data['results']
    else:
        print(f"API Request Failed: {response.text}")  # چاپ خطای احتمالی
        return None

def save_movies_to_db(api_key):
    movies_data = fetch_movies(api_key)
    if movies_data:
        for movie_data in movies_data:
            try:
                genre_ids = movie_data.get('genre_ids', [])
                categories = []
                for genre_id in genre_ids:
                    category, created = Category.objects.get_or_create(id=genre_id)
                    categories.append(category)

                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    defaults={
                        'content': movie_data.get('overview', ''),
                        'rate': movie_data.get('vote_average', 0),
                        'image': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
                        'status': not movie_data.get('adult', False),  # تغییر وضعیت به طور معکوس
                        'published_date': movie_data.get('release_date', None),
                        'released_date': movie_data.get('release_date', None),
                        'create_date': timezone.now(),
                    }
                )

                # اضافه کردن دسته‌بندی‌ها به فیلم
                movie.category.set(categories)
                movie.save()
                print(f"Movie '{movie.title}' saved successfully.")  # چاپ پیام موفقیت
            except Exception as e:
                print(f"Error saving movie '{movie_data['title']}': {str(e)}")  # چاپ پیام خطا


# Define movies_view function
def movies_view(request, **kwargs):
    current_time = timezone.now()
    movies = Movie.objects.filter(status=True, published_date__lte=current_time).order_by('-id')
    
    # Filter movies by category name
    if 'cat_name' in kwargs:
        movies = movies.filter(category__name__iexact=kwargs['cat_name'])
        
    # Filter movies by author username
    if 'author_username' in kwargs:
        movies = movies.filter(author__username__iexact=kwargs['author_username'])
    
    # Pagination
    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    try:
        movies = paginator.get_page(page_number)
    except PageNotAnInteger:
        movies = paginator.get_page(1)
    except EmptyPage:
        movies = paginator.get_page(paginator.num_pages)
    
    context = {'movies': movies}
    return render(request, 'blog/movies.html', context)

# Define details_view function
def details_view(request, pid):
    current_time = timezone.now()
    movie = get_object_or_404(Movie, pk=pid, status=True, published_date__lte=current_time)
    
    # Increment view count
    movie.count_views += 1
    movie.save()

    # Fetch previous and next movies
    prev_post = Movie.objects.filter(pk__lt=movie.id, status=True, published_date__lte=current_time).order_by('-pk').first()
    next_post = Movie.objects.filter(pk__gt=movie.id, status=True, published_date__lte=current_time).order_by('pk').first()
    
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
            'comments': comments,
            'form': form,
            'prev_post': prev_post,
            'next_post': next_post,
        }
        return render(request, 'blog/details.html', context)
    else:
        next_url = reverse('blog:details', kwargs={'pid': movie.id})
        return redirect(f"{reverse('accounts:login')}?next={next_url}")

# Define blog_search function
def blog_search(request):
    current_time = timezone.now()
    movies = Movie.objects.filter(status=True, published_date__lte=current_time).order_by('-id')
    
    if 's' in request.GET:
        s = request.GET.get('s')
        movies = movies.filter(title__icontains=s)
    
    context = {'movies': movies}
    return render(request, 'blog/movies.html', context)

# Define a new view for updating movies from TMDB
@login_required
def update_movies(request):
    api_key = '5903757e800fec82004573c343c707d5'  # Replace with your actual TMDB API key
    save_movies_to_db(api_key)
    messages.success(request, "Movies updated successfully from TMDB.")
    return redirect('blog:movies_view')