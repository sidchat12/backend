def compute_scoring(repo_data, role_expectations):

    if not repo_data:
        return {
            "documentation": 0,
            "activity": 0,
            "technical_depth": 0,
            "role_alignment": 0,
            "overall_score": 0,
            "explanation": "No repositories found."
        }

    total_repos = len(repo_data)

    # 1️⃣ Documentation
    documentation_score = sum(
        1 for r in repo_data if r["readme_exists"]
    ) / total_repos

    # 2️⃣ Activity (updated within 90 days)
    activity_score = sum(
        1 for r in repo_data if r["days_since_update"] < 90
    ) / total_repos

    # 3️⃣ Language Diversity
    languages = set(r["language"] for r in repo_data if r["language"])
    diversity_score = min(len(languages) / 5, 1)

    # 4️⃣ Role Alignment (keyword check in descriptions)
    alignment_hits = 0
    for r in repo_data:
        description = (r["description"] or "").lower()
        for keyword in role_expectations:
            if keyword.lower() in description:
                alignment_hits += 1
                break

    role_alignment_score = alignment_hits / total_repos

    overall = round(
        (
            documentation_score * 0.25 +
            activity_score * 0.20 +
            diversity_score * 0.20 +
            role_alignment_score * 0.35
        ) * 100
    )

    return {
        "documentation": round(documentation_score * 100),
        "activity": round(activity_score * 100),
        "technical_depth": round(diversity_score * 100),
        "role_alignment": round(role_alignment_score * 100),
        "overall_score": overall,
        "explanation": "Score based on documentation, activity, diversity, and alignment with target role."
    }
