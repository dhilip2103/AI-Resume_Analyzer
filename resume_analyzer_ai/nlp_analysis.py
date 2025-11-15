import spacy
from textblob import TextBlob
import re

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# **Grammar & Readability Check**
def check_grammar_and_readability(text):
    """Analyzes grammar mistakes and readability for resume sections like summary, projects, and experience."""
    
    if not text.strip():
        return {"grammar_mistakes": "No text provided.", "readability_check": "N/A"}

    doc = nlp(text)
    mistakes = []

    # Detect tense inconsistencies (verbs must match context)
    past_tense_used = any(token.tag_ == "VBD" for token in doc)  # Check if past tense is used
    present_tense_used = any(token.tag_ in ["VBZ", "VBP"] for token in doc)  # Check if present tense is used

    if past_tense_used and present_tense_used:
        mistakes.append("Inconsistent verb tenses detected. Ensure past and present tense usage is correct.")

    # Check for missing subjects (reduce false positives)
    for sent in doc.sents:
        first_token = sent[0]
        if first_token.pos_ == "VERB" and first_token.dep_ == "ROOT":
            # Check if there's a noun/pronoun before the verb
            has_subject = any(token.dep_ in ["nsubj", "nsubjpass"] for token in sent)
            if not has_subject:
                mistakes.append(f"Possible missing subject near '{first_token.text}'. Ensure sentence clarity.")

    # Assess readability based on sentence complexity and length
    sentences = list(doc.sents)
    avg_sentence_length = sum(len(sent.text.split()) for sent in sentences) / max(len(sentences), 1)
    
    readability_score = max(100 - avg_sentence_length, 0)
    readability_check = "Good readability" if avg_sentence_length < 20 else "Needs improvement"

    # Return only real mistakes, otherwise say "No issues"
    return {
        "grammar_mistakes": mistakes if mistakes else "No grammar issues detected. Your resume is well-written!",
        "readability_score": round(readability_score, 1),
        "readability_check": readability_check
    }
    #💡 Try This:
    #❌ "Developed a web application." → Will warn about missing subject.
    #✔ "I developed a web application." → No warning!
    
    
# **ATS Compatibility Check**
def ats_compatibility_check(text):
    """Checks for ATS issues such as missing sections, tables, images, and poor formatting."""
    
    issues = []
    
    # Validate presence of contact details (phone & email)
    if not re.search(r"\b\d{10}\b", text) and not re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text):
        issues.append("Missing contact details (phone or email).")

    # Detect ATS-unfriendly elements (tables, images)
    if "│" in text or "⎜" in text:
        issues.append("Tables or columns detected – ATS may not parse them correctly.")
    if "📷" in text or "🖼️" in text:
        issues.append("Image detected – ATS cannot read images.")

    # Identify missing essential resume sections
    required_sections = ["summary", "experience", "skills", "education"]
    missing_sections = [sec for sec in required_sections if sec not in text.lower()]
    if missing_sections:
        issues.append(f"Missing sections: {', '.join(missing_sections).capitalize()}.")

    return {"ats_issues": issues}

# **Resume Scoring System**
def calculate_resume_score(text):
    """Evaluates resume score based on grammar, ATS compliance, and completeness."""
    
    grammar_results = check_grammar_and_readability(text)
    ats_results = ats_compatibility_check(text)

    score = 100  # Start with a perfect score

    # Deduct points for grammar mistakes
    grammar_penalty = len(grammar_results["grammar_mistakes"]) * 3
    score -= grammar_penalty  

    # Deduct points for ATS issues
    ats_penalty = len(ats_results["ats_issues"]) * 5
    score -= ats_penalty  

    # Deduct points for missing sections
    required_sections = ["summary", "experience", "skills", "education"]
    missing_sections = [sec for sec in required_sections if sec not in text.lower()]
    missing_section_penalty = len(missing_sections) * 5
    score -= missing_section_penalty  

    # Bonus points for achievements or certifications
    if "certification" in text.lower() or "achievement" in text.lower():
        score += 5  

    # Keep score in the range of 0-100
    score = max(0, min(score, 100))

    # Generate feedback based on score
    feedback = (
        "Excellent job! Your resume is well-structured and ATS-friendly." if score >= 75 else
        "Your resume is decent but could be improved in structure and ATS compliance." if score >= 50 else
        "Your resume requires significant improvements. Consider revising key sections and formatting."
    )

    return {
        "resume_score": score,
        "missing_sections": missing_sections,
        "feedback": feedback
    }

# **Predefined Skill Lists**
HARD_SKILLS = {
    "Python", "Java","Data Analyst", "Machine Learning", "Data Science", "SQL", "Django", "React JS",
    "AWS", "C", "C++", "MongoDB", "MySQL", "UI/UX", "HTML", "CSS", "JavaScript",
    "Bootstrap", "Tailwind CSS", "Node.js", "Angular"
}

SOFT_SKILLS = {
    "Communication", "Teamwork", "Leadership", "Problem-Solving",
    "Creativity", "Time Management", "Adaptability"
}

# **Skill Extraction**
def extract_skills(text):
    #Extracts hard and soft skills from the resume text.
    
    doc = nlp(text)
    extracted_skills = set()

    # Identify potential skills using noun phrases
    for chunk in doc.noun_chunks:
        if chunk.text in HARD_SKILLS or chunk.text in SOFT_SKILLS:
            extracted_skills.add(chunk.text)

    return {
        "hard_skills": sorted(skill for skill in extracted_skills if skill in HARD_SKILLS),
        "soft_skills": sorted(skill for skill in extracted_skills if skill in SOFT_SKILLS)
    }

# **Feedback & Improvement Suggestions**
def generate_feedback(text):
    """Provides actionable feedback for improving resumes."""
    
    suggestions = []

    # Suggest adding missing sections
    required_sections = ["summary", "experience", "skills", "education"]
    missing_sections = [sec for sec in required_sections if sec not in text.lower()]
    if missing_sections:
        suggestions.append(f"Consider adding these missing sections: {', '.join(missing_sections).capitalize()}.")

    # Check for readability issues
    grammar_results = check_grammar_and_readability(text)
    readability_feedback = grammar_results.get("readability_check", "")

    if "Needs improvement" in readability_feedback:
        suggestions.append(" Improve readability by using shorter sentences and clearer formatting.")

    # Provide positive feedback if resume is well-written
    if "Good readability" in readability_feedback and not grammar_results["grammar_mistakes"] and not missing_sections:
        suggestions.append(" Your resume is well-structured, readable, and ATS-friendly. Keep up the great work!")
    elif "Good readability" in readability_feedback:
        suggestions.append(" Your resume is good, but minor improvements can enhance clarity and readability.")
    
    return {"suggestions": suggestions}
