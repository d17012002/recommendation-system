import streamlit as st
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3edecd00ecab3757c36ae3761d739277&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'], data['overview'], data['genres'], data['tagline']

#---Display Suggested Movie-------------#
def display_suggestion(names, data):
    st.success("Success!")
    for i in range(len(names)):
        with st.container():
            st.write("###")
            col1, col2 = st.columns((1, 2.5))
            with col1:
                st.image(data[i][0], width=250, caption=data[i][3])
            with col2:
                st.markdown(
                    '<h4 class="movieTitle" >{}</h4>'.format(names[i]), unsafe_allow_html=True)
                st.write("---")
                st.write(data[i][1])
                st.write("Genres of the movie:")
                for genre in data[i][2]:
                    st.write('📌 ', genre['name'])