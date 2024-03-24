import streamlit as st
from streamlit import session_state as ss
from modules.nav import Navigator


st.set_page_config(page_title='Image generator', layout='centered')


def main():
    Navigator()

    st.title('Welcome to image generator :fire:')


if __name__ == '__main__':
    main()
