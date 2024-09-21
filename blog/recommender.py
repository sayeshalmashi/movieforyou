import os
import numpy as np
import pandas as pd
import ast
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
import pickle

# API Key and Base URL for TMDb
API_KEY = '5903757e800fec82004573c343c707d5'
MOVIES_API_URL = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1"
GENRE_API_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"

# Get the list of genres from TMDb
def get_genres():
    response = requests.get(GENRE_API_URL)
    data = response.json()
    genres = {genre['id']: genre['name'] for genre in data['genres']}
    return genres

genres_dict = get_genres()

# Get movies from TMDb API
def get_movies_from_api():
    response = requests.get(MOVIES_API_URL)
    data = response.json()
    movies = data['results']
    
    # Process movie data
    processed_movies = []
    for movie in movies:
        movie_data = {
            'movie_id': movie['id'],
            'title': movie['title'],
            'overview': movie['overview'].split(),
            'genres': [genres_dict[genre_id] for genre_id in movie['genre_ids']],
            'keywords': [],  # If you have keywords available
            'cast': [],  # Cast can be added if available
            'director': []  # Director can be added if available
        }
        processed_movies.append(movie_data)

    return processed_movies

# Fetch movies from API
movies = get_movies_from_api()
movies_df = pd.DataFrame(movies)

# Combine tags into a single string and convert to lowercase
movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['director']
df = movies_df[['movie_id', 'title', 'tags']]

# Fixing the warning by using .loc
df.loc[:, 'tags'] = df['tags'].apply(lambda x: " ".join(x).lower())

# Stemming
ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

df.loc[:, 'tags'] = df['tags'].apply(stem)

# Vectorizing and similarity calculation
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Save model and vectorizer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'similarity.pkl'), 'wb') as f:
    pickle.dump(similarity, f)
with open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'wb') as f:
    pickle.dump(cv, f)

# Movie recommendation function
def recommend(movie):
    # Check if the movie exists in the dataset
    if movie not in df['title'].values:
        print(f"Movie '{movie}' not found in dataset.")
        return []

    # Get movie index
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Sort movie recommendations
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Display recommended movie titles
    recommended_movies = [df.iloc[i[0]].title for i in movies_list]
    print(f"Recommended movies for '{movie}': {recommended_movies}")
    return recommended_movies
