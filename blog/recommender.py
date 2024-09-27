import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movieforyou.settings')

# Setup Django
django.setup()

from blog.models import Movie, Rating
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


# Define the function for generating recommendations
def recommend_movies_for_user(user, num_recommendations=5):
    # Get user's rated movies
    user_ratings = Rating.objects.filter(user=user).select_related('movie')

    # If user hasn't rated any movies, return an empty list
    if not user_ratings.exists():
        return []

    # Create a DataFrame for user-rated movies
    rated_movies_df = pd.DataFrame(
        [(r.movie.id, r.movie.title, r.movie.overview, ' '.join([g.name for g in r.movie.genres.all()]), 
         ' '.join([k.name for k in r.movie.keywords.all()]), r.rating) 
         for r in user_ratings],
        columns=['movie_id', 'title', 'overview', 'genres', 'keywords', 'rating']
    )

    # Combine text data for each rated movie
    rated_movies_df['combined_features'] = rated_movies_df['overview'] + ' ' + rated_movies_df['genres'] + ' ' + rated_movies_df['keywords']

    # Get all other movies
    all_movies = Movie.objects.exclude(id__in=rated_movies_df['movie_id'])

    # Create a DataFrame for all other movies
    all_movies_df = pd.DataFrame(
        [(m.id, m.title, m.overview, ' '.join([g.name for g in m.genres.all()]), 
         ' '.join([k.name for k in m.keywords.all()])) 
         for m in all_movies],
        columns=['movie_id', 'title', 'overview', 'genres', 'keywords']
    )

    # Combine text data for each movie
    all_movies_df['combined_features'] = all_movies_df['overview'] + ' ' + all_movies_df['genres'] + ' ' + all_movies_df['keywords']

    # TF-IDF vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix_rated = tfidf.fit_transform(rated_movies_df['combined_features'])
    tfidf_matrix_all = tfidf.transform(all_movies_df['combined_features'])

    # Calculate cosine similarity between rated movies and all other movies
    cosine_similarities = cosine_similarity(tfidf_matrix_rated, tfidf_matrix_all)

    # Get top rated movies by the user (high rating)
    top_rated_movies = rated_movies_df[rated_movies_df['rating'] >= 4]

    # Get recommendations based on the top-rated movies
    similar_movies = []
    for idx, movie in top_rated_movies.iterrows():
        sim_scores = list(enumerate(cosine_similarities[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        top_similar_movie_indices = [i[0] for i in sim_scores[:num_recommendations]]
        top_similar_movies = all_movies_df.iloc[top_similar_movie_indices]
        similar_movies.append(top_similar_movies)

    # Concatenate all recommended movies and remove duplicates
    recommendations = pd.concat(similar_movies).drop_duplicates(subset=['movie_id']).head(num_recommendations)

    # Return movie titles
    return recommendations['title'].tolist()