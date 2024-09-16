import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# دریافت مسیر ریشه پروژه (محل فایل manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# آدرس‌دهی فایل‌های CSV
movies_path = os.path.join(BASE_DIR, 'tmdb_5000_movies.csv')
credits_path = os.path.join(BASE_DIR, 'tmdb_5000_credits.csv')

# بارگذاری فایل‌های CSV
movies = pd.read_csv(movies_path)
credits = pd.read_csv(credits_path)

# بررسی اینکه ستون movie_id در داده‌های movies وجود دارد
print(movies.columns)  # این خط برای بررسی ستون‌ها است

def preprocess_data():
    global movies

    # ترکیب داده‌های movies و credits
    movies['cast'] = credits['cast']
    movies['crew'] = credits['crew']
    movies = movies.merge(credits, on='title', suffixes=('_movies', '_credits'))
     
    # بررسی وجود ستون movie_id قبل از ادامه پردازش
    if 'movie_id' not in movies.columns:
        raise KeyError("'movie_id' column not found in movies DataFrame")

    # انتخاب ستون‌های مورد نیاز
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies.isnull().sum()
    
    # جایگزینی مقادیر خالی در ستون‌های کلیدی
    movies['overview'] = movies['overview'].fillna('')
    movies['cast'] = movies['cast'].fillna('[]')
    movies['crew'] = movies['crew'].fillna('[]')

    # حذف سطرهایی که هنوز داده‌های نامعتبر دارند
    movies_cleaned = movies.dropna()
    movies_cleaned.isnull().sum()
    movies = movies_cleaned

    if movies.empty:
        raise ValueError("Movies dataset is empty after cleaning")

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
