import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .utils import extract_resume_text
from .nlp_analysis import extract_skills, ats_compatibility_check, calculate_resume_score, generate_feedback, check_grammar_and_readability

# Upload Resume View
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        file_extension = os.path.splitext(resume_file.name)[1].lower()

        if file_extension not in ['.pdf', '.docx']:
            return render(request, 'resume_analyzer/upload_resume.html', {'error': 'Invalid file format. Upload PDF or DOCX.'})

        # Save the file
        fs = FileSystemStorage(location='media/uploads/')
        filename = fs.save(resume_file.name, resume_file)
        file_path = os.path.join('media/uploads/', filename)

        # Extract text from the resume
        extracted_text = extract_resume_text(file_path, file_extension)

        # Store extracted text in session for analysis
        request.session['resume_text'] = extracted_text  

        return redirect('analyze_resume')

    return render(request, 'resume_analyzer/upload_resume.html')

# Analyze Resume View with NLP Analysis
def analyze_resume(request):
    resume_text = request.session.get('resume_text', '')

    if not resume_text:
        return render(request, 'resume_analyzer/analyze.html', {"error": "No resume uploaded."})

    # Perform NLP analysis
    extracted_skills = extract_skills(resume_text)
    ats_results = ats_compatibility_check(resume_text)
    resume_score = calculate_resume_score(resume_text)
    feedback = generate_feedback(resume_text)

     # ✅ Grammar & Readability Check
    grammar_results = check_grammar_and_readability(resume_text)

    # ✅ Positive feedback for well-structured resumes
    positive_feedback = "Your resume is well-structured and optimized for ATS. Great job! Keep it up!" if resume_score["resume_score"] > 80 else ""

    return render(request, 'resume_analyzer/analyze.html', {
        "resume_text": resume_text,
        "extracted_skills": extracted_skills,
        "ats_results": ats_results,
        "resume_score": resume_score["resume_score"],
        "feedback": feedback,
        "grammar_results": grammar_results,
        "positive_feedback": positive_feedback
    })

