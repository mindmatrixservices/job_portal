from django.shortcuts import render
from peeldb.models import *
from django.views.decorators.cache import cache_control, never_cache
# from core.models import Department

def home(request):
    emps_exchanges= New_Employment_Exchange.objects.all()
    return render(request, 'department/home.html',{'emps_exchanges':emps_exchanges})

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

@never_cache
#@department_login_required       
def jobfair_mis(request):
    # if request.user.is_authenticated:
    #     if not request.user.is_jobseeker and not request.user.is_recruiter and not request.user.is_agency_recruiter:
    if request.method == "POST":
        if (request.POST.get("employment_exchange", "")):
            employment_exchange =request.POST.get("employment_exchange")
            print("employment_exchange:",employment_exchange)
            jobfair_data = JobFair.objects.filter(jobfair_type = 'jobfair', created_by = employment_exchange)
            print(jobfair_data)
            jobfair_list = []
            
            for jobfair in jobfair_data: 
                jobfair_dict = {}
                total_shortlisted_count_jf = 0
                total_placement_count_jf = 0
                employers = jobfair.jobpost.values('user').distinct().count()
                jobpost_count = jobfair.jobpost.all().count()
                participated_jobseekers_count = jobfair.candidates_participated.all().count()
                # print(employers)
                for jobpost_instance in jobfair.jobpost.all():
                    shortlisted_count = jobpost_instance.get_shortlisted_users_count() + jobpost_instance.get_selected_users_count()
                    total_shortlisted_count_jf += shortlisted_count
                    placement_count = jobpost_instance.get_selected_users_count()
                    total_placement_count_jf += placement_count

                jobfair_dict['jobfair_id'] = jobfair.jobfair_id
                jobfair_dict['start_date'] = jobfair.start_date
                jobfair_dict['end_date'] = jobfair.end_date
                jobfair_dict['location'] = jobfair.location
                jobfair_dict['employers'] = employers
                jobfair_dict['jobpost_count'] = jobpost_count
                jobfair_dict['participated_jobseekers_count'] = participated_jobseekers_count
                jobfair_dict['shortlisted_count'] = total_shortlisted_count_jf
                jobfair_dict['placement_count'] = total_placement_count_jf
                jobfair_list.append(jobfair_dict)
            
            print("Response Returned to WebPage")    
            #print(s)     
            emps_exchanges= New_Employment_Exchange.objects.all()
            return render(request, 'department/jobfair_mis.html', {'jobfair_list': jobfair_list,'emps_exchanges':emps_exchanges})
    
    emps_exchanges= New_Employment_Exchange.objects.all()
    return render(request, 'department/jobfair_mis.html',{'emps_exchanges':emps_exchanges})
    #return render(request, 'department/login.html')

@never_cache
#@department_login_required
def recruitment_drive_mis(request):
    # if request.user.is_authenticated:
    #     if not request.user.is_jobseeker and not request.user.is_recruiter and not request.user.is_agency_recruiter:
    if request.method == "POST":
        if (request.POST.get("employment_exchange", "")):
            emps_exchanges= New_Employment_Exchange.objects.all()
            employment_exchange =request.POST.get("employment_exchange")
            print(employment_exchange)
            jobfair_data = JobFair.objects.filter(jobfair_type = 'recruitmentdrive', created_by = employment_exchange)
            print(jobfair_data)
            recruitmentdrive_list = []
            
            for recruitmentdrive in jobfair_data: 
                recruitmentdrive_dict = {}
                total_shortlisted_count_rd = 0
                total_placement_count_rd = 0
                employers = recruitmentdrive.jobpost.values('user').distinct().count()
                jobpost_count = recruitmentdrive.jobpost.all().count()
                participated_jobseekers_count = recruitmentdrive.candidates_participated.all().count()
                print(employers)
                for jobpost_instance in recruitmentdrive.jobpost.all():
                    shortlisted_count = jobpost_instance.get_shortlisted_users_count()
                    total_shortlisted_count_rd += shortlisted_count
                    placement_count = jobpost_instance.get_selected_users_count()
                    total_placement_count_rd += placement_count

                recruitmentdrive_dict['jobfair_id'] = recruitmentdrive.jobfair_id
                recruitmentdrive_dict['start_date'] = recruitmentdrive.start_date
                recruitmentdrive_dict['end_date'] = recruitmentdrive.end_date
                recruitmentdrive_dict['location'] = recruitmentdrive.location
                recruitmentdrive_dict['employers'] = employers
                recruitmentdrive_dict['jobpost_count'] = jobpost_count
                recruitmentdrive_dict['participated_jobseekers_count'] = participated_jobseekers_count
                recruitmentdrive_dict['shortlisted_count'] = total_shortlisted_count_rd
                recruitmentdrive_dict['placement_count'] = total_placement_count_rd
                recruitmentdrive_list.append(recruitmentdrive_dict)
            
            print("Response Returned to WebPage")    
            emps_exchanges= New_Employment_Exchange.objects.all()     
            return render(request, 'department/recruitment_drive_mis.html', {'recruitmentdrive_list': recruitmentdrive_list,'emps_exchanges':emps_exchanges})
    emps_exchanges= New_Employment_Exchange.objects.all()        
    return render(request, 'department/recruitment_drive_mis.html',{'emps_exchanges':emps_exchanges})
    #return render(request, 'department/login.html')


