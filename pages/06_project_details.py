import streamlit as st
import datetime
from streamlit_extras.stylable_container import stylable_container
from utils.database import get_project_by_id, update_project, remove_document, get_document_content
from utils.agents import load_agents  # Assuming you have this function in utils/agents.py
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_contract(project_info):
    prompt = f"""
    Generate a legal contract based on the following project information:
    
    Project Name: {project_info['name']}
    Description: {project_info['description']}
    Team: {project_info['team']}
    
    Additional Information:
    {project_info.get('additional_info', 'No additional information provided.')}
    
    Please create a comprehensive legal contract that covers all necessary aspects of this project.
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a legal expert tasked with drafting contracts."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

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
        
        # Create a better text editor with more options
        editor_html = f"""
        <html>
            <head>
                <script src={f"https://cdn.tiny.cloud/1/{os.getenv('TINYMCE_API_KEY')}/tinymce/5/tinymce.min.js"} referrerpolicy="origin"></script>
                <script>
                    tinymce.init({{
                        selector: '#editor',
                        height: 500,
                        plugins: 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount',
                        toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
                        content_style: 'body {{ font-family:Helvetica,Arial,sans-serif; font-size:14px }}'
                    }});
                </script>
            </head>
            <body>
                <textarea id="editor">{contract_text}</textarea>
            </body>
        </html>
        """
        components.html(editor_html, height=600)

        # Create three columns for the buttons
        button_col1, button_col2, button_col3 = st.columns(3)

        with button_col1:
            if st.button("View Previous Versions"):
                show_previous_versions()

        with button_col2:
            if st.button("Export"):
                export_contract(contract_text)

        with button_col3:
            if st.button("Generate Contract"):
                project_info = {
                    "name": new_name,
                    "description": new_description,
                    "team": new_team,
                    "additional_info": ", ".join([doc['name'] for doc in project.get('documents', [])])
                }
                generated_contract = generate_contract(project_info)
                
                # Update the current contract with the generated one
                st.session_state.current_contract = generated_contract
                add_to_previous_versions(contract_text)
                st.rerun()

    with right_col:
        st.header("Agent Feedback")
        
        # Load agents dynamically
        agents = load_agents()
        
        # Agent selection using multiselect
        selected_agent_names = st.multiselect(
            "Select Agents",
            options=[agent['name'] for agent in agents],
            default=st.session_state.selected_agents
        )
        
        # Update selected agents in session state
        st.session_state.selected_agents = selected_agent_names

        # Display feedback for selected agents
        st.subheader("Agent Feedback")
        for agent_name in selected_agent_names:
            st.write(f"**{agent_name}**")
            st.write(get_agent_feedback(agent_name))

        # Regenerate contract button
        if st.button("Regenerate Contract with Feedback"):
            new_contract = regenerate_contract(contract_text, selected_agent_names)
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

def get_agent_feedback(agent_name):
    # This is a placeholder function. In a real application, you would fetch the actual feedback for the agent.
    return f"Feedback for {agent_name}: This is a placeholder feedback. In a real application, this would be actual feedback from the agent."

def regenerate_contract(current_contract, selected_agents):
    # This is a placeholder function. In a real application, you would use the OpenAI API to regenerate the contract based on the feedback.
    new_contract = current_contract + "\n\nUpdated based on feedback from: " + ", ".join(selected_agents)
    return new_contract

def add_to_previous_versions(contract):
    st.session_state.previous_versions.append(contract)

if __name__ == "__main__":
    show_project_details_page()