import streamlit as st
from utils.auth import login_user

st.set_page_config(layout="wide", page_title="Done Deal - AI-Powered Legal Contracts", initial_sidebar_state="collapsed")
# Hide the sidebar
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');

body {
    background-color: #f8f9fa;

}
.stApp {

}
.main-title {
    font-size: 3rem;
    font-weight: 700;
    
    margin-bottom: 20px;
}
.subtitle {
    font-size: 1.2rem;
    color: #34495e;
    margin-top: 0;
    font-weight: 300;
    margin-bottom: 30px;
}
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 40px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.stTextInput > div > div > input {
    background-color: #f8f9fa;
    color: #2c3e50;
    border: 1px solid #ced4da;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
}
.stButton > button {
    background-color: #3498db;
    color: white;
    padding: 12px 24px;
    border-radius: 5px;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 20px;
}
.stButton > button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}
.forgot-password {
    margin-top: 20px;
    font-size: 14px;
    text-align: center;
}
.forgot-password a {
    color: #3498db;
    text-decoration: none;
}
.forgot-password a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Main content
# st.markdown("<div class='login-container'>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Done Deal</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Log in to your account</p>", unsafe_allow_html=True)

username = st.text_input("Email or username")
password = st.text_input("Password", type="password")

if st.button("Log In"):
    if login_user(username, password):
        st.success("Logged in successfully!")
        st.switch_page("pages/03_dashboard.py")
    else:
        st.error("Invalid username or password")

st.markdown("<div class='forgot-password'><a href='#'>Forgot password?</a></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Remove Streamlit's default menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)