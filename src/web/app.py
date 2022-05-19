import streamlit as st
from pyrebase import pyrebase
from datetime import datetime
import pickle
import requests
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(page_title="WeFlix", layout="wide")

# Firebase Configuration
firebaseConfig = {
    'apiKey': "AIzaSyAsJ1rS75PeOwUvFwbJhPMjPVQWzhlvB68",
    'authDomain': "recommendation-system-29815.firebaseapp.com",
    'projectId': "recommendation-system-29815",
    'databaseURL': "https://recommendation-system-29815-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "recommendation-system-29815.appspot.com",
    'messagingSenderId': "1008385906880",
    'appId': "1:1008385906880:web:76b1b8a84cf055cb187525",
    'measurementId': "G-3YSZ04PK20"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()


# Import modelled data
movies_dict = pickle.load(open('modelled-data/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('modelled-data/similarity.pkl', 'rb'))

#-----USE LOCAL CSS---------#


def local_css(file_namae):
    with open(file_namae) as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)


local_css("style/main.scss")


#------- MAKRDOWN CONTENT-------------#
latest_movies = """
<iframe width="350" height="215" src="https://www.youtube.com/embed/aWzlQ2N6qqg?start=5&autoplay=1&mute=1" title="Dr. Strange" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<iframe width="350" height="215" src="https://www.youtube.com/embed/JKa05nyUmuQ?start=8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<iframe width="350" height="215" src="https://www.youtube.com/embed/eHp3MbsCbMg?start=20" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<br><br><br>
"""
upcoming_movies = """
<iframe width="350" height="215" src="https://www.youtube.com/embed/waTob1IM4UM?start=24&autoplay=1&mute=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<iframe width="350" height="215" src="https://www.youtube.com/embed/Ymu9wVN7pWs?start=24" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<iframe width="350" height="215" src="https://www.youtube.com/embed/6AvFHlKS6OE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

"""


app_description = '<p class="big-font">Pellentesque ornare quam id risus vulputate efficitur. Donec eleifend dictum ipsum sit amet auctor. Vivamus volutpat sapien eget justo bibendum varius. Nulla pharetra placerat nulla, ac condimentum lectus blandit eget. Ut varius rutrum lectus, sit amet aliquet sapien condimentum sed.</p><br>'
movie_description = '<p class="big-font">Donec eleifend dictum ipsum sit amet auctor. Vivamus volutpat sapien eget justo bibendum varius. Nulla pharetra placerat nulla, ac condimentum lectus blandit eget. Ut varius rutrum lectus, sit amet aliquet sapien condimentum sed.</p><br>'
#----HEADER SECTION-----------#

st.markdown('<h3 class="app-name">WeFlix App <3</h3><br>', unsafe_allow_html=True)


#--------------HOME SECTION-----------#
def home():
    with st.container():
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Recommender System :movie_camera:")
        st.markdown(app_description, unsafe_allow_html=True)
        st.write("---")

    # Movies in home page
    with st.container():
        st.write("Latest movies:")
        st.markdown(latest_movies, unsafe_allow_html=True)
        st.write("Upcoming movies:")
        st.markdown(upcoming_movies, unsafe_allow_html=True)


#---------------MOVIE SECTION------------#

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3edecd00ecab3757c36ae3761d739277&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'], data['overview'], data['genres'], data['tagline']


def suggest(movie):
    # gives index of the movie
    movieIndex = movies[movies['title'] == movie].index[0]
    # distance of that movie from other movies
    distances = similarity[movieIndex]

    movies_list = (sorted(list(enumerate(distances)),
                   reverse=True, key=lambda x: x[1])[1:7])

    recommended_movies = []
    recommended_movies_data = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch (poster,overview) from API
        recommended_movies_data.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_data


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


#-----Sidebar---------#
st.sidebar.title("WeFlix - Authentication")
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
        st.subheader("Welcome "+handle)
        st.info('Login via login drop down selected')


def navbar():
        #------HORIZONTAL NAVBAR------------#
        selected = option_menu(
            menu_title=None,
            options=["Home", "Movies", "Explore", "Logout"],
            icons=["house", "bi-pc-display-horizontal",
                   "bi-person-lines-fill", "bi-x-circle"],
            menu_icon="cast",
            styles={
                "container": {"width": "70%"},
            },
            orientation="horizontal"
        )
        return selected


if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        if email=="" or password=="":
            st.error("Invalid email and password. Please try again")

        user = auth.sign_in_with_email_and_password(email, password)

        selected = navbar()
        if selected == "Home":
            home()
        if selected == "Movies":
            movie()

        

