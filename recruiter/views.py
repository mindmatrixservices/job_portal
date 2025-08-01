from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from peeldb.models import *
from datetime import datetime
from django.core.exceptions import ValidationError
def home(request):
    return render(request, 'recruiter/home.html')

def job_post(request):
    if request.method == 'POST':
        try:
            print("yes")
            # Process form data
            job_posted_for = request.POST.get('job_posted_for', 'Open')
            job_type = request.POST.get('job_type')
            title = request.POST.get('title')
            job_role = request.POST.get('job_role')
            
            # Initialize date variables as None
            age_as_on_date = None
            last_date = None
            
            # Process age_as_on_date
            age_date_str = request.POST.get('age_as_on_date')
            if age_date_str:
                try:
                    age_as_on_date = datetime.strptime(age_date_str, '%Y-%m-%d').date()
                except ValueError:
                    raise ValidationError("Age as on date must be in YYYY-MM-DD format")

            # Process last_date
            last_date_str = request.POST.get('last_date')
            if last_date_str:
                try:
                    last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
                except ValueError:
                    raise ValidationError("Last date must be in YYYY-MM-DD format")
            # Create job post instance
            job_post = JobPost(
                job_id=f"JOB-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                job_posted_for=job_posted_for,
                job_type=job_type,
                title=title,
                job_role=job_role,
                min_age=request.POST.get('min_age'),
                max_age=request.POST.get('max_age'),
                age_as_on_date=age_as_on_date,
                age_relaxation=request.POST.get('age_relaxation', 'No'),
                jobfor=request.POST.get('jobfor', 'Fresher'),
                min_exp=request.POST.get('min_exp', 0) or 0,
                max_exp=request.POST.get('max_exp', 0) or 0,
                company_name=request.POST.get('company_name'),
                company_address=request.POST.get('company_address'),
                company_description=request.POST.get('company_description'),
                company_links=request.POST.get('company_links'),
                vacancies_for=request.POST.get('vacancies_for', 'Private'),
                pay_scale=request.POST.get('pay_scale'),
                salary_type=request.POST.get('salary_type'),
                min_salary=request.POST.get('min_salary', 0) or 0,
                max_salary=request.POST.get('max_salary', 0) or 0,
                selection_process=request.POST.get('selection_process'),
                obligation_for_reservation_preference=request.POST.get('obligation_for_reservation_preference', 'No'),
                total_vacancy=request.POST.get('total_vacancy'),
                mode_of_application=request.POST.get('mode_of_application'),
                approchingOfficerName=request.POST.get('approchingOfficerName'),
                approchingOfficerEmail=request.POST.get('approchingOfficerEmail'),
                approchingOfficerDesignation=request.POST.get('approchingOfficerDesignation'),
                indentingOfficerName=request.POST.get('indentingOfficerName'),
                indentingOfficerEmail=request.POST.get('indentingOfficerEmail'),
                indentingOfficerDesignation=request.POST.get('indentingOfficerDesignation'),
                last_date=last_date,
                published_on = datetime.now().date(),
                published_message=request.POST.get('published_message', ''),
                status='Draft'
            )
            print(job_post.published_on)
           
            # Handle file uploads
            if 'scanned_seal_job_post' in request.FILES:
                job_post.scanned_seal_job_post = request.FILES['scanned_seal_job_post']
            if 'scanned_signature_job_post' in request.FILES:
                job_post.scanned_signature_job_post = request.FILES['scanned_signature_job_post']
            
            print("save hou hou")
            job_post.save()
            print("save hoi gol")
            # Process many-to-many relationships
            # Keywords
            keywords = request.POST.get('keywords', '').split(',')
            for keyword in keywords:
                if keyword.strip():
                    kw, created = Keyword.objects.get_or_create(name=keyword.strip())
                    job_post.keywords.add(kw)
            
            # Sector
            # sector_id = request.POST.get('sector')
            sector_id = request.POST.get('sector')
            if sector_id:
                sector = Sector.objects.get(id=sector_id)
                job_post.sector.add(sector)
            
            # Functional Area
            functional_area_id = request.POST.get('functional_area')
            if functional_area_id:
                functional_area = FunctionalArea.objects.get(id=functional_area_id)
                job_post.functional_area.add(functional_area)
            
            # Skills
            skills_id = request.POST.get('skills')
            if skills_id:
                skill = Skill.objects.get(id=skills_id)
                job_post.skills.add(skill)
            
            # Education Qualification
            education_qualification_id = request.POST.get('educationQualification')
            if education_qualification_id:
                qualification = Qualification.objects.get(id=education_qualification_id)
                job_post.edu_qualification.add(qualification)
            
            # Handle vacancies based on PWD status
            if job_post.obligation_for_reservation_preference == 'Yes':
                # PWD vacancies
                location_id = request.POST.get('location2')
                custom_location = request.POST.get('custom_location_for_other_location')
                
                if location_id == 'other_location' and custom_location:
                    # Create new city for custom location
                    city = City.objects.create(name=custom_location)
                else:
                    city = City.objects.get(id=location_id)
                
                # Create vacancy location
                vacancy_location = Vacancy_location.objects.create(
                    job=job_post,
                    city=city
                )
                
                # Create vacancies for each category
                categories = [
                    ('opencategory_total_vacancy1', 'Open Category/Unreserved'),
                    ('obc_total_vacancy', 'OBC'),
                    ('sc_total_vacancy1', 'SC'),
                    ('st_total_vacancy1', 'ST'),
                    ('ews_total_vacancy1', 'EWS'),
                    ('exservicemen_total_vacancy1', 'Ex-Servicemen'),
                    ('pwd_total_vacancy1', 'PwD'),
                    ('women_total_vacancy1', 'Women')
                ]
                
                for field_name, category in categories:
                    vacancy_count = request.POST.get(field_name, 0) or 0
                    if vacancy_count:
                        Vacancy.objects.create(
                            vacancy_location=vacancy_location,
                            vacancy=vacancy_count,
                            reservation_category=category
                        )
            else:
                # Non-PWD vacancies (multiple locations)
                locations = request.POST.getlist('location[]')
                posts = request.POST.getlist('locationPosts[]')
                
                for loc, post in zip(locations, posts):
                    if loc and post:
                        city, created = City.objects.get_or_create(name=loc)
                        vacancy_location = Vacancy_location.objects.create(
                            job=job_post,
                            city=city
                        )
                        Vacancy.objects.create(
                            vacancy_location=vacancy_location,
                            vacancy=post,
                            reservation_category='Open Category/Unreserved'
                        )
            
            messages.success(request, 'Job posted successfully!')
            return render(request, 'recruiter/job_post.html')  # Replace with your success URL
            
        except Exception as e:
            messages.error(request, f'Error submitting job post: {str(e)}')
            # Instead of redirecting, render the form with existing data and error
            return render_job_post_form(request, str(e))
        
    # GET request - render empty form
    return render_job_post_form(request)

