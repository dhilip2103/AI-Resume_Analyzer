from django.db import models

class JobMatch(models.Model):
    resume = models.FileField(upload_to="resumes/")
    job_description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Stores upload timestamp

    def __str__(self):
        return f"Job Match - {self.id}"
