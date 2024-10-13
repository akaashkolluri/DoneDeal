import streamlit as st
import datetime
from streamlit_extras.stylable_container import stylable_container
from utils.database import get_project_by_id, update_project, remove_document, get_document_content
from utils.agents import load_agents
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components
from fpdf import FPDF
from streamlit_extras.app_logo import add_logo

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TINYMCE_API_KEY = os.getenv("TINYMCE_API_KEY")





def generate_contract(project_info, agent_feedback=None):
    prompt = f"""
    Generate a legal contract based on the following project information:
    
    Project Name: {project_info['name']}
    Description: {project_info['description']}
    Team: {project_info['team']}
    
    Additional Information:
    {project_info.get('additional_info', 'No additional information provided.')}
    
    Please create a comprehensive legal contract that covers all necessary aspects of this project.
    
    After generating the contract, provide a brief summary of the key points or changes made.
    Format your response as follows:
    CONTRACT:
    [Your generated contract here]
    SUMMARY:
    [Brief summary of key points or changes, less than 30 words]
    """
    
    if agent_feedback:
        prompt += "\n\nConsider the following feedback from agents when creating the contract:\n"
        for agent, feedback in agent_feedback.items():
            prompt += f"\n{agent}: {feedback}\n"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a legal expert tasked with drafting contracts and summarizing changes."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def parse_contract_and_summary(response):
    parts = response.split("SUMMARY:")
    contract = parts[0].replace("CONTRACT:", "").strip()
    summary = parts[1].strip() if len(parts) > 1 else "No summary provided."
    return contract, summary

