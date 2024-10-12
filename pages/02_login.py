import streamlit as st
from utils.auth import login_user

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login_user(username, password):
        st.success("Logged in successfully!")
        st.switch_page("pages/03_dashboard.py")
    else:
        st.error("Invalid username or password")

if st.button("Create Account"):
    st.info("Account creation functionality to be implemented")