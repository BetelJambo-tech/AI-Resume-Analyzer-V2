import streamlit as st
import PyPDF2
import pandas as pd
import re
from html import escape
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

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
    # Programming Languages
    "python", "java", "javascript", "typescript",
    "c++", "c#", "php", "ruby", "matlab", "swift",
    "kotlin",

    # Web Development
    "html", "css", "react", "angular", "vue.js",
    "node.js", "flask", "django", "fastapi",
    "bootstrap", "streamlit", "rest api",

    # Data Science and Analytics
    "data analysis", "data visualization",
    "data science", "pandas", "numpy", "excel",
    "tableau", "power bi", "statistics",
    "data mining", "matplotlib", "sas", "spss",

    # Artificial Intelligence
    "artificial intelligence", "machine learning",
    "deep learning", "natural language processing",
    "nlp", "tensorflow", "pytorch", "scikit-learn",
    "opencv", "computer vision", "generative ai",

    # Databases
    "sql", "mysql", "postgresql", "mongodb",
    "sqlite", "oracle", "firebase", "nosql",

    # Cloud Computing and DevOps
    "aws", "azure", "google cloud", "docker",
    "kubernetes", "jenkins", "git", "github",
    "gitlab", "ci/cd", "terraform", "linux",

    # Cybersecurity
    "cybersecurity", "network security",
    "information security", "wireshark",
    "penetration testing", "risk management",
    "incident response", "encryption",

    # Healthcare and Health Informatics
    "health informatics", "biomedical informatics",
    "clinical informatics", "ehr", "emr", "epic",
    "cerner", "hl7", "fhir", "hipaa",
    "clinical data", "medical terminology",
    "healthcare analytics", "public health",
    "clinical research", "patient care",
    "bioinformatics", "medical imaging",

    # Business and Management
    "project management", "business analysis",
    "agile", "scrum", "jira", "strategic planning",
    "customer service", "budgeting",
    "microsoft office", "powerpoint",

    # Research
    "research", "literature review",
    "systematic review", "academic writing",
    "data collection", "statistical analysis",

    # Soft Skills
    "communication", "leadership", "teamwork",
    "problem solving", "critical thinking",
    "time management", "adaptability",
    "collaboration", "organization",
    "attention to detail", "decision making"
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
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0
    matched = set(resume_skills).intersection(set(job_skills))
    score = (len(matched) / len(job_skills)) * 100
    return round(score, 2)


def format_skill(skill):
    special_names = {
        "sql": "SQL",
        "numpy": "NumPy",
        "javascript": "JavaScript",
        "github": "GitHub",
        "html": "HTML",
        "css": "CSS",
        "power bi": "Power BI",
        "node.js": "Node.js",
        "mongodb": "MongoDB",
        "typescript": "TypeScript",
        "postgresql": "PostgreSQL",
        "nlp": "NLP",
        "api": "API",
        "aws": "AWS",
        "ai": "AI",
        "ui/ux": "UI/UX",
        "c++": "C++",
        "c#": "C#",
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "scikit-learn": "scikit-learn",
        "excel": "Excel"
    }

    return special_names.get(skill.lower(), skill.title())



def generate_recommendations(match_score, matched_skills, missing_skills):
    recommendations = []

    if match_score >= 80:
        assessment = "Excellent Match"
        recommendations.append(
            "Your resume aligns strongly with the detected job requirements."
        )

    elif match_score >= 60:
        assessment = "Good Match"
        recommendations.append(
            "Your resume matches many of the detected job requirements."
        )

    elif match_score >= 40:
        assessment = "Moderate Match"
        recommendations.append(
            "Your resume has relevant skills, but there is room for improvement."
        )

    else:
        assessment = "Needs Improvement"
        recommendations.append(
            "Consider developing more skills relevant to this position."
        )

    if matched_skills:
        strengths = ", ".join(
            format_skill(skill) for skill in sorted(matched_skills)[:5]
        )
        recommendations.append(
            f"Highlight your experience with {strengths}."
        )

    if missing_skills:
        gaps = ", ".join(
            format_skill(skill) for skill in sorted(missing_skills)[:5]
        )
        recommendations.append(
            f"Consider developing or demonstrating these skills: {gaps}."
        )

    recommendations.append(
        "Use measurable achievements and relevant projects to strengthen your resume."
    )

    recommendations.append(
        "Only include skills that you genuinely possess."
    )

    return assessment, recommendations