def render_job_post_form(request, error_message=None):
    sectors = Sector.objects.all()
    functional_areas = FunctionalArea.objects.all()
    qualifications = Qualification.objects.filter(status='Active')
    skills = Skill.objects.all()
    cities = City.objects.all()
    
    context = {
        'sectors': sectors,
        'functional_areas': functional_areas,
        'qualifications': qualifications,
        'skills': skills,
        'cities': cities,
        'error_message': error_message,
    }
    return render(request, 'recruiter/job_post.html', context)

def job_post_success(request):
    return render(request, 'recruiter/job_post_success.html')

    # GET request - render empty form
    sectors = Sector.objects.all()
    functional_areas = FunctionalArea.objects.all()
    qualifications = Qualification.objects.filter(status='Active')
    skills = Skill.objects.all()
    cities = City.objects.all()

    context = {
        'sectors': sectors,
        'functional_areas': functional_areas,
        'qualifications': qualifications,
        'skills': skills,
        'cities': cities,
    }

    return render(request, 'recruiter/job_post.html', context)


def profile(request):
    return render(request, 'recruiter/profile.html')

def er1(request):
    return render(request, 'recruiter/er1.html')

def er2(request):
    return render(request, 'recruiter/er2.html')
def er1_view(request):
    return render(request, 'recruiter/er1_view.html')

