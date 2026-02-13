import numpy as np
from app.services.embeddings_service import get_embedding

TUTORIAL_PROJECTS = [
    "Basic ToDo App with CRUD operations",
    "Weather App using public API",
    "MERN Blog Application",
    "Netflix Clone UI",
    "Simple Calculator App",
    "Basic Chat App using Socket.io",
    "Simple E-commerce Clone"
]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def detect_tutorial_similarity(project_text: str):

    project_embedding = get_embedding(project_text)

    highest_similarity = 0
    matched_template = None

    for tutorial in TUTORIAL_PROJECTS:
        tutorial_embedding = get_embedding(tutorial)

        similarity = cosine_similarity(project_embedding, tutorial_embedding)

        if similarity > highest_similarity:
            highest_similarity = similarity
            matched_template = tutorial

    return {
        "similarity_score": round(float(highest_similarity), 3),
        "matched_template": matched_template,
        "is_low_impact": highest_similarity > 0.75
    }
