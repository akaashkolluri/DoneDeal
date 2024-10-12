import streamlit as st
from components.project_card import project_card
from utils.database import get_projects, add_project

st.title("Projects")

projects = get_projects()

for project in projects:
    project_card(project)

st.subheader("Add New Project")
project_name = st.text_input("Project Name")
project_description = st.text_area("Project Description")
if st.button("Add Project"):
    new_project = add_project(project_name, project_description)
    st.success(f"Project '{new_project['name']}' added successfully!")
    st.experimental_rerun()