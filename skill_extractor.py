import re

# ─────────────────────────────────────────────────────────────
#  COMPLETE SKILLS DATABASE
#  Contains every skill present in final_job_dataset.csv
#  PLUS common resume keywords so matching actually works.
#
#  Key fix: multi-word skills (e.g. "machine learning",
#  "rest apis", "stakeholder management") are listed in full
#  so regex word-boundary matching catches them.
# ─────────────────────────────────────────────────────────────

SKILLS_DB = [
    # ── Every skill in final_job_dataset.csv ──────────────────
    "python", "java", "c++", "sql", "git", "html", "css",
    "javascript", "react", "node.js", "mongodb",
    "docker", "kubernetes", "linux", "shell scripting",
    "aws", "azure", "gcp", "cloud", "terraform",
    "ci/cd",
    "machine learning", "deep learning", "tensorflow", "pytorch",
    "pandas", "numpy", "data preprocessing",
    "data cleaning", "data visualization", "data structures",
    "statistics", "excel", "power bi", "tableau",
    "rest apis", "apis", "microservices", "oop",
    "agile", "jira", "problem solving", "communication",
    "stakeholder management", "requirement gathering",
    "network security", "ethical hacking", "firewalls",
    "siem", "risk assessment",
    "selenium", "manual testing", "automation testing",
    "test cases",
    "networking",

    # ── Common resume extras ──────────────────────────────────
    "flask", "django", "fastapi", "spring boot",
    "typescript", "angular", "vue",
    "mysql", "postgresql", "redis", "sqlite",
    "spark", "hadoop", "kafka", "airflow",
    "scikit-learn", "keras", "nlp", "computer vision",
    "data analysis", "data science",
    "scrum", "devops", "mlops",
    "pytest", "unit testing",
    "cybersecurity", "penetration testing",
    "c#", "go", "rust", "scala", "kotlin", "swift",
]


def extract_skills(text: str) -> list:
    """
    Scan resume text and return list of matched skills.
    Matching is case-insensitive. Returns skills in Title Case
    so they display nicely and compare correctly against the
    dataset skills (which are also Title Case).
    """
    text_lower = text.lower()
    found = []
    seen  = set()

    for skill in SKILLS_DB:
        skill_lower = skill.lower()
        if skill_lower in seen:
            continue

        # Word-boundary pattern — handles "c++" and "node.js" safely
        escaped = re.escape(skill_lower)
        pattern = r'(?<![a-zA-Z0-9])' + escaped + r'(?![a-zA-Z0-9])'

        if re.search(pattern, text_lower):
            seen.add(skill_lower)
            # Format for display: keep acronyms upper, title-case rest
            UPPER_KEEP = {
                "sql","html","css","aws","gcp","api","apis","oop",
                "ci/cd","siem","nlp","jira","rest apis","c++","c#",
            }
            if skill_lower in UPPER_KEEP:
                found.append(skill.upper())
            else:
                found.append(skill.title())

    return found