import streamlit as st
import PyPDF2
import pandas as pd
import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #f8fafc;
}

.stMetric {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

[data-testid="stFileUploader"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 12px;
}

textarea {
    border-radius: 12px !important;
}

.result-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #f8fafc;
}

.small-note {
    color: #cbd5e1;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)
st.title("📄 AI Resume Analyzer + Job Matcher")
st.caption("Upload a resume and compare it with a job description.")
st.info("Upload a PDF resume and paste a job description to see your match score, missing skills, and suggestions.")

st.info("""
🔍 How it works:
- Upload your resume (PDF)
- Paste a job description
- Get match score, missing skills, and suggestions
""")

SKILL_KEYWORDS = [
    "python", "java", "javascript", "html", "css", "sql", "react", "node.js",
    "flask", "streamlit", "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "opencv", "scikit-learn", "git", "github", "aws",
    "docker", "mongodb", "firebase", "rest api", "linux"
]

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))

def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0
    matched = set(resume_skills).intersection(set(job_skills))
    score = (len(matched) / len(job_skills)) * 100
    return round(score, 2)

col1, col2 = st.columns(2)

st.markdown('<div class="section-title">Upload and Compare</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Job Description", height=250)

if uploaded_resume and job_description:
    resume_text = extract_text_from_pdf(uploaded_resume)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    missing_skills = sorted(set(job_skills) - set(resume_skills))
    match_score = calculate_match(resume_skills, job_skills)

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Analysis Results</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Match Score", f"{match_score}%")
    metric2.metric("Resume Skills Found", len(resume_skills))
    metric3.metric("Missing Skills", len(missing_skills))

    st.markdown("### ❌ Missing Skills")
    if missing_skills:
        st.error(", ".join(missing_skills))
    else:
        st.success("No missing skills. Great match!")

    st.markdown("### 📌 Resume Skills")
    if resume_skills:
        st.write(", ".join(resume_skills))
    else:
        st.write("No known skills detected.")

    st.markdown("### 💡 Suggestions")
    if missing_skills:
        st.write("Consider adding or improving these skills in your resume if you have experience with them:")
        for skill in missing_skills:
            st.write(f"- {skill}")
    else:
        st.write("Your resume matches the job description very well.")

st.markdown("---")
st.caption("Built with Python, Streamlit, spaCy, and PyPDF2")
st.caption("AI Resume Analyzer Project by Betel")