def generate_pdf_report(match_score, resume_skills, matched_skills, missing_skills):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "CustomTitle",
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#7C3AED"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER
    )

    story.append(Paragraph("AI Resume Analyzer V2", title_style))
    story.append(Paragraph("Resume Analysis Report", subtitle_style))
    story.append(Spacer(1, 25))

    summary_data = [
        ["Job Match", "Detected", "Matched", "Missing"],
        [
            f"{match_score:.2f}%",
            str(len(resume_skills)),
            str(len(matched_skills)),
            str(len(missing_skills))
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[110, 110, 110, 110]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F1F5F9")),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#7C3AED")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTSIZE", (0, 1), (-1, 1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))
    
    detected_style = ParagraphStyle(
        "DetectedSkills",
        parent=styles["Normal"],
        textColor=colors.HexColor("#334155"),
        fontSize=11,
        leading=17
    )

    matched_style = ParagraphStyle(
        "MatchedSkills",
        parent=styles["Normal"],
        textColor=colors.HexColor("#15803D"),
        fontSize=11,
        leading=17
    )

    missing_style = ParagraphStyle(
        "MissingSkills",
        parent=styles["Normal"],
        textColor=colors.HexColor("#DC2626"),
        fontSize=11,
        leading=17
    )

    
    
    story.append(Paragraph("Skills Detected", styles["Heading2"]))

    detected_text = ", ".join(
        escape(format_skill(skill)) for skill in resume_skills
    )

    story.append(Paragraph(
        detected_text or "No skills detected.",
        detected_style
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph("Matched Job Skills", styles["Heading2"]))

    matched_text = ", ".join(
        escape(format_skill(skill)) for skill in matched_skills
    )

    story.append(Paragraph(
        matched_text or "No matching skills detected.",
        matched_style
    ))

    story.append(Spacer(1, 15))

    story.append(Paragraph("Missing Job Skills", styles["Heading2"]))

    missing_text = ", ".join(
        escape(format_skill(skill)) for skill in missing_skills
    )

    story.append(Paragraph(
        missing_text or "No missing skills detected.",
        missing_style if missing_skills else matched_style
    ))

    story.append(Spacer(1, 20))


    
    story.append(Paragraph(
        "Personalized Recommendations",
        styles["Heading2"]
    ))

    assessment, recommendations = generate_recommendations(
        match_score,
        matched_skills,
        missing_skills
    )

    story.append(Paragraph(
        f"<b>Assessment: {escape(assessment)}</b>",
        matched_style if match_score >= 60 else detected_style
    ))

    story.append(Spacer(1, 8))

    for recommendation in recommendations:
        story.append(Paragraph(
            f"- {escape(recommendation)}",
            detected_style
        ))


    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()

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
  


if uploaded_resume is None and not job_description.strip():
    st.info("Please upload your resume and paste a job description to begin.")

elif uploaded_resume is None:
    st.info("Please upload your resume to begin the analysis.")

elif not job_description.strip():
    st.info("Please paste a job description to begin your resume analysis.")

else:

    
    try:
        resume_text = extract_text_from_pdf(uploaded_resume)

    except Exception:
        st.error("Unable to read the uploaded PDF. Please upload a valid, unprotected PDF file.")
        st.stop()

    if not resume_text or not resume_text.strip():
        st.warning("No readable text was found in your resume.")
        st.info("Please upload a text-based PDF instead of a scanned image.")
        st.stop()


    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    
    if not resume_skills:
        st.warning("⚠️ No recognizable skills were found in your resume.")
        st.info("Please check that your resume includes relevant skills, experience, and qualifications.")
        st.stop()

    
    if not job_skills:
        st.warning("⚠️ No recognizable skills were found in the job description.")
        st.info("Please provide a more detailed job description that includes required skills, qualifications, or technical requirements.")
        st.stop()

    
    matched_skills = sorted(set(resume_skills) & set(job_skills))
    missing_skills = sorted(set(job_skills) - set(resume_skills))
    match_score = calculate_match(resume_skills, job_skills)

    st.markdown("---")
    st.markdown("### 📊 Analysis Results")

    st.markdown("### 📈 Your Job Match Overview")

    
    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric("🎯 Job Match", f"{match_score}%")

    with metric2:
        st.metric("✅ Skills Detected", len(resume_skills))

    with metric3:
        st.metric("🎯 Matched Skills", len(matched_skills))

    with metric4:
        st.metric("⚠️ Missing Skills", len(missing_skills))



    st.markdown("#### Resume-to-Job Match")

    st.progress(
        min(max(float(match_score) / 100, 0.0), 1.0)
    )

    if match_score >= 80:
        st.success("Strong keyword match! Your resume includes most of the detected job skills.")
    elif match_score >= 50:
        st.warning("Moderate keyword match. Some job skills may be missing.")
    else:
        st.error("Low keyword match. Review the missing skills below.")


    
    from html import escape
    
    st.markdown("### ✅ Skills Detected")
    
    if resume_skills:
        badges = "".join(
            f'<span style="display:inline-block; background:#153D35; '
            f'color:#6EE7B7; padding:9px 15px; margin:5px; '
            f'border-radius:20px; font-size:14px;">'
            f'✓ {escape(skill.title())}</span>'
            for skill in resume_skills
        )
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.info("No known skills detected.")
        
    
    st.markdown("### 🎯 Matched Job Skills")
    st.caption("Skills found in both your resume and the job description.")

    if matched_skills:
        badges = "".join(
            f'<span style="display:inline-block; background:#153D35; '
            f'color:#6EE7B7; padding:9px 15px; margin:5px; '
            f'border-radius:20px; font-size:14px;">'
            f'✓ {escape(skill.title())}</span>'
            for skill in matched_skills
        )
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.info("No matching job skills detected.")


    st.markdown("### ⚠️ Missing Job Skills")
    
    if missing_skills:
        badges = "".join(
            f'<span style="display:inline-block; background:#4C2535; '
            f'color:#FDA4AF; padding:9px 15px; margin:5px; '
            f'border-radius:20px; font-size:14px;">'
            f'✕ {escape(skill.upper() if skill.lower() == "aws" else skill.title())}</span>'
            for skill in missing_skills
        )
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.success("No missing skills detected. Great match!")
    
    
        
    
    st.subheader("Personalized Recommendations")

    assessment, recommendations = generate_recommendations(
        match_score,
        matched_skills,
        missing_skills
    )

    if match_score >= 80:
        st.success(f"Excellent Match — {match_score:.2f}%")

    elif match_score >= 60:
        st.success(f"Good Match — {match_score:.2f}%")

    elif match_score >= 40:
        st.warning(f"Moderate Match — {match_score:.2f}%")

    else:
        st.warning(f"Needs Improvement — {match_score:.2f}%")

    for recommendation in recommendations:
        st.write(f"• {recommendation}")


    st.markdown("### 📥 Download Your Analysis Report")

    pdf_report = generate_pdf_report(
        match_score,
        resume_skills,
        matched_skills,
        missing_skills
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_report,
        file_name="AI_Resume_Analysis_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


st.markdown("---")
st.caption("Built with Python, Streamlit, spaCy, and PyPDF2")
st.caption("AI Resume Analyzer Project by Betel")
