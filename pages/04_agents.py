import streamlit as st

st.title("Agents")

st.write("This page displays information about agents.")

# Placeholder for agent data
agents = [
    {"name": "John Doe", "sales": 100000},
    {"name": "Jane Smith", "sales": 150000},
    {"name": "Bob Johnson", "sales": 120000},
]

for agent in agents:
    st.subheader(agent["name"])
    st.write(f"Total Sales: ${agent['sales']:,}")
    st.write("---")

st.button("Add New Agent")