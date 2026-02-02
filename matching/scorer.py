import re

def calculate_project_score(resume_text: str) -> float:
    """
    Scoring based on action verbs in the resume.
    Proxy for "Doer" vs "Watcher".
    """
    action_keywords = [
        "led", "managed", "created", "built", "developed", 
        "designed", "architected", "delivered", "implemented", 
        "engineered", "spearheaded", "deployed", "launched"
    ]
    
    count = 0
    text_lower = resume_text.lower()
    for word in action_keywords:
        # Simple word boundary regex
        if re.search(r'\b' + word + r'\b', text_lower):
            count += 1
            
    # Cap at 1.0 (e.g. 5 action words = full score)
    return min(count * 0.2, 1.0)


def score_resume(parsed_resume: dict, parsed_jd: dict, skill_match: dict) -> dict:
    skill_score = skill_match["match_ratio"]

    experience_years = parsed_resume.get("experience_years", 0)
    required_years = parsed_jd.get("min_experience", 0)

    experience_score = (
        min(experience_years / required_years, 1.0)
        if required_years > 0 else 1.0
    )

    jd_similarity = parsed_resume.get("jd_similarity", 0.0)
    project_score = parsed_resume.get("project_score", 0.0)

    final_score = (
        0.4 * skill_score +
        0.25 * experience_score +
        0.25 * jd_similarity +
        0.1 * project_score
    )

    return {
        "final_score": round(final_score * 100, 2),
        "skill_match": f"{len(skill_match['matched'])}/{len(parsed_jd['required_skills'])}",
        "experience_match": f"{experience_years} vs {required_years}+",
        "jd_similarity": round(jd_similarity, 2),
        "matched_skills": skill_match["matched"],
        "missing_skills": skill_match["missing"]
    }
