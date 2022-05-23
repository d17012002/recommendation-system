import firebaseDB
import streamlit as st
import pickle
import requests
import pandas as pd
import components.Home as Home
import components.Navbar as nav

from pyrebase import pyrebase
st.set_page_config(page_title="WeFlix", layout="wide")

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseDB.firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()


#-----USE LOCAL CSS---------#
Home.local_css("style/main.scss")

#----HEADER SECTION-----------#
title = '<h3 class="app-name">WeFlix App <3</h3><br>'
st.markdown(title, unsafe_allow_html=True)

#-----Sidebar---------#
st.sidebar.title("WeFlix - Authentication")

# Import modelled data
movies_dict = pickle.load(open('./modelled-data/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('./modelled-data/similarity.pkl', 'rb'))


# Authentication
choice = st.sidebar.selectbox('LogIn/SignUp', ['Login', 'SignUp'])
email = st.sidebar.text_input("Please enter your email address")
password = st.sidebar.text_input("Please enter your password", type="password")

if choice == 'SignUp':
    handle = st.sidebar.text_input("Input your username", value="Default")
    submit = st.sidebar.button('Create my account')
    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created successfully!')
        st.balloons()
        # sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.subheader("Welcome! "+handle)
        st.info('Login via login drop down selected')

# Sorting list of tuples based on cosine distances
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
    for i in range(1, 6):
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
        st.write("###")
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
            flag = 0
            data = db.child("users").get()

            if (data.val() is not None):
                for i in data.each():
                    if(i.val()["Email_Id"]==email and i.val()["Searched_movie"]==selected_movie):
                        flag=1

            if flag==0:
                #store in database for history
                searched_movie = selected_movie
                #save in database
                search_history = {"Email_Id": str(email),"Searched_movie": searched_movie}
                db.child("users").push(search_history)
            
            names, data = suggest(selected_movie)
            display_suggestion(names, data)


#---------------EXPLORE SECTION-----------------#

def fetch_poster_explore(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3edecd00ecab3757c36ae3761d739277&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    

def explore_suggest(movie):
    # gives index of the movie
    movieIndex = movies[movies['title'] == movie].index[0]

    # distance of that movie from other movies
    arr = list(enumerate(similarity[movieIndex]))
    # sorting arr
    distances = merge_sort(arr)

    movies_list = []
    n = len(distances)
    for i in range(2, 6):
        movies_list.append(distances[n-i])

    recommended_movies = []
    recommended_movies_data = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch (poster,overview) from API
        recommended_movies_data.append(fetch_poster_explore(movie_id))

    return recommended_movies, recommended_movies_data

explore_description = '<p class="big-font">Vivamus volutpat sapien eget justo bibendum varius. Nulla pharetra placerat nulla, ac condimentum lectus blandit eget. Ut varius rutrum lectus, sit amet aliquet sapien condimentum sed.</p><br>'

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


def explore():
    search_history = db.child("users").get()
    with st.container():
        st.write("###")
        st.subheader("Movies you might like 💖")
        st.markdown(explore_description,unsafe_allow_html=True)
    if (search_history.val() is not None):     
        n = len(search_history.val())
        for i in range(n-1,-1,-1):
            if(search_history[i].val()["Email_Id"]==email):
                st.write("Because you liked: "+search_history[i].val()["Searched_movie"])
                names, data = explore_suggest(search_history[i].val()["Searched_movie"])
                display_explore(names,data)
                

#-------- Navbar -------------#
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        if email == "" or password == "":
            st.error("Invalid email and password. Please try again")

        user = auth.sign_in_with_email_and_password(email, password)

        selected = nav.navbar()
        if selected == "Home":
            Home.home()
        if selected == "Movies":
            movie()
        if selected == "Explore":
            explore()

