import json
from datetime import datetime

def get_projects():
    # This is a placeholder. In a real app, you'd fetch from a database.
    try:
        with open('data/projects.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_project(name, description):
    projects = get_projects()
    new_project = {
        'name': name,
        'description': description,
        'status': 'New',
        'created_at': datetime.now().isoformat()
    }
    projects.append(new_project)
    with open('data/projects.json', 'w') as f:
        json.dump(projects, f)
    return new_project