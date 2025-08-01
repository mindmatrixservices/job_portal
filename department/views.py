from django.shortcuts import render
# from core.models import Department

def home(request):
    
    return render(request, 'department/home.html')

def mis_application(request):
    
    return render(request, 'department/mis_application.html')

def old_mis_dashboard(request):
    
    return render(request, 'department/old_mis_dashboard.html')

def job_portal_mis_dashboard(request):
    
    return render(request, 'department/job_portal_mis_dashboard.html')

def jobseeker_mis(request):
    
    return render(request, 'department/jobseeker_mis.html')

def employer_mis(request):
    
    return render(request, 'department/employer_mis.html')

def post_notification_mis(request):
    
    return render(request, 'department/post_notification_mis.html')

def placement_mis(request):
    
    return render(request, 'department/placement_mis.html')

def employer_details(request):
    
    return render(request, 'department/employer_details.html')

def jobseeker_details(request):
    
    return render(request, 'department/jobseeker_details.html')

def jobfair_mis(request):
    
    return render(request, 'department/jobfair_mis.html')

def recruitment_drive_mis(request):
    
    return render(request, 'department/recruitment_drive_mis.html')

def sponsor_feedback(request):
    
    return render(request, 'department/sponsor_feedback.html')

def sponsor_list(request):
    
    return render(request, 'department/sponsor_list.html')

def pending_counselor_requests(request):
    
    return render(request, 'department/pending_counselor_requests.html')

def verified_counselor_list(request):
    
    return render(request, 'department/verified_counselor_list.html')

def reject_counselor_list(request):
    
    return render(request, 'department/reject_counselor_list.html')

def pending_college_requests(request):
    
    return render(request, 'department/pending_college_requests.html')

def assigened_college_requests(request):
    
    return render(request, 'department/assigened_college_requests.html')

def vocational_guidance_dashboard(request):
    
    return render(request, 'department/vocational_guidance_dashboard.html')
