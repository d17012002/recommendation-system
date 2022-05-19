import firebaseDB
import streamlit as st
import components.Home as Home
import components.Navbar as nav
import components.Movie as Movie

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
            Movie.movie()
