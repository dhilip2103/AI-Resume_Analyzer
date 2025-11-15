from django import forms
from .models import JobMatch

class JobMatchForm(forms.ModelForm):
    class Meta:
        model = JobMatch 
        fields = ["resume", "job_description"]
