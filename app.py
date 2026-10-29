import streamlit as st
import PyPDF2
import pandas as pd
import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0B1020, #141B34);
    color: #F8FAFC;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Headings */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #334155;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    background-color: #1E293B !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #2563EB);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #6D28D9, #1D4ED8);
    color: white;
}

/* Result cards */
.result-box {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-top: 15px;
    margin-bottom: 15px;
}

/* Section titles */
.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
    color: #C4B5FD;
}

/* Small text */
.small-note {
    color: #94A3B8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:35px 0 25px 0;">
    <div style="font-size:45px; margin-bottom:12px;">✨</div>
    <h1 style="font-size:46px; margin-bottom:12px;">
        AI Resume Analyzer
        <span style="color:#A78BFA;">V2</span>
    </h1>
    <p style="font-size:18px; color:#CBD5E1;">
        Analyze your resume. Discover missing skills.
        Improve your chances of matching your dream job.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("### How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="result-box" style="text-align:center;">
        <h2>📤</h2>
        <h3>01. Upload</h3>
        <p>Upload your resume in PDF format.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="result-box" style="text-align:center;">
        <h2>💼</h2>
        <h3>02. Compare</h3>
        <p>Paste the job description you want to match.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="result-box" style="text-align:center;">
        <h2>📊</h2>
        <h3>03. Improve</h3>
        <p>Get your match score and skill suggestions.</p>
    </div>
    """, unsafe_allow_html=True)


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


col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📄 Upload Your Resume")
    st.caption("Upload your resume in PDF format.")

    uploaded_resume = st.file_uploader(
        "Choose your resume",
        type=["pdf"]
    )

    if uploaded_resume is not None:
        st.success(f"✅ {uploaded_resume.name} uploaded successfully!")

with col2:
    st.markdown("### 💼 Job Description")
    st.caption("Paste the job description you want to compare.")

    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job requirements here...",
        label_visibility="collapsed"
    )
  

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
