import streamlit as st


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


#-----Use local css--------#
def local_css(file_namae):
    with open(file_namae) as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)


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

