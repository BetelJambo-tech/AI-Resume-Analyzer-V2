# AI Resume Analyzer V2

## Project Overview

Resume Analyzer is a web-based application developed as part of my Computer Science capstone project at Truman State University.

The application helps job seekers compare their resumes with job descriptions, identify relevant and missing skills, and receive recommendations for improving their resumes.

## Live Demo

[Launch Resume Analyzer](https://ai-resume-analyzer-v2-betel.streamlit.app/)

## Features

- Upload resumes in PDF format.
- Extract text and identify skills from resumes.
- Compare resume skills with job requirements.
- Calculate a job match percentage.
- Identify matched and missing skills.
- Provide personalized recommendations.
- Generate downloadable PDF analysis reports.
- Handle empty inputs and unreadable PDF files.
- Provide a clean and user-friendly interface.

## How It Works

1. Upload a resume in PDF format.
2. Paste the target job description.
3. The application extracts and compares skills.
4. Review the match score, matched skills, and missing skills.
5. Review recommendations and download the analysis report.

## Technologies Used

- Python
- Streamlit
- Regular Expressions (Regex)
- ReportLab
- HTML and CSS
- Git and GitHub
- Streamlit Community Cloud

## Match Score Calculation

The application uses keyword-based skill matching to compare the skills found in a resume with those identified in a job description.

The match percentage is calculated using:

Match Score = (Matched Skills / Total Job Skills) × 100

For example, if a job description contains 14 recognized skills and the resume contains 5 of those skills, the match score is 35.71%.

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/BetelJambo-tech/AI-Resume-Analyzer-V2.git
```

Navigate to the project folder:

```bash
cd AI-Resume-Analyzer-V2
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Testing

The application was tested using several scenarios:

| Test Scenario | Result |
|---|---|
| Complete skill match | Passed |
| Partial skill match | Passed |
| Zero skill match | Passed |
| Missing resume | Passed |
| Missing job description | Passed |
| Job description without recognized skills | Passed |
| Resume without recognized skills | Passed |
| Blank PDF file | Passed |
| PDF report generation | Passed |

## Limitations

- Skill detection depends on a predefined skill database.
- The application does not currently support scanned or image-based resumes.
- Keyword matching may not recognize every synonym or related skill.
- The match score measures skill overlap, not the likelihood of being hired.

## Future Improvements

- Semantic matching using natural language processing.
- Support for scanned resumes using OCR.
- Support for additional resume file formats.
- More detailed resume feedback.
- Expansion of the skill database.

## Author

Betel Gurara

Computer Science

Truman State University

Senior Capstone Project — 2026
