# AI Resume Analyzer

AI Resume Analyzer is a web-based application that analyzes a candidate's resume and compares it with job descriptions to determine how well the resume matches a specific role. The system extracts skills from the uploaded resume and compares them with job requirements from a dataset to generate a compatibility score and recommendations.

This project demonstrates the use of Python, Flask, and Natural Language Processing techniques to build an intelligent resume analysis system.

---

## Live Demo

You can try the application here:

https://ai-resumeanalyzer-g.vercel.app/

This live demo allows users to upload a resume and see how well it matches available job roles from the dataset.

---

## Key Features

* Resume Upload and Analysis
* Automatic Skill Extraction from Resume
* Job Matching based on Skills
* Compatibility Score Calculation
* Dataset-driven Job Role Matching
* Clean and Responsive Web Interface
* AI-powered Resume Intelligence

---

## Technologies Used

Frontend
HTML5
CSS3
JavaScript

Backend
Python
Flask

Libraries & Tools
Pandas
Natural Language Processing (NLP)
PDF / DOCX Resume Parsing

Deployment
Vercel (Frontend hosting)

---

## Project Folder Structure

Mini Project/

app.py
requirements.txt
final_job_dataset.csv

templates/
 index.html
 result.html
 error.html

static/
 style.css

uploads/

resume_parser.py
skill_extractor.py
match_engine.py
genai_helper.py

---

## Installation Guide

Follow these steps to run the project locally.

### 1. Clone the repository

git clone https://github.com/Gobiga13/AI-Resume-Analyzer.git

### 2. Navigate to the project directory

cd AI-Resume-Analyzer

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the virtual environment

Windows

venv\Scripts\activate

### 5. Install dependencies

pip install -r requirements.txt

### 6. Run the application

python app.py

### 7. Open the application in browser

http://127.0.0.1:5000

---

## Dataset Information

The project uses a job dataset containing:

30+ Companies
10 Job Roles
Skill Requirements
Job Descriptions

The dataset is used to match resumes with suitable job opportunities.

---

## Future Improvements

Add AI-based resume improvement suggestions
Add support for multiple resume formats
Implement advanced machine learning matching models
Add user login and profile management
Deploy full backend API on cloud

---

## Author

Gobiga



---

## License

This project is created for educational and learning purposes.
