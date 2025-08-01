from django.shortcuts import render

def home(request):
    return render(request, 'jobseeker/home.html')
