import streamlit as st
from streamlit_lottie import st_lottie
import requests


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


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_contract = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_9wpyhdzo.json")
lottie_ai = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_wqypnpu5.json")

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;600&display=swap');

body {
    color: #2c3e50;
}
.stApp {
}
.main-title {
    font-size: 4rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0;
}
.subtitle {
    font-size: 1.5rem;
    color: #34495e;
    margin-top: 0;
    font-weight: 300;
}
.cta-button {
    background-color: #3498db;
    color: white;
    padding: 12px 24px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    display: inline-block;
}
.cta-button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}
.card {
    background-color: #ffffff;
    border-radius: 10px;
    padding: 25px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    height: 100%;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
.feature-icon {
    font-size: 2.5rem;
    color: #3498db;
    margin-bottom: 15px;
}
h2 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 30px;
}
h3 {
    color: #34495e;
    font-size: 1.5rem;
}
.stLottie {
    background: transparent !important;
}
.lottie-container {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h1 class='main-title'>Done Deal</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-Powered Legal Contracts for the Modern Lawyer</p>", unsafe_allow_html=True)
    
    # Log In button
    if st.button("Log In", key="login_button", help="Click to log in"):
        st.switch_page("pages/02_login.py")  # This will navigate to login.py

with col2:
    st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
    st_lottie(lottie_contract, height=300, key="contract")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Features section
st.markdown("<h2 style='text-align: center;'>Why Choose Done Deal?</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='feature-icon'>⚖️</div>
        <h3>Intelligent Contracts</h3>
        <p>Create legally sound contracts with AI assistance, ensuring comprehensive coverage and clarity.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='feature-icon'>🔍</div>
        <h3>Risk Analysis</h3>
        <p>Identify potential legal risks and loopholes in your contracts with our advanced AI analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='card'>
        <div class='feature-icon'>🚀</div>
        <h3>Efficiency Boost</h3>
        <p>Streamline your contract creation process, saving time and resources for your practice.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='card'>
        <div class='feature-icon'>👥</div>
        <h3>Team Simulation</h3>
        <p>Create simulations of your team and adversarial teams to craft bulletproof contracts that anticipate every scenario.</p>
    </div>
    """, unsafe_allow_html=True)

# AI section
st.markdown("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
    st_lottie(lottie_ai, height=300, key="ai")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h2>Powered by Advanced AI</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <p>Our state-of-the-art AI technology analyzes thousands of legal documents to provide you with the most accurate and up-to-date contract suggestions. With Done Deal, you're not just getting a contract generator – you're getting an AI-powered legal assistant that evolves with the law.</p>
    </div>
    """, unsafe_allow_html=True)

# Call to action
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>Ready to revolutionize your legal practice?</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><a href='#' class='cta-button'>Start Your Free Trial</a></p>", unsafe_allow_html=True)