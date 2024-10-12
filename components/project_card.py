import streamlit as st

def project_card(project):
    with st.expander(project['name']):
        st.write(f"Description: {project['description']}")
        st.write(f"Status: {project['status']}")
        st.write(f"Created: {project['created_at']}")
        if st.button(f"View {project['name']} Details"):
            st.session_state['current_project'] = project
            st.experimental_rerun()