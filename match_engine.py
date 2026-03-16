def calculate_match(resume_skills: list, jd_skills: list) -> int:
    """
    Calculate % match between resume skills and job description skills.
    Both lists are compared case-insensitively.
    Returns integer 0-100.
    """
    if not jd_skills:
        return 0
    if not resume_skills:
        return 0

    resume_set = set(s.lower().strip() for s in resume_skills)
    jd_set     = set(s.lower().strip() for s in jd_skills)

    matched = resume_set & jd_set
    score   = (len(matched) / len(jd_set)) * 100
    return round(score)