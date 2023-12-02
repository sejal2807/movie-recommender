import pickle
import streamlit as st
import requests
import pandas as pd
streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=PT+Serif&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)

import requests

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=b029056b23ab082b8613c7aec5ecb0ec&language=en-US".format(movie_id)
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        
        # Check if 'poster_path' is present in the response
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "Poster path not available for this movie."

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"Movie with ID {movie_id} not found. API response: {response.text}"
        else:
            return f"HTTP Error: {response.status_code} - {http_err}"

    except requests.exceptions.RequestException as req_err:
        return f"Request Exception: {req_err}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies_dictionary.pickle','rb'))
similarity = pickle.load(open('recommend_list.pickle','rb'))
movies = pd.DataFrame(movies)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


