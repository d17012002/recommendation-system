import streamlit as st
import requests
import pandas as pd
import pickle

# Import modelled data
movies_dict = pickle.load(open('./modelled-data/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('./modelled-data/similarity.pkl', 'rb'))

#Sorting list of tuples based on cosine distances
def merge_sort(arr, key=lambda x: x[1]):
    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    merge_sort(left)
    merge_sort(right)

    i = j = k = 0
    while i < len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return arr



#---------MOVIE SECTION------------#
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3edecd00ecab3757c36ae3761d739277&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'], data['overview'], data['genres'], data['tagline']

#----Recommend Movie ---------------#
def suggest(movie):
    # gives index of the movie
    movieIndex = movies[movies['title'] == movie].index[0]

    # distance of that movie from other movies
    arr = list(enumerate(similarity[movieIndex]))
    # sorting arr
    distances = merge_sort(arr)

    movies_list = []
    n = len(distances)
    for i in range (1,7):
        movies_list.append(distances[n-i])
    


    recommended_movies = []
    recommended_movies_data = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch (poster,overview) from API
        recommended_movies_data.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_data


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

movie_description = '<p class="big-font">Donec eleifend dictum ipsum sit amet auctor. Vivamus volutpat sapien eget justo bibendum varius. Nulla pharetra placerat nulla, ac condimentum lectus blandit eget. Ut varius rutrum lectus, sit amet aliquet sapien condimentum sed.</p><br>'
def movie():
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Get all your favourite movies here...")
        st.markdown(movie_description, unsafe_allow_html=True)
        movie_display_list = []
        x = 0
        for i in movies["title"].values:
            if(x < 4800):
                movie_display_list.append(i)
                x = x+1
        selected_movie = st.selectbox(
            'Select any movie',
            movie_display_list
        )
        if st.button('Recommend'):
            names, data = suggest(selected_movie)
            display_suggestion(names, data)