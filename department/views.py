from django.shortcuts import render, redirect
from peeldb.models import *
from django.views.decorators.cache import cache_control, never_cache
from django.http import JsonResponse
# from core.models import Department

def home(request):
    emps_exchanges= New_Employment_Exchange.objects.all()
    return render(request, 'department/home.html',{'emps_exchanges':emps_exchanges})

def mis_application(request):
    
    return render(request, 'department/mis_application.html')

def old_mis_dashboard(request):
    
    return render(request, 'department/old_mis_dashboard.html')

@never_cache
#@department_login_required
def job_portal_mis_dashboard(request):
    # if request.user.is_authenticated:
    #     if not request.user.is_jobseeker and not request.user.is_recruiter and not request.user.is_agency_recruiter: 
    if ( request.POST.get("timestamp", "")):

        timestamp = request.POST.get("timestamp")
        date1 = request.POST.get('timestamp').split(' - ')
        if len(date1[0].split()) == 3:
            start_string = date1[0] + " 00:00"
        else:
            start_string = date1[0]
        start_date = datetime.strptime(start_string, "%b %d, %Y %H:%M")

        # Handle end date
        if len(date1[1].split()) == 3:
            end_string = date1[1] + " 00:00"
        else:
            end_string = date1[1]
        end_date = datetime.strptime(end_string, "%b %d, %Y %H:%M")
        start_date1 = start_date.strftime("%b %d, %Y")
        end_date1 = end_date.strftime("%b %d, %Y")
        print("start date:",start_date)
        print("end_date:",end_date)
        jobseeker_details = User.objects.filter(user_type = 'JS', date_joined__range = [start_date, end_date])
        jobseeker_count = jobseeker_details.count()
        jobseeker_male_count =  jobseeker_details.filter(Q(user_type = 'JS') & Q(gender = 'Male') | Q(gender = 'M')).count()
        jobseeker_female_count =  jobseeker_details.filter(Q(user_type = 'JS') & Q(gender = 'Female')| Q(gender = 'F')).count()
        jobseeker_other_count =  jobseeker_details.filter(Q(user_type = 'JS') & Q(gender = 'Others')).count()
        employer_count = User.objects.filter(user_type = 'RR', date_joined__range = [start_date, end_date]).count()
        jobpost_details = JobPost.objects.filter(published_on__range = [start_date, end_date])
        jobpost_count = jobpost_details.count()
        open_count = jobpost_details.filter(mode_of_recruitment = 'Open(Self Management)').count()
        jobfair_count = jobpost_details.filter(mode_of_recruitment = 'Career Center/Employment Exchange', job_post_options = 'JobFair').count()
        sponsoring_count = jobpost_details.filter(mode_of_recruitment = 'Career Center/Employment Exchange', job_post_options = 'Sponsoring').count()
        applied_jobs = AppliedJobs.objects.filter(job_post__published_on__range = [start_date, end_date])
        shortlist_details = applied_jobs.filter(Q(status = 'Shortlisted') |Q(status = 'Selected')).count()
        shortlist_open_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Open(Self Management)') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        shortlist_sponsor_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'JobFair') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        shortlist_rd_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'Sponsoring') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        placement_details = applied_jobs.filter(Q(status = 'Selected')).count()
        placement_open_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Open(Self Management)') & Q(status = 'Selected')).count()
        placement_sponsor_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'JobFair') & Q(status = 'Selected')).count()
        placement_rd_count = applied_jobs.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'Sponsoring') & Q(status = 'Selected')).count()

    else:
        start_date1 = ''
        end_date1 = ''
        jobseeker_details = User.objects.filter(user_type = 'JS')
        jobseeker_count = jobseeker_details.count()
        jobseeker_male_count =  User.objects.filter(Q(user_type = 'JS') & Q(gender = 'Male') | Q(gender = 'M')).count()
        jobseeker_female_count =  User.objects.filter(Q(user_type = 'JS') & Q(gender = 'Female')| Q(gender = 'F')).count()
        jobseeker_other_count =  User.objects.filter(Q(user_type = 'JS') & Q(gender = 'Others')).count()
        employer_count = User.objects.filter(user_type = 'RR').count()
        jobpost_details = JobPost.objects.all()
        jobpost_count = jobpost_details.count()
        open_count = jobpost_details.filter(mode_of_recruitment = 'Open(Self Management)').count()
        jobfair_count = jobpost_details.filter(mode_of_recruitment = 'Career Center/Employment Exchange', job_post_options = 'JobFair').count()
        sponsoring_count = jobpost_details.filter(mode_of_recruitment = 'Career Center/Employment Exchange', job_post_options = 'Sponsoring').count()
        shortlist_details = AppliedJobs.objects.filter(Q(status = 'Shortlisted') |Q(status = 'Selected')).count()
        shortlist_open_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Open(Self Management)') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        shortlist_sponsor_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'JobFair') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        shortlist_rd_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'Sponsoring') & (Q(status = 'Shortlisted') |Q(status = 'Selected'))).count()
        placement_details = AppliedJobs.objects.filter(Q(status = 'Selected')).count()
        placement_open_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Open(Self Management)') & Q(status = 'Selected')).count()
        placement_sponsor_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'JobFair') & Q(status = 'Selected')).count()
        placement_rd_count = AppliedJobs.objects.filter(Q(job_post__mode_of_recruitment = 'Career Center/Employment Exchange') & Q(job_post__job_post_options = 'Sponsoring') & Q(status = 'Selected')).count()

    # Get the third-highest score
    top_score_details = Employment_Exchange_Performance.objects.order_by('-score')[:3]
    # Get the top three scores and ties
    
    top_dict = {}
    for details in top_score_details:
        top_dict[details.employment_exchange]={}
        top_dict[details.employment_exchange]['score']=details.score
        
    # Get the third-lowest score
    bottom_score_details = Employment_Exchange_Performance.objects.order_by('score')[:3]
    
    bottom_dict={}
    
    for details in bottom_score_details:
        bottom_dict[details.employment_exchange]={}
        bottom_dict[details.employment_exchange]['score']=details.score
    emps_exchanges= New_Employment_Exchange.objects.all()
    formatted_date = datetime.today().strftime("%a %b %d %Y")
    return render(request, 'department/job_portal_mis_dashboard.html',{ "formatted_end_date": formatted_date,'emps_exchanges':emps_exchanges,
                                                                    'jobseeker_count' : jobseeker_count,
                                                                      'jobseeker_other_count' : jobseeker_other_count,
                                                                      'jobseeker_female_count' : jobseeker_female_count, 
                                                                      'jobseeker_male_count' : jobseeker_male_count,
                                                                      'employer_count' : employer_count,
                                                                      'jobpost_count' : jobpost_count,
                                                                      'open_count' : open_count,
                                                                      'jobfair_count' : jobfair_count,
                                                                      'sponsoring_count' : sponsoring_count,
                                                                      'shortlist_details' : shortlist_details,
                                                                      'shortlist_open_count': shortlist_open_count,
                                                                      'shortlist_sponsor_count': shortlist_sponsor_count,
                                                                      'shortlist_rd_count': shortlist_rd_count,
                                                                      'placement_open_count': placement_open_count,
                                                                      'placement_sponsor_count': placement_sponsor_count,
                                                                      'placement_rd_count': placement_rd_count,
                                                                      'placement_details' : placement_details,
                                                                      'top_dict': top_dict,
                                                                      'bottom_dict': bottom_dict, 
                                                                      'start_date1': start_date1,
                                                                      'end_date1': end_date1})

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
            
            l.append(D)
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

