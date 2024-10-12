
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

# Function to show the modal
def show_modal():
    modal_html = """
    <div id="myModal" class="modal">
        <div class="modal-content">
            <h2>Add New Project</h2>
            <input type="text" id="projectName" placeholder="Project Name">
            <textarea id="projectDescription" placeholder="Project Description"></textarea>
            <button onclick="createProject()">Create Project</button>
            <button onclick="closeModal()">Cancel</button>
        </div>
    </div>
    """
    return modal_html

# Display projects in a grid
cols = st.columns(3)
for i, project in enumerate(st.session_state.projects):
    with cols[i % 3]:
        project_card(project)

# Add Project button
if st.button("Add Project"):
    st.components.v1.html(show_modal(), height=300)

# JavaScript to handle modal interactions
st.components.v1.html(
    """
    <script>
    function createProject() {
        const name = document.getElementById('projectName').value;
        const description = document.getElementById('projectDescription').value;
        if (name && description) {
            window.parent.postMessage({type: 'create_project', name: name, description: description}, '*');
        }
    }

    function closeModal() {
        document.getElementById('myModal').style.display = 'none';
    }
    </script>
    """,
    height=0,
)

# Handle the creation of a new project
if st.session_state.get('new_project'):
    new_project = add_project(st.session_state.new_project['name'], st.session_state.new_project['description'])
    st.session_state.projects.append(new_project)
    del st.session_state.new_project
    st.experimental_rerun()

# JavaScript to listen for messages from the iframe
components.html(
    """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'create_project') {
            window.parent.postMessage({type: 'streamlit:set_session_state', data: {new_project: event.data}}, '*');
        }
    });
    </script>
    """,
    height=0,
)