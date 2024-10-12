import json
from datetime import datetime
import uuid
import os
import base64

DATA_DIR = 'data'
PROJECTS_FILE = os.path.join(DATA_DIR, 'projects.json')
UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')

def get_projects():
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
            # Add id to existing projects if they don't have one
            for project in projects:
                if 'id' not in project:
                    project['id'] = str(uuid.uuid4())
            return projects
    except FileNotFoundError:
        return []

def save_projects(projects):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def get_project_by_id(project_id):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            return project
    return None

def save_uploaded_file(file):
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.name)[1]
    file_path = os.path.join(UPLOADS_DIR, f"{file_id}{file_extension}")
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return {
        'id': file_id,
        'name': file.name,
        'path': file_path,
        'type': file.type,
        'size': file.size
    }




def add_project(name, description, team, documents):
    new_project = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'team': team,
        'status': 'New',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'documents': [save_uploaded_file(doc) for doc in documents] if documents else []
    }
    projects = get_projects()
    projects.append(new_project)
    save_projects(projects)
    return new_project

def update_project(project_id, name, description, status, team, new_documents):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            project['name'] = name
            project['description'] = description
            project['status'] = status
            project['team'] = team
            # Add new documents
            if new_documents:
                project['documents'].extend([save_uploaded_file(doc) for doc in new_documents])
            project['updated_at'] = datetime.now().isoformat()
            save_projects(projects)
            return project
    return None

def remove_document(project_id, document_id):
    projects = get_projects()
    for project in projects:
        if project['id'] == project_id:
            project['documents'] = [doc for doc in project['documents'] if doc['id'] != document_id]
            save_projects(projects)
            return True
    return False

def get_document_content(document_path):

    with open(document_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')