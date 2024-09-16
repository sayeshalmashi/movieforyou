import numpy as np # linear algebra
import pandas as pd # data processing
from sklearn.metrics.pairwise import cosine_similarity
movies = pd.read_csv('D:\\Project403\\tmdb_5000_movies.csv')
credits = pd.read_csv('D:\\Project403\\tmdb_5000_credits.csv')
def preprocess_data():
    movies['cast'] = credits['cast']
    movies['crew'] = credits['crew']
    movies = movies.merge(credits, on='title', suffixes=('_movies', '_credits'))
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.isnull().sum()
    movies_cleaned = movies.dropna()
    movies_cleaned.isnull().sum()
    movies = movies_cleaned
    return movies
def recommend_movies(movie_title, movies_df, num_recommendations=10):
    # جستجو برای فیلم مورد نظر کاربر
    idx = movies_df[movies_df['title'] == movie_title].index[0]

    # استفاده از یک روش مشابهت (مثلاً cosine similarity) برای پیدا کردن فیلم‌های مشابه
    cosine_sim = cosine_similarity(movies_df['overview'])  # شباهت بر اساس ویژگی‌های محتوایی

    # دریافت اندیس‌های فیلم‌های مشابه
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]  # بازگرداندن n فیلم مشابه

    # بازگرداندن عنوان فیلم‌های مشابه
    movie_indices = [i[0] for i in sim_scores]
    return movies_df['title'].iloc[movie_indices]




