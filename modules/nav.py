import streamlit as st


def HomeNav():
    st.sidebar.page_link('streamlit_app.py', label='Home')


def DalleNav():
    st.sidebar.page_link('./pages/dalle.py', label='Image Generator')


def Navigator():
    HomeNav()
    DalleNav()
