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

    # Create two columns for the filters
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        # Add a dropdown to filter agents by allegiance
        allegiance_filter = st.selectbox(
            "Filter by Allegiance",
            ["All", "Your Side", "Opposing Side", "Neutral"],
            key="allegiance_filter"
        )

    with filter_col2:
        # Add a dropdown to filter agents by type
        agent_type_filter = st.selectbox(
            "Filter by Agent Type",
            ["All", "in-house counsel", "opposing counsel", "corporate plaintiff", "individual plaintiff", "judge"],
            key="agent_type_filter"
        )

    # Filter agents based on the selected allegiance and agent type
    filtered_agents = st.session_state.agents

    if allegiance_filter != "All":
        filtered_agents = [agent for agent in filtered_agents if agent['allegiance'] == allegiance_filter]

    if agent_type_filter != "All":
        filtered_agents = [agent for agent in filtered_agents if agent['type'] == agent_type_filter]

    # Display filtered agents in a grid
    if filtered_agents:
        agent_cols = st.columns(3)
        for i, agent in enumerate(filtered_agents):
            with agent_cols[i % 3]:
                if AgentCard(agent):
                    st.session_state.selected_agent = agent
                    st.session_state.show_details = True
                    st.rerun()
    else:
        st.write("No agents match the selected filters.")

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
        # Dropdown for Allegiance
        allegiance_options = ["your side", "opposing side", "neutral"]
        new_allegiance = st.selectbox("Allegiance", allegiance_options, key="new_allegiance")

        # Dropdown for Allegiance
        agent_options = ["in-house counsel", "opposing counsel", "corporate plaintiff", "individual plaintiff", "judge"]
        new_type = st.selectbox("Agent Type", agent_options, key="new_type")


        if st.button("Add Agent"):
            if new_name and new_description and new_purpose:
                new_agent = add_agent(new_name, new_description, new_purpose, new_past_work, new_allegiance, new_type)
                st.session_state.agents.append(new_agent)
                save_agents(st.session_state.agents)
                st.success(f"Agent '{new_name}' added successfully!")
                # Clear the form by resetting the session state
                for key in ['new_name', 'new_description', 'new_purpose', 'new_past_work', 'new_allegiance', 'new_type']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
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