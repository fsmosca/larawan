import streamlit as st


def HomeNav():
    st.sidebar.page_link('streamlit_app.py', label='Home', icon='🌳')


def DalleNav():
    st.sidebar.page_link('./pages/dalle.py', label='Image Generator', icon='🌿')


def Navigator():
    HomeNav()
    DalleNav()
