import streamlit as st
from utils.database import get_project_by_id, update_project

st.title("Project Details")

# Get the project ID from the URL query parameter
project_id = st.experimental_get_query_params().get("id", [None])[0]

if project_id is None:
    st.error("No project ID provided")
else:
    project = get_project_by_id(project_id)
    
    if project is None:
        st.error("Project not found")
    else:
        st.header(project['name'])
        
        # Display project details
        st.write(f"Description: {project['description']}")
        st.write(f"Status: {project['status']}")
        st.write(f"Created: {project['created_at']}")
        
        # Edit project details
        with st.form("edit_project"):
            new_name = st.text_input("Project Name", project['name'])
            new_description = st.text_area("Project Description", project['description'])
            new_status = st.selectbox("Status", ["New", "In Progress", "Completed"], index=["New", "In Progress", "Completed"].index(project['status']))
            
            if st.form_submit_button("Update Project"):
                updated_project = update_project(project_id, new_name, new_description, new_status)
                if updated_project:
                    st.success("Project updated successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to update project")

        # Add "Back to All Projects" button
        if st.button("Back to All Projects"):
            st.switch_page("pages/05_projects.py")