def view_cc(request,user_id): 
    print("user id:",user_id)
    counsellor = CounsellorDetails.objects.filter(user_id=user_id).first()
    documents = CounsellorDoc.objects.filter(user_id=user_id)
    
    # print("documents:",documents.user_id)
    for document in documents:
        print("documents:==",document.file_name)
    return render(request, 'department/view_cc.html', {
            "counsellor": counsellor,  # Pass existing data to pre-fill the form
            "documents": documents, 
            "MEDIA_URL": settings.MEDIA_URL             
        }) 

def verified_counselor_list(request):
    if request.method == "POST":
        try:
            unqid = request.POST.get('record_id')
            print("Inside TRY Function-----------------")
            counsellor = CounsellorDetails.objects.filter(user_id=unqid).first()
            counsellor.status = 'Approved'
            counsellor.save()
            
            return redirect("department:pending_cc")
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    counsellor = CounsellorDetails.objects.filter(form_status='Yes', status='Approved')
    return render(request, 'department/verified_counselor_list.html',{'counsellor':counsellor})

def reject_counselor_list(request):
    if request.method == "POST":
        try:
            unqid = request.POST.get('record_id')
            print("Inside TRY Function-----------------")
            counsellor = CounsellorDetails.objects.filter(user_id=unqid).first()
            counsellor.status = 'Rejected'
            counsellor.save()
            
            return redirect("department:pending_counselor_requests")
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    counsellor = CounsellorDetails.objects.filter(form_status='Yes', status = 'Rejected')
    return render(request, 'department/reject_counselor_list.html',{'counsellor':counsellor})

