import streamlit as st
from utils.agents import load_agents, add_agent, AgentCard, show_agent_details, save_agents

st.set_page_config(page_title="Agents", layout="wide")

# Load agents from the database every time the page is loaded
st.session_state.agents = load_agents()

if 'show_details' not in st.session_state:
    st.session_state.show_details = False
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = None

# Create two columns for the main layout
main_col, side_panel = st.columns([2, 1])

with main_col:
    st.title("Agents")

    # Display agents in a grid
    agent_cols = st.columns(3)
    for i, agent in enumerate(st.session_state.agents):
        with agent_cols[i % 3]:
            if AgentCard(agent):
                st.session_state.selected_agent = agent
                st.session_state.show_details = True
                st.experimental_rerun()

# Side panel for Add Agent form and Edit Agent details
with side_panel:
    if st.session_state.show_details and st.session_state.selected_agent:
        show_agent_details(st.session_state.selected_agent)
    else:
        st.title("Add New Agent")
        
        new_name = st.text_input("Name", key="new_name")
        new_description = st.text_area("Description", key="new_description")
        new_purpose = st.text_input("Purpose", key="new_purpose")
        new_past_work = st.file_uploader("Past Work", accept_multiple_files=True, key="new_past_work")
        
        if st.button("Add Agent"):
            if new_name and new_description and new_purpose:
                new_agent = add_agent(new_name, new_description, new_purpose, new_past_work)
                st.session_state.agents.append(new_agent)
                save_agents(st.session_state.agents)
                st.success(f"Agent '{new_name}' added successfully!")
                # Clear the form by resetting the session state
                for key in ['new_name', 'new_description', 'new_purpose', 'new_past_work']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()
            else:
                st.error("Please fill in all required fields.")

# Custom CSS for agent card styling
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