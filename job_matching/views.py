from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobMatchForm
from .models import JobMatch
from .utils import extract_text_from_resume, match_skills
from django.views.generic import TemplateView
import json
import os
from django.conf import settings

#Corrected Path to Load skills_db.json
SKILLS_DB_PATH = os.path.join(settings.BASE_DIR, 'resume_analyzer', 'job_matching', 'skills_db.json')

try:
    with open(SKILLS_DB_PATH, 'r', encoding='utf-8') as file:
        SKILLS_DB = json.load(file)
    print("skills_db.json loaded successfully!")
except FileNotFoundError:
    print(" Warning: skills_db.json not found! Using an empty skills database.")
    SKILLS_DB = {}  # Use an empty dictionary if the file is missing
except json.JSONDecodeError:
    print(" Warning: Invalid JSON format in skills_db.json!")
    SKILLS_DB = {}

class JobMatchingView(TemplateView):
    """Renders the job matching input page."""
    template_name = 'job_matching/job_matching.html'

def job_matching(request):
    """Handles job matching form submission and redirects to results."""
    if request.method == "POST":
        form = JobMatchForm(request.POST, request.FILES)
        if form.is_valid():
            job_match = form.save()
            return redirect("job_matching:job_result", job_match_id=job_match.id)
        else:
            print(" Form validation failed:", form.errors)  # Debugging log

    else:
        form = JobMatchForm()

    return render(request, 'job_matching/job_matching.html', {"form": form})

def job_result(request, job_match_id):
    """Displays job matching results after analysis."""
    job_match = get_object_or_404(JobMatch, id=job_match_id)

    #Error Handling for Resume Extraction
    try:
        resume_text = extract_text_from_resume(job_match.resume.path)
    except Exception as e:
        resume_text = ""
        print(f" Error extracting resume text: {e}")

    #Extract job description
    job_description = job_match.job_description

    #Perform skill gap analysis with skills database
    match_score, matched_skills, missing_skills, feedback = match_skills(resume_text, job_description)

    return render(request, "job_matching/job_result.html", {
        "resume_name": job_match.resume.name,
        "job_description": job_description,
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "feedback": feedback,
        "job_match_id": job_match_id
    })
