import streamlit as st
import datetime
from streamlit_extras.stylable_container import stylable_container
from utils.database import get_project_by_id, update_project, remove_document, get_document_content
import os
import base64

def show_project_details_page():
    st.title("Project Details")

    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = []
    if 'previous_versions' not in st.session_state:
        st.session_state.previous_versions = []

    # Get the project ID from the session state
    project_id = st.session_state.get('selected_project_id')

    if project_id is None:
        st.error("No project selected.")
        st.write("Please go back to the projects page and select a project.")
        if st.button("Back to Projects"):
            st.switch_page("pages/05_projects.py")
        return

    # Fetch the project details
    project = get_project_by_id(project_id)
    if project is None:
        st.error(f"Project with ID {project_id} not found.")
        if st.button("Back to Projects"):
            st.switch_page("pages/05_projects.py")
        return

    # Create three columns for the panels
    left_col, middle_col, right_col = st.columns([1, 2, 1])

    with left_col:
        st.header("Project Information")
        
        # Project name
        new_name = st.text_input("Project Name", value=project['name'])
        
        # Project description (now editable)
        new_description = st.text_area("Project Description", value=project['description'])
        
        # Project team
        new_team = st.text_input("Project Team", value=project.get('team', 'Not specified'))
        
        # Display current documents
        st.subheader("Current Documents")
        for doc in project.get('documents', []):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(doc['name'])
            with col2:
                if st.button("Download", key=f"download_{doc['id']}"):
                    file_content = get_document_content(doc['path'])
                    st.download_button(
                        label="Click to Download",
                        data=base64.b64decode(file_content),
                        file_name=doc['name'],
                        mime=doc['type']
                    )
            with col3:
                if st.button("Remove", key=f"remove_{doc['id']}"):
                    if remove_document(project_id, doc['id']):
                        st.success(f"Document {doc['name']} removed.")
                        st.rerun()
                    else:
                        st.error("Failed to remove document.")

        # Add new documents
        new_documents = st.file_uploader("Add New Documents", accept_multiple_files=True)

        # Save changes button
        if st.button("Save Changes"):
            updated_project = update_project(project_id, new_name, new_description, project.get('status', 'New'), new_team, new_documents)
            if updated_project:
                st.success("Project updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update project.")

        if st.button("Back to Projects"):
            st.switch_page("pages/05_projects.py")

    contract_text = load_current_contract()
    with middle_col:
        st.header("Legal Contract")
        
        # Create an editable text area for the contract
        edited_contract = st.text_area("Edit Contract", value=contract_text, height=400)

        # Create two columns for the buttons
        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if st.button("View Previous Versions"):
                show_previous_versions()

        with button_col2:
            if st.button("Export"):
                export_contract(edited_contract)

    with right_col:
        st.header("Agent Feedback")
        
        # Agent selection
        st.subheader("Select Agents")
        agents = {
            "Outside Counsel": "👨‍⚖️",
            "In-House Counsel": "👩‍💼",
            "Opposing Counsel": "🧑‍⚖️",
            "Compliance Officer": "🕵️",
        }
        
        for agent, icon in agents.items():
            with stylable_container(key=f"agent_{agent}", css_styles="""
                button {
                    background-color: #f0f2f6;
                    border: none;
                    color: black;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 12px;
                    padding: 10px 24px;
                }
                button:hover {
                    background-color: #dfe3e8;
                }
                button:focus {
                    background-color: #21c7e8;
                }
            """):
                if st.button(f"{icon} {agent}", key=f"btn_{agent}"):
                    if agent in st.session_state.selected_agents:
                        st.session_state.selected_agents.remove(agent)
                    else:
                        st.session_state.selected_agents.append(agent)

        # Display feedback for selected agents
        st.subheader("Agent Feedback")
        for agent in st.session_state.selected_agents:
            st.write(f"**{agent}**")
            st.write(get_agent_feedback(agent))

        # Regenerate contract button
        if st.button("Regenerate Contract with Feedback"):
            new_contract = regenerate_contract(edited_contract, st.session_state.selected_agents)
            add_to_previous_versions(contract_text)
            st.session_state.current_contract = new_contract
            st.rerun()

def load_current_contract():
    if 'current_contract' not in st.session_state:
        st.session_state.current_contract = "This is the current version of the legal contract."
    return st.session_state.current_contract

def show_previous_versions():
    if not st.session_state.previous_versions:
        st.info("No previous versions available.")
    else:
        selected_version = st.selectbox(
            "Select a previous version:",
            options=range(len(st.session_state.previous_versions)),
            format_func=lambda x: f"Version {x + 1}"
        )
        st.text_area("Previous Version", value=st.session_state.previous_versions[selected_version], height=300)
        if st.button("Restore This Version"):
            st.session_state.current_contract = st.session_state.previous_versions[selected_version]
            st.rerun()

def export_contract(contract_text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"contract_export_{timestamp}.txt"
    st.download_button(
        label="Download Contract",
        data=contract_text,
        file_name=filename,
        mime="text/plain"
    )

def get_agent_feedback(agent):
    # Dummy feedback for each agent
    feedback = {
        "Outside Counsel": "Suggest adding a clause about intellectual property rights.",
        "In-House Counsel": "The liability section needs to be more specific.",
        "Opposing Counsel": "The termination conditions are too restrictive.",
        "Compliance Officer": "Ensure GDPR compliance in the data handling section."
    }
    return feedback.get(agent, "No feedback available.")

def regenerate_contract(current_contract, selected_agents):
    # Dummy logic to regenerate the contract
    new_contract = current_contract + "\n\nUpdated based on feedback from: " + ", ".join(selected_agents)
    return new_contract

def add_to_previous_versions(contract):
    st.session_state.previous_versions.append(contract)

if __name__ == "__main__":
    show_project_details_page()