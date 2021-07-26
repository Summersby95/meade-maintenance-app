from django.shortcuts import render

# Create your views here.

def dashboard(request):
    """Returns dashboard home"""
    return render(request, 'dashboard/dashboard.html')