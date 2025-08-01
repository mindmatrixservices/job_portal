from django.urls import path
from . import views

app_name = 'recruiter'
urlpatterns = [
    # Example route
    path('', views.home, name='home'),
    path('job_post/', views.job_post, name='job_post'),
    path('profile/', views.profile, name='profile'),
    path('er1/', views.er1, name='er1'),
    path('er2/', views.er2, name='er2'),
    path('er1_view/', views.er1_view, name='er1_view'),
    path('er2_view/', views.er2_view, name='er2_view'),
    path('delete_job_post/<str:job_id>/', views.delete_job_post, name='delete_job_post'),
    # ===============ER=========
    path('check_quarter/', views.check_quarter, name='check_quarter'),
    path('er1form_save/', views.er1form_save, name='er1form_save'),
    path('view_er1report/', views.view_er1report, name='view_er1report'),
    path('new_er1_report_detail/<str:increment_number>/', views.new_er1_report_detail, name='new_er1_report_detail'),
    path('print_page/<str:increment_number>/', views.print_page, name='print_page'),
    path('er2form_save/', views.er2form_save, name='er2form_save'),
    path('success/', views.success, name='success'),
    path('view_er2report/', views.view_er2report, name='view_er2report'),
    path('new_er2_report_detail/<str:id>/', views.new_er2_report_detail, name='new_er2_report_detail'),
    path('print_er2_page/<str:id>/', views.print_er2_page, name='print_er2_page'),
]
