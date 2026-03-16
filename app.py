from flask import Flask, render_template, request
import os
import pandas as pd
import ast

from resume_parser import extract_text
from skill_extractor import extract_skills
from match_engine import calculate_match

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ─────────────────────────────────────────────────────────────
# FIND THE CSV — tries every possible filename variation
# because Windows sometimes saves as .csv.csv double extension
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

POSSIBLE_CSV_NAMES = [
    "final_job_dataset.csv",
    "final_job_dataset.csv.csv",   # Windows double-extension bug
    "final_job_dataset_csv.csv",
    "final_job_dataset (1).csv",
    "final_job_dataset.CSV",
]

CSV_PATH = None
for name in POSSIBLE_CSV_NAMES:
    candidate = os.path.join(BASE_DIR, name)
    if os.path.exists(candidate):
        CSV_PATH = candidate
        print(f"✅ Found CSV: {candidate}")
        break

if CSV_PATH is None:
    # Last resort: scan folder for any .csv file
    for f in os.listdir(BASE_DIR):
        if f.lower().endswith(".csv") and "job" in f.lower():
            CSV_PATH = os.path.join(BASE_DIR, f)
            print(f"✅ Found CSV by scan: {CSV_PATH}")
            break

# ─────────────────────────────────────────────────────────────
# LOAD DATASET
# ─────────────────────────────────────────────────────────────
job_data = None

if CSV_PATH:
    try:
        job_data = pd.read_csv(CSV_PATH)
        job_data.columns = job_data.columns.str.strip().str.lower()
        job_data["company_name"] = job_data["company_name"].str.strip()
        job_data["job_title"]    = job_data["job_title"].str.strip()
        print(f"✅ Dataset loaded: {len(job_data)} rows")
        print(f"   Columns  : {job_data.columns.tolist()}")
        print(f"   Companies: {job_data['company_name'].nunique()}")
        print(f"   Roles    : {job_data['job_title'].nunique()}")
    except Exception as e:
        print(f"❌ Dataset load error: {e}")
        job_data = None
else:
    print("❌ No CSV file found in project folder!")
    print(f"   Searched in: {BASE_DIR}")
    print(f"   Files present: {os.listdir(BASE_DIR)}")


# ─────────────────────────────────────────────────────────────
# FETCH JOB SKILLS
# ─────────────────────────────────────────────────────────────
def fetch_job_skills(company_name, job_title):
    if job_data is None:
        print("❌ job_data is None — CSV not loaded")
        return None

    c = company_name.strip()
    j = job_title.strip()

    # Exact match (case-insensitive)
    mask = (
        (job_data["company_name"].str.lower() == c.lower()) &
        (job_data["job_title"].str.lower()    == j.lower())
    )
    result = job_data[mask]

    # Partial match fallback
    if result.empty:
        mask2 = (
            job_data["company_name"].str.lower().str.contains(c.lower(), na=False) &
            job_data["job_title"].str.lower().str.contains(j.lower(), na=False)
        )
        result = job_data[mask2]

    if result.empty:
        print(f"❌ No dataset match for '{c}' / '{j}'")
        return None

    raw = result.iloc[0]["skills"]
    print(f"✅ Raw skills: {raw}")

    try:
        skills = ast.literal_eval(raw)
        return [str(s).strip() for s in skills]
    except Exception as e:
        print(f"❌ Skills parse error: {e}")
        return None


# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    print("\n" + "="*55)
    print("📥 /analyze called")
    print(f"   Form keys : {list(request.form.keys())}")
    print(f"   Form data : {dict(request.form)}")
    print(f"   File keys : {list(request.files.keys())}")

    # ── Resume ──
    if "resume" not in request.files:
        return render_template("error.html",
            message="Resume file not received. Please go back and upload your PDF or DOCX.")

    resume = request.files["resume"]
    if resume.filename == "":
        return render_template("error.html",
            message="No file selected. Please choose a PDF or DOCX resume file.")

    # ── Form fields — names match the hidden inputs in index.html ──
    company = request.form.get("company", "").strip()
    title   = request.form.get("job_title", "").strip()

    print(f"   company   = '{company}'")
    print(f"   job_title = '{title}'")

    if not company:
        return render_template("error.html",
            message="Company name is missing. Please go back and select a company.")
    if not title:
        return render_template("error.html",
            message="Job title is missing. Please go back and select a job title.")

    # ── Dataset lookup ──
    if job_data is None:
        return render_template("error.html",
            message=(
                "Dataset not loaded. Make sure 'final_job_dataset.csv' is in the "
                "same folder as app.py and restart Flask."
            ))

    jd_skills = fetch_job_skills(company, title)
    if jd_skills is None:
        return render_template("error.html",
            message=f"No job found for '{title}' at '{company}'. Please check your selection.")

    # ── Save resume ──
    safe_name = os.path.basename(resume.filename)
    filepath  = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    resume.save(filepath)
    print(f"   Saved : {filepath}")

    # ── Extract text ──
    resume_text = extract_text(filepath)
    print(f"   Text length : {len(resume_text)} chars")
    if not resume_text.strip():
        return render_template("error.html",
            message="Could not read text from your resume. Make sure it is not a scanned/image PDF.")

    # ── Extract skills ──
    resume_skills = extract_skills(resume_text)
    print(f"   Resume skills : {resume_skills}")
    print(f"   JD skills     : {jd_skills}")

    # ── Match ──
    score = calculate_match(resume_skills, jd_skills)

    resume_lower = set(s.lower().strip() for s in resume_skills)
    jd_lower     = set(s.lower().strip() for s in jd_skills)

    matched_skills = sorted(list(resume_lower & jd_lower))
    missing_skills = sorted(list(jd_lower - resume_lower))

    print(f"   Score   : {score}%")
    print(f"   Matched : {matched_skills}")
    print(f"   Missing : {missing_skills}")
    print("="*55 + "\n")

    return render_template(
        "result.html",
        score          = score,
        company        = company,
        job_title      = title,
        resume_skills  = resume_skills,
        job_skills     = jd_skills,
        matched_skills = matched_skills,
        missing_skills = missing_skills,
    )


if __name__ == "__main__":
    app.run(debug=True)