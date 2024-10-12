import streamlit as st
from components.navigation import create_tabs

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

st.title("Dashboard")

tab1, tab2 = create_tabs(["Agents", "Projects"])

with tab1:
    st.write("Agents information will be displayed here")
    if st.button("Go to Agents Page"):
        st.switch_page("pages/04_agents.py")

with tab2:
    st.write("Projects information will be displayed here")
    if st.button("Go to Projects Page"):
        st.switch_page("pages/05_projects.py")