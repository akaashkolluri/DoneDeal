import json
from datetime import datetime
import uuid
import streamlit as st
import os
def get_projects():
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
            # Add id to existing projects if they don't have one
            for project in projects:
                if 'id' not in project:
                    project['id'] = str(uuid.uuid4())
            return projects
    except FileNotFoundError:
        return []
def save_projects(projects):
    os.makedirs('data', exist_ok=True)
    with open('data/projects.json', 'w') as f:
        json.dump(projects, f)
def add_project(name, description):
    projects = get_projects()
    new_project = {
        'id': str(uuid.uuid4()),  # Generate a unique ID
        'name': name,
        'description': description,
        'team': 'New',
        'agents': 'New',
        'created_at': datetime.now().isoformat()
    }
    projects.append(new_project)
    save_projects(projects)
    return new_project
def get_project_by_id(project_id):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            return project
    return None
def update_project(project_id, name, description, team, agents):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            project['name'] = name
            project['description'] = description
            project['team'] = team
            project['agents'] = agents
            return True
    return False
def ProjectCard(project):
    card_content = f"""
    {project['name']}
    {project['team']}
    {project['agents']}
    {project['description'][:20] + "..." if len(project['description']) > 20 else project['description']}
    """
    return st.button(card_content, key=f"project_{project['id']}")
def delete_project(project_id):
    projects = get_projects()
    updated_projects = [project for project in projects if project['id'] != project_id]
    if len(projects) != len(updated_projects):
        save_projects(updated_projects)
        return True
    return False
def show_project_details(project):
    st.title(f"{project['name']} Details")
    
    new_name = st.text_input("Name", project['name'])
    new_description = st.text_area("Description", project['description'])
    new_team = st.text_input("Team", project['team'])
    new_agents = st.text_input("agents", project['agents'])
    if st.button("Update Project"):
        if update_project(project['id'], new_name, new_description, new_team, new_agents):
            st.success("Agent updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update agent.")
    if st.button("Delete Project"):
        if delete_project(project['id']):
            st.success(f"Project '{project['name']}' deleted successfully!")
            st.session_state.projects = get_projects()
            st.session_state.selected_project = None
            st.session_state.show_details = False
            st.rerun()
        else:
            st.error("Failed to delete project.")
    
    if st.button("Back to Add Project"):
        st.session_state.selected_project = None
        st.session_state.show_details = False
        st.rerun()