def generate_agent_feedback(contract, agent, specific_instructions, section_to_edit):
    prompt = f"""
    You are {agent['name']}, a {agent['description']}.
    
    Please review the following contract and provide feedback as if you were this agent. 
    Consider the agent's expertise, background, and any specific information provided about them.
    
    Specific Instructions: {specific_instructions}
    
    Section to Edit: {section_to_edit}
    
    Contract:
    {contract}
    
    Provide your feedback, speaking in first person as if you were {agent['name']}. 
    If a specific section to edit was provided, focus your feedback on that section.

    Keep feedback to under 150 words.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant providing feedback on a contract from the perspective of a specific agent."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def export_as_pdf(contract_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, contract_text)
    return pdf.output(dest="S").encode("latin-1")

def show_project_details_page():
    if 'new_feedback_generated' not in st.session_state:
        st.session_state.new_feedback_generated = False
    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = []
    if 'previous_versions' not in st.session_state:
        st.session_state.previous_versions = []
    if 'agent_feedback' not in st.session_state:
        st.session_state.agent_feedback = {}
    if 'current_contract' not in st.session_state:
        st.session_state.current_contract = "Draft your contract here"
    if 'contract_changes' not in st.session_state:
        st.session_state.contract_changes = None

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

    # Create four columns for the panels
    left_col, middle_left_col, middle_right_col, right_col = st.columns([2, 4, 2, 2])

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
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(doc['name'])
            # with col2:
            #     if st.button("📥", key=f"download_{doc['id']}", help="Download document"):
            #         file_content = get_document_content(doc['path'])
            #         st.download_button(
            #             label="Click to Download",
            #             data=base64.b64decode(file_content),
            #             file_name=doc['name'],
            #             mime=doc['type']
            #         )
            with col3:
                if st.button("🗑️", key=f"remove_{doc['id']}", help="Remove document"):
                    if remove_document(project_id, doc['id']):
                        st.success(f"Document {doc['name']} removed.")
                        st.rerun()
                    else:
                        st.error("Failed to remove document.")

        # Add new documents
        new_documents = st.file_uploader("Add New Documents", accept_multiple_files=True)

        # Save changes button
        if st.button("Upload File"):


            updated_project = update_project(project_id, new_name, new_description, project.get('status', 'New'), new_team, new_documents)
            
            if updated_project:
                st.success("Project updated successfully!")

                st.rerun()
            else:
                st.error("Failed to update project.")

        # if st.button("Back to Projects"):
        #     st.switch_page("pages/05_projects.py")

    with middle_left_col:
        st.header("Legal Contract")
        
        # Add loading message placeholder
        loading_placeholder = st.empty()

        # Display the changes explanation if available
        changes_placeholder = st.empty()
        if st.session_state.contract_changes:
            changes_placeholder.success(f"Changes made: {st.session_state.contract_changes}")
        else:
            changes_placeholder.empty() 

        # Create a better text editor with more options
        editor_html = f"""
        <html>
            <head>
                <script src={f"https://cdn.tiny.cloud/1/{TINYMCE_API_KEY}/tinymce/5/tinymce.min.js"} referrerpolicy="origin"></script>
                <script>
                    tinymce.init({{
                        selector: '#editor',
                        height: 500,
                        plugins: 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount',
                        toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
                        content_style: 'body {{ font-family:Helvetica,Arial,sans-serif; font-size:14px }}',
                        setup: function(editor) {{
                            editor.on('change', function() {{
                                editor.save();
                            }});
                        }}
                    }});
                </script>
            </head>
            <body>
                <textarea id="editor">{st.session_state.current_contract}</textarea>
            </body>
        </html>
        """
        components.html(editor_html, height=510)

       
        # Create three columns for the buttons
        button_col1, button_col2, button_col3, button_col4 = st.columns(4)

        # with button_col1:
        #     if st.button("View Previous Versions"):
        #         show_previous_versions()

        # with button_col2:
        #     if st.button("Export as Text"):
        #         export_contract(st.session_state.current_contract)

        with button_col3:
            if st.button("Export as PDF"):
                pdf_output = export_as_pdf(st.session_state.current_contract)
                st.download_button(
                    label="Download PDF",
                    data=pdf_output,
                    file_name="contract.pdf",
                    mime="application/pdf"
                )

        with button_col4:
            if st.button("Generate Contract"):
                project_info = {
                    "name": new_name,
                    "description": new_description,
                    "team": new_team,
                    "additional_info": ", ".join([doc['name'] for doc in project.get('documents', [])])
                }
                
                loading_placeholder.warning("Contract Writing Agent is currently considering your documents...")
                generated_response = generate_contract(project_info)
                generated_contract, summary = parse_contract_and_summary(generated_response)
                
                # Update the current contract with the generated one
                st.session_state.current_contract = generated_contract
                add_to_previous_versions(st.session_state.current_contract)
                st.session_state.contract_changes = summary
                
                st.rerun()

    with middle_right_col:
        st.header("Agent Selection")
        
        # Input for specific instructions and desired section to edit
        specific_instructions = st.text_area("Specific Instructions", "")
        section_to_edit = st.text_area("Desired Section to Edit", "")
        
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

        # Button to generate feedback
        if st.button("Generate feedback from agents"):
            st.session_state.agent_feedback = {}  # Clear previous feedback
            st.session_state.new_feedback_generated = False  # Reset the flag
            with st.spinner("Feedback Agents are currently reviewing the content..."):
                for agent in agents:
                    if agent['name'] in selected_agent_names:
                        feedback = generate_agent_feedback(st.session_state.current_contract, agent, specific_instructions, section_to_edit)
                        st.session_state.agent_feedback[agent['name']] = feedback
            st.session_state.new_feedback_generated = True  # Set the flag to True after generating new feedback
            st.success("Feedback generated for selected agents!")
            st.rerun()

        # Regenerate contract button
        if st.button("Regenerate Contract with Feedback"):
            project_info = {
                "name": new_name,
                "description": new_description,
                "team": new_team,
                "additional_info": ", ".join([doc['name'] for doc in project.get('documents', [])])
            }
            st.session_state.contract_changes = None  # Clear the previous changes message
            changes_placeholder.empty()

            
            loading_placeholder.warning("Contract Writing Agent is considering feedback from Counsel Agents to strengthen the contract...")
            generated_response = generate_contract(project_info, st.session_state.agent_feedback)
            new_contract, summary = parse_contract_and_summary(generated_response)
            add_to_previous_versions(st.session_state.current_contract)
            st.session_state.current_contract = new_contract
            st.session_state.contract_changes = summary
            loading_placeholder.success("Contract regenerated successfully!")
            st.rerun()

    with right_col:
        st.header("Agent Feedback")

        # Check if new agent feedback has been generated
        if st.session_state.new_feedback_generated:
            st.success("Agent Feedback has been generated, look below!")
            st.session_state.new_feedback_generated = False  # Reset the flag after showing the message

        # Display feedback for selected agents with toggles
        for agent_name in selected_agent_names:
            expander = st.expander(f"{agent_name}'s Feedback")
            with expander:
                if agent_name in st.session_state.agent_feedback:
                    st.write(st.session_state.agent_feedback[agent_name])
                else:
                    st.write("Feedback not yet generated for this agent.")
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

def add_to_previous_versions(contract):
    st.session_state.previous_versions.append(contract)

if __name__ == "__main__":
    show_project_details_page()