def revert_cc(request):
    if request.method == "POST":
        try:
            unqid = request.POST.get('record_id')
            print("Inside TRY Function-----------------")
            counsellor = CounsellorDetails.objects.filter(user_id=unqid).first()
            counsellor.form_status = 'No'
            counsellor.status = 'Pending'
            counsellor.save()
            
            
            return redirect("department:pending_counselor_requests")
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    counsellor = CounsellorDetails.objects.filter(form_status='Yes')
    return render(request,"department/pending_cc.html", {'counsellor':counsellor})

def pending_college_requests(request):
    if request.method == "POST":
        print("Enter post=======================")
        counsellor_id = request.POST.get('counsellor')
        college_id = request.POST.get('college_id')
        institution_request_table = institution_request.objects.filter(id=college_id).first()
        institution_request_table.assigned_counsellor = counsellor_id
        institution_request_table.status = 'Approved'
        institution_request_table.save()
    instreq = institution_request.objects.filter(assigned_counsellor__isnull=True, status = 'Pending')
    counsellor = CounsellorDetails.objects.filter(form_status='Yes', status='Approved') 
    return render(request, 'department/pending_college_requests.html',{'instreq':instreq, 'counsellor':counsellor})

def assigned_college_requests(request):
    if request.method == "POST":
        college_id = request.POST.get('college_id')
        counsellor_id = request.POST.get('counsellor_id')
        institution = institution_request.objects.filter(id=college_id).first()
        if institution:
            institution.status = 'Completed'
            institution.save()

    instreq = institution_request.objects.filter(assigned_counsellor__isnull=False, status='Approved')
    counsellors = CounsellorDetails.objects.filter(form_status='Yes', status='Approved')

    # Create a mapping of id → name
    counsellor_map = {str(c.id): c.name for c in counsellors}

    # 🔁 Inject counsellor name into each item
    for i in instreq:
        i.counsellor_name = counsellor_map.get(str(i.assigned_counsellor), "Unknown")
    return render(request, 'department/assigned_college_requests.html', {'instreq': instreq})

