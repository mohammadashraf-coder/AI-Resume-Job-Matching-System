import streamlit as st
import PyPDF2
from docx import Document
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="AI Resume & Job Matcher",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume & Job Matching System")
st.caption("Intelligent resume analysis, ranking and explainable candidate matching")


# =========================================================
# SKILLS DATABASE
# =========================================================

skills = [
    "python", "java", "c", "c++", "sql", "mysql",
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "pandas", "numpy", "tensorflow", "pytorch",
    "html", "css", "javascript", "react", "node.js",
    "django", "flask", "git", "github", "excel",
    "power bi", "tableau", "communication", "problem solving",
    "cloud", "aws", "azure"
]


education_keywords = [
    "b.tech", "btech", "b.e", "be", "b.sc", "bsc",
    "m.tech", "mtech", "m.e", "me", "m.sc", "msc",
    "bachelor", "master", "mba",
    "computer science", "information technology",
    "electronics", "engineering"
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def skill_present(text, skill):
    """
    Detect a skill as a complete term.
    Prevents C from matching words such as communication.
    """
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def find_skills(text):
    found = []

    for skill in skills:
        if skill_present(text, skill):
            found.append(skill)

    return found


def find_education(text):
    found = []

    for education in education_keywords:
        if skill_present(text, education):
            found.append(education)

    return found


def extract_experience(text):
    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)"
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for value in matches:
            try:
                values.append(float(value))
            except:
                pass

    if values:
        return max(values)

    return 0


def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file):
    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(file):

    if file.name.lower().endswith(".pdf"):
        return extract_pdf_text(file)

    if file.name.lower().endswith(".docx"):
        return extract_docx_text(file)

    return ""


def get_status(score):

    if score >= 75:
        return "🟢 Strong Match"

    elif score >= 50:
        return "🟡 Moderate Match"

    return "🔴 Low Match"


def check_claims(text, detected_skills, experience):

    warnings = []

    # Detect suspicious experience claims
    if experience > 15:
        warnings.append(
            "Unusually high experience value detected. Please verify."
        )

    # Detect repeated skills
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    for skill in detected_skills:
        if skill in ["python", "java", "sql"]:
            count = words.count(skill)

            if count >= 15:
                warnings.append(
                    f"'{skill}' appears unusually frequently. Verify the claim."
                )

    return warnings


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🔎 Candidate Filters")

search_name = st.sidebar.text_input(
    "Search candidate"
)

