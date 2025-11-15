from django.urls import path
from .views import job_matching, job_result 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'job_matching'

urlpatterns = [
    
    path('job_match/', job_matching, name='job_matching'),  # Upload page
    path('job_result/<int:job_match_id>/', job_result, name='job_result'),  # Results page

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

