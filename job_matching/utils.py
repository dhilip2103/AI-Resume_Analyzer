import os
import json
import docx
import PyPDF2
import spacy
from fuzzywuzzy import process
from django.conf import settings

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Load skills database
def load_skills_db():
    skills_path = os.path.join(settings.BASE_DIR, 'job_matching', 'data', 'skills_db.json')
    with open(skills_path, 'r', encoding='utf-8') as file:
        return json.load(file)

SKILLS_DB = load_skills_db()

def extract_text_from_resume(file_path):
    """Extracts text from PDF or DOCX resume files."""
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension == ".pdf":
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text

    elif file_extension in [".doc", ".docx"]:
        doc = docx.Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])
    
    return "Unsupported file format"

def extract_skills(text):
    """Extracts skills using NLP and fuzzy matching."""
    doc = nlp(text.lower())
    extracted_skills = set()

    for token in doc:
        for category, skills in SKILLS_DB.items():
            best_match, score = process.extractOne(token.text, skills)
            if score >= 80:  # Fuzzy match threshold
                extracted_skills.add(best_match.lower())

    return list(extracted_skills)

def extract_resume_skills(resume_text):
    """Extracts skills from different sections of a resume."""
    sections = resume_text.lower().split("\n\n")  # Split by empty lines (simulating sections)
    extracted_skills = set()

    for section in sections:
        if "projects" in section or "certifications" in section or "experience" in section:
            extracted_skills.update(extract_skills(section))

    return list(extracted_skills)

def generate_feedback(match_score, missing_skills):
    """
    Generates feedback based on the match score and missing skills.
    """
    if match_score > 85:
        feedback = "Excellent match! Your resume is well-aligned with the job description."
    elif match_score > 70:
        feedback = " Good match! Your resume fits well, but improving a few key areas could make it stronger."
    elif match_score > 50:
        feedback = " Decent match. You have relevant skills, but adding more industry-specific expertise would help."
    else:
        feedback = " Poor match. Many key skills are missing. Consider improving your resume by adding relevant skills and experience."

    # Convert set to list before slicing
    missing_skills_list = list(missing_skills)  # Convert set to list
    if missing_skills_list:
        top_missing_skills = ", ".join(missing_skills_list[:5])  # Now slicing works
        feedback += f" Focus on improving these skills: **{top_missing_skills}**."

    return feedback


def match_skills(resume_text, job_description):
    """Compares extracted skills from resume and job description."""
    job_skills = extract_skills(job_description)
    resume_skills = extract_resume_skills(resume_text)

    matched_skills = set(job_skills) & set(resume_skills)
    missing_skills = set(job_skills) - set(resume_skills)

    match_score = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
    
    feedback = generate_feedback(match_score, missing_skills)

    return round(match_score, 2), list(matched_skills), list(missing_skills), feedback
