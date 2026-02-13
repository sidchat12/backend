ROLE_EXPECTATIONS = {
    "Backend Engineer": [
        "API Design",
        "Database Integration",
        "Authentication",
        "Scalability",
        "Testing"
    ],
    "Frontend Engineer": [
        "UI/UX",
        "State Management",
        "Performance Optimization",
        "Responsive Design"
    ],
    "ML Engineer": [
        "Model Training",
        "Evaluation Metrics",
        "Dataset Handling",
        "Deployment"
    ]
}

def get_role_expectations(role: str):
    return ROLE_EXPECTATIONS.get(role, [])