@never_cache
#@department_login_required
def vocational_guidance_dashboard(request):
    # if request.user.is_authenticated:
    #     if not request.user.is_jobseeker and not request.user.is_recruiter and not request.user.is_agency_recruiter: 
    if ( request.POST.get("timestamp", "")):

        timestamp = request.POST.get("timestamp")
        date1 = timestamp.split(' - ')
        # Handle start date
        if len(date1[0].split()) == 3:
            start_string = date1[0] + " 00:00"
        else:
            start_string = date1[0]
        start_date = datetime.strptime(start_string, "%b %d, %Y %H:%M")

        # Handle end date
        if len(date1[1].split()) == 3:
            end_string = date1[1] + " 00:00"
        else:
            end_string = date1[1]
        end_date = datetime.strptime(end_string, "%b %d, %Y %H:%M")

        start_date1 = start_date.strftime("%b %d, %Y")
        end_date1 = end_date.strftime("%b %d, %Y")
        
        print('start_date:',start_date)
        print('end_date:',end_date)
        #----------------------------for CS
        
        
        cs_user_ids = User.objects.filter(user_type='CS',date_joined__range=[start_date, end_date]).values_list('id', flat=True)

        # Step 2: Use these IDs to filter CounsellorDetails
        cs_details = CounsellorDetails.objects.filter(form_status='Yes', status='Approved',user_id__in=cs_user_ids)
        
        filtered_cs_users = User.objects.filter(id__in=cs_details.values_list('user_id', flat=True))

        
        cs_count = cs_details.count()
        cs_male_count = filtered_cs_users.filter(gender = 'Male').count()
        cs_female_count = filtered_cs_users.filter(gender ='Female').count()
        cs_other_count =  filtered_cs_users.filter(gender ='Other').count()
        # cs_male_counts =  filtered_cs_users.filter(gender ='Male')
        # print("cs_male_counts-:",cs_male_counts)
        
        print("cs_male_count---------------:",cs_male_count)
        print("cs_female_count---------------:",cs_female_count)
        
        #-----for counsellor pending verify card...start-------- 
        
        
        active_cs = CounsellorDetails.objects.filter(status = 'Pending',form_status='Yes', user_id__in=cs_user_ids)
        active_cs_count = active_cs.count()
        for css in active_cs:
            print(css.user_id)
        print("active_cs---------------:",active_cs)
        active_cs_male = 0
        active_cs_female = 0
        active_cs_other = 0

        for cs in active_cs:
            try:
                user = User.objects.get(id=cs.user_id)
                print(user.gender)
                if user.gender.lower() == 'male':
                    active_cs_male += 1
                elif user.gender.lower() == 'other':
                    active_cs_others += 1
                else :
                    active_cs_female += 1
            except User.DoesNotExist:
                print(f"User with ID {cs.user_id} does not exist.")
                continue
            
        print("total active Counsellors:", active_cs_count)       
        print("Male active Counsellors:", active_cs_male)
        print("Female active Counsellors:", active_cs_female)
        
        #-----for counsellor pending verify card...end-------- 
        
        #-----for counsellor verification not started  card...start
        # counsellor_user_ids = CounsellorDetails.objects.values_list('user_id', flat=True)

        # # Step 3: Get the count of CS users whose IDs are not in CounsellorDetails
        # non_active_cs = cs_user_ids.exclude(id__in=counsellor_user_ids)
        # # non_active_cs = CounsellorDetails.objects.filter(user_id__in=cs_user_ids).exclude(status='Approved')
        # non_active_cs_count = non_active_cs.count()
        
        # non_active_cs_male = 0
        # non_active_cs_female = 0
        # non_active_cs_other = 0

        # for cs in non_active_cs:
        #     try:
        #         user = User.objects.get(id=cs.user_id)
        #         print(user.gender)
        #         if user.gender.lower() == 'male':
        #             non_active_cs_male += 1
        #         elif user.gender.lower() == 'other':
        #             non_active_cs_others += 1
        #         else :
        #             non_active_cs_female += 1
        #     except User.DoesNotExist:
        #         print(f"User with ID {cs.user_id} does not exist.")
        #         continue
        # Step 1: Get CS users within the date range
        cs_user_ids = User.objects.filter(user_type='CS',date_joined__range=[start_date, end_date]).values_list('id', flat=True)
        print("cs_user_ids:",cs_user_ids)
        # Step 2: Get all user_ids from CounsellorDetails
        counsellor_user_ids = CounsellorDetails.objects.values_list('user_id', flat=True)
        print("counsellor_user_ids:",counsellor_user_ids)
        # Step 3: Get CS users (in date range) who are NOT in CounsellorDetails
        non_active_cs = User.objects.filter(id__in=cs_user_ids).exclude(id__in=counsellor_user_ids)
        print("non_active_cs:",non_active_cs)
        non_active_cs_count = non_active_cs.count()

        # Gender counts
        non_active_cs_male = non_active_cs.filter(gender='Male').count()
        non_active_cs_female = non_active_cs.filter(gender='Female').count()
        non_active_cs_other = non_active_cs.filter(gender='Other').count()


        print("total nonactive Counsellors:", non_active_cs_count)       
        print("Male nonactive Counsellors:", non_active_cs_male)
        print("Female nonactive Counsellors:", non_active_cs_female)

        #-----for counsellor verification not started  card...end 
        
        online_total_session_data = Counselling_Booking.objects.filter(counselling_mode='Online',created_at__range = [start_date, end_date])
        online_total_session = Counselling_Booking.objects.filter(counselling_mode='Online',created_at__range = [start_date, end_date]).count()
        online_onetoone_session = online_total_session_data.filter(counselling_mode='Online',session_type='One-To-One').count()
        online_group_session = online_total_session_data.filter(counselling_mode='Online',session_type='Group').count()
        
        # online_total_session_co = Counselling_Booking.objects.filter(counselling_mode='Online',created_at__range = [start_date, end_date])
        # online_onetoone_session_co = online_total_session_co.filter(counselling_mode='Online',session_type='One-To-One')
        # online_group_session_co = online_total_session_co.filter(counselling_mode='Online',session_type='Group')
        
        # print("online_total__co:", online_total_session_co)
        # print("online_onetoone__co:", online_onetoone_session_co)
        # print("online_group__co:", online_group_session_co)
        # print("online_total_session:", online_total_session)       
        # print("online_onetoone_session:", online_onetoone_session)
        # print("online_group_session:", online_group_session)
        
        offline_total_session_data = Counselling_Booking.objects.filter(counselling_mode='Offline',created_at__range = [start_date, end_date])
        offline_total_session = Counselling_Booking.objects.filter(counselling_mode='Offline',created_at__range = [start_date, end_date]).count()
        offline_onetoone_session = offline_total_session_data.filter(counselling_mode='Offline',session_type='One-To-One').count()
        offline_group_session = offline_total_session_data.filter(counselling_mode='Offline',session_type='Group').count()
        
        print("offline_total_session:", offline_total_session)       
        print("offline_onetoone_session:", offline_onetoone_session)
        print("offline_group_session:", offline_group_session)
        
        top_counsellors = Counselling_Booking.objects.values('counsellor_id').annotate(total=Count('id')).order_by('-total')[:3]

        top_ids = [item['counsellor_id'] for item in top_counsellors]
        top_dict = {item['counsellor_id']: item['total'] for item in top_counsellors}

        top_counsellors = Counselling_Booking.objects.values('counsellor_id').annotate(total=Count('id')).order_by('-total')[:3]
        # print(top_counsellors)
        top_ids = [item['counsellor_id'] for item in top_counsellors]

        # Step 3: Map counsellor_id (reg_no) to session count
        top_dict = {item['counsellor_id']: item['total'] for item in top_counsellors}

        # Step 4: Get counsellor details by matching reg_no
        counsellor_details = CounsellorDetails.objects.filter(user_id__in=top_ids) #added user_id inplace of reg_no

        # Step 5: Create a final list with counsellor name and session count
        final_top_list = []
        for c in counsellor_details:
            final_top_list.append({
                'name': c.name,
                'total_bookings': top_dict.get(c.user_id, 0)#added user_id inplace of reg_no
            })
        # print(final_top_list)
        #-----------------for cs end-----
        
    else:
        start_date1 = ''
        end_date1 = ''
        cs_details = CounsellorDetails.objects.filter(form_status = 'Yes',status='Approved')
        cs_count = cs_details.count()
        # cs_male_count =  User.objects.filter(Q(user_type = 'CS') & Q(gender = 'Male')).count()
        # cs_female_count =  User.objects.filter(Q(user_type = 'CS') & Q(gender = 'Female')).count()
        # cs_other_count =  User.objects.filter(Q(user_type = 'CS') & Q(gender = 'Others')).count()
        
        cs_male_count = 0
        cs_female_count = 0
        cs_other_count = 0

        for cs in cs_details:
            try:
                user = User.objects.get(id=cs.user_id)
                print(user.gender)
                if user.gender.lower() == 'male':
                    cs_male_count += 1
                elif user.gender.lower() == 'other':
                    cs_other_count += 1
                else :
                    cs_female_count += 1
            except User.DoesNotExist:
                print(f"User with ID {cs.user_id} does not exist.")
                continue
        
        # print("cs_male_count---------------:",cs_male_count)
        # print("cs_female_count---------------:",cs_female_count) 
        
        #-----for counsellor pending verify card...start 
        active_cs = CounsellorDetails.objects.filter(status = 'Pending',form_status='Yes')
        active_cs_count = active_cs.count()
        # print("cs_male_count---------------:",cs_male_count)
        # print("cs_female_count---------------:",cs_female_count)
        
        # counsellor_counts = Counselling_Booking.objects.values('counsellor_id').annotate(total=Count('id'))
        # print('counsellor_counts:',counsellor_counts)
        
        
        
        # cs_male =  User.objects.filter(Q(user_type = 'CS') & Q(gender = 'Male'))
        # cs_female =  User.objects.filter(Q(user_type = 'CS') & Q(gender = 'Female'))
        # print("cs_male---------------:",cs_male)
        # print("cs_female---------------:",cs_female)
        
        active_cs_male = 0
        active_cs_female = 0
        active_cs_other = 0

        for cs in active_cs:
            try:
                user = User.objects.get(id=cs.user_id)
                # print(user.gender)
                if user.gender.lower() == 'male':
                    active_cs_male += 1
                elif user.gender.lower() == 'other':
                    active_cs_others += 1
                else :
                    active_cs_female += 1
            except User.DoesNotExist:
                print(f"User with ID {cs.user_id} does not exist.")
                continue

        # print("total active Counsellors:", active_cs_count)       
        # print("Male active Counsellors:", active_cs_male)
        # print("Female active Counsellors:", active_cs_female)
        
        #-----for counsellor pending verify card...end-------- 
        
        #-----for counsellor verification not started  card...start 
        cs_user_ids = User.objects.filter(user_type='CS').values_list('id', flat=True)
        
        
        counsellor_user_ids = CounsellorDetails.objects.values_list('user_id', flat=True)

        # Step 3: Get the count of CS users whose IDs are not in CounsellorDetails
        non_active_cs = cs_user_ids.exclude(id__in=counsellor_user_ids)
        non_active_cs_count = non_active_cs.count()
        
        non_active_cs_male = non_active_cs.filter(gender = 'Male').count()
        non_active_cs_female = non_active_cs.filter(gender ='Female').count()
        non_active_cs_other = non_active_cs.filter(gender ='Other').count()
        

        # print("total nonactive Counsellors:", non_active_cs_count)       
        # print("Male nonactive Counsellors:", non_active_cs_male)
        # print("Female nonactive Counsellors:", non_active_cs_female)
        
        #-----for counsellor verification not started  card...end----------
        
        online_total_session = Counselling_Booking.objects.filter(counselling_mode='Online').count()
        online_onetoone_session = Counselling_Booking.objects.filter(counselling_mode='Online',session_type='One-To-One').count()
        online_group_session = Counselling_Booking.objects.filter(counselling_mode='Online',session_type='Group').count()
        
        # print("online_total_session:", online_total_session)       
        # print("online_onetoone_session:", online_onetoone_session)
        # print("online_group_session:", online_group_session)
        
        offline_total_session = Counselling_Booking.objects.filter(counselling_mode='Offline').count()
        offline_onetoone_session = Counselling_Booking.objects.filter(counselling_mode='Offline',session_type='One-To-One').count()
        offline_group_session = Counselling_Booking.objects.filter(counselling_mode='Offline',session_type='Group').count()
        
        # print("offline_total_session:", offline_total_session)       
        # print("offline_onetoone_session:", offline_onetoone_session)
        # print("offline_group_session:", offline_group_session)
        
        # top_counsellors = Counselling_Booking.objects.values('counsellor_id').annotate(total=Count('id')).order_by('-total')[:3]
        
        
        # # Convert to dictionary {counsellor_id: count}
        # top_dict = {item['counsellor_id']: item['total'] for item in top_counsellors}
        
        top_counsellors = Counselling_Booking.objects.values('counsellor_id').annotate(total=Count('id')).order_by('-total')[:3]
        # print(top_counsellors)
        top_ids = [item['counsellor_id'] for item in top_counsellors]

        # Step 3: Map counsellor_id (reg_no) to session count
        top_dict = {item['counsellor_id']: item['total'] for item in top_counsellors}

        # Step 4: Get counsellor details by matching reg_no
        counsellor_details = CounsellorDetails.objects.filter(user_id__in=top_ids) #added user_id inplace of reg_no

        # Step 5: Create a final list with counsellor name and session count
        final_top_list = []
        for c in counsellor_details:
            final_top_list.append({
                'name': c.name,
                'total_bookings': top_dict.get(c.user_id, 0)
            })
        print(final_top_list)
        # Sort list by total_bookings in descending order
        final_top_list.sort(key=lambda x: x['total_bookings'], reverse=True)
        print(final_top_list)
    return render(request, 'department/vocational_guidance_dashboard.html', {'cs_count' : cs_count,
                                                                      'cs_other_count' : cs_other_count,
                                                                      'cs_female_count' : cs_female_count, 
                                                                      'cs_male_count' : cs_male_count,
                                                                      'active_cs_count' : active_cs_count,
                                                                      'active_cs_male' : active_cs_male,
                                                                      'active_cs_female' : active_cs_female,
                                                                      'active_cs_other' : active_cs_other,
                                                                      'non_active_cs_male' : non_active_cs_male,
                                                                      'non_active_cs_female' : non_active_cs_female,
                                                                      'non_active_cs_count' : non_active_cs_count,
                                                                      'non_active_cs_other' : non_active_cs_other,
                                                                      'online_onetoone_session' : online_onetoone_session,
                                                                      'online_total_session' : online_total_session,
                                                                      'online_group_session' : online_group_session,
                                                                      'offline_onetoone_session' : offline_onetoone_session,
                                                                      'offline_total_session' : offline_total_session,
                                                                      'offline_group_session': offline_group_session,
                                                                      'final_top_list': final_top_list, 
                                                                      'start_date1': start_date1,
                                                                      'end_date1': end_date1})
