import streamlit as st

import streamlit as st

def project_card(project):
    with st.container():
        st.subheader(project['name'])
        st.write(f"Status: {project['status']}")
        if st.button(f"View {project['name']} Details", key=f"view_{project['id']}"):
            st.experimental_set_query_params(id=project['id'])
            st.switch_page("pages/06_project_details.py")