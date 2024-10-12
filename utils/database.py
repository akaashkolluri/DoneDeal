import json
from datetime import datetime
import uuid

def get_projects():
    try:
        with open('data/projects.json', 'r') as f:
            projects = json.load(f)
            # Add id to existing projects if they don't have one
            for project in projects:
                if 'id' not in project:
                    project['id'] = str(uuid.uuid4())
            return projects
    except FileNotFoundError:
        return []

def add_project(name, description):
    projects = get_projects()
    new_project = {
        'id': str(uuid.uuid4()),  # Generate a unique ID
        'name': name,
        'description': description,
        'status': 'New',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    projects.append(new_project)
    with open('data/projects.json', 'w') as f:
        json.dump(projects, f)
    return new_project

def get_project_by_id(project_id):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            return project
    return None

def update_project(project_id, name, description, status):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            project['name'] = name
            project['description'] = description
            project['status'] = status
            project['updated_at'] = datetime.now().isoformat()
            with open('data/projects.json', 'w') as f:
                json.dump(projects, f)
            return project
    return None