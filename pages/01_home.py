import streamlit as st

st.title("Done Deal - Home")

st.write("""
Welcome to Done Deal, your ultimate platform for managing agents and projects.

Done Deal provides a comprehensive solution for:
- Tracking agent performance
- Managing multiple projects
- Streamlining your workflow

Get started by signing in or creating an account!
""")

if st.button("Sign In"):
    st.switch_page("pages/02_login.py")