def sponsor_feedback(request):
    
    return render(request, 'department/sponsor_feedback.html')

@never_cache
#@department_login_required
def sponsor_list(request):
    # if request.user.is_authenticated:
    #     if not request.user.is_jobseeker and not request.user.is_recruiter and not request.user.is_agency_recruiter:
    jobfair_jobs = JobPost.objects.filter(job_post_options = 'JobFair')
    if request.method == "POST":
        data_dict = {}
        if request.POST.get("emp_exchange1", ""):
            emp_ex_name = request.POST.get('emp_exchange1')
            data_dict['employment_exchange']=emp_ex_name
            
        if request.POST.get("district", ""):
            district = request.POST.get('district')
            data_dict['district']=district

        if request.POST.get("qualification", ""):
            qualification = request.POST.get('qualification')
            data_dict['highest_educational_level']=qualification
            
        if request.POST.get("physically_handicapped", ""):
            physically_handicapped = request.POST.get('physically_handicapped')
            data_dict['are_you_differently_abled_pwd']=physically_handicapped
        
        
        if request.POST.get("disability_category", ""):
            disability_category = request.POST.get('disability_category')
            data_dict['disability_category']=disability_category
        
            
        if request.POST.get("caste", ""):
            caste = request.POST.get('caste')
            data_dict['caste']=caste 
            
        if request.POST.get("gender", ""):     
            gender = request.POST.get('gender')
            data_dict['applicant_gender']=gender

        age_at_the_date =""
        if request.POST.get("age_at_the_date", ""):
            age_at_the_date = request.POST.get('age_at_the_date')
            age_at_date = datetime.strptime(age_at_the_date, '%Y-%m-%d')
            print(age_at_the_date)

        if request.POST.get("age_from", ""): 
            
            age_from = int(request.POST.get('age_from'))
            age_to = int(request.POST.get('age_to'))

            if age_at_the_date == '':
                from_age = date.today() - relativedelta(years=+(int(age_from)))
                to_age = date.today() - relativedelta(years=+(int(age_to)))
                data_dict['date_of_birth__range']=[to_age, from_age]
            
            else:
                from_age = age_at_date - relativedelta(years=+age_from)
                to_age= age_at_date - relativedelta(years=+age_to)
                data_dict['date_of_birth__range']=[to_age, from_age]
        
        
        if request.POST.get("exam_passed", ""):
            exam_passed = request.POST.get('exam_passed')
            data_dict['education_qualification__examination_passed__istartswith']=exam_passed

        if request.POST.get("percentage", ""):
            percentage = float(request.POST.get('percentage'))
            data_dict['education_qualification__percentage_of_marks__gte']=percentage

        if request.POST.get("registration_no", ""):
            registration_no = request.POST.get('registration_no')
            data_dict['registration_no']=registration_no

        if request.POST.get("subject", ""):
            subject = request.POST.getlist('subject')
            subjects =''
            for sub in subject:
                if subjects =='':
                    subjects = sub
                else:
                    subjects+=  "," + sub
            print(subjects)
        
        start = int(request.POST.get("start"))
        length = int(request.POST.get("length"))
        draw = int(request.POST.get("draw"))
        if data_dict=={}:
            return HttpResponse(json.dumps(""))

        elif Ex1_Applicant.objects.filter(**data_dict).exists():
            if request.POST.get("subject", ""):
                count_desired_candidates = Ex1_Applicant.objects.filter( **data_dict).annotate(sub=Concat('education_qualification__major_elective_subject', Value(','), 'education_qualification__subjects_other_subjects')
                    ).filter(sub__icontains=subjects).distinct().order_by("id").count()
                desired_candidates = Ex1_Applicant.objects.filter( **data_dict).annotate(sub=Concat('education_qualification__major_elective_subject', Value(','), 'education_qualification__subjects_other_subjects')
                    ).filter(sub__icontains=subjects).distinct().order_by("id")[start: (start+length)]
            else:
                count_desired_candidates = Ex1_Applicant.objects.filter( **data_dict).distinct().order_by("id").count()
                desired_candidates = Ex1_Applicant.objects.filter( **data_dict).distinct().order_by("id")[start: (start+length)]
                print("Desired Candidates Filled")
        else:     
            return HttpResponse(json.dumps(""))
        
            # print(desired_candidates.highest_educational_level)
            # print(desired_candidates.education_qualification.values('percentage_of_marks'))
        
        l =[]
        
        print("Dictionary Section")
        for candidate in desired_candidates:
            D={}
            D["employment_exchange"]=candidate.employment_exchange
            D["registration_no"] = candidate.registration_no
            D["applicant_name"]=candidate.applicant_name
            D["mobile_number"]= candidate.mobile_number
            D["email"]=candidate.email
            D["pincode"] = candidate.pin_code
            D["address"] = candidate.vill_town_ward_city
            D["fathers_name"] = candidate.fathers_name
            D["district"]= candidate.district 
            if candidate.date_of_birth is None or candidate.date_of_birth == '':
                D["date_of_birth"]= ""
            else:
                D["date_of_birth"] = (candidate.date_of_birth).isoformat() 
            
            D["applicant_gender"] = candidate.applicant_gender
            D["religion"] = candidate.religion
            D["caste"] = candidate.caste
            D["highest_educational_level"] = candidate.highest_educational_level
            D["disability_category"] = candidate.disability_category
            D["th10_percentage"] = ""
            D["th12_stream"] = ""
            D["th12_percentage"] = ""
            D["graduate_stream"] = ""
            D["graduate_percentage"] = "" 
            D["post_graduate_stream"] = ""
            D["post_graduate_percentage"] = "" 
            D["diploma"] = ""
            D["iti"] = ""
            # D["highest_qualification_percentage"] = ""
            
            for d in candidate.education_qualification.all():
                
                if "10th" in str(d.examination_passed):
                    D["th10_percentage"] = d.percentage_of_marks
                elif str(d.examination_passed).startswith("12th"):
                    if " " in str(d.examination_passed):
                        degree, stream = str(d.examination_passed).split(' ') 
                        D["th12_stream"] = stream
                    D["th12_percentage"] = d.percentage_of_marks
                
                elif str(d.examination_passed).startswith("B"):
                    D["graduate_stream"] = d.examination_passed
                    D["graduate_percentage"] = d.percentage_of_marks
                
                elif str(d.examination_passed).startswith("M"):
                    D["post_graduate_stream"] = d.examination_passed
                    D["post_graduate_percentage"] = d.percentage_of_marks
                
                elif "Diploma" in str(d.examination_passed):
                    D["diploma"] = d.examination_passed
                
                elif "ITI" in str(d.examination_passed):
                    D["iti"] = d.examination_passed

                    # D["percentage"] = d.percentage_of_marks
                #  print(d.major_elective_subject)
            
            #  D["year_of_procurement"]=(list.year_of_procurement).isoformat()
            
            l.append(D)
        
            # if s =="":
            #     s+=str(json.dumps(D))
            # else:
            #     s= s+", "+ str(json.dumps(D))
                
        # s="[" + s + "]"
        
        
        

        response_data = {
        
            "draw": draw,
            "recordsTotal" : count_desired_candidates,
            "recordsFiltered" : count_desired_candidates,
            "data": l
    
        }
        print("Response Returned to WebPage")    
        #print(s)     
        return HttpResponse(json.dumps(response_data))
    else:
        return render(request, 'department/sponsor_list.html', {'jobs': jobfair_jobs})
    #     else:
    #         return HttpResponseRedirect("/")
    # else:
    #     return render(request, 'department/login.html')


def pending_counselor_requests(request):
    counsellor = CounsellorDetails.objects.filter(form_status='Yes', status = 'Pending')
    return render(request, 'department/pending_counselor_requests.html', {'counsellor':counsellor})

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
