# AI Resume & Job Matching System

## ALGOTHON'26 — ALG-AI-01

### 📌 Problem

Recruiters often receive many resumes for a single job opening. Manually checking and comparing every resume takes time and can lead to inconsistent candidate selection.

This project automatically analyzes resumes against a given job description, calculates a match score, ranks candidates, and explains why each candidate matches the job.

### 💡 Solution

The system allows recruiters to:

* Upload multiple resumes
* Enter a job description
* Extract candidate skills, education, and experience
* Compare resumes with the job requirements
* Calculate candidate match scores
* Rank candidates from best to lowest match
* Search and filter candidates
* View matched and missing skills
* Understand why a candidate received their score
* Check for unusual or unsupported claims

### ⭐ Key Features

* 📄 PDF and DOCX resume upload
* 📝 Job description input
* 🔍 Automatic information extraction
* 🧠 NLP-based resume matching
* 📊 Candidate scoring and ranking
* 🎯 Required skill matching
* 🎓 Education matching
* 💼 Experience matching
* 🔎 Candidate search and filtering
* 💡 Explainable match results
* ⚠️ Basic unusual-claim detection
* 📱 Simple Streamlit web interface

### 📊 Scoring System

The overall candidate score is calculated using:

| Component            | Weight |
| -------------------- | -----: |
| Text Similarity      |    45% |
| Required Skill Match |    35% |
| Education Match      |    10% |
| Experience Match     |    10% |

This produces a score between 0% and 100%.

### 🛠️ Technology Stack

* Python
* Streamlit
* PyPDF2
* python-docx
* Scikit-learn
* Pandas
* TF-IDF
* Cosine Similarity

### 🏗️ System Architecture

```text
             Job Description
                    │
                    ▼
          ┌──────────────────┐
          │ Requirement      │
          │ Extraction       │
          └────────┬─────────┘
                   │
                   ▼
Resume Files ──► Resume Text Extraction
                   │
                   ▼
          ┌──────────────────┐
          │ Skill / Education│
          │ / Experience     │
          │ Extraction       │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Resume Matching  │
          │ & Scoring        │
          └────────┬─────────┘
                   │
                   ▼
          Candidate Ranking
                   │
                   ▼
       Explainable Match Results
```

### ▶️ How to Run

#### 1. Install Python

Install Python 3.x on your computer.

#### 2. Install required libraries

```bash
pip install streamlit PyPDF2 python-docx scikit-learn pandas
```

#### 3. Run the application

Open the project folder in VS Code terminal and run:

```bash
streamlit run app.py
```

The application will open in your web browser.

### 🧪 Testing

The application was tested using multiple sample resumes with different:

* Technical skills
* Education qualifications
* Experience levels
* Job-role backgrounds

The system successfully ranked stronger candidates above candidates with fewer required skills.

### 🔍 Edge Cases Considered

* PDF resumes
* DOCX resumes
* Multiple resumes uploaded together
* Missing required skills
* Different education formats
* Different experience formats
* Resumes with unrelated technical skills
* Candidates with low job-description similarity

### ⚠️ Limitations

* Resume information extraction is based mainly on text and keyword patterns.
* Experience extraction may not correctly understand every possible resume format.
* Claim checking is a basic detection mechanism and is not a complete fact-verification system.
* Scanned image-only resumes may require OCR for better extraction.

### 🚀 Future Improvements

* OCR support for scanned resumes
* Transformer-based embeddings
* Semantic skill matching
* Better experience extraction
* Advanced contradiction detection
* Database integration
* Recruiter authentication
* Job and candidate history
* More advanced analytics
* Cloud deployment

### 🤖 AI-Assisted Development Disclosure

AI-assisted development tools were used during the development of this project for coding assistance, debugging, documentation, and solution improvement.

The project was tested and reviewed by the participant, who is responsible for the final implementation and submission.

### 🏆 Hackathon

**Event:** ALGOTHON'26
**Problem ID:** ALG-AI-01
**Problem:** AI Resume & Job Matching System

### 👨‍💻 Project Status

Working prototype completed for ALGOTHON'26.
