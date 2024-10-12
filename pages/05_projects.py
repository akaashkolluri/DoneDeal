import streamlit as st
from utils.projects import get_projects, add_project, ProjectCard, show_project_details, save_projects

st.set_page_config(page_title="Projects", layout="wide")

# Load projects from the database every time the page is loaded
if 'projects' not in st.session_state:
    st.session_state.projects = get_projects()

if 'show_details' not in st.session_state:
    st.session_state.show_details = False
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None

# Create two columns for the main layout
main_col, side_panel = st.columns([2, 1])

with main_col:
    st.title("Projects")

    # Display projects in a grid
    project_cols = st.columns(3)
    for i, project in enumerate(st.session_state.projects):
        with project_cols[i % 3]:
            # if ProjectCard(project):
            #     st.session_state.selected_project = project
            #     st.session_state.show_details = True
            #     st.rerun()
            if st.button(f"{project['name']}\n{project['team']}\n{project['description'][:20]}...", key=f"project_{project['id']}"):
                st.session_state.selected_project_id = project['id']
                st.switch_page("pages/06_project_details.py")

# Side panel for Add Project form and Edit Project details
with side_panel:
    if st.session_state.show_details and st.session_state.selected_project:
        show_project_details(st.session_state.selected_project)
    else:
        st.title("Add New Project")

        new_name = st.text_input("Name", key="new_name")
        new_description = st.text_area("Description", key="new_description")
        new_team = st.text_input("Team", key="new_team")

        if st.button("Add Project"):
            if new_name and new_description:
                new_project = add_project(new_name, new_description)
                st.session_state.projects.append(new_project)
                save_projects(st.session_state.projects)
                st.success(f"Project '{new_name}' added successfully!")
                # Clear the form by resetting the session state
                for key in ['new_name', 'new_description', 'new_team']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# Custom CSS for project card styling
st.markdown("""
<style>
    div.stButton > button:first-child {
        background-color: #f0f0f0;
        border: 1px solid #d3d3d3;
        padding: 10px;
        border-radius: 10px;
        text-align: left;
        width: 100%;
    }
    div.stButton > button:hover {
        border: 1px solid #a0a0a0;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)