import streamlit as st
from components.project_card import project_card
from utils.database import get_projects, add_project
import streamlit.components.v1 as components

st.set_page_config(page_title="Projects", layout="wide")
st.markdown('<link rel="stylesheet" href="static/style.css">', unsafe_allow_html=True)

st.title("Projects")

# Initialize session state for projects if it doesn't exist
if 'projects' not in st.session_state:
    st.session_state.projects = get_projects()

# Add Project form
with st.form("add_project_form"):
    new_project_name = st.text_input("Project Name")
    new_project_description = st.text_area("Project Description")
    submit_button = st.form_submit_button("Add Project")

if submit_button:
    if new_project_name and new_project_description:
        new_project = add_project(new_project_name, new_project_description)
        st.session_state.projects.append(new_project)
        st.success(f"Project '{new_project_name}' added successfully!")
        st.experimental_rerun()
    else:
        st.error("Please provide both a name and description for the new project.")

# Display projects in a grid
cols = st.columns(3)
for i, project in enumerate(st.session_state.projects):
    with cols[i % 3]:
        project_card(project)

# Refresh projects button
if st.button("Refresh Projects"):
    st.session_state.projects = get_projects()
    st.experimental_rerun()