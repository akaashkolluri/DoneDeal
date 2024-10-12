import streamlit as st
import importlib

st.set_page_config(page_title="Done Deal", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.info("Select a page above.")

st.title("Welcome to Done Deal")
st.write("This is the main page of the Done Deal application.")
st.write("Please use the sidebar to navigate to different pages.")