minimum_score = st.sidebar.slider(
    "Minimum match score",
    0,
    100,
    0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Scoring:\n\n"
    "• 60% Job-description text similarity\n\n"
    "• 40% Required skill match"
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.subheader("1️⃣ Job Description")

job_description = st.text_area(
    "Enter the job description",
    height=180,
    placeholder=(
        "Example:\n"
        "Looking for a Python developer with SQL, "
        "Machine Learning, Pandas, NumPy and Git experience."
    )
)


# =========================================================
# RESUME UPLOAD
# =========================================================

st.subheader("2️⃣ Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload multiple PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


# =========================================================
# ANALYZE
# =========================================================

if st.button("🚀 Analyze & Rank Candidates", use_container_width=True):

    if not job_description.strip():
        st.warning("⚠️ Please enter a job description.")
        st.stop()

    if not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
        st.stop()

    candidates = []

    # -----------------------------------------------------
    # READ RESUMES
    # -----------------------------------------------------

    for file in uploaded_files:

        try:
            resume_text = extract_text(file)

            if not resume_text.strip():
                continue

            candidate_skills = find_skills(resume_text)
            candidate_education = find_education(resume_text)
            candidate_experience = extract_experience(resume_text)

            candidates.append({
                "name": file.name,
                "text": resume_text,
                "skills": candidate_skills,
                "education": candidate_education,
                "experience": candidate_experience
            })

        except Exception as error:

            st.error(
                f"Could not read {file.name}: {error}"
            )


    if not candidates:
        st.error("No readable resumes were found.")
        st.stop()


    # -----------------------------------------------------
    # JOB INFORMATION
    # -----------------------------------------------------

    job_skills = find_skills(job_description)
    job_education = find_education(job_description)

    job_experience = extract_experience(job_description)


    # -----------------------------------------------------
    # TF-IDF SIMILARITY
    # -----------------------------------------------------

    documents = [job_description]

    for candidate in candidates:
        documents.append(candidate["text"])


    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    )[0]


    # -----------------------------------------------------
    # SCORE EACH CANDIDATE
    # -----------------------------------------------------

    for i, candidate in enumerate(candidates):

        text_similarity = similarities[i] * 100


        # Skills
        matched_skills = [
            skill
            for skill in job_skills
            if skill in candidate["skills"]
        ]

        missing_skills = [
            skill
            for skill in job_skills
            if skill not in candidate["skills"]
        ]


        if job_skills:

            skill_match = (
                len(matched_skills)
                / len(job_skills)
            ) * 100

        else:

            skill_match = text_similarity


        # Education match
        if job_education:

            education_matches = [
                education
                for education in job_education
                if education in candidate["education"]
            ]

            education_match = (
                len(education_matches)
                / len(job_education)
            ) * 100

        else:

            education_matches = []
            education_match = 100


        # Experience match
        if job_experience > 0:

            experience_match = min(
                (candidate["experience"] / job_experience) * 100,
                100
            )

        else:

            experience_match = 100


        # -------------------------------------------------
        # FINAL SCORE
        # -------------------------------------------------

        final_score = (
            text_similarity * 0.45
            + skill_match * 0.35
            + education_match * 0.10
            + experience_match * 0.10
        )


        warnings = check_claims(
            candidate["text"],
            candidate["skills"],
            candidate["experience"]
        )


        candidate["text_similarity"] = text_similarity
        candidate["skill_match"] = skill_match
        candidate["education_match"] = education_match
        candidate["experience_match"] = experience_match
        candidate["matched_skills"] = matched_skills
        candidate["missing_skills"] = missing_skills
        candidate["education_matches"] = education_matches
        candidate["claim_warnings"] = warnings
        candidate["score"] = final_score
        candidate["status"] = get_status(final_score)


    # -----------------------------------------------------
    # RANK
    # -----------------------------------------------------

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    filtered_candidates = []

    for candidate in candidates:

        if search_name:

            if search_name.lower() not in candidate["name"].lower():
                continue

        if candidate["score"] < minimum_score:
            continue

        filtered_candidates.append(candidate)


    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    st.markdown("---")
    st.subheader("📊 Recruitment Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resumes Analyzed",
            len(candidates)
        )

    with col2:
        st.metric(
            "Required Skills",
            len(job_skills)
        )

    with col3:
        if candidates:
            st.metric(
                "Top Match",
                f"{candidates[0]['score']:.1f}%"
            )
        else:
            st.metric("Top Match", "0%")

    with col4:
        strong_matches = sum(
            1
            for c in candidates
            if c["score"] >= 75
        )

        st.metric(
            "Strong Matches",
            strong_matches
        )


    # =====================================================
    # RESULTS
    # =====================================================

    st.markdown("---")
    st.subheader("🏆 Candidate Ranking")


    if not filtered_candidates:

        st.info(
            "No candidates match the selected filters."
        )


    for rank, candidate in enumerate(
        filtered_candidates,
        start=1
    ):

        st.markdown("---")

        st.markdown(
            f"## #{rank} — {candidate['name']}"
        )

        st.write(candidate["status"])


        # -------------------------------------------------
        # MAIN METRICS
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Overall Match",
                f"{candidate['score']:.2f}%"
            )

        with col2:
            st.metric(
                "Skill Match",
                f"{candidate['skill_match']:.1f}%"
            )

        with col3:
            st.metric(
                "Experience",
                f"{candidate['experience']:.1f} years"
            )

        with col4:
            st.metric(
                "Text Similarity",
                f"{candidate['text_similarity']:.1f}%"
            )


        # -------------------------------------------------
        # EXPLANATION
        # -------------------------------------------------

        st.markdown("### 💡 Why this candidate matched")


        if candidate["matched_skills"]:

            st.success(
                "✅ Matched Skills: "
                + ", ".join(
                    candidate["matched_skills"]
                )
            )

        else:

            st.warning(
                "No required skills were detected."
            )


        if candidate["missing_skills"]:

            st.warning(
                "⚠️ Missing Skills: "
                + ", ".join(
                    candidate["missing_skills"]
                )
            )

        else:

            st.success(
                "🎯 All required skills were detected."
            )


        # -------------------------------------------------
        # EDUCATION
        # -------------------------------------------------

        st.markdown("### 🎓 Education")

        if candidate["education"]:

            st.write(
                ", ".join(
                    candidate["education"]
                )
            )

        else:

            st.write(
                "Education information not detected."
            )


        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        st.markdown("### 💼 Experience")

        st.write(
            f"{candidate['experience']:.1f} years detected."
        )


        # -------------------------------------------------
        # MATCH BREAKDOWN
        # -------------------------------------------------

        with st.expander("📈 View Match Breakdown"):

            st.write(
                f"Text similarity: "
                f"{candidate['text_similarity']:.2f}%"
            )

            st.write(
                f"Skill match: "
                f"{candidate['skill_match']:.2f}%"
            )

            st.write(
                f"Education match: "
                f"{candidate['education_match']:.2f}%"
            )

            st.write(
                f"Experience match: "
                f"{candidate['experience_match']:.2f}%"
            )


        # -------------------------------------------------
        # CLAIM CHECK
        # -------------------------------------------------

        with st.expander("🛡️ Resume Claim Check"):

            if candidate["claim_warnings"]:

                for warning in candidate["claim_warnings"]:
                    st.warning(warning)

            else:

                st.success(
                    "No obvious unsupported or unusual claims were detected."
                )


        # -------------------------------------------------
        # RAW RESUME
        # -------------------------------------------------

        with st.expander("📄 View Resume Text"):

            st.text(
                candidate["text"]
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI Resume & Job Matching System • ALGOTHON'26"
)