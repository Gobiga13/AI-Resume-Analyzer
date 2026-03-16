# AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes and matches them with job descriptions using Natural Language Processing (NLP). The system extracts skills from uploaded resumes and compares them with a job dataset to provide compatibility scores and job match insights.

---

## Features

* Upload and analyze resumes
* Extract skills automatically from resumes
* Match resumes with job descriptions
* Compatibility score based on job requirements
* Job recommendations from dataset
* Simple and responsive user interface

---

## Technologies Used

* Python
* Flask
* HTML5
* CSS3
* JavaScript
* Natural Language Processing (NLP)
* Pandas
* Machine Learning techniques

---

## Project Structure

```
Mini Project/
│
├── app.py
├── requirements.txt
├── final_job_dataset.csv
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── error.html
│
├── static/
│   └── style.css
│
├── uploads/
│
├── resume_parser.py
├── skill_extractor.py
├── match_engine.py
└── genai_helper.py
```

---

## Installation

1. Clone the repository

```
git clone https://github.com/yourusername/AI-Resume-Analyzer.git
```

2. Navigate to the project folder

```
cd AI-Resume-Analyzer
```

3. Create and activate virtual environment

```
python -m venv venv
```

Windows:

```
venv\Scripts\activate
```

4. Install required dependencies

```
pip install -r requirements.txt
```

---

## Running the Application

Run the Flask application:

```
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Dataset

The project uses a job dataset containing:

* 30+ companies
* 10 job roles
* Skills and job descriptions

The dataset is used to match resumes with suitable job opportunities.

---

## Future Improvements

* Advanced AI resume scoring
* Resume improvement suggestions
* Multiple resume format support
* Job recommendation system
* Cloud deployment

---

## Author

Gobiga

---

## License

This project is for educational and learning purposes.
