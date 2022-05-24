import pickle
import firebaseDB
import pandas as pd
import streamlit as st
import components.Home as Home
import components.Navbar as Nav
import components.Movie as Movie
import components.Sorting as Sorting
import components.Explore as Explore
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


#----Recommend Movie ---------------#
def suggest(movie):
    # gives index of the movie
    movieIndex = movies[movies['title'] == movie].index[0]

    # distance of that movie from other movies
    arr = list(enumerate(similarity[movieIndex]))
    # sorting arr
    distances = Sorting.merge_sort(arr)

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

        recommended_movies_data.append(Movie.fetch_poster(movie_id))

    return recommended_movies, recommended_movies_data


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
            Movie.display_suggestion(names, data)


#---------------EXPLORE SECTION-----------------#
def explore_suggest(movie):
    # gives index of the movie
    movieIndex = movies[movies['title'] == movie].index[0]

    # distance of that movie from other movies
    arr = list(enumerate(similarity[movieIndex]))
    # sorting arr
    distances = Sorting.merge_sort(arr)

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
        recommended_movies_data.append(Explore.fetch_poster_explore(movie_id))
    return recommended_movies, recommended_movies_data

explore_description = '<p class="big-font">Vivamus volutpat sapien eget justo bibendum varius. Nulla pharetra placerat nulla, ac condimentum lectus blandit eget. Ut varius rutrum lectus, sit amet aliquet sapien condimentum sed.</p><br>'

def delete_message():
    st.write("---")
    st.info("Oops! It seems you have no interactions yet.")
    #st.markdown("<p class='big-font'>Oops! It seems you have no interactions yet.</p>",unsafe_allow_html=True)

def explore():
    search_history = db.child("users").get()
    with st.container():
        st.write("###")
        st.subheader("Movies you might like 💖")
        st.markdown(explore_description,unsafe_allow_html=True)

    #clear search history
    if st.button("Clear History"):
        temp = db.child("users").get()
        for i in temp.each(): 
            if(i.val()["Email_Id"]==email):
                db.child("users").child(i.key()).remove()
        delete_message()

    else:
        st.write("---")
        if (search_history.val() is not None):     
            n = len(search_history.val())
            for i in range(n-1,-1,-1):
                if(search_history[i].val()["Email_Id"]==email):
                    st.write("Because you liked: "+search_history[i].val()["Searched_movie"])
                    names, data = explore_suggest(search_history[i].val()["Searched_movie"])
                    Explore.display_explore(names, data)
                

#-------- Navbar -------------#
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        if email == "" or password == "":
            st.error("Invalid email and password. Please try again")

        user = auth.sign_in_with_email_and_password(email, password)

        selected = Nav.navbar()
        if selected == "Home":
            Home.home()
        if selected == "Movies":
            movie()
        if selected == "Explore":
            explore()

