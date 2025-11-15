from django.shortcuts import render

# Create your views here.

# Landing Page View

def landing_page(request):
    return render(request, 'user_management/landing.html')

# Dashboard page view

def dashboard(request):
    return render(request, 'user_management/dashboard.html')