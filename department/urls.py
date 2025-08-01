from django.urls import path
from . import views
app_name = 'department'
urlpatterns = [
    path('', views.home, name='home'),
    path('mis_application/', views.mis_application, name='mis_application'),
    path('old_mis_dashboard/', views.old_mis_dashboard, name='old_mis_dashboard'),
    path('job_portal_mis_dashboard/', views.job_portal_mis_dashboard, name='job_portal_mis_dashboard'),
    path('jobseeker_mis/', views.jobseeker_mis, name='jobseeker_mis'),
    path('employer_mis/', views.employer_mis, name='employer_mis'),
    path('post_notification_mis/', views.post_notification_mis, name='post_notification_mis'),
    path('placement_mis/', views.placement_mis, name='placement_mis'),
    path('employer_details/', views.employer_details, name='employer_details'),
    path('jobseeker_details/', views.jobseeker_details, name='jobseeker_details'),
    path('jobfair_mis/', views.jobfair_mis, name='jobfair_mis'),
    path('recruitment_drive_mis/', views.recruitment_drive_mis, name='recruitment_drive_mis'),
    path('sponsor_feedback/', views.sponsor_feedback, name='sponsor_feedback'),
    path('sponsor_list/', views.sponsor_list, name='sponsor_list'),
    path('pending_counselor_requests/', views.pending_counselor_requests, name='pending_counselor_requests'),
    path('verified_counselor_list/', views.verified_counselor_list, name='verified_counselor_list'),
    path('reject_counselor_list/', views.reject_counselor_list, name='reject_counselor_list'),
    path('pending_college_requests/', views.pending_college_requests, name='pending_college_requests'),
    path('assigened_college_requests/', views.assigened_college_requests, name='assigened_college_requests'),
    path('vocational_guidance_dashboard/', views.vocational_guidance_dashboard, name='vocational_guidance_dashboard'),
]