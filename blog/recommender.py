import os
import numpy as np
import pandas as pd
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
import pickle

# Load movie data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_file = os.path.join(BASE_DIR, 'tmdb_5000_movies.csv')
credits_file = os.path.join(BASE_DIR, 'tmdb_5000_credits.csv')

movies = pd.read_csv(movies_file)
credits = pd.read_csv(credits_file)
movies = movies.merge(credits, on='title', suffixes=('_movies', '_credits'))
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies_cleaned = movies.dropna()
movies = movies_cleaned

# Data processing functions
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

def convert3(obj):
    l = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter += 1
        else:
            break
    return l

movies['cast'] = movies['cast'].apply(convert3)

def crew_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

movies['crew'] = movies['crew'].apply(crew_director)
movies = movies.rename(columns={'crew': 'director'})
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Combine tags into a single string and convert to lowercase
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['director']
df = movies[['movie_id', 'title', 'tags']]

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
with open(os.path.join(BASE_DIR, 'similarity.pkl'), 'wb') as f:
    pickle.dump(similarity, f)
with open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'wb') as f:
    pickle.dump(cv, f)

# Movie recommendation function
def recommend(movie):
    # بررسی اینکه آیا فیلم در دیتافریم وجود دارد
    if movie not in df['title'].values:
        print(f"Movie '{movie}' not found in dataset.")
        return []

    # پیدا کردن ایندکس فیلم
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]

    # مرتب‌سازی لیست فیلم‌ها
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # نمایش عناوین فیلم‌های پیشنهادی
    recommended_movies = [df.iloc[i[0]].title for i in movies_list]
    print(f"Recommended movies for '{movie}': {recommended_movies}")
    return recommended_movies