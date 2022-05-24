#------HORIZONTAL NAVBAR------------#
from streamlit_option_menu import option_menu

def navbar():
    selected = option_menu(
        menu_title=None,
        options=["Home", "Movies", "Explore"],
        icons=["house", "bi-pc-display-horizontal",
               "bi-person-lines-fill", "bi-x-circle"],
        menu_icon="cast",
        styles={
            "container": {"width": "48%"},
        },
        orientation="horizontal"
    )
    return selected
