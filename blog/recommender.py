import numpy as np # linear algebra
import pandas as pd # data processing
movies = pd.read_csv('D:\\Project403\\tmdb_5000_movies.csv')
credits = pd.read_csv('D:\\Project403\\tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title', suffixes=('_movies', '_credits'))
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies_cleaned = movies.dropna()
movies = movies_cleaned
import ast
def convert(obj):
    l = []
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l
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
    l = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
            break
    return l
movies['crew'] = movies['crew'].apply(crew_director)
movies = movies.rename(columns={'crew': 'director'})
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['director']
df = movies[['movie_id', 'title', 'tags']]
df['tags'] = df['tags'].apply(lambda x: " ".join(x))
df['tags'] = df['tags'].apply(lambda x: x.lower())
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
df['tags'].apply(stem)
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
cv.get_feature_names_out()
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]
def recommend(movie):
    movie_index = df[df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]    
    for i in movies_list:
        print(df.iloc[i[0]].title)
import pickle
with open('similarity.pkl','wb')as f:
    pickle.dump(similarity,f)
with open('vectorizer.pkl','wb')as f:
    pickle.dump(cv,f)