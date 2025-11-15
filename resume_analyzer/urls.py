"""
URL configuration for resume_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from resume_analyzer_ai.views import upload_resume, analyze_resume  # Import newly added views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    path('', include('user_management.urls')),   # Connents to User_management app/module
    path('analyzer/', include('resume_analyzer_ai.urls')),
    path('job_matching/', include('job_matching.urls', namespace='job_matching')), 
 
    # URLs for Resume Upload & Analysis
    path('upload/', upload_resume, name='upload_resume'),
    path('analyze/', analyze_resume, name='analyze_resume'),
    
]

# Serve media files correctly (Only in Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)