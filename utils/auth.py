import streamlit as st

def login_user(username, password):
    # This is a placeholder. In a real app, you'd check against a database.
    if username == "admin" and password == "password":
        st.session_state['logged_in'] = True
        return True
    return False

def is_logged_in():
    return st.session_state.get('logged_in', False)

def logout_user():
    st.session_state['logged_in'] = False