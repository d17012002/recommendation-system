import streamlit as st
import requests

#-------fetch poster for explore section ----------------#
def fetch_poster_explore(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3edecd00ecab3757c36ae3761d739277&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


#----- Display names and images----------------#
def display_explore(names, img):
    with st.container():
        st.write("###")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(img[0], width=240, caption=names[0])
        with col2:
            st.image(img[1], width=240, caption=names[1])
        with col3:
            st.image(img[2], width=240, caption=names[2])
        with col4:
            st.image(img[3], width=240, caption=names[3])
