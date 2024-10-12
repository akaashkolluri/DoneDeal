import streamlit as st

def project_card(project):
    with st.container():
        st.subheader(project['name'])
        st.write(f"Status: {project['status']}")
        if st.button(f"View {project['name']} Details", key=f"view_{project['id']}"):
            st.query_params["id"] = project['id']
            return True
    return False