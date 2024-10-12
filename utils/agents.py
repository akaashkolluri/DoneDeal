import streamlit as st
import json
import uuid
from datetime import datetime
import random
import os

PERSON_EMOJIS = [
    "👨", "👩", "👱‍♂️", "👱‍♀️", "👨‍🦰", "👩‍🦰", "👨‍🦱", "👩‍🦱", "👨‍🦳", "👩‍🦳", "👨‍🦲", "👩‍🦲",
    "🧔", "🧔‍♀️", "👴", "👵", "🧓", "👨‍💼", "👩‍💼", "👨‍🏫", "👩‍🏫", "👨‍🎓", "👩‍🎓", "👨‍🔬", "👩‍🔬"
]

def load_agents():
    try:
        with open('data/agents.json', 'r') as f:
            agents = json.load(f)
    except FileNotFoundError:
        agents = []
    except json.JSONDecodeError:
        agents = []
    return agents

def save_agents(agents):
    os.makedirs('data', exist_ok=True)
    with open('data/agents.json', 'w') as f:
        json.dump(agents, f)

def add_agent(name, description, purpose, past_work, allegiance, agent_type):
    new_agent = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'purpose': purpose,
        'allegiance': allegiance, 
        'type': agent_type,
        'pixelart': random.choice(PERSON_EMOJIS),
        'past_work': [{'filename': file.name, 'content': file.getvalue().decode()} for file in past_work],
        'created_at': datetime.now().isoformat()
    }
    agents = load_agents()
    agents.append(new_agent)
    save_agents(agents)
    return new_agent

def update_agent(agent_id, name, description, purpose, pixelart, allegiance, agent_type):
    agents = load_agents()
    for agent in agents:
        if agent['id'] == agent_id:
            agent['name'] = name
            agent['description'] = description
            agent['purpose'] = purpose
            agent['allegiance'] = allegiance  
            agent['pixelart'] = pixelart
            agent['type'] = agent_type
            save_agents(agents)
            return True
    return False

def delete_agent(agent_id):
    agents = load_agents()
    updated_agents = [agent for agent in agents if agent['id'] != agent_id]
    if len(agents) != len(updated_agents):
        save_agents(updated_agents)
        return True
    return False

def AgentCard(agent):
    card_content = f"""
    {agent['pixelart']}
    {agent['name']}
    {agent['description'][:20] + "..." if len(agent['description']) > 20 else agent['description']}
    """
    return st.button(card_content, key=f"agent_{agent['id']}")

def show_agent_details(agent):
    st.title(f"{agent['name']} Details")
    
    new_name = st.text_input("Name", agent['name'])
    new_description = st.text_area("Description", agent['description'])
    new_purpose = st.text_input("Purpose", agent['purpose'])
    new_pixelart = st.text_input("Pixelart (emoji)", agent['pixelart'])
    
     # Dropdown for Allegiance
    allegiance_options = ["your side", "opposing side", "neutral"]
    new_allegiance = st.selectbox("Allegiance", allegiance_options, index=allegiance_options.index(agent['allegiance']))
    
    # Dropdown for Allegiance
    agent_options = ["in-house counsel", "opposing counsel", "corporate plaintiff", "individual plaintiff", "judge"]
    new_type = st.selectbox("Agent Type", agent_options, index=agent_options.index(agent['type']))

    # if st.button("Shuffle Emoji"):
    #     new_pixelart = random.choice(PERSON_EMOJIS)
    #     st.session_state.temp_pixelart = new_pixelart
    #     st.experimental_rerun()
    
    if st.button("Update Agent"):
        if update_agent(agent['id'], new_name, new_description, new_purpose, new_pixelart, new_allegiance, new_type):
            st.success("Agent updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update agent.")
    
    st.subheader("Past Work")
    if agent['past_work']:
        for work in agent['past_work']:
            st.download_button(f"Download {work['filename']}", work['content'], file_name=work['filename'])
    else:
        st.write("No past work available.")
    
    if st.button("Delete Agent"):
        if delete_agent(agent['id']):
            st.success(f"Agent '{agent['name']}' deleted successfully!")
            st.session_state.agents = load_agents()
            st.session_state.selected_agent = None
            st.session_state.show_details = False
            st.rerun()
        else:
            st.error("Failed to delete agent.")
    
    if st.button("Back to Add Agent"):
        st.session_state.selected_agent = None
        st.session_state.show_details = False
        st.rerun()