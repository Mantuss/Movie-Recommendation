import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended = []
    recommended_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetchPoster(movie_id))

    return recommended, recommended_poster


def fetchPoster(id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=&language=en-US'.format(id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500" + str(data['poster_path'])


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')
selected = st.selectbox(
    "",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected)
    col = st.columns(len(names))

    count = 0;
    for i in col:
        with i:
            st.text(names[count]);
            st.image(posters[count]);
            count+=1
    