def er2_view(request):
    return render(request, 'recruiter/er2_view.html')


def delete_job_post(request, job_id):
    if request.method == 'GET':  # Or 'POST' if you prefer
        try:
            job_post = JobPost.objects.get(job_id=job_id)
            
            
            job_post.delete()
            return JsonResponse({'success': True})
        except JobPost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Job post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)





#----------------------------------EMI MODULE------------------------------------------------------------------




def check_quarter(request):
    current_year = datetime.now().year
    today = now().date()
    print("Check quarter Done")
    return render(request,"recruiter/new_check_quarter.html",{"today" : today})


# @login_required


def er1form_save(request):
    if request.method == "GET":
        # Get the currently authenticated user
        user = request.user
        
        # Access the employment_exchange_name
        employment_exchange_name = user.employment_exchange_name
        print(f"Employment Exchange Name: {employment_exchange_name}")
        
        current_year = datetime.now().year
        quarter = request.GET.get("quarter")
        
        # Parse the selected quarter to extract the end date
        quarter_end_dates = {
            "31st March": date(current_year, 3, 31),
            "30th June": date(current_year, 6, 30),
            "30th September": date(current_year, 9, 30),
            "31st December": date(current_year, 12, 31) 
        }
        
        print(f"Selected quarter: '{quarter}'")
        selected_quarter_end_date = quarter_end_dates.get(quarter)
        print(f"Selected quarter end date: '{selected_quarter_end_date}'")

        # Ensure selected_quarter_end_date is not None
        if selected_quarter_end_date is None:
            messages.error(request, "Invalid quarter selected.")
            print("Error Redirect")
            return redirect("/recruiter/new_check_quarter")

        # Adjust current_year if "31st December" is selected
        if quarter == "31st December":
            current_year -= 1

        # Calculate the allowed submission period (one month after the end of the selected quarter)
        allowed_submission_start_date = selected_quarter_end_date + timedelta(days=1)
        allowed_submission_end_date = allowed_submission_start_date + timedelta(days=30)

        # For testing, use a manual date
        # today = datetime.strptime("2025-04-15", "%Y-%m-%d").date()
        today = datetime.now().date()
        # Check if today's date is within the allowed submission period
        if allowed_submission_start_date <= today <= allowed_submission_end_date:
            return render(request, "recruiter/er1form.html", {"quarter": quarter, "current_year": current_year, 'employment_exchange_name':employment_exchange_name})
        else:
            django_messages.error(request, "You can only submit the form within 30 days after the end of the selected quarter.")
            print("Quarter not allowed issue")
            return redirect("/recruiter/check_quarter")
    else:
        
        print("ENTERED IN ELSE")
        emp_name = request.POST.get("emp_name")
        select_quarter = request.POST.get("selected_quarter")
        emp_address = request.POST.get("emp_address")
        emp_bus_activity = request.POST.get("emp_bus_activity")
        flexRadioDefault = request.POST.get("flexRadioDefault")
        men_previous_quarter = request.POST.get("men_previous_quarter")
        men_current_quarter = request.POST.get("men_current_quarter")
        women_previous_quarter = request.POST.get("women_previous_quarter")
        women_current_quarter = request.POST.get("women_current_quarter")
        total_previous_quarter = request.POST.get("total_previous_quarter")
        total_current_quarter = request.POST.get("total_current_quarter")
        emp_reason = request.POST.get("emp_reason")
        # Vacancies
        vacancy_occured_purview = request.POST.get("vacancy_occured")
        vacancy_emp_exchange_purview = request.POST.get("vacancy_emp_exchange")
        vacancy_filled_purview = request.POST.get("vacancy_filled")
        vacancy_source_purview = request.POST.get("vacancy_source")
        vacancy_reason_for_not_notifying = request.POST.get("vacancy_reason_for_not_notifying")
        # Manpower shortage
        mp_shortage_occupation = request.POST.get("mp_shortage_occupation")
        mp_essential_qual = request.POST.get("mp_essential_qual")
        mp_essential_exp = request.POST.get("mp_essential_exp")
        mp_exp_not = request.POST.get("mp_exp_not")
        dif_occupations  = request.POST.get("dif_occupations")
        signature_file = request.FILES.get('signature')
        print("temp sign file:",signature_file)
        if signature_file:
            # Generate unique filename
            unique_filename = unique_image_name_generate(signature_file)
            
            # Save the file in the 'signatures/' directory
            upload_path = os.path.join(settings.MEDIA_ROOT, 'signatures', unique_filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            # Write the file to the directory
            with open(upload_path, 'wb+') as destination:
                for chunk in signature_file.chunks():
                    destination.write(chunk)

            # Now assign the path to the model
            signature_upload_path = os.path.join('signatures', unique_filename)
        else:
            signature_upload_path = None
        print(signature_file)
        latest_instance = ER1_report.objects.order_by('-serial_no').first()
        if latest_instance:
            last_serial_no = latest_instance.serial_no
            # Extract the serial number part and convert it to an integer
            serial_number = int(last_serial_no.split('/')[-3])
        else:
            # If no previous instance exists, start with 1
            serial_number = 0

            # Increment the serial number
        new_serial_number = serial_number + 1

            # Get the current year
        current_year = datetime.now().year

            # Construct the new serial number
        new_serial_no = f"AS/GHY/PVTACT/ES01/{new_serial_number:04d}/{select_quarter}/{current_year}"
        
        data = ER1_report(
            serial_no = new_serial_no,
            selected_quarter_user = select_quarter,
            emp_name=emp_name,
            emp_address=emp_address,
            emp_nature_of_bussiness=emp_bus_activity,
            office_type=flexRadioDefault,
            men_previous_quarter=men_previous_quarter,
            men_current_quarter=men_current_quarter,
            women_previous_quarter=women_previous_quarter,
            women_current_quarter=women_current_quarter,
            total_previous_quarter=total_previous_quarter,
            total_current_quarter=total_current_quarter,
            emp_reason=emp_reason,
            vacancy_occured_purview=vacancy_occured_purview,
            vacancy_emp_exchange_purview=vacancy_emp_exchange_purview,
            vacancy_filled_purview=vacancy_filled_purview,
            vacancy_source_purview=vacancy_source_purview,
            vacancy_reason_for_not_notifying=vacancy_reason_for_not_notifying,
            dif_occupations = dif_occupations,
            district = vacancy_emp_exchange_purview,
            signature_upload=signature_upload_path,
            date = datetime.now().date()
            
                )
        data.save()
        # Extract and save manpower shortage data
        manpower_shortage_occupations = request.POST.getlist("mp_shortage_occupation")
        manpower_essential_quals = request.POST.getlist("mp_essential_qual")
        manpower_essential_exps = request.POST.getlist("mp_essential_exp")
        
        print("manpower_shortage_occupations:", manpower_shortage_occupations)
        print("manpower_essential_quals:", manpower_essential_quals)
        print("manpower_essential_exps:", manpower_essential_exps)

        # Get the values of dynamically generated checkboxes
        manpower_exps_not = []
        for i in range(len(manpower_shortage_occupations)):
            checkbox_name = "manpower_exps_not_" + str(i)
            checkbox_value = request.POST.get(checkbox_name, "no")  # Default value "no" if checkbox not checked
            manpower_exps_not.append(checkbox_value)
        
        print("manpower_exps_not:", manpower_exps_not)
        
        # Convert the checkbox values to boolean
        manpower_exp_not_bool = [value == 'yes' for value in manpower_exps_not]
        
        print("manpower_exp_not_bool:", manpower_exp_not_bool)

        # Ensure all lists have the same length by padding with empty values if necessary
        max_length = max(len(manpower_shortage_occupations), len(manpower_essential_quals), len(manpower_essential_exps), len(manpower_exp_not_bool))
        
        print("max_length:", max_length)

        while len(manpower_shortage_occupations) < max_length:
            manpower_shortage_occupations.append('')
        
        while len(manpower_essential_quals) < max_length:
            manpower_essential_quals.append('')
        
        while len(manpower_essential_exps) < max_length:
            manpower_essential_exps.append('')
        
        while len(manpower_exp_not_bool) < max_length:
            manpower_exp_not_bool.append(False)
        
        print("Adjusted manpower_shortage_occupations:", manpower_shortage_occupations)
        print("Adjusted manpower_essential_quals:", manpower_essential_quals)
        print("Adjusted manpower_essential_exps:", manpower_essential_exps)
        print("Adjusted manpower_exp_not_bool:", manpower_exp_not_bool)
        
        latest_er1_report = ER1_report.objects.order_by('-serial_no').first()
        
        for i in range(max_length):
            print(f"Creating ManpowerShortage object {i}:")
            print("mp_shortage_occupation:", manpower_shortage_occupations[i])
            print("mp_essential_qual:", manpower_essential_quals[i])
            print("mp_essential_exp:", manpower_essential_exps[i])
            print("mp_exp_not:", manpower_exp_not_bool[i])

            mp_essential_exp = manpower_essential_exps[i]
    
            # Check if mp_essential_exp is blank and set mp_exp_not accordingly
            mp_exp_not = not mp_essential_exp.strip()  # Set mp_exp_not to True if mp_essential_exp is blank

            ManpowerShortage.objects.create(
                er1_report=latest_er1_report,
                mp_shortage_occupation=manpower_shortage_occupations[i],
                mp_essential_qual=manpower_essential_quals[i],
                mp_essential_exp=mp_essential_exp,
                mp_exp_not=mp_exp_not,
            )
        response = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>Form Submission</title>
            <meta http-equiv="refresh" content="5;url=/recruiter/index2" />
            </head>
            <body>
            <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <p style="font-weight: bold;">Form is submitted. The reference Number is {}</p>
            </div>
            <a href="recruiter/profile" style="margin-left: 20%;"><button type="button" class="btn btn-danger">Back</button></a>

            </body>
            </html>
            """.format(new_serial_no)
        return HttpResponse(response)




def view_er1report(request):
    if request.method =="GET":
        employment_exchange = request.user.employment_exchange_name
        print("RECRUITER",employment_exchange)
       
        filter_data = ER1_report.objects.filter(district=employment_exchange)
        print(filter_data)
        return render(request,"recruiter/new_view_er1report.html",{'filter_data':filter_data})



def er2form_save(request):
    if request.method == "GET":
        return render(request, "recruiter/er2form.html")
    else:
        employer_name = request.POST.get("name")
        employer_address = request.POST.get("employer_address")  # This should be changed to address if it is the address field
        nat_buss = request.POST.get("nature_of_business")  # This should be the correct name for nature of business field
        total_employees = request.POST.get("total_employees")  # This should be the correct name for total employees field
        districts = request.user.employment_exchange_name
        print("EMP EXCHANGE : ",districts)
        total_mens = request.POST.get("hidden_total_men")
        total_womens = request.POST.get("hidden_total_women")
        grand_totals = request.POST.get("hidden_grand_total")
        total_vacanciess = request.POST.get("hidden_total_vacancies")
        signature_file = request.FILES.get('signature')
        print("temp sign file:",signature_file)
        if signature_file:
            # Generate unique filename
            unique_filename = unique_image_name_generate(signature_file)
            
            # Save the file in the 'signatures/' directory
            upload_path = os.path.join(settings.MEDIA_ROOT, 'signatures', unique_filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            # Write the file to the directory
            with open(upload_path, 'wb+') as destination:
                for chunk in signature_file.chunks():
                    destination.write(chunk)

            # Now assign the path to the model
            signature_upload_path = os.path.join('signatures', unique_filename)
        else:
            signature_upload_path = None
        officer_ent_date = request.POST.get('Officer_date')
        print(officer_ent_date)

        # Create the main ER2 report entry
        report = ER2Report.objects.create(
            employer_name=employer_name,
            employer_address=employer_address,
            nature_of_business=nat_buss,
            total_employees=total_employees,
            district=districts,
            total_men=total_mens,
            total_women=total_womens,
            grand_total=grand_totals,
            total_approx_vacancies=total_vacanciess,
            signature_upload=signature_upload_path,
            officer_entered_date=officer_ent_date,
        )

        # Get the occupations data
        occupations = request.POST.getlist("occupation[]")
        men = request.POST.getlist("men[]")
        women = request.POST.getlist("women[]")
        totals = request.POST.getlist("total[]")
        approx_vacancies = request.POST.getlist("approx_vac[]")

        # Save each occupation entry
        for i in range(len(occupations)):
            ER2_table.objects.create(
                report=report,
                occupation=occupations[i],
                men=men[i],
                women=women[i],
                total=totals[i],
                approx_vacancies=approx_vacancies[i],
            )

        # Redirect to the success page
        return redirect('/recruiter/success/')



def new_er1_report_detail(request, increment_number):
    employment_exchange = request.user.employment_exchange_name
    print("RECRUITER",employment_exchange)
    district = employment_exchange
    employer_view = ER1_report.objects.filter(district=district, serial_no__contains=increment_number).first()
    
    if employer_view and employer_view.signature_upload:
        print(employer_view.signature_upload.url)  # Debug print to check the URL
    
    manpower_shortages = ManpowerShortage.objects.filter(er1_report=employer_view) if employer_view else []

    return render(request, "recruiter/new_er1_detail.html", {
        'employer_view': employer_view,
        'employer_view_mp': employer_view,
        'manpower_shortages': manpower_shortages
    })

    


def print_page(request, increment_number):
    print(increment_number)
    employment_exchange = request.user.employment_exchange_name
    print("RECRUITER",employment_exchange)
    employer_view = ER1_report.objects.filter(district=employment_exchange,  serial_no__contains=increment_number).first()
    manpower_shortages = ManpowerShortage.objects.filter(er1_report=employer_view) if employer_view else []
    
    return render(request, "recruiter/print_template.html", {'employer_view': employer_view,'manpower_shortages': manpower_shortages})


def success(request):    
    return render(request, "recruiter/success.html")



def view_er2report(request):
    if request.method =="GET":
        employment_exchange = request.user.employment_exchange_name
        print("RECRUITER",employment_exchange)
        filter_data = ER2Report.objects.filter(district=employment_exchange)
        print(filter_data)
        return render(request,"recruiter/new_view_er2report.html",{'filter_data':filter_data})


def new_er2_report_detail(request,id):
    employment_exchange = request.user.employment_exchange_name
    print("RECRUITER",employment_exchange)
    employer_view = ER2Report.objects.filter(district=employment_exchange,id = id).first()
    print(employer_view)
    er2_table = ER2_table.objects.filter(report=employer_view) if employer_view else []

    return render(request, "recruiter/new_er2_detail.html", {'employer_view': employer_view, 'er2_table': er2_table})



def print_er2_page(request, id):
    print(id)
    employment_exchange = request.user.employment_exchange_name
    print("RECRUITER",employment_exchange)
    employer_view = ER2Report.objects.filter(district=employment_exchange, id = id).first()
    er2_table = ER2_table.objects.filter(report=employer_view) if employer_view else []
    
    return render(request, "recruiter/print_er2_template.html", {'employer_view': employer_view,'er2_table': er2_table})

