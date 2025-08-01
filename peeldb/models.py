import hashlib
import json
from datetime import datetime, date
import re
import uuid
import arrow
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
# from oauth2client.contrib.django_util.models import CredentialsField
from django.conf import settings
# from twython.api import Twython


from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q, Count, F, JSONField, Sum,Max
from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

#from django_blog_it.django_blog_it.models import Post
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from month.models import MonthField

from datetime import datetime, timedelta

# from microurl import google_mini
import os

COMPANY_SIZE = (
    ('1-10', '1-10'),
    ('11-20', '11-20'),
    ('21-50', '21-50'),
    ('50-200', '50-200'),
    ('200+', '200+'),
)

STATUS = (
    ('Active', 'Active'),
    ('InActive', 'InActive'),
)

current_date = datetime.strptime(
    str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")


class New_Course(models.Model):
    name = models.CharField(unique=True, max_length=200)
    
class New_Subject(models.Model):
    name = models.CharField(unique=True, max_length=200)

class New_Highest_Educational_Level(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_Qualification(models.Model):
    name = models.CharField(unique=True, max_length=200)
    
class New_Current_Employment_Status(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_State(models.Model):
    name = models.CharField(unique=True, max_length=200)
    
class New_District(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_Subdivision(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_RevenueCircle(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_Employment_Exchange(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=300)
    
class New_Disability_Category(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=200)
    
class New_Additional_Disability_Type(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=500)
    
class New_Disability_Percentage(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(unique=True, max_length=500)

class New_Designation(models.Model):
    name = models.CharField(unique=True, max_length=500)
    
class New_Specialization(models.Model):
    name = models.CharField(unique=True, max_length=500)
    
class New_Religion(models.Model):
    name = models.CharField(unique=True, max_length=500)
    
class New_Medium(models.Model):
    name = models.CharField(unique=True, max_length=500)


class OTP_Verify(models.Model):
    mobile = models.BigIntegerField()
    otp = models.BigIntegerField()
    otp_created = models.DateField(auto_now_add=True)
    
class OTP_Verify_Email(models.Model):
    email = models.EmailField()
    otp = models.BigIntegerField()
    otp_created = models.DateField(auto_now_add=True)
    
class Pincode(models.Model):
    pincode = models.IntegerField(unique=True)
   
class Subjects(models.Model):
    name= models.CharField(unique=True, max_length=100)

class Police_Station(models.Model):
    name= models.CharField(unique=True, max_length=100)

class Employment_Exchange(models.Model):
    name= models.CharField(unique=True, max_length=100)
    abbreviation = models.CharField(max_length=30, blank = True, null = True)
    city_name = models.CharField(max_length=500, blank = True, null = True)

class Organisation_Type(models.Model):
    name= models.CharField(unique=True, max_length=50)
    abbreviation = models.CharField(max_length=30, blank = True, null = True)
    
class Employment_Exchange_Details(models.Model):
    police_station = models.CharField(max_length=100)
    emp_ex = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100)

class Caste(models.Model):
    name = models.CharField(unique=True, max_length=100)
    
class NIC_code_of_establishment(models.Model):
    sub_class = models.CharField(max_length=5)
    description = models.CharField(max_length=800)
    
class NCO_code_of_post(models.Model):
    nco_code = models.FloatField()
    occupation = models.CharField(max_length=800)
    
class Industry(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=10)
    slug = models.SlugField(max_length=500)
    meta_title = models.TextField(default='')
    meta_description = models.TextField(default='')
    page_content = models.TextField(default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Industry, self).save(*args, **kwargs)

    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug

    @property
    def get_job_url(self):
        if not self.slug:
            self.slug = slugify(self.name)
        job_url = '/' + str(self.slug) + '-industry-jobs/'
        return job_url

    def get_no_of_jobposts(self):
        return JobPost.objects.filter(industry__in=[self], status='Live')

    def get_no_of_all_jobposts(self):
        return JobPost.objects.filter(industry__in=[self])


class Keyword(models.Model):
    name = models.CharField(max_length=2000)



USER_TYPE = (
    ('JS', 'Job Seeker'),
    ('RR', 'Recruiter'),
    ('RA', 'Recruiter Admin'),
    ('AA', 'Agency Admin'),   #Consultancy
    ('AR', 'Agency Recruiter'),
    ('DEE', 'DistrictEmploymentExchange'),
    ('D', 'Department'),
    ('Zonal', 'ZonalUser'),
    ('GUSER', 'GuestUser'),
)

# GENDER_TYPES = (
#     ('F', 'Female'),
#     ('M', 'Male'),
# )

STATUS_TYPES = (
    ('Enabled', 'Enabled'),
    ('Disabled', 'Disabled'),
)

DEGREE_TYPES = (
    ('FullTime', 'FullTime'),
    ('PartTime', 'PartTime'),
)

COMPANY_TYPES = (
    ('Consultant', 'consultant'),
    ('Company', 'company'),
)


def img_url(self, filename):
    hash_ = hashlib.md5()
    hash_.update(
        str(filename).encode('utf-8') + str(datetime.now()).encode('utf-8'))
    file_hash = hash_.hexdigest()

    if self.__class__.__name__ == "Company":
        # parsed_target_url = urlparse(self.website)
        # domain = str(parsed_target_url.netloc).split('.')[0]
        filename = self.slug + '.' + str(filename.split('.')[-1])
    else:
        filename = filename
    return "%s%s/%s" % (self.file_prepend, file_hash, filename)

def signature_file(self, filename):
    hash_ = hashlib.md5()
    hash_.update(
        str(filename).encode('utf-8') + str(datetime.now()).encode('utf-8'))
    file_hash = hash_.hexdigest()

    if self.__class__.__name__ == "Company":
        # parsed_target_url = urlparse(self.website)
        # domain = str(parsed_target_url.netloc).split('.')[0]
        filename = self.slug + '.' + str(filename.split('.')[-1])
    else:
        filename = filename
    return "%s%s/%s" % (self.file_prepend, file_hash, filename)

def scanned_seal(self, filename):
    hash_ = hashlib.md5()
    hash_.update(
        str(filename).encode('utf-8') + str(datetime.now()).encode('utf-8'))
    file_hash = hash_.hexdigest()

    if self.__class__.__name__ == "Company":
        # parsed_target_url = urlparse(self.website)
        # domain = str(parsed_target_url.netloc).split('.')[0]
        filename = self.slug + '.' + str(filename.split('.')[-1])
    else:
        filename = filename
    return "%s%s/%s" % (self.file_prepend, file_hash, filename)

class Type_of_Establishment(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=10)

class Qualification(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=10, default = 'Active')
    slug = models.SlugField(max_length=500, blank = True, null = True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Qualification, self).save(*args, **kwargs)

    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug

    def get_no_of_jobposts(self):
        return JobPost.objects.filter(edu_qualification__in=[self], status= 'Live')


class Country(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS_TYPES, max_length=10, default='Enabled')
    slug = models.SlugField(max_length=500, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    def get_no_of_jobposts(self):
        return JobPost.objects.filter(location__state__country=self, status='Live')


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    status = models.CharField(
        choices=STATUS_TYPES, max_length=10, default='Enabled')
    slug = models.SlugField(max_length=500, default='')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(State, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    def get_no_of_jobposts(self):
        return JobPost.objects.filter(location__in=City.objects.filter(state=self), status='Live')

    def get_state_cities(self):
        cities = self.state.annotate(
            num_posts=Count('locations')
        ).filter(status='Enabled').exclude(name=F('state__name')).order_by('-num_posts')
        return cities[:5]



class Ex_District(models.Model):
    name = models.CharField( max_length=200)
    code = models.IntegerField(null=True, blank=True)



class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    status = models.CharField(
        choices=STATUS_TYPES, max_length=10, default='Enabled')
    slug = models.SlugField(max_length=500, default='')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(District, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    

SKILL_TYPE = (
    ('IT', 'IT'),
    ('Aerospace & Aviation', 'Aerospace & Aviation'),
    ('Agriculture', 'Agriculture'),
    ('Apparel Made-Ups & Home Furnishing', 'Apparel Made-Ups & Home Furnishing'),
    ('Automotive', 'Automotive'),
    ('Beauty & Wellness', 'Beauty & Wellness'),
    ('Banking & Financial Services', 'Banking & Financial Services'),
    ('Capital Goods', 'Capital Goods'),
    ('Construction', 'Construction'),
    ('Domestic Workers', 'Domestic Workers'),
    ('Electronics', 'Electronics'),
    ('Food Industry', 'Food Industry'),
    ('Furniture & Fittings', 'Furniture & Fittings'),
    ('Gem & Jewellery', 'Gem & Jewellery'),
    ('Green Jobs', 'Green Jobs'),
    ('Handicrafts & Carpet', 'Handicrafts & Carpet'),
    ('Healthcare', 'Healthcare'),
    ('Infrastructure Equipment', 'Infrastructure Equipment'),
    ('Instrumentation Automation Surveillance & Communication', 'Instrumentation Automation Surveillance & Communication'),
    ('Iron & Steel', 'Iron & Steel'),
    ('Leather','Leather'),
    ('Life Sciences', 'Life Sciences'),
    ('Logistics', 'Logistics'),
    ('Management & Entrepreneurship', 'Management & Entrepreneurship'),
    ('Media & Entertainment', 'Media & Entertainment'),
    ('Mining', 'Mining'),
    ('Paints & Coatings', 'Paints & Coatings'),
    ('Plumbing', 'Plumbing'),
    ('Power', 'Power'),
    ('Retailers Association', 'Retailers Association'),
    ('Rubber ', 'Rubber '),
    ('Sports, Physical Education & Fitness', 'Sports, Physical Education & Fitness'),
    ('Strategic Manufacturing', 'Strategic Manufacturing'),
    ('Telecom', 'Telecom'),
    ('Textile', 'Textile'),
    ('Tourism & Hospitality', 'Tourism & Hospitality'),
    ('Persons with Disability', 'Persons with Disability'),
    ('Hydrocarbon', 'Hydrocarbon'),
)

class Area(models.Model):
    name = models.CharField(max_length=50)
    pincode = models.IntegerField()
    district_name = models.CharField(max_length=50)
    district=models.ForeignKey(District, on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=500)
    status = models.CharField(choices=STATUS, max_length=10)
    icon = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=500)
    meta_title = models.TextField(default='')
    meta_description = models.TextField(default='')
    page_content = models.TextField(default='')
    meta = JSONField(default=dict)
    skill_type = models.CharField(
        choices=SKILL_TYPE, max_length=100, default='IT')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Skill, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug

    @property
    def get_job_url(self):
        if not self.slug:
            self.slug = slugify(self.name)
        job_url = '/' + str(self.slug) + '-jobs/'
        return job_url

    def get_no_of_jobposts(self):
        return JobPost.objects.filter(skills__in=[self], status='Live')

    def get_no_of_jobposts_all(self):
        return JobPost.objects.filter(skills__in=[self])

    def get_no_of_subscriptions(self):
        return Subscriber.objects.filter(skill=self)

    def get_no_of_applicants(self):
        return User.objects.filter(skills__skill=self)

    def get_no_of_resume_applicants(self):
        return AgencyResume.objects.filter(skill=self)

    def get_meta_data(self):
        if self.meta:
            return json.dumps(self.meta)
        else:
            return ''


class FunctionalArea(models.Model):
    name = models.CharField(max_length=500, unique=True)
    status = models.CharField(choices=STATUS, max_length=10)
    slug = models.SlugField(max_length=500)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(FunctionalArea, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    def get_no_of_jobposts(self):
        return JobPost.objects.filter(functional_area__in=[self], status = 'Live')


class Language(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class UserLanguage(models.Model):
    # language = models.CharField(Language, on_delete=models.CASCADE)
    language = models.CharField(max_length=200)
    # ability = models.CharField(max_length=50)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    speak = models.BooleanField(default=False)
    proficiency = models.CharField(max_length=30, blank=True,null=True)
    
    


class Skill_Qualification(models.Model):
    certificate_id = models.CharField(max_length=800)
    sector = models.CharField( blank=True,null=True, max_length=800)
    course_job_role = models.CharField( blank=True,null=True, max_length=800)
    exam_diploma_certificate = models.CharField( blank=True,null=True, max_length=800)
    duration = models.CharField( max_length=30)

    
class Training_Courses(models.Model):
    admission_year = MonthField(blank=True,null=True)
    pass_year = MonthField(blank=True,null=True)
    duration = models.CharField(max_length=200)
    certificate_name = models.CharField(max_length=200)
    issued_by = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True,null=True)
    
    
    
        
   

class City(models.Model):
    name = models.CharField(max_length=500)
    state = models.ForeignKey(State, related_name='state', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_TYPES, max_length=10, default='Enabled')
    slug = models.SlugField(max_length=500, blank = True, null = True)
    internship_text = models.CharField(max_length=1000, blank = True, null = True)
    meta_title = models.TextField(blank = True, null = True)
    meta_description = models.TextField(blank = True, null = True)
    internship_meta_title = models.TextField(blank = True, null = True)
    internship_meta_description = models.TextField(blank = True, null = True)
    page_content = models.TextField(blank = True, null = True)
    internship_content = models.TextField(blank = True, null = True)
    meta = JSONField(default=dict, blank = True, null = True)
    parent_city = models.ForeignKey('self', related_name='child_cities', null=True, blank=True, on_delete=models.CASCADE)
    emp_exchange = models.CharField(max_length=1000, blank = True, null = True)
    abbreviation = models.CharField(max_length=30, blank = True, null = True)
    
    def display_location(self): #Added on 28 march 2025
        if self.parent_city and self.name != self.parent_city.name:
            return f"{self.name}, {self.parent_city.name}"
        return self.name


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    @property
    def get_job_url(self):
        if not self.slug:
            self.slug = slugify(self.name)
        job_url = '/jobs-in-' + str(self.slug) + '/'
        return job_url

    def get_no_of_jobposts(self):
        return JobPost.objects.filter(location__in=[self], status='Live')

    def get_no_of_all_jobposts(self):
        return JobPost.objects.filter(location__in=[self])

    def get_meta_data(self):
        if self.meta:
            return json.dumps(self.meta)
        else:
            return ''
FIRM_LEGAL_ENTITITIES = (
    ('Proprietorship', 'Proprietorship'),
    ('Partnership firm', 'Partnership firm'),
    ('Company', 'Company'),
    ('NGO', 'NGO'),
    ('Cooperative Society', 'Cooperative Society'),
    ('Startup firm ', 'Startup firm '),
    ('Trust', 'Trust')
)

class Company(models.Model):
    file_prepend = "company/logo/"
    name = models.CharField(max_length=5000)
    website = models.CharField(max_length=5000, null=True, blank=True)
    company_registration_no = models.CharField(max_length=30, null=True, blank=True)
    company_pan_no = models.CharField(max_length=20, null=True, blank=True)
    company_gst_no = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField()
    key_official_details = models.TextField(default='')
    profile_pic = models.FileField(
        max_length=1000, upload_to=img_url, null=True, blank=True)
    size = models.CharField(choices=COMPANY_SIZE, max_length=10, default='')
    level = models.IntegerField(null=True, blank=True)
    company_type = models.CharField(choices=COMPANY_TYPES, max_length=50, default='')
    firm_legal_entity = models.CharField(choices=FIRM_LEGAL_ENTITITIES, max_length=100, default=FIRM_LEGAL_ENTITITIES[2][0])
    firm_registration_number = models.CharField(max_length=250, default='')
    profile = models.TextField()
    phone_number = models.CharField(max_length=15)
    registered_date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=255, null=True)

    short_code = models.CharField(max_length=50, null=True)
    pan_or_gst_no = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=5000)
    meta_title = models.TextField(default='')
    meta_description = models.TextField(default='')
    campaign_icon = models.CharField(max_length=3000, null=True)
    created_from = models.CharField(max_length=200, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)
    
    @property
    def get_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return self.slug
    
    def is_company(self):
        if str(self.company_type) == 'Company':
            return True
        return False

    def is_agency(self):
        if str(self.company_type) == 'Consultant':
            return True
        return False

    def get_company_admin(self):
        return User.objects.filter(is_admin=True, company=self).first()

    def get_company_recruiters(self):
        return User.objects.filter(company=self)

    def get_company_jobposts(self):
        return JobPost.objects.filter(user__company=self)

    def get_jobposts(self):
        return JobPost.objects.filter(company=self, status='Live')

    def get_total_jobposts(self):
        return JobPost.objects.filter(company=self)

    def get_company_tickets(self):
        return Ticket.objects.filter(user__company=self)

    def get_company_menu(self):
        return Menu.objects.filter(company=self)

    def get_active_company_menu(self):
        return Menu.objects.filter(company=self, status=True).order_by('id')

    def get_live_jobposts(self):
        return JobPost.objects.filter(user__company=self, status='Live')

    def get_unique_recruiters(self):
        job_posts = list(set(list(JobPost.objects.filter(
            company=self, status='Live').values_list('user', flat=True))))
        users = User.objects.filter(id__in=job_posts)
        return users

    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return '/' + str(self.slug) + '-job-openings/'
    
    @property
    def get_logo_url(self):
        if self.profile_pic:
            return str(self.profile_pic)
        return settings.MEDIA_URL + os.path.sep + 'img/company_logo.png'

    def get_description(self):
        from bs4 import BeautifulSoup
        html = self.profile
        # create a new bs4 object from the html data loaded
        soup = BeautifulSoup(html)
        # remove all javascript and stylesheet code
        for script in soup(["script", "style"]):
            script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n<br>'.join(chunk for chunk in chunks if chunk)
        return text

    def get_website(self):
        site = self.website
        if site is not None and '//' in site:
            site = site.split("//")[1]
        return site
class EducationInstitue(models.Model):
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=2000, default='')
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class EmploymentHistory(models.Model):
    # SALARY_TYPE = (
    #     ('Monthly', 'Monthly'),
    #     ('Yearly', 'Yearly'),
    # )
    company = models.CharField(max_length=500)
    from_date = models.DateField()
    to_date = models.DateField(null = True, blank = True)
    # TODO: this need to be be sorted as standard designation at some point in future
    designation = models.CharField(max_length=500)
    # salary = models.CharField(max_length=100)
    salary = models.IntegerField( blank=True,null=True)
    # salary_type = models.CharField(
    #     choices=SALARY_TYPE, max_length=20, default='Yearly')
    nature_of_work = models.CharField(max_length = 200, null = True, blank = True)
    # industry_sector = models.CharField(max_length = 200, null = True, blank = True)
    # functional_role = models.CharField(max_length = 200, null = True, blank = True)
    current_job = models.BooleanField(default=False)
    notice_period = models.CharField(max_length = 100, null = True, blank = True)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
    

    # job_profile = models.TextField()



class Degree(models.Model):
    degree_name = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    degree_type = models.CharField(choices=DEGREE_TYPES, max_length=50)
    specialization = models.CharField(max_length=500)


class EducationDetails(models.Model):
    # institute = models.ForeignKey(EducationInstitue, on_delete=models.CASCADE)
    date_from = MonthField(null=True, blank=True)
    # to_date = models.DateField(null=True, blank=True)
    institute =models.CharField(max_length=300)
    date_of_passing = MonthField(null=True, blank=True)
    # degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=300, blank=True, null= True)
    medium = models.CharField(max_length=300, blank=True, null= True)
    degree = models.CharField(max_length=300)
    board = models.CharField(max_length=300, blank=True, null= True)
    course_type = models.CharField(max_length=300, blank=True, null= True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    score = models.FloatField(max_length=50, blank = True, null = True)
    specialization = models.CharField(max_length=200, blank = True, null = True)
    qualification = models.CharField(max_length=50, blank = True, null = True)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    stream = models.CharField(max_length=200, blank=True,null=True)

class Project(models.Model):
    name = models.CharField(max_length=500)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    description = models.TextField(max_length=2000, default='')
    location = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=500, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)


TechnicalSkill_STATUS = (
    ('Poor', 'Poor'),
    ('Average', 'Average'),
    ('Good', 'Good'),
    ('Expert', 'Expert'),
)


class TechnicalSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    last_used = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    proficiency = models.CharField(
        choices=TechnicalSkill_STATUS, max_length=100, null=True, blank=True)
    is_major = models.BooleanField(default=False)


MARTIAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed')
)

REGISTERED_FROM = (
    ('Email', 'Email'),
    ('Social', 'Social'),
    ('ResumePool', 'ResumePool'),
    ('Resume', 'Resume'),
    ('Careers', 'Careers'),
)

class Ex_Zone(models.Model):
    name= models.CharField(unique=True, max_length=100)


class JobPost_Approval_details(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    date_of_receipt_of_vacancies = models.DateTimeField(null=True, blank=True)
    establishment_code = models.CharField(max_length=800)
    nco_code = models.CharField(max_length=300)
    job_id = models.CharField(max_length=300)
    approval_date = models.DateTimeField(auto_now_add=True)
# class Department_User(AbstractBaseUser, PermissionsMixin):
#    first_name = models.CharField(max_length=100, blank=True)
#    last_name = models.CharField(max_length=100, blank=True, null=True)
#    email = models.EmailField(max_length=255, unique=True, db_index=True)
#    user_type = models.CharField(choices=USER_TYPE, max_length=10)
#    signature = models.CharField(max_length=2000, default='')
#    is_active = models.BooleanField(default=False)
#    last_password_reset_on = models.DateTimeField(auto_now_add=True)
#    gender = models.CharField(
#         choices=GENDER_TYPES, max_length=10, blank=True, null=True)
#    mobile = models.CharField(max_length=20, blank=True, null=True)
#    is_active = models.BooleanField(default=False)
#    date_joined = models.DateTimeField(default=timezone.now)
#    email_verified = models.BooleanField(default=False)  
#    last_mobile_code_verified_on = models.DateTimeField(auto_now_add=True)
#    mobile_verified = models.BooleanField(default=False)
#    email_notifications = models.BooleanField(default=True)
#    is_admin = models.BooleanField(default=False)  # agency created user
#    activation_code = models.CharField(max_length=100, null=True, blank=True)
#    registered_from = models.CharField(choices=REGISTERED_FROM, max_length=15, default='')

#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['username']
#    is_user_enabled = models.BooleanField(default=True)
#    objects = UserManager()

class Counselling_Booking(models.Model):
    counselling_mode = models.CharField(max_length=50)
    session_type = models.CharField(max_length=50)
    group_allotement = models.CharField(max_length=50,default = "Not Alloted") #When jobseeker apply for group counseling this will help to detect the group allotement status
    # category = models.CharField(max_length=100)
    counselling_date = models.DateField(null=True, blank=True)
    counselling_time = models.TimeField(null=True, blank=True)
    booking_status = models.CharField(max_length=100,default = "Pending") #to only track Pending/Approved/Cancelled
    counsellor_id = models.CharField(max_length=100,default=0)
    booking_flag = models.IntegerField(default=1) #when councelling is completed its set to 1 by councellor so that booking can be done
    jobseeker_id = models.CharField(max_length=50)
    booking_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    address = models.TextField(max_length=1000, blank=True, null=True)
    

class Counselling_cateory(models.Model):
    category_name = models.CharField(max_length = 500)
    
class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "user/img/"
    username = models.CharField(max_length=300)
    applicant_name = models.CharField(max_length=300, blank=True)
    recruiter_name = models.CharField(max_length=300, blank=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    guardians_name = models.CharField(blank=True, null=True, max_length=200)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        max_length=1000, upload_to='profile', null=True, blank=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=10)
    signature = models.CharField(max_length=2000, default='')
    is_active = models.BooleanField(default=False)
    is_feedback_submitted = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    # gender = models.CharField(
    #     choices=GENDER_TYPES, max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)
    permanent_address = models.TextField(
        max_length=1000, blank=True, null=True)
    nationality = models.TextField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    employment_exchange_registration_no = models.CharField(max_length=50)
    aadhaar_no = models.CharField(max_length=16, blank=True, null=True)
    alternate_mobile = models.BigIntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    highest_educational_level = models.CharField(max_length=200, blank=True, null=True)
    highest_examination_passed = models.CharField(max_length=800, blank=True, null=True)
    religion = models.CharField(max_length=200, blank=True, null=True)
    caste = models.CharField(max_length=50, blank=True, null=True)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    prominent_identification_mark = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    physically_handicapped = models.CharField(max_length=20, blank=True, null=True)
    disability_category = models.CharField(max_length=200, blank=True, null=True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    whether_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    height_in_cm = models.CharField(max_length=800, blank=True, null=True)
    weight_kgs = models.CharField(max_length=800, blank=True, null=True)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    current_employment_status = models.CharField(max_length=200, blank=True, null=True)
    fresher_experience_sts = models.CharField(max_length=50, blank=True, null=True)
    skill_or_unskill = models.CharField(max_length=50, blank=True, null=True)
    nco_code = models.CharField(max_length=12, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    # city = models.ForeignKey(City, null=True, blank=True, related_name='user_city', on_delete=models.CASCADE)
    # state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
    # district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    # country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    # current_pincode = models.ForeignKey(Pincode, null=True, related_name='current_pincode', on_delete=models.CASCADE)
    current_pincode = models.CharField(null=True, max_length=50)
    current_location = models.CharField(null=True, max_length=300)
    # police_station = models.ForeignKey(Police_Station, null=True, related_name='police_station', on_delete=models.CASCADE)
    location = models.CharField(null=True, max_length=300)
    pincode = models.CharField(null=True, max_length=12)
    police_station = models.CharField(null=True, max_length=100)
    post_office = models.CharField(null=True, max_length=100)
    sub_division = models.CharField(max_length=100, blank=True, null=True)
    revenue_circle= models.CharField(max_length=100, blank=True, null=True)
    residence = models.CharField(max_length=50, blank=True, null=True)
    last_password_reset_on = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=500)
    # TODO: this needs to be choice field
    marital_status = models.CharField(
        choices=MARTIAL_STATUS, max_length=50, blank=True, null=True)
    employment_history = models.ManyToManyField(EmploymentHistory)
    current_city = models.ForeignKey(
        City, blank=True, null=True, related_name='current_city', on_delete=models.CASCADE)
    # preferred_city = models.ManyToManyField(
    #     City, related_name='preferred_city')
    functional_area = models.ManyToManyField(FunctionalArea)
    job_role = models.CharField(max_length=500, default='')
    education = models.ManyToManyField(EducationDetails)
    project = models.ManyToManyField(Project)
    skills = models.ManyToManyField(TechnicalSkill)
    language = models.ManyToManyField(UserLanguage)
    current_salary = models.CharField(max_length=50, blank=True, null=True)
    expected_salary = models.CharField(max_length=500, blank=True, null=True)
    skill_qualification = models.ManyToManyField(Skill_Qualification)
    certification = models.ManyToManyField(Training_Courses)
    # prefered_industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.CASCADE)
    industry = models.ManyToManyField(
        Industry, related_name='recruiter_industries')
    technical_skills = models.ManyToManyField(
        Skill, related_name='recruiter_skill')
    dob = models.DateField(blank=True, null=True)
    profile_description = models.CharField(max_length=2000, default='')
    # this must be s3 file key
    resume = models.CharField(max_length=2000, default='')
    NOC = models.CharField(max_length=2000, default='')
    affidavit = models.CharField(max_length=2000, default='')
    relocation = models.BooleanField(default=False)
    notice_period = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    # month = models.CharField(max_length=50, default='')
    month = models.CharField(max_length=50, blank=True, null=True)
    show_email = models.BooleanField(default=False)
    resume_title = models.TextField(max_length=2000, blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)
    mobile_verification_code = models.CharField(max_length=50, default='')
    last_mobile_code_verified_on = models.DateTimeField(auto_now_add=True)
    mobile_verified = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    profile_updated = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)  # agency created user
    profile_completeness = models.CharField(max_length=500, default='')
    activation_code = models.CharField(max_length=100, null=True, blank=True)
    # is_register_through_mail = models.BooleanField(default=False)
    registered_from = models.CharField(choices=REGISTERED_FROM, max_length=15, default='')
    is_unsubscribe = models.BooleanField(default=False)
    is_bounce = models.BooleanField(default=False)
    unsubscribe_code = models.CharField(max_length=100, null=True, blank=True)
    # Other admins in agency other than agency created user
    agency_admin = models.BooleanField(default=False)
    referer = models.TextField(null=True, blank=True)
    unsubscribe_reason = models.TextField(default='')
    emp_exchange = models.ForeignKey(Employment_Exchange, null=True, blank=True, on_delete=models.CASCADE)
    employment_exchange_name = models.CharField(max_length=300, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    is_user_enabled = models.BooleanField(default=True)
    is_account_activation_request = models.BooleanField(default=False)
    account_activation_applied_on = models.DateTimeField(null=True, blank=True)
    is_employed = models.BooleanField(default=False)
    zone = models.ForeignKey(Ex_Zone, blank = True, null = True, on_delete=models.CASCADE)
    # skills_used = ArrayField(models.CharField(max_length=200, blank=True),size=20, null = True, blank = True)
    skills_used = models.TextField(null=True, blank=True)
    type_of_establishment = models.CharField(max_length=100, null=True, blank=True)
    establishment_code = models.ForeignKey(NIC_code_of_establishment, null=True, blank=True, on_delete=models.CASCADE)
    economic_activity_details = models.CharField(max_length=1000, null=True, blank=True)
    scanned_signature = models.ImageField(
        max_length=1000, upload_to='signature_file', null=True, blank=True)
    scanned_seal = models.ImageField(
        max_length=1000, upload_to='scanned_seal', null=True, blank=True)
    test_data = models.CharField(max_length=20, null=True, blank=True)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField(blank = True, null = True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    coun_booking = models.ManyToManyField(Counselling_Booking, blank=True)
    booking_flag = models.IntegerField(default=1)
    logo = models.CharField(max_length=800, null=True, blank=True)
    gst_certificate = models.CharField(max_length=800, null=True, blank=True)
    pan_card = models.CharField(max_length=800, null=True, blank=True)
    objects = UserManager()


    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_staff:
            return True

        # return _user_has_perm(self, perm, obj)
        else:
            try:
                user_perm = self.user_permissions.get(codename=perm)
            except ObjectDoesNotExist:
                user_perm = False
            if user_perm:
                return True
            else:
                return False

    class Meta:
        permissions = (
            ('blog_view', 'can view blog posts and categories'),
            ('blog_edit', 'can edit blog category and post'),
            ("support_view", "can view tickets"),
            ("support_edit", "can edit tickets"),
            ("activity_view",
             "can view recruiters, applicants, data, posts"),
            ("activity_edit", "can edit data"),
            ("jobposts_edit", "can manage jobposts"),
            ("jobposts_invoice_access", "can manage invoice"),
            ("jobposts_resume_profiles", "can manage resume profiles"),
        )

    # def get_full_name(self):
    #     full_name = '%s %s' % (
    #         self.first_name, self.last_name if self.last_name else '')
    #     return full_name.strip()
    
    def get_full_name(self):
        full_name = '%s ' % (self.username)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @property
    def generate_session_id(self):
        # Generate a UUID (version 4) as the session identifier
        return str(uuid.uuid4())
    
    def get_full_username(self):
        return " ".join(re.findall("[a-zA-Z]+", self.username))

    def get_first_name(self):
        name = (self.applicant_name).split(' ', 1)
        return name[0]

    @property
    def is_fb_connected(self):
        if self.facebook_user.all():
            return True
        else:
            return False

    @property
    def is_gp_connected(self):
        if self.google_user.all():
            return True
        else:
            return False

    @property
    def is_tw_connected(self):
        if self.twitter.all():
            return True
        else:
            return False

    @property
    def is_ln_connected(self):
        if self.linkedin.all():
            return True
        else:
            return False

    @property
    def is_gh_connected(self):
        if self.github.all():
            return True
        else:
            return False

    @property
    def is_recruiter(self):
        if str(self.user_type) == 'RR' or str(self.user_type) == 'RA' or str(self.user_type) == 'RA':
            return True
        else:
            return False

    @property
    def is_so_connected(self):
        if self.stackoverflow.all():
            return True
        else:
            return False

    @property
    def is_connect_social_networks(self):
        if self.facebook_user.all() and self.google_user.all() and self.linkedin.all() and self.twitter.all():
            return True
        else:
            return False

    

    @property
    def is_recruiter_active(self):
        if self.is_connect_social_networks and self.is_active and self.mobile_verified:
            return True
        else:
            return False

    def is_company_recruiter(self):
        if self.is_recruiter:
            return True
        else:
            return False

    @property
    def is_agency_recruiter(self):
        if self.company and str(self.company.company_type) == 'Consultant':
            return True
        return False

    @property
    def is_agency_admin(self):
        if self.company and self.agency_admin:
            return True
        return False

    @property
    def is_jobseeker(self):
        if str(self.user_type) == 'JS':
            return True
        return False

    @property
    def is_employment_exchange_officer(self):
        if str(self.user_type) == 'DEE':
            return True
        return False
    
    @property
    def is_department(self):
        if str(self.user_type) == 'D':
            return True
        return False
    
    @property
    def is_counsellor(self):
        if str(self.user_type) == 'CS':
            return True
        return False
    
    @property
    def is_zonal_officer(self):
        if str(self.user_type) == 'Zonal':
            return True
        return False

    @property
    def is_guest_user(self):
        if str(self.user_type) == 'GUSER':
            return True
        return False
    
    @property
    def profile_completion_percentage(self):
        complete = 0
        if self.year:
            complete += 10
        if self.mobile:
            complete += 20
        if self.is_active:
            complete += 10
        if self.user_type == 'JS':
            if len(self.resume):
                complete += 15
            if len(self.profile_description):
                complete += 5
            if self.education.all():
                complete += 10
            if self.project.all():
                complete += 10
            if self.skills.all():
                complete += 15
            if self.language.all():
                complete += 5
        else:
            if self.job_role:
                complete += 10
            if self.industry.all():
                complete += 10
            if self.profile_description:
                complete += 15
            if self.technical_skills.all():
                complete += 15
            if self.functional_area.all():
                complete += 10
        return complete
    
    def get_age(self):
        birth_date = self.dob
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
        
    def calculate_experience(self):
        employment_history_records = self.employment_history.all()

        total_experience = 0  # in days

        for record in employment_history_records:
            date_from = record.from_date
            date_to = record.to_date if record.to_date else date.today()

            experience_duration = (date_to - date_from).days
            total_experience += experience_duration
        
        # Convert total_experience from days to months
        total_experience_months = total_experience // 30  # assuming 30 days per month for simplicity

        return total_experience_months

        # # Convert total_experience from days to years
        # total_experience_years = total_experience / 365.25  # accounting for leap years

        # return self.format_experience(total_experience_years)
        
    def format_experience(self, total_experience_months):
        # Convert total_experience_months to years and months
        years = total_experience_months // 12
        months = total_experience_months % 12

        # Format the result
        if years == 1:
            year_str = "1 yr"
        else:
            year_str = f"{years} yrs"

        if months == 1:
            month_str = "1 month"
        else:
            month_str = f"{months} months"

        if years == 0:
            return month_str
        elif months == 0:
            return year_str
        else:
            return f"{year_str} {month_str}"
    
    # def format_experience(self, experience_years):
    #     # Extract integer part as years
    #     years = int(experience_years)

    #     # Extract decimal part and convert to months
    #     months_decimal = (experience_years - years) * 12
    #     months = int(months_decimal)

    #     # Round the remaining decimal places to get a whole number of days
    #     remaining_decimal = months_decimal - months
    #     remaining_days = round(remaining_decimal * 30)  # Assuming an average month has 30 days

    #     # Format the result
    #     if years == 1:
    #         year_str = "1 yr"
    #     else:
    #         year_str = f"{years} yrs"

    #     if months == 1:
    #         month_str = "1 month"
    #     else:
    #         month_str = f"{months} months"

    #     if years == 0:
    #         return f"{month_str} {remaining_days} days"
    #     elif months == 0:
    #         return year_str
    #     else:
    #         return f"{year_str} {month_str} {remaining_days} days"

    def get_jobposts_count(self):
        return len(JobPost.objects.filter(user=self))

    def get_total_job_post_views_count(self):
        job_posts = JobPost.objects.filter(user=self)
        total_views = 0
        for each in job_posts:
            total_views = each.fb_views + each.tw_views + \
                each.ln_views + each.other_views
        return total_views

    def get_total_jobposts(self):
        return JobPost.objects.filter(user=self)
    
    def get_total_jobposts_by_recruiter_count(self):
        return len(JobPost.objects.filter(user=self).exclude(status = 'Pending'))

    def get_shortlist_users_count(self):
        return len(AppliedJobs.objects.filter(Q(job_post__user=self) & (Q(status='Shortlisted') | Q(status= 'Selected'))))
    def get_placement_users_count(self):
        return len(AppliedJobs.objects.filter(Q(job_post__user=self) & Q(status= 'Selected')))

    def get_active_jobposts_count(self):
        return len(JobPost.objects.filter(user=self, status='Live'))

    def get_inactive_jobposts_count(self):
        return len(JobPost.objects.filter(Q(user=self) & Q(status='Disabled') | Q(status='Expired')))

    def get_applied_users(self):
        return AppliedJobs.objects.filter(job_post__user=self, status='Pending')

    def get_applied_jobs(self):
        ids = AppliedJobs.objects.filter(user=self).exclude(ip_address='', user_agent='').values_list('job_post', flat=True)
        applied_jobs = JobPost.objects.filter(job_id__in=ids)
        return applied_jobs

    def get_all_applied_jobs(self):
        return AppliedJobs.objects.filter(user=self).select_related('job_post')

    def get_facebook_id(self):
        return Facebook.objects.filter(user=self).first().facebook_id

    def get_facebook_url(self):
        return Facebook.objects.filter(user=self).first().facebook_url

    def get_google_url(self):
        return Google.objects.filter(user=self).first().google_url

    def get_user_emails(self):
        return UserEmail.objects.filter(user=self)

    def get_user_facebook_groups(self):
        return FacebookGroup.objects.filter(user=self)

    def get_user_facebook_friends(self):
        return FacebookFriend.objects.filter(user=self)

    def get_user_facebook_pages(self):
        return FacebookPage.objects.filter(user=self)

    def get_user_twitter_friends(self):
        return TwitterFriend.objects.filter(user=self)

    def get_user_twitter_followers(self):
        return TwitterFollower.objects.filter(user=self)

    def get_user_google_friends(self):
        return GoogleFirend.objects.filter(user=self)

    def get_open_tickets(self):
        return Ticket.objects.filter(Q(user=self) & Q(status='Open') | Q(status='Ongoing'))

    def get_closed_tickets(self):
        return Ticket.objects.filter(user=self, status='Closed')

    def get_major_skills(self):
        return self.skills.filter(is_major=True)

    def get_search_done(self):
        return SearchResult.objects.filter(user=self)

    def get_visited_jobs(self):
        return VisitedJobs.objects.filter(user=self)

    def get_stack_overflow_object(self):
        return self.stackoverflow.all().first()

    def get_facebook_object(self):
        return self.facebook_user.all().first()

    def get_twitter_url(self):
        screen_name = self.twitter.all().first().screen_name if self.twitter.all() else ''
        return 'http://twitter.com/' + str(screen_name) + '/'

    def get_google_object(self):
        return self.google_user.all().first()

    def get_github_object(self):
        return self.google_user.all().first()

    def get_linkedin_object(self):
        return self.linkedin.all().first()

    def get_subscribed_skills(self):
        user_emails = UserEmail.objects.filter(
            user=self).values_list('email', flat=True).distinct()
        return Skill.objects.filter(id__in=Subscriber.objects.filter(email__in=user_emails, is_verified=True).values_list('skill', flat=True)).distinct()

    def get_jobs_list(self):
        job_posts = JobPost.objects.filter(user=self)
        return job_posts

    def get_live_jobs_list(self):
        job_posts = JobPost.objects.filter(user=self, status='Live')
        return job_posts

    def get_tickets_list(self):
        tickets = Ticket.objects.filter(user=self)
        return tickets

    def get_assigned_jobs_list(self):
        job_posts = JobPost.objects.filter(
            agency_recruiters__in=[self]).exclude(status='Hired')
        return job_posts

    def get_resumes_uploaded(self):
        agency_resumes = AgencyResume.objects.filter(uploaded_by=self)
        return agency_resumes

    def get_selected_applicants(self):
        selected_applicants = AgencyApplicants.objects.filter(
            applicant__uploaded_by=self, created_on__date=current_date)
        return selected_applicants

    def get_hired_applicants(self):
        selected_applicants = AgencyApplicants.objects.filter(
            applicant__uploaded_by=self, created_on__date=current_date)
        return selected_applicants

    # def is_agency_admin(self, job_post_id):
    #     job_post = get_object_or_404(JobPost, id=job_post_id)

    #     if self.company == job_post.user.company and str(self.user_type) == 'AA' and self.is_admin:
    #         return True
    #     return False
    def get_user_login_only_once(self):
        last_login = arrow.get(self.last_login).format('YYYY-MM-DD HH:mm:ss')
        date_joined = arrow.get(self.date_joined).format('YYYY-MM-DD HH:mm:ss')
        if str(last_login) == str(date_joined):
            return True
        else:
            self.is_login = True
            self.save()
            return False

    def get_email_name(self):
        user = User.objects.filter(id=self.id)[0]
        if '@' in user.username:
            return user.username.split('@')[0]
        return user.username

    def get_user_alerts(self):
        return JobAlert.objects.filter(email=self.email)

    def related_walkin_jobs(self):
        skill_ids = self.skills.all().values_list('skill_id', flat=True)
        job_posts = JobPost.objects.filter(status='Live', job_type='walk-in')
        job_posts = job_posts.filter(
            skills__in=Skill.objects.filter(id__in=skill_ids))
        if len(job_posts) > 0:
            if len(job_posts) < 15:
                all_job_posts = JobPost.objects.filter(
                    status='Live').order_by('-published_on')
                rest = 15 - len(job_posts)
                job_posts = list(job_posts) + list(all_job_posts[:rest])
        else:
            job_posts = JobPost.objects.filter(
                status='Live', job_type='walk-in').order_by('-published_on')[:15]
        return job_posts

    def related_jobs(self):
        print("test --- Hi ----")
        ids = AppliedJobs.objects.filter(user=self).exclude(ip_address='', user_agent='').values_list('job_post', flat=True)
        user_skills = Skill.objects.filter(id__in=self.skills.all().values('skill'))
        related_jobs = JobPost.objects.filter(Q(status='Live') & Q(mode_of_recruitment='Open(Self Management)') & Q(skills__in=user_skills) | Q(location__in=[self.current_city])).exclude(job_id__in=ids)
        related_jobs = list(related_jobs) + list(JobPost.objects.filter(status='Live', mode_of_recruitment='Open(Self Management)').order_by('-published_on')[:15])
        jobs_test = JobPost.objects.filter(status='Live', mode_of_recruitment='Open(Self Management)')
        print("related_jobs:",related_jobs)
        print("related_jobs only 15:",related_jobs[:15])
        print("jobs_test:",jobs_test)
        return related_jobs[:15]

    def get_similar_recruiters(self):
        if self.agency_admin:
            return User.objects.filter(company=self.company)
        jobs = AgencyRecruiterJobposts.objects.filter(user=self).values('job_post')
        users = AgencyRecruiterJobposts.objects.filter(job_post__in=jobs).values('user')
        return User.objects.filter(id__in=users)


PRIORITY_TYPES = (
    ('Low', 'Low'),
    ('Normal', 'Normal'),
    ('High', 'High'),
)

TICKET_TYPES = (
    ('Bug', 'Bug'),
    ('Feature', 'Feature'),
    ('Enhancement', 'Enhancement'),
    ('Performance', 'Performance'),
    ('Design', 'Design'),
    ('Other', 'Other'),
)

STATUS = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
    ('Ongoing', 'Ongoing'),
)



class Attachment(models.Model):
    file_prepend = "ticket/attachments/"
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    attached_file = models.FileField(
        max_length=500, null=True, blank=True, upload_to=img_url)


class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='ticket', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    priority = models.CharField(choices=PRIORITY_TYPES, max_length=20)
    ticket_type = models.CharField(choices=TICKET_TYPES, max_length=20)
    status = models.CharField(choices=STATUS, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=1, blank=True)

    def get_ticket_comments(self):
        return Comment.objects.filter(ticket=self)

    def get_ticket_attachments(self):
        return self.attachments.filter()


class Comment(models.Model):
    comment = models.TextField(blank=True)
    commented_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name="ticket", on_delete=models.CASCADE)
    attachments = models.ManyToManyField(Attachment, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def get_comments_attatchments(self):
        return self.attachments.filter()


class UserEmail(models.Model):
    user = models.ForeignKey(User, related_name='user_email', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    is_primary = models.BooleanField(default=False)





class InterviewLocation(models.Model):
    venue_details = models.TextField()
    show_location = models.BooleanField(default=False)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)

    def get_map_coordinates_list(self):
        coordinates = []
        coordinates.append(str(self.id))
        coordinates.append(self.latitude)
        coordinates.append(self.longitude)
        return json.dumps(coordinates)

    def get_coordinates_list(self):
        coordinates = []
        coordinates.append(self.latitude)
        coordinates.append(self.longitude)
        return json.dumps(coordinates)


GOV_JOB_TYPE = (
    ('Central', 'Central'),
    ('State', 'State'),
)

JOB_TYPE = (
    ('full-time', 'Full Time'),
    ('internship', 'Internship'),
    ('walk-in', 'Walk-in'),
    ('government', 'Government'),
    ('fresher', 'Fresher'),
    ('part-time', 'Part Time'),
    ('contractual', 'Contractual'),
)

WALKIN_TYPE = (
    ('this_week', 'This Week'),
    ('this_month', 'This Month'),
    ('next_week', 'Next Week'),
    ('custom_range', 'Custom Range'),
)

AGENCY_JOB_TYPE = (
    ('Permanent', 'Permanent'),
    ('Contract', 'Contract'),
)

AGENCY_INVOICE_TYPE = (
    ('Recurring', 'Recurring'),
    ('Non_Recurring', 'Non Recurring'),
)

MONTHS = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
)


class AgencyCompanyBranch(models.Model):
    location = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    contact_details = models.TextField()
    is_major = models.BooleanField(default=False)


class AgencyCompanyCatogery(models.Model):
    name = models.CharField(max_length=1000)
    percantage = models.CharField(max_length=255, default='')


class AgencyContractDetails(models.Model):
    month = models.CharField(
        choices=MONTHS,  max_length=50)
    percantage = models.CharField(max_length=255, default='')


class AgencyCompany(models.Model):
    file_prepend = "agencycompany/logo/"
    name = models.CharField(max_length=255)
    website = models.URLField()
    decription = models.TextField()
    logo = models.FileField(upload_to=img_url, null=True, blank=True)
    branch_details = models.ManyToManyField(AgencyCompanyBranch)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    company_categories = models.ManyToManyField(
        AgencyCompanyCatogery, related_name='categories')
    contract_details = models.ManyToManyField(
        AgencyContractDetails, related_name='contract_details')


class JobPostManager(models.Manager):

    def get_queryset(self):
        return super(JobPostManager, self).get_queryset().order_by('-created_on')




class City_details(models.Model):
    city1= models.CharField(max_length=100)
    emp_ex1= models.CharField(max_length = 100)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    email_of_officer = models.EmailField()


class JobPost(models.Model):
    POST_STATUS = (
        ('Draft', 'Draft'),
        ('Expired', 'Expired'),
        ('Live', 'Live'),
        ('Disabled', 'Disabled'),
        ('Pending', 'Pending'),
        ('Published', 'Published'),
        ('Hired', 'Hired'),
        ('Process', 'Process'),
        ('Sponsored', 'Sponsored'),
        ('JobFair', 'JobFair'),
        ('RecruitmentDrive', 'RecruitmentDrive')
    )
    SALARY_TYPE = (
        ('Month', 'Month'),
        ('Year', 'Year'),
    )
    job_id =models.CharField(primary_key = True, max_length=30)
    user = models.ForeignKey(User, related_name='jobposts', on_delete=models.CASCADE)
    code = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=5000)
    location = models.ManyToManyField(City, related_name='locations')
    job_role = models.CharField(max_length=50, default='')
    total_vacancy = models.IntegerField()
    #vacancies = models.ManyToManyField(Vacancy, related_name='vacancies')
    industry = models.ManyToManyField(Industry)
   
    job_interview_location = models.ManyToManyField(InterviewLocation)
    country = models.ForeignKey(Country, null=True, related_name='job_country', on_delete=models.CASCADE)
    functional_area = models.ManyToManyField(FunctionalArea)
    keywords = models.ManyToManyField(Keyword)
    description = models.TextField()
    min_year = models.IntegerField(default=0)
    min_month = models.IntegerField(default=0)
    max_year = models.IntegerField(default=0)
    max_month = models.IntegerField(default=0)
    fresher = models.BooleanField(default=False)
    edu_qualification = models.ManyToManyField(Qualification)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    #job_pincode=models.ManyToManyField(Pincode, related_name='job_pincode')
    #pincode = models.ForeignKey(Pincode, null=True, blank=True, on_delete=models.CASCADE)
    # tech_qualification =

    # govt jobpost
    application_fee = models.IntegerField(default=0)
    govt_job_type = models.CharField(
        choices=GOV_JOB_TYPE,  max_length=50, default='Central')
    selection_process = models.TextField(default='')
    how_to_apply = models.TextField(default='')
    important_dates = models.TextField(default='')
    # validity
    govt_from_date = models.DateField(null=True, blank=True)
    govt_to_date = models.DateField(null=True, blank=True)
    govt_exam_date = models.DateField(null=True, blank=True)
    age_relaxation = models.TextField(default='')

    walkin_contactinfo = models.TextField(default='')
    walkin_show_contact_info = models.BooleanField(default=False)
    walkin_from_date = models.DateField(null=True, blank=True)
    walkin_to_date = models.DateField(null=True, blank=True)
    walkin_time = models.TimeField(blank=True, null=True)

    agency_job_type = models.CharField(
        choices=AGENCY_JOB_TYPE,  max_length=50, default='Permanent')
    agency_invoice_type = models.CharField(
        choices=AGENCY_INVOICE_TYPE,  max_length=50, default='Recurring')
    agency_amount = models.CharField(max_length=1000, default='')
    agency_recruiters = models.ManyToManyField(User, related_name='recruiters')
    agency_client = models.ForeignKey(AgencyCompany, null=True, on_delete=models.CASCADE)
    send_email_notifications = models.BooleanField(default=False)
    agency_category = models.ForeignKey(AgencyCompanyCatogery, null=True, on_delete=models.CASCADE)

    visa_required = models.BooleanField(default=False)
    visa_country = models.ForeignKey(
        Country, null=True, related_name='visa_country', on_delete=models.CASCADE)
    visa_type = models.CharField(max_length=50, default='')
    skills = models.ManyToManyField(Skill)
    salary_type = models.CharField(
        choices=SALARY_TYPE, max_length=20, blank=True, null=True)
    min_salary = models.IntegerField(default=0)
    max_salary = models.IntegerField(default=0)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    age_as_on_date = models.DateField(null=True)
    age_relaxation = models.CharField(max_length = 30, blank = True, null = True)
    pay_scale = models.IntegerField(null = True, blank = True)
    last_date = models.DateField(null=True)
    published_on = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    post_request_date = models.DateTimeField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now=True)
    # created_on = models.DateField(auto_now_add=True)
    created_on = models.DateField(auto_now=True)
    status = models.CharField(choices=POST_STATUS, max_length=50)
    previous_status = models.CharField(
        choices=POST_STATUS, max_length=50, default='Draft')
    post_on_fb = models.BooleanField(default=False)
    post_on_tw = models.BooleanField(default=False)
    post_on_ln = models.BooleanField(default=False)
    fb_views = models.IntegerField(default=0)
    tw_views = models.IntegerField(default=0)
    ln_views = models.IntegerField(default=0)
    other_views = models.IntegerField(default=0)
    job_type = models.CharField(choices=JOB_TYPE, max_length=50)
    published_message = models.TextField()
    company_name = models.CharField(max_length=100, default='')
    company_address = models.TextField()
    company_description = models.TextField()
    company_links = models.TextField()
    company_emails = models.EmailField(blank=True, null=True)
    meta_title = models.TextField()
    meta_description = models.TextField()
    major_skill = models.ForeignKey(Skill, null=True, blank=True, related_name='major_skill', on_delete=models.CASCADE)
    closed_date = models.DateTimeField(null=True, blank=True)
    minified_url = models.URLField(blank=True, null=True)
    duration_of_employment = models.CharField(max_length = 100, blank = True, null = True)
    number_of_post = models.IntegerField(null = True, blank = True)
    vacancies_for = models.CharField(max_length=30, blank = True, null = True)
    mode_of_application = models.CharField(max_length=30, blank = True, null = True)
    job_post_options = models.CharField(max_length=100, blank = True, null = True)
    preferred_employment_exchange = models.CharField(max_length=800, blank = True, null = True)
    mode_of_recruitment = models.CharField(max_length=100, blank = True, null = True)
    obligation_for_reservation_preference = models.CharField(max_length=30, blank = True, null = True)
    indenting_officer_name = models.CharField(max_length=100, blank = True, null = True)
    indenting_officer_email = models.EmailField(max_length=300, blank = True, null = True)
    indenting_officer_designation = models.CharField(max_length=100, blank = True, null = True)
    indenting_officer_mobile = models.CharField(max_length=13, blank=True, null=True)
    approach_officer_name = models.CharField(max_length=100, blank = True, null = True)
    approach_officer_email = models.EmailField(max_length=300, blank = True, null = True)
    approach_officer_designation = models.CharField(max_length=100, blank = True, null = True)
    approach_officer_mobile = models.CharField(max_length=13, blank=True, null=True)
    employment_exchange_name  = models.CharField(max_length=400, blank = True, null = True)
    recruiter_employment_exchange_name = models.CharField(max_length=400, blank = True, null = True)
    fb_groups = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    scanned_signature_job_post = models.ImageField(upload_to='signature_file/', null=True, blank=True)
    scanned_seal_job_post = models.ImageField(upload_to='scanned_seal/', null=True, blank=True)
    recruiter_jobpost_id = models.CharField(max_length=200, blank=True, null=True)
    custom_location_for_other_location = models.CharField(max_length=500, blank=True, null=True) #Only used when selected other location in dropdown
    def signature_file(self, filename):
        # Keep the original filename
        return os.path.join('signature_file', filename)

    def scanned_seal(self, filename):
        # Keep the original filename
        return os.path.join('scanned_seal', filename)

    # objects = JobPostManager()
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_data(self):
        return self

    def get_absolute_url(self):
        qs = self.title.replace("/[^a-zA-Z-]/g", "").title().strip().strip(".")
        qs = qs.replace(" ", "-").lower()
        qs = qs.replace("/", "-").replace(",", "").lower()
        qs = qs.replace(".", "dot-")
        if self.job_type is None:
            self.job_type = 'full-time'
        if str(self.job_type) == "internship":
            if self.company:
                company_name = self.company.slug
            else:
                company_name = self.company_name
            qs = "/" + qs + "-" + str(company_name) + "-" + str(self.id) + "/"
        else:
            qs = (
                "/"
                + qs
                + "-"
                + str(self.min_year)
                + "-to-"
                + str(self.max_year)
                + "-years-"
                + str(self.job_id)
                + "/"
            )
        return qs
    @property
    def get_job_minified_url(self):
        url = self.get_absolute_url()
        job_url = 'http://localhost:8000/' + url
        return job_url

    def get_total_views_count(self):
        total_views = self.fb_views + self.tw_views + \
            self.ln_views + self.other_views
        return total_views

    def get_similar_jobposts(self):
        # current_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        jobs = JobPost.objects.filter(Q(skills__in=self.skills.all())).filter(Q(min_year=self.min_year) | Q(
            max_year=self.max_year)).exclude(pk=self.job_id).distinct()
        jobs = jobs.filter(status='Live').select_related('company').prefetch_related('location')
        # no_of_jobs = len(jobs)
        # if no_of_jobs < 10:
        #     jobs = JobPost.objects.filter(status='Live')
        return jobs

    def get_recommended_jobposts(self):
        jobs = JobPost.objects.filter(Q(skills__in=self.skills.all()) | Q(
                location__in=self.location.all())).exclude(pk=self.id).distinct()
        jobs = jobs.filter(status='Live').select_related('company').prefetch_related('location')
        # no_of_jobs = len(jobs)
        # if no_of_jobs < 10:
        #     jobs = JobPost.objects.filter(status='Live')
        return jobs

    def get_locations(self):
        return self.location.values_list('name', flat=True)
    
    # def get_job_pincode(self):
    #     return self.job_pincode.values_list('pincode', flat=True)

    def get_job_type(self):
        if str(self.job_type) == 'walk-in':
            return 'walkin'
        elif str(self.job_type) == 'Full_Time' or str(self.job_type) == 'full_time':
            return 'full-time'
        else:
            return self.job_type

    def get_active_skills(self):
        return self.skills.filter(status='Active').values_list('name', flat=True)

    def get_skills(self):
        return self.skills.filter().order_by('id')

    def get_active_functional_area(self):
        return self.functional_area.filter(status='Active').order_by('name')

    def get_active_qualification(self):
        return self.edu_qualification.filter(status='Active').order_by('name')

    def get_active_industries(self):
        return self.industry.filter(status='Active').order_by('name')

    def get_all_applied_users_count(self):
        return AppliedJobs.objects.filter(job_post=self).count()
    
    def get_all_applied_user_ids(self):
         # Return all unique user IDs for this job post
        return AppliedJobs.objects.filter(job_post=self).values_list('candidate_id', flat=True).distinct()


    def get_selected_users(self):
        return AppliedJobs.objects.filter(job_post=self, status='Selected')
    
    def get_selected_users_count(self):
        return AppliedJobs.objects.filter(job_post=self, status='Selected').count()

    def get_shortlisted_users(self):
        return AppliedJobs.objects.filter(job_post=self, status='Shortlisted')
    
    def get_shortlisted_users_count(self):
        return AppliedJobs.objects.filter(Q(job_post=self) &( Q(status='Shortlisted') | Q(status= 'Selected'))).count()

    def get_rejected_users(self):
        return AppliedJobs.objects.filter(job_post=self, status='Rejected')
    def non_elgible_users_count(self):
        return AppliedJobs.objects.filter(job_post=self).exclude(Q(status= 'Shortlisted' )  | Q(status = 'Selected')).count()

    def is_expired(self):
        current_date = datetime.strptime(
            str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")
        if str(current_date) > str(self.last_date):
            return True
        else:
            return False

    def get_content(self):
        return ''

    def get_recruiter_assigned_jobposts(self):
        return AgencyRecruiterJobposts.objects.filter(job_post=self)

    def get_recruiter_hired_jobpost(self):
        return AgencyRecruiterJobposts.objects.filter(job_post=self, status='Hired').first()

    def get_hired_applicants(self):
        selected_applicants = AgencyApplicants.objects.filter(
            job_post=self, status='Hired').distinct()
        return selected_applicants

    def get_post_last_date(self):
        # today = arrow.utcnow().to('Asia/Calcutta').format('YYYY-MM-DD')
        current_date = datetime.strptime(
            str(self.last_date), "%Y-%m-%d").strftime('%d %b %Y')
        return current_date

    def get_post_created_date(self):
        # today = arrow.utcnow().to('Asia/Calcutta').format('YYYY-MM-DD')
        current_date = datetime.strptime(
            str(self.created_on), "%Y-%m-%d").strftime('%d %b %Y')
        return current_date

    def adding_applicants(self):
        job_post = self
        user_technical_skills = TechnicalSkill.objects.filter(
            skill__in=job_post.skills.all().values_list('id', flat=True))
        users = User.objects.filter(
            user_type='JS', skills__in=user_technical_skills)
        for user in users:
            if not AppliedJobs.objects.filter(user=user, job_post=job_post):
                AppliedJobs.objects.create(
                    user=user, job_post=job_post, status='Pending', ip_address='', user_agent='')

    def get_job_status(self):
        if self.status == 'Disabled':
            return 'inactive'
        return 'active'

    def get_job_salary(self):
        if self.salary_type == 'Month':
            return self.min_salary * 12, self.max_salary * 12
        else:
            return self.min_salary, self.max_salary

    def get_job_description(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.description)
        for s in soup(['script', 'style']):
            s.extract()
        return ' '.join(soup.stripped_strings)

    def get_description(self):
        from bs4 import BeautifulSoup
        html = self.description
        # create a new bs4 object from the html data loaded
        soup = BeautifulSoup(html)
        # remove all javascript and stylesheet code
        for script in soup(["script", "style"]):
            script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def get_company_emails(self):
        return self.company_emails

    def is_work_from_home(self):
        title = self.title.lower().replace(' ', '')
        if 'workfromhome' in title or 'parttime' in title:
            return True
        return False


POST = (
    ('Page', 'Page'),
    ('Group', 'Group'),
    ('PeelJobs', 'PeelJobs'),
)

POST_STATUS = (
    ('Posted', 'Posted'),
    ('Deleted', 'Deleted'),
)

RESERVATION_CATEGORY = (
    ('Open Category/Unreserved', 'Open Category/Unreserved'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('EWS', 'EWS'),
    ('Ex-Servicemen', 'Ex-Servicemen'),
    ('PwD', 'PwD'),
    ('Women', 'Women')
)


class Vacancy_location(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    def get_city(self):
        return self.city.values_list('name', flat=True)
    
class Vacancy(models.Model):
    vacancy_location = models.ForeignKey(Vacancy_location, on_delete=models.CASCADE)
    vacancy = models.IntegerField()
    
    reservation_category = models.CharField(
        max_length=50, choices=RESERVATION_CATEGORY, default = 'Open Category/Unreserved')
    custom_location_for_other_location = models.CharField(max_length=500, blank=True, null=True) #Only used when selected other location in dropdown

class Job_Feedback(models.Model):
    job=models.OneToOneField(JobPost, on_delete=models.CASCADE)
    total_candidates_selected = models.IntegerField()  
    comment=models.CharField(null=True, blank=True, max_length=500)
    total_candidates_joined = models.IntegerField()
    feedback_type = models.CharField(blank=True, null=True, max_length=500)

class Job_Feedback_city_details(models.Model):
    feedback = models.ForeignKey(Job_Feedback, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    candidates_joined = models.IntegerField()

class Job_Feedback_candidate_details(models.Model):
    feedback = models.ForeignKey(Job_Feedback, on_delete=models.CASCADE)
    candidates_joined_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    

class AgencyResume(models.Model):
    resume = models.CharField(max_length=5000, blank=True)
    candidate_name = models.CharField(max_length=1000)
    email = models.EmailField()
    mobile = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    skill = models.ManyToManyField(Skill)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=POST, default='Pending')
    user = models.ForeignKey(
        User, blank=True, null=True, related_name='Applicant', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)


POST = (
    ('Pending', 'Pending'),
    ('Shortlisted', 'Shortlisted'),
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
    ('Process', 'Process'),
)


class AppliedJobs(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(choices=POST_STATUS, max_length=50)
    hired = models.CharField(max_length=2000, default='', null=True)
    recruiter_jobpost_id = models.CharField(max_length=2000, default='', null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=2000, default='')
    ip_address = models.CharField(max_length=2000, default='')
    user_agent = models.CharField(max_length=2000, default='')
    resume_applicant = models.ForeignKey(AgencyResume, null=True, blank=True, on_delete=models.CASCADE)


ENQUERY_TYPES = (
                ('Suggestion', 'Suggestion'),
                ('Technical Issue', 'Technical Issue'),
                # ('Complaint', 'Complaint'),
                ('others', 'Others'),
)


class simplecontact(models.Model):
    name = models.CharField(max_length=100)
    employment_exchange_registration_no = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField()
    email = models.EmailField()
    phone = models.BigIntegerField(blank=True, null=True)
    contacted_on = models.DateField(auto_now=True)
    subject = models.CharField(max_length=500)
    enquery_type = models.CharField(max_length=100, choices=ENQUERY_TYPES)

    # def __unicode__(self):
    #     return self.full_name


class MailTemplate(models.Model):
    message = models.TextField()
    subject = models.TextField()
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField()
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    show_recruiter = models.BooleanField(default=False)
    applicant_status = models.CharField(choices=POST_STATUS, max_length=50)


class SentMail(models.Model):
    send_on = models.DateTimeField(auto_now=True)
    recruiter = models.ManyToManyField(User)
    template = models.ForeignKey(MailTemplate, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, null=True, blank=True, on_delete=models.CASCADE)


class JobAlert(models.Model):
    skill = models.ManyToManyField(Skill)
    location = models.ManyToManyField(City)
    min_year = models.IntegerField(null=True, blank=True)
    max_year = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    min_salary = models.IntegerField(null=True, blank=True)
    industry = models.ManyToManyField(Industry)
    role = models.CharField(max_length=2000, blank=True, null=True)
    related_jobs = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=2000, unique=True)
    unsubscribe_code = models.CharField(max_length=100, null=True, blank=True)
    is_unsubscribe = models.BooleanField(default=False)
    subscribe_code = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    unsubscribe_reason = models.TextField(default='')


class SearchResult(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    job_post = models.CharField(max_length=1000, default=0)
    skills = models.ManyToManyField(Skill, related_name='skill_search')
    other_skill = models.CharField(max_length=1000)
    locations = models.ManyToManyField(City, related_name='location_search')
    other_location = models.CharField(max_length=1000)
    search_text = JSONField(default=dict)
    industry = models.CharField(max_length=1000)
    search_on = models.DateTimeField(auto_now=True)
    functional_area = models.CharField(max_length=1000)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE, blank=True, null=True)
    expierence = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=200)


class Subscriber(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    job_post = models.ForeignKey(JobPost, blank=True, null=True, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    unsubscribe_code = models.CharField(max_length=100, null=True, blank=True)
    is_unsubscribe = models.BooleanField(default=False)
    subscribe_code = models.CharField(max_length=100, null=True, blank=True)
    unsubscribe_reason = models.TextField(default='')

    def user_subscription_list(self):
        return Subscriber.objects.filter(email=self.email).exclude(id=self.id)


class VisitedJobs(models.Model):
    visited_on = models.DateTimeField(auto_now=True)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    firm_type = models.CharField(max_length=250, default='Company')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class DailySearchLog(models.Model):
    no_of_job_posts = models.IntegerField(default='0')
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE)
    created_on = models.DateField()
    no_of_searches = models.IntegerField(default='0')


class AgencyApplicants(models.Model):
    applicant = models.ForeignKey(AgencyResume, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=POST, default='Pending')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)


AGENCY_RECRUITER_JOB_TYPE = (
    ('Pending', 'Pending'),
    ('Shortlisted', 'Shortlisted'),
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
    ('Hired', 'Hired'),
    ('Process', 'Process'),
)


class AgencyRecruiterJobposts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=AGENCY_RECRUITER_JOB_TYPE, default='Pending')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    message = models.TextField(default='')


def skills_update(skill_slug, slug):
    removed_skill = Skill.objects.get(slug=skill_slug)
    job_posts = JobPost.objects.filter(skills__in=[removed_skill])
    latest_skill = Skill.objects.get(slug=slug)
    for i in job_posts:
        i.skills.add(latest_skill)
    removed_skill.delete()


class AgencyWorkLog(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    no_of_profiles = models.IntegerField()
    summary = models.TextField()
    timegap = models.CharField(max_length=100)


#class BlogAttachment(models.Model):
#    file_prepend = "blog/attachments/"
#    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#    created_on = models.DateTimeField(auto_now_add=True)
#    attached_file = models.FileField(
#        max_length=1000, null=True, blank=True, upload_to=img_url)
#    post = models.ForeignKey(Post, on_delete=models.CASCADE)


def updating_skills_jobposts(skill, update_skill):
    job_posts = JobPost.objects.filter(skills__in=[skill])
    for each in job_posts:
        each.skills.add(update_skill)
    skill.remove()


STATUS = (
    ('Pending', 'Pending'),
    ('Live', 'Live'),
    ('Closed', 'Closed'),
)


class Solution(models.Model):
    description = models.TextField()
    given_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    attachments = models.ManyToManyField(Attachment)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def get_dislikes(self):
        dislikes = AssessmentData.objects.filter(solution=self, comment='', dislike=True)
        return dislikes

    def get_likes(self):
        likes = AssessmentData.objects.filter(solution=self, comment='', like=True)
        return likes

    def get_comments(self):
        comments = AssessmentData.objects.filter(solution=self).exclude(comment='')
        return comments


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.ForeignKey(Skill, related_name='skill_questions', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='questions', blank=True, null=True, on_delete=models.CASCADE)
    solutions = models.ManyToManyField(Solution)
    status = models.CharField(choices=STATUS, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    attachments = models.ManyToManyField(Attachment)
    slug = models.SlugField(max_length=500)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('title', 'skills',)
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title

    def get_dislikes(self):
        dislikes = AssessmentData.objects.filter(question=self, comment='', dislike=True)
        return dislikes

    def get_likes(self):
        likes = AssessmentData.objects.filter(question=self, comment='', like=True)
        return likes

    def get_solutions(self):
        solutions = self.solutions.filter(status='Live')
        return solutions

    def get_comments(self):
        comments = AssessmentData.objects.filter(question=self).exclude(comment='')
        return comments


class AssessmentData(models.Model):
    question = models.ForeignKey(Question, related_name='question_data', on_delete=models.CASCADE, null=True)
    solution = models.ForeignKey(Solution, related_name='solution_data', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='user_data', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


# class CredentialsModel(models.Model):
#     id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
#     credential = CredentialsField()
    
    
class News_Notifications(models.Model):
    title=models.CharField(max_length=300)
    description =models.CharField(max_length=300)
    link=models.CharField(max_length=300, blank= True, null= True)
    start_date=models.DateField()
    end_date = models.DateField()
    is_active =models.BooleanField(default="True")
    
    
class Ex_Employment_Exchange(models.Model):
    name= models.CharField(unique=True, max_length=100)

class Ex_Education_Qualification(models.Model):
    date_of_passing = models.DateField()
    course_major_subjects = models.CharField( blank=True,null=True, max_length=800)
    examination_passed = models.CharField(max_length=800)
    cleaned_examination_passed = models.CharField(max_length=800, blank = True, null = True)
    class_division = models.CharField( blank=True,null=True, max_length=800)
    board_university = models.CharField( blank=True,null=True, max_length=800)
    registration_no = models.CharField( blank=True,null=True, max_length=800)
    percentage_of_marks = models.FloatField( blank=True,null=True)
    other_examination_name = models.CharField( blank=True,null=True, max_length=800)
    major_elective_subject = models.CharField( blank=True,null=True, max_length=800)
    subjects_other_subjects = models.CharField( blank=True,null=True, max_length=800)
    institution_school_college = models.CharField(max_length=800)
    
    
class Ex_Work_Experience(models.Model):
    From = models.DateField()
    to = models.DateField() 
    industry_sector = models.CharField( blank=True,null=True, max_length=800)
    functional_area = models.CharField( blank=True,null=True, max_length=800)
    nature_of_work = models.CharField( blank=True,null=True, max_length=800)
    functional_roles = models.CharField( blank=True,null=True, max_length=800)
    other_functional_roles = models.CharField( blank=True,null=True, max_length=800)
    employer = models.CharField(max_length=800)
    duration = models.CharField( blank=True,null=True, max_length=800)
    other_industry_sector = models.CharField( blank=True,null=True, max_length=800)
    other_functional_area = models.CharField( blank=True,null=True, max_length=800)
    highest_designation = models.CharField( blank=True,null=True, max_length=800)
    last_salary_drawn = models.CharField( blank=True,null=True, max_length=800)
    

class Ex_Skill_Qualification(models.Model):
    sector = models.CharField( blank=True,null=True, max_length=800)
    course_job_role = models.CharField( blank=True,null=True, max_length=800)
    exam_diploma_certificate = models.CharField(max_length=800)
    duration = models.CharField(blank=True,null=True, max_length=800)
    certificate_id = models.CharField( max_length=800)
    engagement = models.CharField( blank=True,null=True, max_length=800)

class Ex_Other_Qualification_Trainings_Courses(models.Model):
    date_of_passing = models.DateField()
    duration_in_months = models.CharField( max_length=800)
    certificate_name = models.CharField(max_length=800)
    issued_by = models.CharField(max_length=800)
    
# class Ex_Enclosure_Details(models.Model):
#     key = models.CharField( blank=True,null=True, max_length=800)
#     value = models.CharField( blank=True,null=True, max_length=800)


    
class Ex_Languages_Known(models.Model):
    options = models.CharField(max_length=800)
    language = models.CharField(max_length=800)
    
class Ex_Applicant(models.Model):
    applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    user_name = models.CharField( blank = True, null = True, max_length=800)
    applicant_name =models.CharField(max_length=200)
    applicant_gender = models.CharField(max_length=20, blank=True, null=True)
    mobile_number = models.CharField(max_length=800, blank=True, null=True)
    email = models.EmailField(max_length=255, db_index=True)
    fathers_name = models.CharField(blank=True, max_length=200)
    types_of_re_registration = models.CharField(blank=True, max_length=200)
    already_registered = models.CharField(blank=True, max_length=100)
    caste = models.CharField(max_length=50, blank=True, null=True)
    mothers_name = models.CharField(blank=True, max_length=200)
    whether_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    prominent_identification_mark = models.CharField(max_length=200, blank=True, null=True)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    fathers_name_guardians_name = models.CharField(blank=True, max_length=200)
    unique_identification_no = models.CharField(max_length=200, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    occupation_type = models.CharField(max_length=200, blank=True, null=True)
    unique_identification_type = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)
    passport_photo = models.CharField(max_length=800, blank=True, null=True)
    height_in_cm = models.CharField(max_length=800, blank=True, null=True)
    weight_kgs = models.CharField(max_length=800, blank=True, null=True)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=800, blank=True, null=True)
    disability_category = models.CharField(max_length=100, blank=True, null=True)
    highest_educational_level = models.CharField(max_length=200, blank=True, null=True)
    declaration = models.CharField(max_length=800, blank=True, null=True)
    signature = models.CharField(max_length=800, blank=True, null=True)
    current_employment_status = models.CharField(max_length=200, blank=True, null=True)
    post_office_p = models.CharField(max_length=200, blank=True, null=True)
    sub_division = models.CharField(max_length=200, blank=True, null=True)
    revenue_circle= models.CharField(max_length=200, blank=True, null=True)
    police_station_p = models.CharField(max_length=200, blank=True, null=True)
    district_p = models.CharField(max_length=200, blank=True, null=True)
    pin_code_p = models.CharField(max_length=800, blank=True, null=True)
    name_of_the_house_apartment_p = models.CharField(max_length=800, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=800, blank=True, null=True)
    building_no_block_no_p = models.CharField(max_length=800, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city_p = models.CharField(max_length=800, blank=True, null=True)
    police_station = models.CharField(max_length=800, blank=True, null=True)
    same_as_permanent_address = models.CharField(max_length=800, blank=True, null=True)
    name_of_the_house_apartment = models.CharField(max_length=800, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=800, blank=True, null=True)
    building_no_block_no = models.CharField(max_length=800, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city = models.CharField(max_length=800, blank=True, null=True)
    post_office = models.CharField(max_length=800, blank=True, null=True)
    pin_code = models.CharField(max_length=800, blank=True, null=True)
    district = models.CharField(max_length=800, blank=True, null=True)
    employment_exchange = models.CharField(max_length=800, blank=True, null=True)
    lgd_employment_exchange = models.CharField(max_length=800, blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    aadhaar_number_virtual_id = models.CharField(max_length=800, blank=True, null=True)
    full_name_as_in_aadhaar_card = models.CharField(max_length=800, blank=True, null=True)
    highest_examination_passed = models.CharField(max_length=800, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    registration_no = models.CharField(max_length=800, db_index=True)
    religion = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    education_qualification = models.ManyToManyField(Ex_Education_Qualification)
    work_experience = models.ManyToManyField(Ex_Work_Experience)
    skill_qualification = models.ManyToManyField(Ex_Skill_Qualification)
    other_qualification_training_courses = models.ManyToManyField(Ex_Other_Qualification_Trainings_Courses)
    # enclosure_details = models.ManyToManyField(Ex_Enclosure_Details)
    languages_known = models.ManyToManyField(Ex_Languages_Known)
    
    
class Ex_Additional_Info(models.Model):
    oid = models.CharField( blank=True,null=True, max_length=800)
    department_id = models.CharField( blank=True,null = True, max_length=800)
    department_name = models.CharField( blank=True,null=True, max_length=800)
    service_id = models.CharField( blank=True,null=True, max_length=800)
    service_name = models.CharField( blank=True,null=True, max_length=800)
    appl_id = models.CharField( blank=True,null=True, max_length=800)
    appl_ref_no = models.CharField( blank=True,null=True, max_length=800)
    no_of_attachment = models.CharField( blank=True,null=True, max_length=800)
    submission_mode_id = models.CharField( blank=True,null=True, max_length=800)
    submission_mode = models.CharField( blank=True,null=True, max_length=800)
    applied_by = models.CharField( blank=True,null=True, max_length=800)
    submission_location = models.CharField( blank=True,null=True, max_length=800)
    submission_date = models.DateTimeField( blank=True,null=True)
    payment_mode = models.CharField( blank=True,null=True, max_length=800)
    reference_no = models.CharField( blank=True,null=True, max_length=800)
    payment_date = models.CharField( blank=True,null=True, max_length=800)
    amount = models.CharField( blank=True,null=True, max_length=800)
    registration_id = models.CharField( blank=True,null=True, max_length=800)
    base_service_id = models.CharField( blank=True,null=True, max_length=800)
    version_no = models.CharField( blank=True,null=True, max_length=800)
    sub_version = models.CharField( blank=True,null=True, max_length=800)
    due_date = models.DateField( blank=True,null=True)
    submission_date_str = models.DateField( blank=True,null=True)
    pit = models.CharField( blank=True,null=True, max_length=800)
    pbt = models.CharField( blank=True,null=True, max_length=800)
    dit = models.CharField( blank=True,null=True, max_length=800)
    dbt = models.CharField( blank=True,null=True, max_length=800)
    rit = models.CharField( blank=True,null=True, max_length=800)
    rbt = models.CharField( blank=True,null=True, max_length=800)
    execution_date_str = models.DateField( blank=True,null=True)
    service_timeline = models.CharField( blank=True,null=True, max_length=800)
    appl_status = models.CharField( blank=True,null=True, max_length=800)
    district = models.CharField( blank=True,null=True, max_length=800)
    district_code = models.CharField( blank=True,null=True, max_length=800)
    cin_no = models.CharField( blank=True,null=True, max_length=800)
    govt_charge = models.CharField( blank=True,null=True, max_length=800)
    grn_no = models.CharField( blank=True,null=True, max_length=800)
    service_charge = models.CharField( blank=True,null=True, max_length=800)
    user = models.ForeignKey(Ex_Applicant, related_query_name="ex_additional_info", related_name='ex_additional_info', on_delete=models.CASCADE)
    
    
class Ex_All_Qualifications(models.Model):
    name = models.CharField( max_length=800)
    status = models.CharField(choices=STATUS, max_length=10)
    slug = models.SlugField(blank= True, null = True, max_length=500)
    code = models.IntegerField(null=True, blank=True)
    


class Ex_Examination_Passed(models.Model):
    name = models.CharField(max_length = 500)
    code = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(blank= True, null = True, max_length=500)

class API_Fetch_History(models.Model):
    username= models.CharField(max_length=20, blank = True, null = True)
    date_on_which_data_is_fetched = models.DateTimeField(default=timezone.now)
    parameter_start_date = models.DateField()
    parameter_end_date = models.DateField()
    count_of_students_data = models.CharField(max_length=20, blank = True, null = True)

class NIC_API_Fetch_History(models.Model):
    fetch_date = models.DateTimeField(default=timezone.now)
    parameter_date = models.DateField()
    total = models.CharField(max_length=20, blank = True, null = True)





class Ex_Employment_Exchanges_Under_Zones(models.Model):
    name = models.CharField(unique=True, max_length=300)
    zone = models.ForeignKey(Ex_Zone, on_delete=models.CASCADE)
    
#  #   
# #class Job_Fair_JobPost(models.Model):
#     POST_STATUS = (
#         ('Draft', 'Draft'),
#         ('Expired', 'Expired'),
#         ('Live', 'Live'),
#         ('Disabled', 'Disabled'),
#         ('Pending', 'Pending'),
#         ('Published', 'Published'),
#         ('Hired', 'Hired'),
#         ('Process', 'Process'),
#     )
#     SALARY_TYPE = (
#         ('Month', 'Month'),
#         ('Year', 'Year'),
#     )
#     user = models.ForeignKey(User, related_name='jobposts', on_delete=models.CASCADE)
#     code = models.CharField(max_length=50, null=True)
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=5000)
#     location = models.ManyToManyField(City, related_name='locations')
#     job_role = models.CharField(max_length=50, default='')
#     total_vacancy = models.IntegerField()
#     #vacancies = models.ManyToManyField(Vacancy, related_name='vacancies')
#     industry = models.ManyToManyField(Industry)
   
#     job_interview_location = models.ManyToManyField(InterviewLocation)
#     country = models.ForeignKey(Country, null=True, related_name='job_country', on_delete=models.CASCADE)
#     functional_area = models.ManyToManyField(FunctionalArea)
#     keywords = models.ManyToManyField(Keyword)
#     description = models.TextField()
#     min_year = models.IntegerField(default=0)
#     min_month = models.IntegerField(default=0)
#     max_year = models.IntegerField(default=0)
#     max_month = models.IntegerField(default=0)
#     fresher = models.BooleanField(default=False)
#     edu_qualification = models.ManyToManyField(Qualification)
#     company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
#     #job_pincode=models.ManyToManyField(Pincode, related_name='job_pincode')
#     #pincode = models.ForeignKey(Pincode, null=True, blank=True, on_delete=models.CASCADE)
#     # tech_qualification =

#     # govt jobpost
#     application_fee = models.IntegerField(default=0)
#     govt_job_type = models.CharField(
#         choices=GOV_JOB_TYPE,  max_length=50, default='Central')
#     selection_process = models.TextField(default='')
#     how_to_apply = models.TextField(default='')
#     important_dates = models.TextField(default='')
#     # validity
#     govt_from_date = models.DateField(null=True, blank=True)
#     govt_to_date = models.DateField(null=True, blank=True)
#     govt_exam_date = models.DateField(null=True, blank=True)
#     age_relaxation = models.TextField(default='')

#     walkin_contactinfo = models.TextField(default='')
#     walkin_show_contact_info = models.BooleanField(default=False)
#     walkin_from_date = models.DateField(null=True, blank=True)
#     walkin_to_date = models.DateField(null=True, blank=True)
#     walkin_time = models.TimeField(blank=True, null=True)

#     agency_job_type = models.CharField(
#         choices=AGENCY_JOB_TYPE,  max_length=50, default='Permanent')
#     agency_invoice_type = models.CharField(
#         choices=AGENCY_INVOICE_TYPE,  max_length=50, default='Recurring')
#     agency_amount = models.CharField(max_length=1000, default='')
#     agency_recruiters = models.ManyToManyField(User, related_name='recruiters')
#     agency_client = models.ForeignKey(AgencyCompany, null=True, on_delete=models.CASCADE)
#     send_email_notifications = models.BooleanField(default=False)
#     agency_category = models.ForeignKey(AgencyCompanyCatogery, null=True, on_delete=models.CASCADE)

#     visa_required = models.BooleanField(default=False)
#     visa_country = models.ForeignKey(
#         Country, null=True, related_name='visa_country', on_delete=models.CASCADE)
#     visa_type = models.CharField(max_length=50, default='')
#     skills = models.ManyToManyField(Skill)
#     salary_type = models.CharField(
#         choices=SALARY_TYPE, max_length=20, blank=True, null=True)
#     min_salary = models.IntegerField(default=0)
#     max_salary = models.IntegerField(default=0)
#     last_date = models.DateField(null=True)
#     published_on = models.DateTimeField(null=True, blank=True)
#     published_date = models.DateTimeField(null=True, blank=True)
#     posted_on = models.DateTimeField(auto_now=True)
#     created_on = models.DateField(auto_now_add=True)
#     status = models.CharField(choices=POST_STATUS, max_length=50)
#     previous_status = models.CharField(
#         choices=POST_STATUS, max_length=50, default='Draft')
    
#     job_type = models.CharField(choices=JOB_TYPE, max_length=50)
#     published_message = models.TextField()
#     company_name = models.CharField(max_length=100, default='')
#     company_address = models.TextField()
#     company_description = models.TextField()
#     company_links = models.TextField()
#     company_emails = models.EmailField(blank=True, null=True)
#     meta_title = models.TextField()
#     meta_description = models.TextField()
#     major_skill = models.ForeignKey(Skill, null=True, blank=True, related_name='major_skill', on_delete=models.CASCADE)
#     closed_date = models.DateTimeField(null=True, blank=True)
#     minified_url = models.URLField(blank=True, null=True)

#     # objects = JobPostManager()
#     class Meta:
#         ordering = ['-created_on']

#     def __str__(self):
#         return self.title

#     def get_data(self):
#         return self

#     def get_absolute_url(self):
#         qs = self.title.replace("/[^a-zA-Z-]/g", "").title().strip().strip(".")
#         qs = qs.replace(" ", "-").lower()
#         qs = qs.replace("/", "-").replace(",", "").lower()
#         qs = qs.replace(".", "dot-")
#         if self.job_type is None:
#             self.job_type = 'full-time'
#         if str(self.job_type) == "internship":
#             if self.company:
#                 company_name = self.company.slug
#             else:
#                 company_name = self.company_name
#             qs = "/" + qs + "-" + str(company_name) + "-" + str(self.id) + "/"
#         else:
#             qs = (
#                 "/"
#                 + qs
#                 + "-"
#                 + str(self.min_year)
#                 + "-to-"
#                 + str(self.max_year)
#                 + "-years-"
#                 + str(self.id)
#                 + "/"
#             )
#         return qs
#     @property
#     def get_job_minified_url(self):
#         url = self.get_absolute_url()
#         job_url = 'http://localhost:8000/' + url
#         return job_url

    

#     def get_similar_jobposts(self):
#         # current_date = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")
#         jobs = JobPost.objects.filter(Q(skills__in=self.skills.all())).filter(Q(min_year=self.min_year) | Q(
#             max_year=self.max_year)).exclude(pk=self.id).distinct()
#         jobs = jobs.filter(status='Live').select_related('company').prefetch_related('location')
#         # no_of_jobs = len(jobs)
#         # if no_of_jobs < 10:
#         #     jobs = JobPost.objects.filter(status='Live')
#         return jobs

#     def get_recommended_jobposts(self):
#         jobs = JobPost.objects.filter(Q(skills__in=self.skills.all()) | Q(
#                 location__in=self.location.all())).exclude(pk=self.id).distinct()
#         jobs = jobs.filter(status='Live').select_related('company').prefetch_related('location')
#         # no_of_jobs = len(jobs)
#         # if no_of_jobs < 10:
#         #     jobs = JobPost.objects.filter(status='Live')
#         return jobs

#     def get_locations(self):
#         return self.location.values_list('name', flat=True)
    
#     # def get_job_pincode(self):
#     #     return self.job_pincode.values_list('pincode', flat=True)

#     def get_job_type(self):
#         if str(self.job_type) == 'walk-in':
#             return 'walkin'
#         elif str(self.job_type) == 'Full_Time' or str(self.job_type) == 'full_time':
#             return 'full-time'
#         else:
#             return self.job_type

#     def get_active_skills(self):
#         return self.skills.filter(status='Active').values_list('name', flat=True)

#     def get_skills(self):
#         return self.skills.filter().order_by('id')

#     def get_active_functional_area(self):
#         return self.functional_area.filter(status='Active').order_by('name')

#     def get_active_qualification(self):
#         return self.edu_qualification.filter(status='Active').order_by('name')

#     def get_active_industries(self):
#         return self.industry.filter(status='Active').order_by('name')

#     def get_all_applied_users_count(self):
#         return AppliedJobs.objects.filter(job_post=self).count()

#     def get_selected_users(self):
#         return AppliedJobs.objects.filter(job_post=self, status='Selected')

#     def get_shortlisted_users(self):
#         return AppliedJobs.objects.filter(job_post=self, status='Shortlisted')

#     def get_rejected_users(self):
#         return AppliedJobs.objects.filter(job_post=self, status='Rejected')

#     def is_expired(self):
#         current_date = datetime.strptime(
#             str(datetime.now().date()), "%Y-%m-%d").strftime("%Y-%m-%d")
#         if str(current_date) > str(self.last_date):
#             return True
#         else:
#             return False

#     def get_content(self):
#         return ''

#     def get_recruiter_assigned_jobposts(self):
#         return AgencyRecruiterJobposts.objects.filter(job_post=self)

#     def get_recruiter_hired_jobpost(self):
#         return AgencyRecruiterJobposts.objects.filter(job_post=self, status='Hired').first()

#     def get_hired_applicants(self):
#         selected_applicants = AgencyApplicants.objects.filter(
#             job_post=self, status='Hired').distinct()
#         return selected_applicants

#     def get_post_last_date(self):
#         # today = arrow.utcnow().to('Asia/Calcutta').format('YYYY-MM-DD')
#         current_date = datetime.strptime(
#             str(self.last_date), "%Y-%m-%d").strftime('%d %b %Y')
#         return current_date

#     def get_post_created_date(self):
#         # today = arrow.utcnow().to('Asia/Calcutta').format('YYYY-MM-DD')
#         current_date = datetime.strptime(
#             str(self.created_on), "%Y-%m-%d").strftime('%d %b %Y')
#         return current_date

#     def adding_applicants(self):
#         job_post = self
#         user_technical_skills = TechnicalSkill.objects.filter(
#             skill__in=job_post.skills.all().values_list('id', flat=True))
#         users = User.objects.filter(
#             user_type='JS', skills__in=user_technical_skills)
#         for user in users:
#             if not AppliedJobs.objects.filter(user=user, job_post=job_post):
#                 AppliedJobs.objects.create(
#                     user=user, job_post=job_post, status='Pending', ip_address='', user_agent='')

#     def get_job_status(self):
#         if self.status == 'Disabled':
#             return 'inactive'
#         return 'active'

#     def get_job_salary(self):
#         if self.salary_type == 'Month':
#             return self.min_salary * 12, self.max_salary * 12
#         else:
#             return self.min_salary, self.max_salary

#     def get_job_description(self):
#         from bs4 import BeautifulSoup
#         soup = BeautifulSoup(self.description)
#         for s in soup(['script', 'style']):
#             s.extract()
#         return ' '.join(soup.stripped_strings)

#     def get_description(self):
#         from bs4 import BeautifulSoup
#         html = self.description
#         # create a new bs4 object from the html data loaded
#         soup = BeautifulSoup(html)
#         # remove all javascript and stylesheet code
#         for script in soup(["script", "style"]):
#             script.extract()
#         # get text
#         text = soup.get_text()
#         # break into lines and remove leading and trailing space on each
#         lines = (line.strip() for line in text.splitlines())
#         # break multi-headlines into a line each
#         chunks = (phrase.strip()
#                   for line in lines for phrase in line.split("  "))
#         # drop blank lines
#         text = '\n'.join(chunk for chunk in chunks if chunk)
#         return text

#     def get_company_emails(self):
#         return self.company_emails

#     def is_work_from_home(self):
#         title = self.title.lower().replace(' ', '')
#         if 'workfromhome' in title or 'parttime' in title:
#             return True
#         return False

# class Job_Fair_Company(AbstractBaseUser, PermissionsMixin):
#     file_prepend = "company/logo/"
#     name = models.CharField(max_length=5000)
#     website = models.CharField(max_length=5000, null=True, blank=True)
#     company_registration_no = models.CharField(max_length=30, null=True, blank=True)
#     company_pan_no = models.CharField(max_length=20, null=True, blank=True)
#     company_gst_no = models.CharField(max_length=30, null=True, blank=True)
#     address = models.TextField()
#     key_official_details = models.TextField(default='')
#     profile_pic = models.FileField(
#         max_length=1000, upload_to=img_url, null=True, blank=True)
#     size = models.CharField(choices=COMPANY_SIZE, max_length=10, default='')
#     level = models.IntegerField(null=True, blank=True)
#     company_type = models.CharField(choices=COMPANY_TYPES, max_length=50, default='')
#     firm_legal_entity = models.CharField(choices=FIRM_LEGAL_ENTITITIES, max_length=100, default=FIRM_LEGAL_ENTITITIES[2][0])
#     firm_registration_number = models.CharField(max_length=250, default='')
#     profile = models.TextField()
#     phone_number = models.CharField(max_length=15)
#     registered_date = models.DateField(auto_now_add=True)
#     email = models.EmailField(max_length=255, null=True)

#     short_code = models.CharField(max_length=50, null=True)
#     pan_or_gst_no = models.CharField(max_length=50, default='')
#     is_active = models.BooleanField(default=False)
#     slug = models.SlugField(max_length=5000)
#     meta_title = models.TextField(default='')
#     meta_description = models.TextField(default='')
#     campaign_icon = models.CharField(max_length=3000, null=True)
#     created_from = models.CharField(max_length=200, default='')
    
    
#     objects = UserManager()

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Company, self).save(*args, **kwargs)
    
#     @property
#     def get_slug(self):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         return self.slug
    
#     def is_company(self):
#         if str(self.company_type) == 'Company':
#             return True
#         return False

#     def is_agency(self):
#         if str(self.company_type) == 'Consultant':
#             return True
#         return False

#     def get_company_admin(self):
#         return User.objects.filter(is_admin=True, company=self).first()

#     def get_company_recruiters(self):
#         return User.objects.filter(company=self)

#     def get_company_jobposts(self):
#         return JobPost.objects.filter(user__company=self)

#     def get_jobposts(self):
#         return JobPost.objects.filter(company=self, status='Live')

#     def get_total_jobposts(self):
#         return JobPost.objects.filter(company=self)

#     def get_company_tickets(self):
#         return Ticket.objects.filter(user__company=self)

#     def get_company_menu(self):
#         return Menu.objects.filter(company=self)

#     def get_active_company_menu(self):
#         return Menu.objects.filter(company=self, status=True).order_by('id')

#     def get_live_jobposts(self):
#         return JobPost.objects.filter(user__company=self, status='Live')

#     def get_unique_recruiters(self):
#         job_posts = list(set(list(JobPost.objects.filter(
#             company=self, status='Live').values_list('user', flat=True))))
#         users = User.objects.filter(id__in=job_posts)
#         return users

#     def get_absolute_url(self):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         return '/' + str(self.slug) + '-job-openings/'
    
#     @property
#     def get_logo_url(self):
#         if self.profile_pic:
#             return str(self.profile_pic)
#         return settings.MEDIA_URL + os.path.sep + 'img/company_logo.png'

#     def get_description(self):
#         from bs4 import BeautifulSoup
#         html = self.profile
#         # create a new bs4 object from the html data loaded
#         soup = BeautifulSoup(html)
#         # remove all javascript and stylesheet code
#         for script in soup(["script", "style"]):
#             script.extract()
#         # get text
#         text = soup.get_text()
#         # break into lines and remove leading and trailing space on each
#         lines = (line.strip() for line in text.splitlines())
#         # break multi-headlines into a line each
#         chunks = (phrase.strip()
#                   for line in lines for phrase in line.split("  "))
#         # drop blank lines
#         text = '\n<br>'.join(chunk for chunk in chunks if chunk)
#         return text

#     def get_website(self):
#         site = self.website
#         if site is not None and '//' in site:
#             site = site.split("//")[1]
#         return site 
    
# class Job_Vacancy(models.Model):
#     job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
#     vacancy = models.IntegerField()
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
    
#     def get_city(self):
#         return self.city.values_list('name', flat=True)
    
# class Job_Fair_Job_Feedback(models.Model):
#     job=models.OneToOneField(JobPost, on_delete=models.CASCADE)
#     total_candidates_selected = models.IntegerField()  
#     comment=models.CharField(null=True, blank=True, max_length=500)
#     total_candidates_joined = models.IntegerField()

# class Job_Fair_Job_Feedback_city_details(models.Model):
#     feedback = models.ForeignKey(Job_Feedback, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     candidates_joined = models.IntegerField()

# class Job_Fair_Job_Feedback_candidate_details(models.Model):
#     feedback = models.ForeignKey(Job_Feedback, on_delete=models.CASCADE)
#     candidates_joined_user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Job_Fair_AppliedJobs(models.Model):
#     job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
#     status = models.CharField(choices=POST_STATUS, max_length=50)
#     applied_on = models.DateTimeField(auto_now_add=True)
#     remarks = models.CharField(max_length=2000, default='')
#     ip_address = models.CharField(max_length=2000, default='')
#     user_agent = models.CharField(max_length=2000, default='')
#     resume_applicant = models.ForeignKey(AgencyResume, null=True, blank=True, on_delete=models.CASCADE)


class Ex1_Education_Qualification(models.Model):
    date_of_passing = models.DateField()
    course_major_subjects = models.CharField( blank=True,null=True, max_length=800)
    examination_passed = models.CharField(max_length=800)
    cleaned_examination_passed = models.CharField(max_length=800, blank = True, null = True)
    class_division = models.CharField( blank=True,null=True, max_length=800)
    board_university = models.CharField( blank=True,null=True, max_length=800)
    registration_no = models.CharField( blank=True,null=True, max_length=800)
    percentage_of_marks = models.FloatField( blank=True,null=True)
    other_examination_name = models.CharField( blank=True,null=True, max_length=800)
    major_elective_subject = models.CharField( blank=True,null=True, max_length=1200)
    subjects_other_subjects = models.CharField( blank=True,null=True, max_length=1200)
    institution_school_college = models.CharField(max_length=800)
    
    
class Ex1_Work_Experience(models.Model):
    From = models.DateField()
    to = models.DateField() 
    industry_sector = models.CharField( blank=True,null=True, max_length=800)
    functional_area = models.CharField( blank=True,null=True, max_length=800)
    nature_of_work = models.CharField( blank=True,null=True, max_length=800)
    functional_roles = models.CharField( blank=True,null=True, max_length=800)
    other_functional_roles = models.CharField( blank=True,null=True, max_length=800)
    employer = models.CharField(max_length=800)
    duration = models.CharField( blank=True,null=True, max_length=800)
    other_industry_sector = models.CharField( blank=True,null=True, max_length=800)
    other_functional_area = models.CharField( blank=True,null=True, max_length=800)
    highest_designation = models.CharField( blank=True,null=True, max_length=800)
    last_salary_drawn = models.CharField( blank=True,null=True, max_length=800)
    

class Ex1_Skill_Qualification(models.Model):
    sector = models.CharField( blank=True,null=True, max_length=800)
    course_job_role = models.CharField( blank=True,null=True, max_length=800)
    exam_diploma_certificate = models.CharField(max_length=800)
    duration = models.CharField(blank=True,null=True, max_length=800)
    certificate_id = models.CharField( max_length=800)
    engagement = models.CharField( blank=True,null=True, max_length=800)

class Ex1_Other_Qualification_Trainings_Courses(models.Model):
    date_of_passing = models.DateField()
    duration_in_months = models.CharField( max_length=800)
    certificate_name = models.CharField(max_length=800)
    issued_by = models.CharField(max_length=800)
    
# class Ex_Enclosure_Details(models.Model):
#     key = models.CharField( blank=True,null=True, max_length=800)
#     value = models.CharField( blank=True,null=True, max_length=800)


    
class Ex1_Languages_Known(models.Model):
    options = models.CharField(max_length=800)
    language = models.CharField(max_length=800)
    

##OLD MIS DATA STORED HERE    
class Ex1_Applicant(models.Model):
    applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    user_name = models.CharField( blank = True, null = True, max_length=800)
    applicant_name =models.CharField(max_length=200)
    applicant_gender = models.CharField(max_length=20, blank=True, null=True, db_index = True)
    mobile_number = models.CharField(max_length=800, blank=True, null=True)
    email = models.EmailField(max_length=255, db_index=True)
    fathers_name = models.CharField(blank=True, max_length=200)
    types_of_re_registration = models.CharField(blank=True, max_length=200)
    already_registered = models.CharField(blank=True, max_length=100, db_index=True)
    caste = models.CharField(max_length=50, blank=True, null=True, db_index = True)
    mothers_name = models.CharField(blank=True, max_length=200)
    whether_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    prominent_identification_mark = models.CharField(max_length=200, blank=True, null=True)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, db_index = True)
    fathers_name_guardians_name = models.CharField(blank=True, max_length=200)
    unique_identification_no = models.CharField(max_length=200, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    occupation_type = models.CharField(max_length=200, blank=True, null=True)
    unique_identification_type = models.CharField(max_length=200, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)
    passport_photo = models.CharField(max_length=800, blank=True, null=True)
    height_in_cm = models.CharField(max_length=800, blank=True, null=True)
    weight_kgs = models.CharField(max_length=800, blank=True, null=True)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=800, blank=True, null=True)
    disability_category = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    highest_educational_level = models.CharField(max_length=200, blank=True, null=True, db_index = True)
    declaration = models.CharField(max_length=800, blank=True, null=True)
    signature = models.CharField(max_length=800, blank=True, null=True)
    current_employment_status = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    post_office_p = models.CharField(max_length=200, blank=True, null=True)
    sub_division = models.CharField(max_length=200, blank=True, null=True)
    revenue_circle= models.CharField(max_length=200, blank=True, null=True)
    police_station_p = models.CharField(max_length=200, blank=True, null=True)
    district_p = models.CharField(max_length=200, blank=True, null=True)
    pin_code_p = models.CharField(max_length=800, blank=True, null=True)
    name_of_the_house_apartment_p = models.CharField(max_length=800, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=800, blank=True, null=True)
    building_no_block_no_p = models.CharField(max_length=800, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city_p = models.CharField(max_length=800, blank=True, null=True)
    police_station = models.CharField(max_length=800, blank=True, null=True)
    same_as_permanent_address = models.CharField(max_length=800, blank=True, null=True)
    name_of_the_house_apartment = models.CharField(max_length=800, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=800, blank=True, null=True)
    building_no_block_no = models.CharField(max_length=800, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city = models.CharField(max_length=800, blank=True, null=True)
    post_office = models.CharField(max_length=800, blank=True, null=True)
    pin_code = models.CharField(max_length=800, blank=True, null=True)
    district = models.CharField(max_length=800, blank=True, null=True)
    employment_exchange = models.CharField(max_length=800, blank=True, null=True, db_index=True)
    lgd_employment_exchange = models.CharField(max_length=800, blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    aadhaar_number_virtual_id = models.CharField(max_length=800, blank=True, null=True)
    full_name_as_in_aadhaar_card = models.CharField(max_length=800, blank=True, null=True)
    highest_examination_passed = models.CharField(max_length=800, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    registration_no = models.CharField(max_length=800, db_index=True)
    religion = models.CharField(max_length=200, blank=True, null=True, db_index = True)
    state = models.CharField(max_length=200, blank=True, null=True)
    education_qualification = models.ManyToManyField(Ex1_Education_Qualification)
    work_experience = models.ManyToManyField(Ex1_Work_Experience)
    skill_qualification = models.ManyToManyField(Ex1_Skill_Qualification)
    other_qualification_training_courses = models.ManyToManyField(Ex1_Other_Qualification_Trainings_Courses)
    # enclosure_details = models.ManyToManyField(Ex_Enclosure_Details)
    languages_known = models.ManyToManyField(Ex1_Languages_Known)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField(blank = True, null = True)
    registration_status = models.CharField(max_length=20, default='Active')
    mail_sent = models.IntegerField(default=0)
    
class Ex1_Additional_Info(models.Model):
    oid = models.CharField( blank=True,null=True, max_length=800)
    department_id = models.CharField( blank=True,null = True, max_length=800)
    department_name = models.CharField( blank=True,null=True, max_length=800)
    service_id = models.CharField( blank=True,null=True, max_length=800)
    service_name = models.CharField( blank=True,null=True, max_length=800)
    appl_id = models.CharField( blank=True,null=True, max_length=800)
    appl_ref_no = models.CharField( blank=True,null=True, max_length=800)
    no_of_attachment = models.CharField( blank=True,null=True, max_length=800)
    submission_mode_id = models.CharField( blank=True,null=True, max_length=800)
    submission_mode = models.CharField( blank=True,null=True, max_length=800)
    applied_by = models.CharField( blank=True,null=True, max_length=800)
    submission_location = models.CharField( blank=True,null=True, max_length=800)
    submission_date = models.DateTimeField( blank=True,null=True, db_index = True)
    payment_mode = models.CharField( blank=True,null=True, max_length=800)
    reference_no = models.CharField( blank=True,null=True, max_length=800)
    payment_date = models.CharField( blank=True,null=True, max_length=800)
    amount = models.CharField( blank=True,null=True, max_length=800)
    registration_id = models.CharField( blank=True,null=True, max_length=800)
    base_service_id = models.CharField( blank=True,null=True, max_length=800, db_index=True)
    version_no = models.CharField( blank=True,null=True, max_length=800)
    sub_version = models.CharField( blank=True,null=True, max_length=800)
    due_date = models.DateField( blank=True,null=True)
    submission_date_str = models.DateField( blank=True,null=True, db_index=True)
    pit = models.CharField( blank=True,null=True, max_length=800)
    pbt = models.CharField( blank=True,null=True, max_length=800)
    dit = models.CharField( blank=True,null=True, max_length=800)
    dbt = models.CharField( blank=True,null=True, max_length=800)
    rit = models.CharField( blank=True,null=True, max_length=800)
    rbt = models.CharField( blank=True,null=True, max_length=800)
    execution_date_str = models.DateField( blank=True,null=True, db_index=True)
    service_timeline = models.CharField( blank=True,null=True, max_length=800)
    appl_status = models.CharField( blank=True,null=True, max_length=800)
    district = models.CharField( blank=True,null=True, max_length=800)
    district_code = models.CharField( blank=True,null=True, max_length=800)
    cin_no = models.CharField( blank=True,null=True, max_length=800)
    govt_charge = models.CharField( blank=True,null=True, max_length=800)
    grn_no = models.CharField( blank=True,null=True, max_length=800)
    service_charge = models.CharField( blank=True,null=True, max_length=800)
    user = models.ForeignKey(Ex1_Applicant, db_index=True, related_query_name="ex1_additional_info", related_name='ex1_additional_info', on_delete=models.CASCADE)
    

class OTPCount(models.Model):
    date = models.DateField(default=timezone.now)
    count_otp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date}: {self.count_otp}"
    
JOBFAIR_STATUS = (
    ('Pending', 'Pending'),
    ('Live', 'Live'),
    ('Closed', 'Closed'),
)
class JobFair(models.Model):
    jobfair_id = models.CharField(primary_key = True, max_length=30)
    sl_id = models.CharField(max_length=30)
    jobfair_type = models.CharField(max_length = 100)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length = 500)
    status = models.CharField(choices = JOBFAIR_STATUS, max_length = 50 )
    location =  models.CharField(max_length = 100)
    jobpost = models.ManyToManyField(JobPost, blank=True)
    candidates_participated = models.ManyToManyField(User, blank=True)
    candidates_shortlisted =  models.ManyToManyField(User, blank=True, related_name='jobfair_shortlisted_candidates')
    candidates_selected =  models.ManyToManyField(User, blank=True, related_name='jobfair_selected_candidates')
    candidates_hired =  models.ManyToManyField(User, blank=True, related_name='jobfair_hired_candidates')



class JobFair_Offline_Event_Data(models.Model):
    jobfair = models.OneToOneField(JobFair, on_delete=models.CASCADE)
    venue = models.CharField(max_length = 100)
    event_date = models.DateField()
    event_time = models.TimeField()
    
class TaskFileMapping(models.Model):
    task_id = models.CharField(primary_key = True, max_length=200)
    file_path = models.CharField(max_length = 2000, default = '')
    user_type = models.CharField(choices=USER_TYPE, max_length=10)
    user_email = models.EmailField(max_length=254)
    
class Employment_Exchange_Performance(models.Model):
    employment_exchange = models.CharField(max_length = 500)
    jobseeker_count = models.IntegerField()
    employer_count = models.IntegerField()
    jobpost_count = models.IntegerField()
    placement_count = models.IntegerField()
    jobseeker_points = models.DecimalField(max_digits=5, decimal_places=2)
    employer_points = models.DecimalField(max_digits=5, decimal_places=2)
    jobpost_points = models.DecimalField(max_digits=5, decimal_places=2)
    placement_points = models.DecimalField(max_digits=5, decimal_places=2)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    
    

class JobFair_Jobpost_Applicant_Details(models.Model):
    jobfair= models.ForeignKey(JobFair, on_delete=models.CASCADE)
    jobpost= models.CharField(max_length=50)
    candidates_applied =  models.ManyToManyField(User, blank=True, related_name='applied_candidates')
    candidates_shortlisted =  models.ManyToManyField(User, blank=True, related_name='shortlisted_candidates')
    candidates_selected =  models.ManyToManyField(User, blank=True, related_name='selected_candidates')
    candidates_hired =  models.ManyToManyField(User, blank=True, related_name='hired_candidates')
    
    
    
    
    
    ##new Employment Exchange Data from NIC through API
class New_Ex_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=300, blank=True,null=True)
    board_university = models.CharField(max_length=300)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=300, blank=True,null=True)
    institution = models.CharField(max_length=300)
    medium = models.CharField(max_length=300)
    course_type = models.CharField( max_length=20)
    admission_year = MonthField(null=True, blank=True)
    pass_year = MonthField(null=True, blank=True)
    stream = models.CharField(max_length=300, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500)
    mark_cert = models.CharField(max_length=500)
    
    
    
class New_Ex_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    doj = models.DateField()
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class New_Ex_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200)
    exam_pass_course = models.CharField( max_length=200)
    duration = models.CharField(max_length=50)
    admission_year = MonthField(null=True, blank=True)
    pass_year = MonthField(null=True, blank=True)
    certificate_provider= models.CharField( max_length=200)
    pass_cert = models.CharField( max_length=500)

    
    
    
class New_Ex_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30)
    
##NEW MIS DATA STORED HERE    
class New_Ex_Applicant(models.Model):
    # applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    # user_name = models.CharField( blank = True, null = True, max_length=800)
    rtps_trans_id = models.CharField(max_length=200)
    applicant_name =models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=800)
    email = models.EmailField(max_length=255, db_index=True)
    applicant_gender = models.CharField(max_length=20, db_index=True)
    date_of_birth = models.DateField(db_index = True)
    caste = models.CharField(max_length=50, db_index=True)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200, db_index = True)
    marital_status = models.CharField(max_length=50)
    prominent_identification_mark = models.CharField(max_length=200)
    whether_exservicemen = models.CharField(max_length=50)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800)
    weight_kgs = models.CharField(max_length=800)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10)
    disability_category = models.CharField(max_length=100, blank=True, null=True, db_index = True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300, db_index = True)
    submission_location = models.CharField(max_length=300)
    registration_no = models.CharField(max_length=50, db_index=True)
    renewal_date = models.DateField()
    date_of_registration = models.DateField()
    current_employment_status = models.CharField(max_length=200, db_index = True)
    current_employment_code = models.CharField(max_length=10)
    nco_code = models.CharField(max_length=30, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=30, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50)
    skill_or_unskill = models.CharField(max_length=50)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200, db_index = True)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800)
    vill_town_ward_city = models.CharField(max_length=800)
    pin_code = models.CharField(max_length=10)
    police_station = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    sub_division = models.CharField(max_length=100)
    revenue_circle= models.CharField(max_length=100)
    residence = models.CharField(max_length=50)
    same_as_permanent_address = models.CharField(max_length=10)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800)
    vill_town_ward_city_p = models.CharField(max_length=800)
    pin_code_p = models.CharField(max_length= 10)
    police_station_p = models.CharField(max_length=200)
    post_office_p = models.CharField(max_length=200)
    district_p = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField()
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    ncsp_id = models.CharField(max_length=50, blank=True, null=True)  
    ncs_api_data_sending_date = models.DateTimeField(blank=True, null=True)
    registration_status = models.CharField(max_length=20, default='Active')
    education_qualification = models.ManyToManyField(New_Ex_Education_Qualification)
    work_experience = models.ManyToManyField(New_Ex_Work_Experience)
    certification = models.ManyToManyField(New_Ex_Addl_Certifications)
    # training_course = models.ManyToManyField(New_Ex_Other_Qualification_Trainings_Courses)
    language = models.ManyToManyField(New_Ex_Language)
    mail_sent = models.IntegerField(default=0)
    def total_experience(self):
        total_years = 0
        total_months = 0

        # Iterate through each work experience associated with the applicant
        for experience in self.work_experience.all():
            # Calculate the experience for each work experience instance
            if experience.end_dt:
                diff = experience.end_dt - experience.doj
            else:
                today = date.today()
                diff = today - experience.doj

            years = diff.days // 365
            remaining_days = diff.days % 365
            months = remaining_days // 30

            # Accumulate the total experience
            total_years += years
            total_months += months

        # Adjust months if they exceed 12
        total_years += total_months // 12
        total_months %= 12

        return total_years, total_months

    
    
class New_Ex_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10, db_index = True)
    service_name = models.CharField(max_length=800)
    appl_id = models.CharField(max_length=30)
    appl_ref_no = models.CharField(max_length=200)
    submission_location = models.CharField(max_length=300)
    submission_date = models.DateTimeField(db_index = True)
    submission_date_str = models.DateField(db_index=True,)
    district = models.CharField(max_length=200)
    execution_date_str = models.DateField(db_index=True)
    user = models.ForeignKey(New_Ex_Applicant, related_query_name="new_ex_additional_info", related_name='new_ex_additional_info', on_delete=models.CASCADE, db_index=True)
    
class New_NIC_API_Fetch_History(models.Model):
    fetch_date = models.DateTimeField(default=timezone.now)
    parameter_date = models.DateField()
    total = models.CharField(max_length=20)
    
class New_JobPortal_Insertion_Fetch_History(models.Model):
    fetch_date = models.DateTimeField(default=timezone.now)
    nic_api_date = models.DateField()
    total = models.CharField(max_length=20)
    count_dp = models.CharField(max_length=5)
    count_consistent = models.CharField(max_length=5)
    
    
class New_Ex1_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=200, blank=True,null=True)
    board_university = models.CharField(max_length=200)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=200, blank=True,null=True)
    institution = models.CharField(max_length=300)
    medium = models.CharField(max_length=200)
    course_type = models.CharField( max_length=20)
    admission_year = MonthField()
    pass_year = MonthField()
    stream = models.CharField(max_length=200, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500)
    mark_cert = models.CharField(max_length=500)
    
    
    
class New_Ex1_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    doj = models.DateField()
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class New_Ex1_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200)
    exam_pass_course = models.CharField( max_length=200)
    duration = models.CharField(max_length=50)
    admission_year = MonthField()
    pass_year = MonthField()
    certificate_provider= models.CharField( max_length=200)
    pass_cert = models.CharField( max_length=500)

    
    
    
class New_Ex1_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30)
    
    
class New_Ex1_Applicant(models.Model):
    # applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    # user_name = models.CharField( blank = True, null = True, max_length=800)
    rtps_trans_id = models.CharField(max_length=200)
    applicant_name =models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=800)
    email = models.EmailField(max_length=255, db_index=True)
    applicant_gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    caste = models.CharField(max_length=50)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=50)
    prominent_identification_mark = models.CharField(max_length=200)
    whether_exservicemen = models.CharField(max_length=50)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800)
    weight_kgs = models.CharField(max_length=800)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10)
    disability_category = models.CharField(max_length=100, blank=True, null=True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300)
    submission_location = models.CharField(max_length=300)
    registration_no = models.CharField(max_length=50)
    renewal_date = models.DateField()
    date_of_registration = models.DateField()
    current_employment_status = models.CharField(max_length=200)
    current_employment_code = models.CharField(max_length=10)
    nco_code = models.CharField(max_length=12, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50)
    skill_or_unskill = models.CharField(max_length=50)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800)
    vill_town_ward_city = models.CharField(max_length=800)
    pin_code = models.CharField(max_length=10)
    police_station = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    sub_division = models.CharField(max_length=100)
    revenue_circle= models.CharField(max_length=100)
    residence = models.CharField(max_length=50)
    same_as_permanent_address = models.CharField(max_length=10)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800)
    vill_town_ward_city_p = models.CharField(max_length=800)
    pin_code_p = models.CharField(max_length= 10)
    police_station_p = models.CharField(max_length=200)
    post_office_p = models.CharField(max_length=200)
    district_p = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField()
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    # already_registered = models.CharField(blank=True, max_length=100)
    education_qualification = models.ManyToManyField(New_Ex1_Education_Qualification)
    work_experience = models.ManyToManyField(New_Ex1_Work_Experience)
    certification = models.ManyToManyField(New_Ex1_Addl_Certifications)
    # training_course = models.ManyToManyField(New_Ex_Other_Qualification_Trainings_Courses)
    language = models.ManyToManyField(New_Ex1_Language)

    
    
class New_Ex1_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10)
    service_name = models.CharField(max_length=800)
    appl_id = models.CharField(max_length=12)
    appl_ref_no = models.CharField(max_length=200)
    submission_location = models.CharField(max_length=300)
    submission_date = models.DateTimeField()
    submission_date_str = models.DateField()
    district = models.CharField(max_length=200)
    execution_date_str = models.DateField()
    user = models.ForeignKey(New_Ex1_Applicant, related_query_name="new_ex1_additional_info", related_name='new_ex1_additional_info', on_delete=models.CASCADE)
    
class New_Ex1_NIC_API_Fetch_History(models.Model):
    fetch_date = models.DateTimeField(default=timezone.now)
    parameter_date = models.DateField()
    total = models.CharField(max_length=20)
    
    
class New_Ex2_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=200, blank=True,null=True)
    board_university = models.CharField(max_length=200)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=200, blank=True,null=True)
    institution = models.CharField(max_length=300)
    medium = models.CharField(max_length=200)
    course_type = models.CharField( max_length=20)
    admission_year = MonthField()
    pass_year = MonthField()
    stream = models.CharField(max_length=200, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500)
    mark_cert = models.CharField(max_length=500)
    
    
    
class New_Ex2_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    doj = models.DateField()
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class New_Ex2_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200)
    exam_pass_course = models.CharField( max_length=200)
    duration = models.CharField(max_length=50)
    admission_year = MonthField()
    pass_year = MonthField()
    certificate_provider= models.CharField( max_length=200)
    pass_cert = models.CharField( max_length=500)

    
    
    
class New_Ex2_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30)
    
    
class New_Ex2_Applicant(models.Model):
    # applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    # user_name = models.CharField( blank = True, null = True, max_length=800)
    rtps_trans_id = models.CharField(max_length=200)
    applicant_name =models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=800)
    email = models.EmailField(max_length=255, db_index=True)
    applicant_gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    caste = models.CharField(max_length=50)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200)
    marital_status = models.CharField(max_length=50)
    prominent_identification_mark = models.CharField(max_length=200)
    whether_exservicemen = models.CharField(max_length=50)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800)
    weight_kgs = models.CharField(max_length=800)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10)
    disability_category = models.CharField(max_length=100, blank=True, null=True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300)
    submission_location = models.CharField(max_length=300)
    registration_no = models.CharField(max_length=50)
    renewal_date = models.DateField()
    date_of_registration = models.DateField()
    current_employment_status = models.CharField(max_length=200)
    current_employment_code = models.CharField(max_length=10)
    nco_code = models.CharField(max_length=12, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50)
    skill_or_unskill = models.CharField(max_length=50)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800)
    vill_town_ward_city = models.CharField(max_length=800)
    pin_code = models.CharField(max_length=10)
    police_station = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    sub_division = models.CharField(max_length=100)
    revenue_circle= models.CharField(max_length=100)
    residence = models.CharField(max_length=50)
    same_as_permanent_address = models.CharField(max_length=10)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800)
    vill_town_ward_city_p = models.CharField(max_length=800)
    pin_code_p = models.CharField(max_length= 10)
    police_station_p = models.CharField(max_length=200)
    post_office_p = models.CharField(max_length=200)
    district_p = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField()
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    # already_registered = models.CharField(blank=True, max_length=100)
    education_qualification = models.ManyToManyField(New_Ex2_Education_Qualification)
    work_experience = models.ManyToManyField(New_Ex2_Work_Experience)
    certification = models.ManyToManyField(New_Ex2_Addl_Certifications)
    # training_course = models.ManyToManyField(New_Ex_Other_Qualification_Trainings_Courses)
    language = models.ManyToManyField(New_Ex2_Language)

    
    
class New_Ex2_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10)
    service_name = models.CharField(max_length=800)
    appl_id = models.CharField(max_length=12)
    appl_ref_no = models.CharField(max_length=200)
    submission_location = models.CharField(max_length=300)
    submission_date = models.DateTimeField()
    submission_date_str = models.DateField()
    district = models.CharField(max_length=200)
    execution_date_str = models.DateField()
    user = models.ForeignKey(New_Ex2_Applicant, related_query_name="new_ex2_additional_info", related_name='new_ex2_additional_info', on_delete=models.CASCADE)
    
class New_Ex2_NIC_API_Fetch_History(models.Model):
    fetch_date = models.DateTimeField(default=timezone.now)
    parameter_date = models.DateField()
    total = models.CharField(max_length=20)
    
    
    
    
class Candidate_Status_Update(models.Model):
    employment_exchange_no = models.CharField(max_length=255, unique=True)
    employment_status = models.CharField(max_length=255)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employment_exchange_no
    
    
    
    
class Employment_Exchange_Wise_Data(models.Model):
    employment_exchange = models.CharField(max_length=255)
    general = models.BigIntegerField()
    obc_mobc = models.BigIntegerField()
    sc = models.BigIntegerField()
    stp = models.BigIntegerField()
    sth = models.BigIntegerField()
    total = models.BigIntegerField()
    
    
    
class Valid_Candidates_Grade3_Grade4(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255)
    full_name = models.CharField(max_length=300)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300)
    mothers_name = models.CharField(max_length=300)
    
    
class Invalid_Candidates_Grade3_Grade4(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    reason = models.CharField(max_length=300, blank=True, null=True)
    
    
class Valid_Candidates_Grade3_Grade4_Improved(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255)
    full_name = models.CharField(max_length=300)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300)
    mothers_name = models.CharField(max_length=300)
    
    
class Invalid_Candidates_Grade3_Grade4_Improved(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    reason = models.CharField(max_length=300, blank=True, null=True)
    
    
    
class Valid_Candidates_Grade3_Grade4_Improved_District(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255)
    full_name = models.CharField(max_length=300)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300)
    mothers_name = models.CharField(max_length=300)
    district = models.CharField(max_length= 200, blank=True, null=True)
    
    
class Invalid_Candidates_Grade3_Grade4_Improved_District(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(max_length= 200, blank=True, null=True)
    reason = models.CharField(max_length=300, blank=True, null=True)
    
    
    
##GRADE3 GRADE4 DATA STORED HERE 
class New_Valid_Candidates_Grade3_Grade4(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255)
    full_name = models.CharField(max_length=300)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300)
    mothers_name = models.CharField(max_length=300)
    district = models.CharField(max_length= 200, blank=True, null=True)
    
    
class New_Invalid_Candidates_Grade3_Grade4(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(max_length= 200, blank=True, null=True)
    reason = models.CharField(max_length=300, blank=True, null=True)   
    
    
class New_Valid_Candidates_Grade3_Grade4_Updated(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255)
    full_name = models.CharField(max_length=300)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300)
    mothers_name = models.CharField(max_length=300)
    district = models.CharField(max_length= 200, blank=True, null=True)
    
    
class New_Invalid_Candidates_Grade3_Grade4_Updated(models.Model):
    sl_id = models.BigIntegerField()
    employment_exchange_no = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=300, blank=True, null=True)
    d_o_b = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=300, blank=True, null=True)
    mothers_name = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(max_length= 200, blank=True, null=True)
    reason = models.CharField(max_length=300, blank=True, null=True)
    
    
    
class Summary_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True,null=True)
    board_university = models.CharField(max_length=300, blank=True, null=True)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=300, blank=True,null=True)
    institution = models.CharField(max_length=300, blank=True, null=True)
    medium = models.CharField(max_length=300, blank=True, null=True)
    course_type = models.CharField( max_length=20, blank=True, null=True)
    admission_year = MonthField(blank=True, null=True)
    pass_year = MonthField(blank=True, null=True)
    stream = models.CharField(max_length=300, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500, blank=True, null=True)
    mark_cert = models.CharField(max_length=500, blank=True, null=True)
    
    
    
class Summary_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300,blank=True, null=True)
    designation = models.CharField(max_length=300, blank=True, null=True)
    doj = models.DateField(blank=True, null=True)
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class Summary_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200, blank=True, null=True)
    exam_pass_course = models.CharField( max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    admission_year = MonthField(blank=True, null=True)
    pass_year = MonthField(blank=True, null=True)
    certificate_provider= models.CharField( max_length=200, blank=True, null=True)
    pass_cert = models.CharField( max_length=500, blank=True, null=True)

    
    
    
class Summary_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30, blank=True, null=True)




class Summary_Applicant(models.Model):
    # applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    # user_name = models.CharField( blank = True, null = True, max_length=800)
    rtps_trans_id = models.CharField(max_length=200, blank = True, null = True)
    applicant_name =models.CharField(max_length=200, blank = True, null = True)
    mobile_number = models.CharField(max_length=800, blank = True, null = True)
    email = models.EmailField(max_length=255, db_index=True, blank = True, null = True,)
    applicant_gender = models.CharField(max_length=20, db_index=True, blank = True, null = True,)
    date_of_birth = models.DateField(blank = True, null = True)
    caste = models.CharField(max_length=50, blank = True, null = True,)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200, blank = True, null = True)
    marital_status = models.CharField(max_length=50, blank = True, null = True)
    prominent_identification_mark = models.CharField(max_length=200, blank = True, null = True)
    whether_exservicemen = models.CharField(max_length=50, blank = True, null = True)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200, blank = True, null = True)
    mothers_name = models.CharField(max_length=200, blank = True, null = True)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800, blank = True, null = True)
    weight_kgs = models.CharField(max_length=800, blank = True, null = True)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10, blank = True, null = True)
    disability_category = models.CharField(max_length=100, blank=True, null=True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300, db_index = True, blank = True, null = True)
    submission_location = models.CharField(max_length=300, blank = True, null = True)
    registration_no = models.CharField(max_length=50, db_index=True, blank = True, null = True)
    renewal_date = models.DateField(blank = True, null = True)
    date_of_registration = models.DateField(blank = True, null = True)
    current_employment_status = models.CharField(max_length=200, blank = True, null = True)
    current_employment_code = models.CharField(max_length=10, blank = True, null = True)
    nco_code = models.CharField(max_length=12, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50, blank=True, null=True)
    skill_or_unskill = models.CharField(max_length=50, blank=True, null=True)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200, blank=True, null=True)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city = models.CharField(max_length=800, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    police_station = models.CharField(max_length=200, blank=True, null=True)
    post_office = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    sub_division = models.CharField(max_length=100, blank=True, null=True)
    revenue_circle= models.CharField(max_length=100, blank=True, null=True)
    same_as_permanent_address = models.CharField(max_length=10, blank=True, null=True)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city_p = models.CharField(max_length=800, blank=True, null=True)
    pin_code_p = models.CharField(max_length= 10, blank=True, null=True)
    police_station_p = models.CharField(max_length=200, blank=True, null=True)
    post_office_p = models.CharField(max_length=200, blank=True, null=True)
    district_p = models.CharField(max_length=100, blank=True, null=True)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField(blank=True, null=True)
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    # already_registered = models.CharField(blank=True, max_length=100)
    education_qualification = models.ManyToManyField(Summary_Education_Qualification)
    work_experience = models.ManyToManyField(Summary_Work_Experience)
    certification = models.ManyToManyField(Summary_Addl_Certifications)
    # training_course = models.ManyToManyField(New_Ex_Other_Qualification_Trainings_Courses)
    language = models.ManyToManyField(Summary_Language)

    
    
class Summary_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10, db_index = True, blank=True, null=True)
    service_name = models.CharField(max_length=800, blank=True, null=True)
    appl_id = models.CharField(max_length=12, blank=True, null=True)
    appl_ref_no = models.CharField(max_length=200, blank=True, null=True)
    submission_location = models.CharField(max_length=300, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    submission_date_str = models.DateField(db_index=True, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    execution_date_str = models.DateField(db_index=True, blank=True, null=True)
    user = models.ForeignKey(Summary_Applicant, related_query_name="summary_additional_info", related_name='summary_additional_info', on_delete=models.CASCADE, db_index=True)
    
    
    
class Trouble_Data_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=300, blank=True,null=True)
    board_university = models.CharField(max_length=300, blank=True, null=True)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=300, blank=True,null=True)
    institution = models.CharField(max_length=300, blank=True, null=True)
    medium = models.CharField(max_length=300, blank=True, null=True)
    course_type = models.CharField( max_length=20, blank=True, null=True)
    admission_year = MonthField(blank=True, null=True)
    pass_year = MonthField(blank=True, null=True)
    stream = models.CharField(max_length=300, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500, blank=True, null=True)
    mark_cert = models.CharField(max_length=500, blank=True, null=True)
    
    
    
class Trouble_Data_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300,blank=True, null=True)
    designation = models.CharField(max_length=300, blank=True, null=True)
    doj = models.DateField(blank=True, null=True)
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class Trouble_Data_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200, blank=True, null=True)
    exam_pass_course = models.CharField( max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    admission_year = MonthField(blank=True, null=True)
    pass_year = MonthField(blank=True, null=True)
    certificate_provider= models.CharField( max_length=200, blank=True, null=True)
    pass_cert = models.CharField( max_length=500, blank=True, null=True)

    
    
    
class Trouble_Data_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30, blank=True, null=True)




class Trouble_Data_Applicant(models.Model):
    # applicant_id = models.CharField(blank = True, null = True, max_length = 20)
    # user_name = models.CharField( blank = True, null = True, max_length=800)
    rtps_trans_id = models.CharField(max_length=200, blank = True, null = True)
    applicant_name =models.CharField(max_length=200, blank = True, null = True)
    mobile_number = models.CharField(max_length=800, blank = True, null = True)
    email = models.EmailField(max_length=255, db_index=True, blank = True, null = True,)
    applicant_gender = models.CharField(max_length=20, db_index=True, blank = True, null = True,)
    date_of_birth = models.DateField(blank = True, null = True)
    caste = models.CharField(max_length=50, blank = True, null = True,)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200, blank = True, null = True)
    marital_status = models.CharField(max_length=50, blank = True, null = True)
    prominent_identification_mark = models.CharField(max_length=200, blank = True, null = True)
    whether_exservicemen = models.CharField(max_length=50, blank = True, null = True)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200, blank = True, null = True)
    mothers_name = models.CharField(max_length=200, blank = True, null = True)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800, blank = True, null = True)
    weight_kgs = models.CharField(max_length=800, blank = True, null = True)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10, blank = True, null = True)
    disability_category = models.CharField(max_length=100, blank=True, null=True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300, db_index = True, blank = True, null = True)
    submission_location = models.CharField(max_length=300, blank = True, null = True)
    registration_no = models.CharField(max_length=50, db_index=True, blank = True, null = True)
    renewal_date = models.DateField(blank = True, null = True)
    date_of_registration = models.DateField(blank = True, null = True)
    current_employment_status = models.CharField(max_length=200, blank = True, null = True)
    current_employment_code = models.CharField(max_length=10, blank = True, null = True)
    nco_code = models.CharField(max_length=12, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50, blank=True, null=True)
    skill_or_unskill = models.CharField(max_length=50, blank=True, null=True)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200, blank=True, null=True)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city = models.CharField(max_length=800, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    police_station = models.CharField(max_length=200, blank=True, null=True)
    post_office = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    sub_division = models.CharField(max_length=100, blank=True, null=True)
    revenue_circle= models.CharField(max_length=100, blank=True, null=True)
    same_as_permanent_address = models.CharField(max_length=10, blank=True, null=True)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800, blank=True, null=True)
    vill_town_ward_city_p = models.CharField(max_length=800, blank=True, null=True)
    pin_code_p = models.CharField(max_length= 10, blank=True, null=True)
    police_station_p = models.CharField(max_length=200, blank=True, null=True)
    post_office_p = models.CharField(max_length=200, blank=True, null=True)
    district_p = models.CharField(max_length=100, blank=True, null=True)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField(blank=True, null=True)
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    # already_registered = models.CharField(blank=True, max_length=100)
    education_qualification = models.ManyToManyField(Trouble_Data_Education_Qualification)
    work_experience = models.ManyToManyField(Trouble_Data_Work_Experience)
    certification = models.ManyToManyField(Trouble_Data_Addl_Certifications)
    # training_course = models.ManyToManyField(New_Ex_Other_Qualification_Trainings_Courses)
    language = models.ManyToManyField(Trouble_Data_Language)

    
    
class Trouble_Data_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10, db_index = True, blank=True, null=True)
    service_name = models.CharField(max_length=800, blank=True, null=True)
    appl_id = models.CharField(max_length=12, blank=True, null=True)
    appl_ref_no = models.CharField(max_length=200, blank=True, null=True)
    submission_location = models.CharField(max_length=300, blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    submission_date_str = models.DateField(db_index=True, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    execution_date_str = models.DateField(db_index=True, blank=True, null=True)
    user = models.ForeignKey(Trouble_Data_Applicant, related_query_name="trouble_data_additional_info", related_name='trouble_data_additional_info', on_delete=models.CASCADE, db_index=True)

  

# Tables to Store count

class Overall_MIS_Count(models.Model):
    datafrom = models.CharField(max_length=255)
    # First registration (f_*) fields
    f_reg_count = models.BigIntegerField(default=0, null=True)
    f_aadhar = models.BigIntegerField(default=0, null=True)
    f_nonaadhar = models.BigIntegerField(default=0, null=True)
    
    # Gender-wise fields
    f_gen_male = models.BigIntegerField(default=0, null=True)
    f_gen_female = models.BigIntegerField(default=0, null=True)
    f_gen_others = models.BigIntegerField(default=0, null=True)
    f_gen_total = models.BigIntegerField(default=0, null=True)

    f_obc_male = models.BigIntegerField(default=0, null=True)
    f_obc_female = models.BigIntegerField(default=0, null=True)
    f_obc_others = models.BigIntegerField(default=0, null=True)
    f_obc_total = models.BigIntegerField(default=0, null=True)

    f_st_p_male = models.BigIntegerField(default=0, null=True)
    f_st_p_female = models.BigIntegerField(default=0, null=True)
    f_st_p_others = models.BigIntegerField(default=0, null=True)
    f_st_p_total = models.BigIntegerField(default=0, null=True)

    f_st_h_male = models.BigIntegerField(default=0, null=True)
    f_st_h_female = models.BigIntegerField(default=0, null=True)
    f_st_h_others = models.BigIntegerField(default=0, null=True)
    f_st_h_total = models.BigIntegerField(default=0, null=True)

    f_sc_male = models.BigIntegerField(default=0, null=True)
    f_sc_female = models.BigIntegerField(default=0, null=True)
    f_sc_others = models.BigIntegerField(default=0, null=True)
    f_sc_total = models.BigIntegerField(default=0, null=True)

    f_male_total = models.BigIntegerField(default=0, null=True)
    f_female_total = models.BigIntegerField(default=0, null=True)
    f_others_total = models.BigIntegerField(default=0, null=True)

    # Re-registration (re_reg_*) fields
    re_reg_reg_count = models.BigIntegerField(default=0, null=True)
    re_reg_aadhar = models.BigIntegerField(default=0, null=True)
    re_reg_nonaadhar = models.BigIntegerField(default=0, null=True)

    re_reg_gen_male = models.BigIntegerField(default=0, null=True)
    re_reg_gen_female = models.BigIntegerField(default=0, null=True)
    re_reg_gen_others = models.BigIntegerField(default=0, null=True)
    re_reg_gen_total = models.BigIntegerField(default=0, null=True)

    re_reg_obc_male = models.BigIntegerField(default=0, null=True)
    re_reg_obc_female = models.BigIntegerField(default=0, null=True)
    re_reg_obc_others = models.BigIntegerField(default=0, null=True)
    re_reg_obc_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_p_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_h_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_total = models.BigIntegerField(default=0, null=True)

    re_reg_sc_male = models.BigIntegerField(default=0, null=True)
    re_reg_sc_female = models.BigIntegerField(default=0, null=True)
    re_reg_sc_others = models.BigIntegerField(default=0, null=True)
    re_reg_sc_total = models.BigIntegerField(default=0, null=True)

    re_reg_male_total = models.BigIntegerField(default=0, null=True)
    re_reg_female_total = models.BigIntegerField(default=0, null=True)
    re_reg_others_total = models.BigIntegerField(default=0, null=True)
    #To Store Old MIS data which are not available in New MIS
    male_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    sth_jobseeker_total = models.BigIntegerField(default=0, null=True)

    # PWD (pwd_*) fields
    pwd_hh_male = models.BigIntegerField(default=0, null=True)
    pwd_hh_female = models.BigIntegerField(default=0, null=True)
    pwd_hh_others = models.BigIntegerField(default=0, null=True)
    pwd_hh_total = models.BigIntegerField(default=0, null=True)

    pwd_mh_male = models.BigIntegerField(default=0, null=True)
    pwd_mh_female = models.BigIntegerField(default=0, null=True)
    pwd_mh_others = models.BigIntegerField(default=0, null=True)
    pwd_mh_total = models.BigIntegerField(default=0, null=True)

    pwd_md_male = models.BigIntegerField(default=0, null=True)
    pwd_md_female = models.BigIntegerField(default=0, null=True)
    pwd_md_others = models.BigIntegerField(default=0, null=True)
    pwd_md_total = models.BigIntegerField(default=0, null=True)

    pwd_oh_male = models.BigIntegerField(default=0, null=True)
    pwd_oh_female = models.BigIntegerField(default=0, null=True)
    pwd_oh_others = models.BigIntegerField(default=0, null=True)
    pwd_oh_total = models.BigIntegerField(default=0, null=True)

    pwd_vh_male = models.BigIntegerField(default=0, null=True)
    pwd_vh_female = models.BigIntegerField(default=0, null=True)
    pwd_vh_others = models.BigIntegerField(default=0, null=True)
    pwd_vh_total = models.BigIntegerField(default=0, null=True)

    pwd_male_total = models.BigIntegerField(default=0, null=True)
    pwd_female_total = models.BigIntegerField(default=0, null=True)
    pwd_others_total = models.BigIntegerField(default=0, null=True)
    pwd_total_total = models.BigIntegerField(default=0, null=True)

    # Age group (age_*) fields
    age_below18_male = models.BigIntegerField(default=0, null=True)
    age_below18_female = models.BigIntegerField(default=0, null=True)
    age_below18_others = models.BigIntegerField(default=0, null=True)
    age_below18_total = models.BigIntegerField(default=0, null=True)

    age_18_24_male = models.BigIntegerField(default=0, null=True)
    age_18_24_female = models.BigIntegerField(default=0, null=True)
    age_18_24_others = models.BigIntegerField(default=0, null=True)
    age_18_24_total = models.BigIntegerField(default=0, null=True)

    age_25_34_male = models.BigIntegerField(default=0, null=True)
    age_25_34_female = models.BigIntegerField(default=0, null=True)
    age_25_34_others = models.BigIntegerField(default=0, null=True)
    age_25_34_total = models.BigIntegerField(default=0, null=True)

    age_35_44_male = models.BigIntegerField(default=0, null=True)
    age_35_44_female = models.BigIntegerField(default=0, null=True)
    age_35_44_others = models.BigIntegerField(default=0, null=True)
    age_35_44_total = models.BigIntegerField(default=0, null=True)

    age_45_54_male = models.BigIntegerField(default=0, null=True)
    age_45_54_female = models.BigIntegerField(default=0, null=True)
    age_45_54_others = models.BigIntegerField(default=0, null=True)
    age_45_54_total = models.BigIntegerField(default=0, null=True)

    age_55_64_male = models.BigIntegerField(default=0, null=True)
    age_55_64_female = models.BigIntegerField(default=0, null=True)
    age_55_64_others = models.BigIntegerField(default=0, null=True)
    age_55_64_total = models.BigIntegerField(default=0, null=True)

    age_above65_male = models.BigIntegerField(default=0, null=True)
    age_above65_female = models.BigIntegerField(default=0, null=True)
    age_above65_others = models.BigIntegerField(default=0, null=True)
    age_above65_total = models.BigIntegerField(default=0, null=True)

    age_male_total = models.BigIntegerField(default=0, null=True)
    age_female_total = models.BigIntegerField(default=0, null=True)
    age_other_total = models.BigIntegerField(default=0, null=True)
    age_total_total = models.BigIntegerField(default=0, null=True)

    # Education (edu_*) fields
    edu_illiterate_male = models.BigIntegerField(default=0, null=True)
    edu_illiterate_female = models.BigIntegerField(default=0, null=True)
    edu_illiterate_others = models.BigIntegerField(default=0, null=True)
    edu_illiterate_total = models.BigIntegerField(default=0, null=True)

    edu_below9_male = models.BigIntegerField(default=0, null=True)
    edu_below9_female = models.BigIntegerField(default=0, null=True)
    edu_below9_others = models.BigIntegerField(default=0, null=True)
    edu_below9_total = models.BigIntegerField(default=0, null=True)

    edu_9pass_male = models.BigIntegerField(default=0, null=True)
    edu_9pass_female = models.BigIntegerField(default=0, null=True)
    edu_9pass_others = models.BigIntegerField(default=0, null=True)
    edu_9pass_total = models.BigIntegerField(default=0, null=True)

    edu_10pass_male = models.BigIntegerField(default=0, null=True)
    edu_10pass_female = models.BigIntegerField(default=0, null=True)
    edu_10pass_others = models.BigIntegerField(default=0, null=True)
    edu_10pass_total = models.BigIntegerField(default=0, null=True)

    edu_12pass_male = models.BigIntegerField(default=0, null=True)
    edu_12pass_female = models.BigIntegerField(default=0, null=True)
    edu_12pass_others = models.BigIntegerField(default=0, null=True)
    edu_12pass_total = models.BigIntegerField(default=0, null=True)
    
    edu_iti_male = models.BigIntegerField(default=0, null=True)
    edu_iti_female = models.BigIntegerField(default=0, null=True)
    edu_iti_others = models.BigIntegerField(default=0, null=True)
    edu_iti_total = models.BigIntegerField(default=0, null=True)

    edu_diploma10_male = models.BigIntegerField(default=0, null=True)
    edu_diploma10_female = models.BigIntegerField(default=0, null=True)
    edu_diploma10_others = models.BigIntegerField(default=0, null=True)
    edu_diploma10_total = models.BigIntegerField(default=0, null=True)
    
    edu_diploma12_male = models.BigIntegerField(default=0, null=True)
    edu_diploma12_female = models.BigIntegerField(default=0, null=True)
    edu_diploma12_others = models.BigIntegerField(default=0, null=True)
    edu_diploma12_total = models.BigIntegerField(default=0, null=True)
    
    edu_diplomapg_male = models.BigIntegerField(default=0, null=True)
    edu_diplomapg_female = models.BigIntegerField(default=0, null=True)
    edu_diplomapg_others = models.BigIntegerField(default=0, null=True)
    edu_diplomapg_total = models.BigIntegerField(default=0, null=True)

    edu_gradaute_male = models.BigIntegerField(default=0, null=True)
    edu_gradaute_female = models.BigIntegerField(default=0, null=True)
    edu_gradaute_others = models.BigIntegerField(default=0, null=True)
    edu_gradaute_total = models.BigIntegerField(default=0, null=True)

    edu_postgraduate_male = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_female = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_others = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_total = models.BigIntegerField(default=0, null=True)

    edu_post_doc_mphill_male = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_female = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_others = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_total = models.BigIntegerField(default=0, null=True)

    edu_male_certificate = models.BigIntegerField(default=0, null=True)
    edu_female_certificate = models.BigIntegerField(default=0, null=True)
    edu_other_certificate = models.BigIntegerField(default=0, null=True)
    edu_total_certificate = models.BigIntegerField(default=0, null=True)
    
    edu_male_total = models.BigIntegerField(default=0, null=True)
    edu_female_total = models.BigIntegerField(default=0, null=True)
    edu_other_total = models.BigIntegerField(default=0, null=True)
    edu_total_total = models.BigIntegerField(default=0, null=True)

    religion_hindu_male = models.BigIntegerField(default=0, null=True)
    religion_hindu_female = models.BigIntegerField(default=0, null=True)
    religion_hindu_others = models.BigIntegerField(default=0, null=True)
    religion_hindu_total = models.BigIntegerField(default=0, null=True)

    religion_islam_male = models.BigIntegerField(default=0, null=True)
    religion_islam_female = models.BigIntegerField(default=0, null=True)
    religion_islam_others = models.BigIntegerField(default=0, null=True)
    religion_islam_total = models.BigIntegerField(default=0, null=True)

    religion_christianity_male = models.BigIntegerField(default=0, null=True)
    religion_christianity_female = models.BigIntegerField(default=0, null=True)
    religion_christianity_others = models.BigIntegerField(default=0, null=True)
    religion_christianity_total = models.BigIntegerField(default=0, null=True)

    religion_jainism_male = models.BigIntegerField(default=0, null=True)
    religion_jainism_female = models.BigIntegerField(default=0, null=True)
    religion_jainism_others = models.BigIntegerField(default=0, null=True)
    religion_jainism_total = models.BigIntegerField(default=0, null=True)

    religion_buddhism_male = models.BigIntegerField(default=0, null=True)
    religion_buddhism_female = models.BigIntegerField(default=0, null=True)
    religion_buddhism_others = models.BigIntegerField(default=0, null=True)
    religion_buddhism_total = models.BigIntegerField(default=0, null=True)

    religion_sikhism_male = models.BigIntegerField(default=0, null=True)
    religion_sikhism_female = models.BigIntegerField(default=0, null=True)
    religion_sikhism_others = models.BigIntegerField(default=0, null=True)
    religion_sikhism_total = models.BigIntegerField(default=0, null=True)

    religion_other_male = models.BigIntegerField(default=0, null=True)
    religion_other_female = models.BigIntegerField(default=0, null=True)
    religion_other_others = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)

    religion_male_total = models.BigIntegerField(default=0, null=True)
    religion_female_total = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)
    religion_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_internship_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_apprentice_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_central_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_state_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_oncontract_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_state_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_central_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_total_total = models.BigIntegerField(default=0, null=True)


    empstatus_dailywage_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_selfemp_with_gov_support_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_selfemp_without_gov_support_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_employed_govt_quasi_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_employed_psu_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_unemployed_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_total_total = models.BigIntegerField(default=0, null=True)
    last_updated = models.DateTimeField(auto_now=True)    

class Emp_ExchangeWise_NewMIS_Count(models.Model):
    # id = models.CharField(max_length=50, primary_key=True)
    emp_exchange_id = models.IntegerField(default=0, null=True, db_index=True)
    emp_exchange_name = models.CharField(max_length=255,db_index=True,blank=True, null=True)
    emp_exchange_zonal = models.IntegerField(default=0, null=True,db_index=True)
    year = models.IntegerField(default=0, null=True,db_index=True)
    month = models.CharField(max_length=255,  db_index=True, blank=True, null=True)
    month_numeric = models.IntegerField(default=0, null=True, db_index=True)
    # First registration (f_*) fields
    f_reg_count = models.BigIntegerField(default=0, null=True)
    f_aadhar = models.BigIntegerField(default=0, null=True)
    f_nonaadhar = models.BigIntegerField(default=0, null=True)
    
    # Gender-wise fields
    f_gen_male = models.BigIntegerField(default=0, null=True)
    f_gen_female = models.BigIntegerField(default=0, null=True)
    f_gen_others = models.BigIntegerField(default=0, null=True)
    f_gen_total = models.BigIntegerField(default=0, null=True)

    f_obc_male = models.BigIntegerField(default=0, null=True)
    f_obc_female = models.BigIntegerField(default=0, null=True)
    f_obc_others = models.BigIntegerField(default=0, null=True)
    f_obc_total = models.BigIntegerField(default=0, null=True)

    f_st_p_male = models.BigIntegerField(default=0, null=True)
    f_st_p_female = models.BigIntegerField(default=0, null=True)
    f_st_p_others = models.BigIntegerField(default=0, null=True)
    f_st_p_total = models.BigIntegerField(default=0, null=True)

    f_st_h_male = models.BigIntegerField(default=0, null=True)
    f_st_h_female = models.BigIntegerField(default=0, null=True)
    f_st_h_others = models.BigIntegerField(default=0, null=True)
    f_st_h_total = models.BigIntegerField(default=0, null=True)

    f_sc_male = models.BigIntegerField(default=0, null=True)
    f_sc_female = models.BigIntegerField(default=0, null=True)
    f_sc_others = models.BigIntegerField(default=0, null=True)
    f_sc_total = models.BigIntegerField(default=0, null=True)

    f_male_total = models.BigIntegerField(default=0, null=True)
    f_female_total = models.BigIntegerField(default=0, null=True)
    f_others_total = models.BigIntegerField(default=0, null=True)

    # Re-registration (re_reg_*) fields
    re_reg_reg_count = models.BigIntegerField(default=0, null=True)
    re_reg_aadhar = models.BigIntegerField(default=0, null=True)
    re_reg_nonaadhar = models.BigIntegerField(default=0, null=True)

    re_reg_gen_male = models.BigIntegerField(default=0, null=True)
    re_reg_gen_female = models.BigIntegerField(default=0, null=True)
    re_reg_gen_others = models.BigIntegerField(default=0, null=True)
    re_reg_gen_total = models.BigIntegerField(default=0, null=True)

    re_reg_obc_male = models.BigIntegerField(default=0, null=True)
    re_reg_obc_female = models.BigIntegerField(default=0, null=True)
    re_reg_obc_others = models.BigIntegerField(default=0, null=True)
    re_reg_obc_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_p_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_h_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_total = models.BigIntegerField(default=0, null=True)

    re_reg_sc_male = models.BigIntegerField(default=0, null=True)
    re_reg_sc_female = models.BigIntegerField(default=0, null=True)
    re_reg_sc_others = models.BigIntegerField(default=0, null=True)
    re_reg_sc_total = models.BigIntegerField(default=0, null=True)

    re_reg_male_total = models.BigIntegerField(default=0, null=True)
    re_reg_female_total = models.BigIntegerField(default=0, null=True)
    re_reg_others_total = models.BigIntegerField(default=0, null=True)

    # PWD (pwd_*) fields
    pwd_hh_male = models.BigIntegerField(default=0, null=True)
    pwd_hh_female = models.BigIntegerField(default=0, null=True)
    pwd_hh_others = models.BigIntegerField(default=0, null=True)
    pwd_hh_total = models.BigIntegerField(default=0, null=True)

    pwd_mh_male = models.BigIntegerField(default=0, null=True)
    pwd_mh_female = models.BigIntegerField(default=0, null=True)
    pwd_mh_others = models.BigIntegerField(default=0, null=True)
    pwd_mh_total = models.BigIntegerField(default=0, null=True)

    pwd_md_male = models.BigIntegerField(default=0, null=True)
    pwd_md_female = models.BigIntegerField(default=0, null=True)
    pwd_md_others = models.BigIntegerField(default=0, null=True)
    pwd_md_total = models.BigIntegerField(default=0, null=True)

    pwd_oh_male = models.BigIntegerField(default=0, null=True)
    pwd_oh_female = models.BigIntegerField(default=0, null=True)
    pwd_oh_others = models.BigIntegerField(default=0, null=True)
    pwd_oh_total = models.BigIntegerField(default=0, null=True)

    pwd_vh_male = models.BigIntegerField(default=0, null=True)
    pwd_vh_female = models.BigIntegerField(default=0, null=True)
    pwd_vh_others = models.BigIntegerField(default=0, null=True)
    pwd_vh_total = models.BigIntegerField(default=0, null=True)

    pwd_male_total = models.BigIntegerField(default=0, null=True)
    pwd_female_total = models.BigIntegerField(default=0, null=True)
    pwd_others_total = models.BigIntegerField(default=0, null=True)
    pwd_total_total = models.BigIntegerField(default=0, null=True)

    # Age group (age_*) fields
    age_below18_male = models.BigIntegerField(default=0, null=True)
    age_below18_female = models.BigIntegerField(default=0, null=True)
    age_below18_others = models.BigIntegerField(default=0, null=True)
    age_below18_total = models.BigIntegerField(default=0, null=True)

    age_18_24_male = models.BigIntegerField(default=0, null=True)
    age_18_24_female = models.BigIntegerField(default=0, null=True)
    age_18_24_others = models.BigIntegerField(default=0, null=True)
    age_18_24_total = models.BigIntegerField(default=0, null=True)

    age_25_34_male = models.BigIntegerField(default=0, null=True)
    age_25_34_female = models.BigIntegerField(default=0, null=True)
    age_25_34_others = models.BigIntegerField(default=0, null=True)
    age_25_34_total = models.BigIntegerField(default=0, null=True)

    age_35_44_male = models.BigIntegerField(default=0, null=True)
    age_35_44_female = models.BigIntegerField(default=0, null=True)
    age_35_44_others = models.BigIntegerField(default=0, null=True)
    age_35_44_total = models.BigIntegerField(default=0, null=True)

    age_45_54_male = models.BigIntegerField(default=0, null=True)
    age_45_54_female = models.BigIntegerField(default=0, null=True)
    age_45_54_others = models.BigIntegerField(default=0, null=True)
    age_45_54_total = models.BigIntegerField(default=0, null=True)

    age_55_64_male = models.BigIntegerField(default=0, null=True)
    age_55_64_female = models.BigIntegerField(default=0, null=True)
    age_55_64_others = models.BigIntegerField(default=0, null=True)
    age_55_64_total = models.BigIntegerField(default=0, null=True)

    age_above65_male = models.BigIntegerField(default=0, null=True)
    age_above65_female = models.BigIntegerField(default=0, null=True)
    age_above65_others = models.BigIntegerField(default=0, null=True)
    age_above65_total = models.BigIntegerField(default=0, null=True)

    age_male_total = models.BigIntegerField(default=0, null=True)
    age_female_total = models.BigIntegerField(default=0, null=True)
    age_other_total = models.BigIntegerField(default=0, null=True)
    age_total_total = models.BigIntegerField(default=0, null=True)

    # Education (edu_*) fields
    edu_illiterate_male = models.BigIntegerField(default=0, null=True)
    edu_illiterate_female = models.BigIntegerField(default=0, null=True)
    edu_illiterate_others = models.BigIntegerField(default=0, null=True)
    edu_illiterate_total = models.BigIntegerField(default=0, null=True)

    edu_below9_male = models.BigIntegerField(default=0, null=True)
    edu_below9_female = models.BigIntegerField(default=0, null=True)
    edu_below9_others = models.BigIntegerField(default=0, null=True)
    edu_below9_total = models.BigIntegerField(default=0, null=True)

    edu_9pass_male = models.BigIntegerField(default=0, null=True)
    edu_9pass_female = models.BigIntegerField(default=0, null=True)
    edu_9pass_others = models.BigIntegerField(default=0, null=True)
    edu_9pass_total = models.BigIntegerField(default=0, null=True)

    edu_10pass_male = models.BigIntegerField(default=0, null=True)
    edu_10pass_female = models.BigIntegerField(default=0, null=True)
    edu_10pass_others = models.BigIntegerField(default=0, null=True)
    edu_10pass_total = models.BigIntegerField(default=0, null=True)

    edu_12pass_male = models.BigIntegerField(default=0, null=True)
    edu_12pass_female = models.BigIntegerField(default=0, null=True)
    edu_12pass_others = models.BigIntegerField(default=0, null=True)
    edu_12pass_total = models.BigIntegerField(default=0, null=True)
    
    edu_iti_male = models.BigIntegerField(default=0, null=True)
    edu_iti_female = models.BigIntegerField(default=0, null=True)
    edu_iti_others = models.BigIntegerField(default=0, null=True)
    edu_iti_total = models.BigIntegerField(default=0, null=True)

    edu_diploma_male = models.BigIntegerField(default=0, null=True)
    edu_diploma_female = models.BigIntegerField(default=0, null=True)
    edu_diploma_others = models.BigIntegerField(default=0, null=True)
    edu_diploma_total = models.BigIntegerField(default=0, null=True)

    edu_gradaute_male = models.BigIntegerField(default=0, null=True)
    edu_gradaute_female = models.BigIntegerField(default=0, null=True)
    edu_gradaute_others = models.BigIntegerField(default=0, null=True)
    edu_gradaute_total = models.BigIntegerField(default=0, null=True)

    edu_postgraduate_male = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_female = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_others = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_total = models.BigIntegerField(default=0, null=True)

    edu_post_doc_mphill_male = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_female = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_others = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_total = models.BigIntegerField(default=0, null=True)

    edu_male_total = models.BigIntegerField(default=0, null=True)
    edu_female_total = models.BigIntegerField(default=0, null=True)
    edu_other_total = models.BigIntegerField(default=0, null=True)
    edu_total_total = models.BigIntegerField(default=0, null=True)

    religion_hindu_male = models.BigIntegerField(default=0, null=True)
    religion_hindu_female = models.BigIntegerField(default=0, null=True)
    religion_hindu_others = models.BigIntegerField(default=0, null=True)
    religion_hindu_total = models.BigIntegerField(default=0, null=True)

    religion_islam_male = models.BigIntegerField(default=0, null=True)
    religion_islam_female = models.BigIntegerField(default=0, null=True)
    religion_islam_others = models.BigIntegerField(default=0, null=True)
    religion_islam_total = models.BigIntegerField(default=0, null=True)

    religion_christianity_male = models.BigIntegerField(default=0, null=True)
    religion_christianity_female = models.BigIntegerField(default=0, null=True)
    religion_christianity_others = models.BigIntegerField(default=0, null=True)
    religion_christianity_total = models.BigIntegerField(default=0, null=True)

    religion_jainism_male = models.BigIntegerField(default=0, null=True)
    religion_jainism_female = models.BigIntegerField(default=0, null=True)
    religion_jainism_others = models.BigIntegerField(default=0, null=True)
    religion_jainism_total = models.BigIntegerField(default=0, null=True)

    religion_buddhism_male = models.BigIntegerField(default=0, null=True)
    religion_buddhism_female = models.BigIntegerField(default=0, null=True)
    religion_buddhism_others = models.BigIntegerField(default=0, null=True)
    religion_buddhism_total = models.BigIntegerField(default=0, null=True)

    religion_sikhism_male = models.BigIntegerField(default=0, null=True)
    religion_sikhism_female = models.BigIntegerField(default=0, null=True)
    religion_sikhism_others = models.BigIntegerField(default=0, null=True)
    religion_sikhism_total = models.BigIntegerField(default=0, null=True)

    religion_other_male = models.BigIntegerField(default=0, null=True)
    religion_other_female = models.BigIntegerField(default=0, null=True)
    religion_other_others = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)

    religion_male_total = models.BigIntegerField(default=0, null=True)
    religion_female_total = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)
    religion_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_internship_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_internship_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_apprentice_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_central_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_central_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_state_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_oncontract_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_state_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_state_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_central_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_central_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_total_total = models.BigIntegerField(default=0, null=True)


    empstatus_dailywage_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_selfemp_with_gov_support_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_with_gov_support_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_selfemp_without_gov_support_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_employed_govt_quasi_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_govt_quasi_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_employed_psu_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_employed_psu_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_unemployed_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_total_total = models.BigIntegerField(default=0, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
class Emp_ExchangeWise_OldMIS_Count(models.Model):
    # id = models.CharField(max_length=50, primary_key=True)
    emp_exchange_id = models.IntegerField(default=0, null=True, db_index=True)
    emp_exchange_name = models.CharField(max_length=255,db_index=True, blank=True, null=True)
    emp_exchange_zonal = models.CharField(max_length=255,db_index=True, blank=True, null=True)
    year = models.IntegerField(default=0, null=True,db_index=True)
    month = models.CharField(max_length=255,  db_index=True, blank=True, null=True)
    month_numeric = models.IntegerField(default=0, null=True, db_index=True)
    # First registration (f_*) fields
    f_reg_count = models.BigIntegerField(default=0, null=True)
    f_aadhar = models.BigIntegerField(default=0, null=True)
    f_nonaadhar = models.BigIntegerField(default=0, null=True)
    
    # Gender-wise fields
    f_gen_male = models.BigIntegerField(default=0, null=True)
    f_gen_female = models.BigIntegerField(default=0, null=True)
    f_gen_others = models.BigIntegerField(default=0, null=True)
    f_gen_total = models.BigIntegerField(default=0, null=True)

    f_obc_male = models.BigIntegerField(default=0, null=True)
    f_obc_female = models.BigIntegerField(default=0, null=True)
    f_obc_others = models.BigIntegerField(default=0, null=True)
    f_obc_total = models.BigIntegerField(default=0, null=True)

    f_st_p_male = models.BigIntegerField(default=0, null=True)
    f_st_p_female = models.BigIntegerField(default=0, null=True)
    f_st_p_others = models.BigIntegerField(default=0, null=True)
    f_st_p_total = models.BigIntegerField(default=0, null=True)

    f_st_h_male = models.BigIntegerField(default=0, null=True)
    f_st_h_female = models.BigIntegerField(default=0, null=True)
    f_st_h_others = models.BigIntegerField(default=0, null=True)
    f_st_h_total = models.BigIntegerField(default=0, null=True)

    f_sc_male = models.BigIntegerField(default=0, null=True)
    f_sc_female = models.BigIntegerField(default=0, null=True)
    f_sc_others = models.BigIntegerField(default=0, null=True)
    f_sc_total = models.BigIntegerField(default=0, null=True)

    f_male_total = models.BigIntegerField(default=0, null=True)
    f_female_total = models.BigIntegerField(default=0, null=True)
    f_others_total = models.BigIntegerField(default=0, null=True)

    # Re-registration (re_reg_*) fields
    re_reg_reg_count = models.BigIntegerField(default=0, null=True)
    re_reg_aadhar = models.BigIntegerField(default=0, null=True)
    re_reg_nonaadhar = models.BigIntegerField(default=0, null=True)

    re_reg_gen_male = models.BigIntegerField(default=0, null=True)
    re_reg_gen_female = models.BigIntegerField(default=0, null=True)
    re_reg_gen_others = models.BigIntegerField(default=0, null=True)
    re_reg_gen_total = models.BigIntegerField(default=0, null=True)

    re_reg_obc_male = models.BigIntegerField(default=0, null=True)
    re_reg_obc_female = models.BigIntegerField(default=0, null=True)
    re_reg_obc_others = models.BigIntegerField(default=0, null=True)
    re_reg_obc_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_p_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_p_total = models.BigIntegerField(default=0, null=True)

    re_reg_st_h_male = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_female = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_others = models.BigIntegerField(default=0, null=True)
    re_reg_st_h_total = models.BigIntegerField(default=0, null=True)

    re_reg_sc_male = models.BigIntegerField(default=0, null=True)
    re_reg_sc_female = models.BigIntegerField(default=0, null=True)
    re_reg_sc_others = models.BigIntegerField(default=0, null=True)
    re_reg_sc_total = models.BigIntegerField(default=0, null=True)

    re_reg_male_total = models.BigIntegerField(default=0, null=True)
    re_reg_female_total = models.BigIntegerField(default=0, null=True)
    re_reg_others_total = models.BigIntegerField(default=0, null=True)
    
    male_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    general_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    obc_mobc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    sc_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    stp_jobseeker_total = models.BigIntegerField(default=0, null=True)
    male_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    female_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    transgender_sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    sth_jobseeker_total = models.BigIntegerField(default=0, null=True)
    

    # PWD (pwd_*) fields
    pwd_hh_male = models.BigIntegerField(default=0, null=True)
    pwd_hh_female = models.BigIntegerField(default=0, null=True)
    pwd_hh_others = models.BigIntegerField(default=0, null=True)
    pwd_hh_total = models.BigIntegerField(default=0, null=True)

    pwd_mh_male = models.BigIntegerField(default=0, null=True)
    pwd_mh_female = models.BigIntegerField(default=0, null=True)
    pwd_mh_others = models.BigIntegerField(default=0, null=True)
    pwd_mh_total = models.BigIntegerField(default=0, null=True)

    pwd_md_male = models.BigIntegerField(default=0, null=True)
    pwd_md_female = models.BigIntegerField(default=0, null=True)
    pwd_md_others = models.BigIntegerField(default=0, null=True)
    pwd_md_total = models.BigIntegerField(default=0, null=True)

    pwd_oh_male = models.BigIntegerField(default=0, null=True)
    pwd_oh_female = models.BigIntegerField(default=0, null=True)
    pwd_oh_others = models.BigIntegerField(default=0, null=True)
    pwd_oh_total = models.BigIntegerField(default=0, null=True)

    pwd_vh_male = models.BigIntegerField(default=0, null=True)
    pwd_vh_female = models.BigIntegerField(default=0, null=True)
    pwd_vh_others = models.BigIntegerField(default=0, null=True)
    pwd_vh_total = models.BigIntegerField(default=0, null=True)

    pwd_male_total = models.BigIntegerField(default=0, null=True)
    pwd_female_total = models.BigIntegerField(default=0, null=True)
    pwd_others_total = models.BigIntegerField(default=0, null=True)
    pwd_total_total = models.BigIntegerField(default=0, null=True)

    # Age group (age_*) fields
    age_below18_male = models.BigIntegerField(default=0, null=True)
    age_below18_female = models.BigIntegerField(default=0, null=True)
    age_below18_others = models.BigIntegerField(default=0, null=True)
    age_below18_total = models.BigIntegerField(default=0, null=True)

    age_18_24_male = models.BigIntegerField(default=0, null=True)
    age_18_24_female = models.BigIntegerField(default=0, null=True)
    age_18_24_others = models.BigIntegerField(default=0, null=True)
    age_18_24_total = models.BigIntegerField(default=0, null=True)

    age_25_34_male = models.BigIntegerField(default=0, null=True)
    age_25_34_female = models.BigIntegerField(default=0, null=True)
    age_25_34_others = models.BigIntegerField(default=0, null=True)
    age_25_34_total = models.BigIntegerField(default=0, null=True)

    age_35_44_male = models.BigIntegerField(default=0, null=True)
    age_35_44_female = models.BigIntegerField(default=0, null=True)
    age_35_44_others = models.BigIntegerField(default=0, null=True)
    age_35_44_total = models.BigIntegerField(default=0, null=True)

    age_45_54_male = models.BigIntegerField(default=0, null=True)
    age_45_54_female = models.BigIntegerField(default=0, null=True)
    age_45_54_others = models.BigIntegerField(default=0, null=True)
    age_45_54_total = models.BigIntegerField(default=0, null=True)

    age_55_64_male = models.BigIntegerField(default=0, null=True)
    age_55_64_female = models.BigIntegerField(default=0, null=True)
    age_55_64_others = models.BigIntegerField(default=0, null=True)
    age_55_64_total = models.BigIntegerField(default=0, null=True)

    age_above65_male = models.BigIntegerField(default=0, null=True)
    age_above65_female = models.BigIntegerField(default=0, null=True)
    age_above65_others = models.BigIntegerField(default=0, null=True)
    age_above65_total = models.BigIntegerField(default=0, null=True)

    age_male_total = models.BigIntegerField(default=0, null=True)
    age_female_total = models.BigIntegerField(default=0, null=True)
    age_other_total = models.BigIntegerField(default=0, null=True)
    age_total_total = models.BigIntegerField(default=0, null=True)

    # Education (edu_*) fields
    edu_illiterate_male = models.BigIntegerField(default=0, null=True)
    edu_illiterate_female = models.BigIntegerField(default=0, null=True)
    edu_illiterate_others = models.BigIntegerField(default=0, null=True)
    edu_illiterate_total = models.BigIntegerField(default=0, null=True)

    edu_below9_male = models.BigIntegerField(default=0, null=True)
    edu_below9_female = models.BigIntegerField(default=0, null=True)
    edu_below9_others = models.BigIntegerField(default=0, null=True)
    edu_below9_total = models.BigIntegerField(default=0, null=True)

    edu_9pass_male = models.BigIntegerField(default=0, null=True)
    edu_9pass_female = models.BigIntegerField(default=0, null=True)
    edu_9pass_others = models.BigIntegerField(default=0, null=True)
    edu_9pass_total = models.BigIntegerField(default=0, null=True)

    edu_10pass_male = models.BigIntegerField(default=0, null=True)
    edu_10pass_female = models.BigIntegerField(default=0, null=True)
    edu_10pass_others = models.BigIntegerField(default=0, null=True)
    edu_10pass_total = models.BigIntegerField(default=0, null=True)

    edu_12pass_male = models.BigIntegerField(default=0, null=True)
    edu_12pass_female = models.BigIntegerField(default=0, null=True)
    edu_12pass_others = models.BigIntegerField(default=0, null=True)
    edu_12pass_total = models.BigIntegerField(default=0, null=True)
    
    edu_iti_male = models.BigIntegerField(default=0, null=True)
    edu_iti_female = models.BigIntegerField(default=0, null=True)
    edu_iti_others = models.BigIntegerField(default=0, null=True)
    edu_iti_total = models.BigIntegerField(default=0, null=True)

    edu_diploma_male = models.BigIntegerField(default=0, null=True)
    edu_diploma_female = models.BigIntegerField(default=0, null=True)
    edu_diploma_others = models.BigIntegerField(default=0, null=True)
    edu_diploma_total = models.BigIntegerField(default=0, null=True)

    edu_gradaute_male = models.BigIntegerField(default=0, null=True)
    edu_gradaute_female = models.BigIntegerField(default=0, null=True)
    edu_gradaute_others = models.BigIntegerField(default=0, null=True)
    edu_gradaute_total = models.BigIntegerField(default=0, null=True)

    edu_postgraduate_male = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_female = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_others = models.BigIntegerField(default=0, null=True)
    edu_postgraduate_total = models.BigIntegerField(default=0, null=True)

    edu_post_doc_mphill_male = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_female = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_others = models.BigIntegerField(default=0, null=True)
    edu_post_doc_mphill_total = models.BigIntegerField(default=0, null=True)

    edu_male_total = models.BigIntegerField(default=0, null=True)
    edu_female_total = models.BigIntegerField(default=0, null=True)
    edu_other_total = models.BigIntegerField(default=0, null=True)
    edu_total_total = models.BigIntegerField(default=0, null=True)

    religion_hindu_male = models.BigIntegerField(default=0, null=True)
    religion_hindu_female = models.BigIntegerField(default=0, null=True)
    religion_hindu_others = models.BigIntegerField(default=0, null=True)
    religion_hindu_total = models.BigIntegerField(default=0, null=True)

    religion_islam_male = models.BigIntegerField(default=0, null=True)
    religion_islam_female = models.BigIntegerField(default=0, null=True)
    religion_islam_others = models.BigIntegerField(default=0, null=True)
    religion_islam_total = models.BigIntegerField(default=0, null=True)

    religion_christianity_male = models.BigIntegerField(default=0, null=True)
    religion_christianity_female = models.BigIntegerField(default=0, null=True)
    religion_christianity_others = models.BigIntegerField(default=0, null=True)
    religion_christianity_total = models.BigIntegerField(default=0, null=True)

    religion_jainism_male = models.BigIntegerField(default=0, null=True)
    religion_jainism_female = models.BigIntegerField(default=0, null=True)
    religion_jainism_others = models.BigIntegerField(default=0, null=True)
    religion_jainism_total = models.BigIntegerField(default=0, null=True)

    religion_buddhism_male = models.BigIntegerField(default=0, null=True)
    religion_buddhism_female = models.BigIntegerField(default=0, null=True)
    religion_buddhism_others = models.BigIntegerField(default=0, null=True)
    religion_buddhism_total = models.BigIntegerField(default=0, null=True)

    religion_sikhism_male = models.BigIntegerField(default=0, null=True)
    religion_sikhism_female = models.BigIntegerField(default=0, null=True)
    religion_sikhism_others = models.BigIntegerField(default=0, null=True)
    religion_sikhism_total = models.BigIntegerField(default=0, null=True)

    religion_other_male = models.BigIntegerField(default=0, null=True)
    religion_other_female = models.BigIntegerField(default=0, null=True)
    religion_other_others = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)

    religion_male_total = models.BigIntegerField(default=0, null=True)
    religion_female_total = models.BigIntegerField(default=0, null=True)
    religion_other_total = models.BigIntegerField(default=0, null=True)
    religion_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_apprentice_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_apprentice_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_state_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_state_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_private_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_fulltime_oncontract_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_fulltime_oncontract_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_parttime_private_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_parttime_private_total_total = models.BigIntegerField(default=0, null=True)


    empstatus_dailywage_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_dailywage_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_selfemp_without_gov_support_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_selfemp_without_gov_support_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_unemployed_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_unemployed_total_total = models.BigIntegerField(default=0, null=True)

    empstatus_male_total = models.BigIntegerField(default=0, null=True)
    empstatus_female_total = models.BigIntegerField(default=0, null=True)
    empstatus_other_total = models.BigIntegerField(default=0, null=True)
    empstatus_total_total = models.BigIntegerField(default=0, null=True)
    last_updated = models.DateTimeField(auto_now=True)
      
#------------------------------------------------------EMI MODULE MODELS----------------------------------------------------------------------------

# Create your models here.
class ER1_report(models.Model):
    serial_no = models.CharField(max_length=50, primary_key=True)
    selected_quarter_user= models.CharField(max_length=255)
    #page-1--> Employement
    emp_name = models.CharField(max_length=500)
    emp_address =  models.CharField(max_length=500)
    emp_nature_of_bussiness  = models.CharField(max_length=500)
    office_type = models.CharField(max_length=500)
    men_previous_quarter = models.IntegerField()
    men_current_quarter = models.IntegerField()
    women_previous_quarter = models.IntegerField()
    women_current_quarter = models.IntegerField()
    total_previous_quarter = models.IntegerField()
    total_current_quarter = models.IntegerField()
    emp_reason = models.TextField(blank=True, null=True)
    #page-2--> Vacancies
    vacancy_occured_purview = models.IntegerField()
    vacancy_emp_exchange_purview = models.CharField(max_length=150)
    vacancy_filled_purview = models.IntegerField()
    vacancy_source_purview = models.CharField(max_length=200)
    vacancy_reason_for_not_notifying  = models.TextField(blank=True, null=True)
    #page-3--> Manpower shortages
    dif_occupations = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=50)
    date = models.DateField()
    signature_upload = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return self.serial_no


class ManpowerShortage(models.Model):
    er1_report = models.ForeignKey(ER1_report, on_delete=models.CASCADE, related_name='manpower_shortages')
    mp_shortage_occupation = models.CharField(max_length=250, blank=True, null=True)
    mp_essential_qual = models.CharField(max_length=500, blank=True, null=True)
    mp_essential_exp = models.CharField(max_length=100, blank=True, null=True)
    mp_exp_not = models.CharField(max_length=50, blank=True, null=True)
    

class ER2Report(models.Model):
    employer_name = models.CharField(max_length=255)
    employer_address = models.CharField(max_length=255)
    nature_of_business = models.CharField(max_length=255)
    total_employees = models.IntegerField()
    submission_date = models.DateField(auto_now_add=True)
    district = models.CharField(max_length=50)
    total_men = models.IntegerField()
    total_women = models.IntegerField()
    grand_total = models.IntegerField()
    total_approx_vacancies = models.IntegerField()
    signature_upload = models.ImageField(upload_to='signatures/', blank=True, null=True)
    officer_entered_date = models.DateField(max_length=50)


class ER2_table(models.Model):
    report = models.ForeignKey(ER2Report, on_delete=models.CASCADE, related_name='occupations')
    occupation = models.CharField(max_length=255)
    men = models.IntegerField()
    women = models.IntegerField()
    total = models.IntegerField()
    approx_vacancies = models.IntegerField()

class emi_statement(models.Model):  
    id = models.AutoField(primary_key=True)
    annexure = models.CharField(max_length=500)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.DateField()
    calendar_year = models.IntegerField()
    final_submit_status = models.IntegerField(default=0)  # New field with default value
    submitted_quarter = models.CharField(max_length=100,blank=True,null= True)

    def __str__(self):
        return f"{self.annexure} - {self.district}"

class emi_statement_fields(models.Model):
    statement = models.ForeignKey(emi_statement, on_delete=models.CASCADE, related_name='nic_data')
    quarter_ended_on = models.CharField(max_length=500)
    previous_quart_ended_on = models.CharField(max_length=500)
    current_quart_ended_on = models.CharField(max_length=500)
    nic_code = models.CharField(max_length=15)
    addressed = models.IntegerField()
    responded = models.IntegerField()
    previous_quart_total  = models.CharField(max_length=20)
    previous_quart_woman  = models.CharField(max_length=20)
    current_quart_total = models.CharField(max_length=20)
    current_quart_woman = models.CharField(max_length=20)
    tot_diff_btn_col_4_6 = models.CharField(max_length=10)
    tot_diff_btn_col_5_7= models.CharField(max_length=10)
    est_emp_def_est_inc_6_7= models.IntegerField()
    reason_for_sign_var_col_8_9 = models.TextField()
    remarks= models.TextField()

    def __str__(self):
        return f"{self.nic_code} - {self.quarter_ended_on}"
    
#-------------------------------------Activities Status Module-----------------------------------------------------------------


class activity_status_module_data(models.Model):
    date = models.DateField()
    district = models.CharField(max_length=50)
    dee_name= models.CharField(max_length=200)
    # Vocational Guidance and career Councelling for Individuals
    participants_individuals = models.IntegerField()
    # Vocational Guidance and career Councelling for Offices
    no_of_voc_guidance_office_dis = models.IntegerField()
    participants_office = models.IntegerField()
    # Vocational Guidance and career Councelling for Educational Insititutions
    no_of_voc_guidance_edu_dis = models.IntegerField()
    participants_edu = models.IntegerField()
    educational_institution_edu = models.CharField(max_length=200)
    # Recruitment Drive yearly
    calendar_year = models.IntegerField()
    # placement drive monthly
    month_pdm = models.CharField(max_length=20) # we can set input to take value upto 12
    no_placemnet_pdm = models.IntegerField()
    # Issue of certificate of people of assam
    no_of_cert_issued = models.IntegerField(default=0)
    cert_issued_month_name = models.CharField(max_length=85)
    # Inspection of Establishment
    no_of_est_visited = models.IntegerField(default=0)
    est_last_month_name = models.CharField(max_length=85)
    # Emi report Collection
    submitted_on_es1= models.DateField()
    not_submitted_es1 = models.CharField(max_length=500)
    Reason_for_non_submission_es1 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es1 = models.CharField(max_length=500,null=True,blank=True)
    #-------
    submitted_on_es2= models.DateField(null=True,blank=True)
    not_submitted_es2 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es2 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es2 = models.CharField(max_length=500,null=True,blank=True)
    #-------
    submitted_on_es3 = models.DateField(null=True,blank=True)
    not_submitted_es3 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es3 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es3 = models.CharField(max_length=500,null=True,blank=True)
    #--------
    submitted_on_es4= models.DateField(null=True,blank=True)
    not_submitted_es4 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es4 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es4 = models.CharField(max_length=500,null=True,blank=True)
    #---------
    submitted_on_es5_p1= models.DateField(null=True,blank=True)
    not_submitted_es5_p1 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es5_p1 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es5_p1 = models.CharField(max_length=500,null=True,blank=True)
    #--------
    submitted_on_es5_p2= models.DateField(null=True,blank=True)
    not_submitted_es5_p2 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es5_p2 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es5_p2 = models.CharField(max_length=500,null=True,blank=True)
    #--------
    submitted_on_es6= models.DateField(null=True,blank=True)
    not_submitted_es6 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es6 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es6 = models.CharField(max_length=500,null=True,blank=True)
    #--------
    submitted_on_es7= models.DateField(null=True,blank=True)
    not_submitted_es7 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es7 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es7 = models.CharField(max_length=500,null=True,blank=True)
    #--------
    submitted_on_es8= models.DateField(null=True,blank=True)
    not_submitted_es8 = models.CharField(max_length=500,null=True,blank=True)
    Reason_for_non_submission_es8 = models.CharField(max_length=500,null=True,blank=True)
    remarks_es8 = models.CharField(max_length=500,null=True,blank=True)


    @classmethod
    def generate_new_id(cls):
        max_id = cls.objects.aggregate(max_id=Max('id'))['max_id']
        new_id = max_id + 1 if max_id is not None else 1
        return new_id

     # Combine individual, office, and educational campus guidance sums into a single query for department login
    @classmethod
    def state_participants_sums(cls):
        return cls.objects.aggregate(
            participants_individuals_sum=Sum('participants_individuals'),
            participants_office_sum=Sum('participants_office'),
            participants_edu_sum=Sum('participants_edu')
        )
    # For individual Guidance
    @classmethod
    def state_participants_sum_indi(cls):
        return cls.objects.aggregate(participants_individuals_sum=Sum('participants_individuals'))['participants_individuals_sum']

    # For Office campus Guidance

    @classmethod
    def state_participants_sum_ofc(cls):
        return cls.objects.aggregate(participants_office_sum=Sum('participants_office'))['participants_office_sum']


    # For Educational campus Guidance
    @classmethod
    def state_participants_sum_edu(cls):
        return cls.objects.aggregate(participants_edu_sum=Sum('participants_edu'))['participants_edu_sum']

    @classmethod
    def district_participants_sum(cls, district):
        result = cls.objects.filter(district=district).aggregate(
            participants_office_sum=Sum('participants_office'),
            participants_edu_sum=Sum('participants_edu'),
            participants_individuals_sum=Sum('participants_individuals')  
        )
        return result
    
    # For individual Guidance
   
    @classmethod
    def state_participants_sum_indi(cls):
        return cls.objects.aggregate(participants_individuals_sum=Sum('participants_individuals'))['participants_individuals_sum']

    # For Office campus Guidance
    
    @classmethod
    def state_participants_sum_ofc(cls):
        return cls.objects.aggregate(participants_office_sum=Sum('participants_office'))['participants_office_sum']

    

    @classmethod
    def state_participants_sum_edu(cls):
        return cls.objects.aggregate(participants_edu_sum=Sum('participants_edu'))['participants_edu_sum']

    # @classmethod
    # def dis_voc_count(cls, district):
    #     voc_count = cls.objects.filter(district=district).count()
    #     new_voc_count = voc_count + 1
    #     return new_voc_count
    

    @classmethod
    def dis_voc_count(cls, district, month, year):
        # Filter records by district, month_pdm, and year
        filtered_records = cls.objects.filter(district=district,month_pdm=month,date__year=year)
        new_voc_count = filtered_records.aggregate(Sum('no_of_voc_guidance_office_dis'))['no_of_voc_guidance_office_dis__sum']
        print(f"Filtered records for District: {district}, Month: {month}, Year: {year}")
        for record in filtered_records:
            print(f"Record ID: {record.id}, District: {record.district}, Month: {record.month_pdm}, Year: {record.date.year}, Participants: {record.participants_individuals}")

        print(new_voc_count)
        return new_voc_count

    

    
  
class rdf_year(models.Model):
    date = models.DateField()
    dee_name = models.CharField(max_length=200)
    calendar_year = models.IntegerField()
    first_quarter = models.IntegerField(default=0)
    second_quarter = models.IntegerField(default=0)
    third_quarter = models.IntegerField(default=0)
    fourth_quarter = models.IntegerField(default=0)
    district = models.CharField(max_length=50)


    @classmethod
    def generate_new_id(cls):
        # Increment the max ID value atomically using F expressions
        max_id = cls.objects.aggregate(max_id=Max('id'))['max_id']
        new_id = max_id + 1 if max_id is not None else 1
        return new_id
    
#-----------------------------------------------------Zonal part--------------------------------------------------------------------------------------------------------------------------

class inspection_of_establishments(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    zone = models.CharField(max_length=200)
    emp_exchange = models.CharField(max_length=200)
    est_visited_by_ade = models.IntegerField()
    est_visited_by_dde = models.IntegerField()
    est_visited_by_ade_month_name = models.CharField(max_length=200)
    est_visited_by_dde_month_name = models.CharField(max_length=200)
    est_visited_by_ade_dde_year = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name_of_officer} ({self.zone}) - {self.date}"



class inspection_of_dee(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    zone = models.CharField(max_length=200)
    name_of_officer = models.CharField(max_length=200)
    number_of_inspection = models.IntegerField()
    quarter = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name_of_officer} ({self.zone}) - {self.date}"

#--------------------------------------------------------------------NCS API MAPPING MODELS------------------------------------------------

class District_ncs(models.Model):
    district_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Castes_ncs(models.Model):
    ncs_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class religion_ncs(models.Model):
    religion_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Marital_status_ncs(models.Model):
    ncs_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    marital_id = models.CharField(max_length=5)

class gender_ncs(models.Model):
    ncs_name = models.CharField(max_length=15)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class major_spec_ncs(models.Model):
    spec_id = models.CharField(max_length=20)
    ncs_name = models.CharField(max_length=150)
    education_id = models.CharField(max_length=50)

    def __str__(self):
        return self.ncs_name

class Emp_status_ncs(models.Model):
    emp_id = models.CharField(max_length=20)
    ncs_name = models.CharField(max_length=50)

    def __str__(self):
        return self.ncs_name

class territory_type_ncs(models.Model):
    ncs_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class hig_edu_level_ncs(models.Model):
    high_ed_id = models.CharField(max_length=10)
    ncs_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class co_nature_ncs(models.Model):
    cona_id = models.CharField(max_length=10)
    ncs_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class edu_quali_ncs(models.Model):
    edu_id = models.CharField(max_length=10)
    ncs_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.edu_id} - {self.ncs_name}"


class medium_ncs(models.Model):
    med_id = models.CharField(max_length=10)
    ncs_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.med_id} - {self.ncs_name}"

#------------------------------------------------------------SEPERATE TABLES-----------------------------------------------------
	
	
    ##new Employment Exchange Data from NIC through API
class Dee_Guwahati_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=300, blank=True,null=True)
    board_university = models.CharField(max_length=300)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=300, blank=True,null=True)
    institution = models.CharField(max_length=300)
    medium = models.CharField(max_length=300)
    course_type = models.CharField( max_length=20)
    admission_year = MonthField()
    pass_year = MonthField()
    stream = models.CharField(max_length=300, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500)
    mark_cert = models.CharField(max_length=500)
    
    
    
class Dee_Guwahati_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    doj = models.DateField()
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class Dee_Guwahati_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200)
    exam_pass_course = models.CharField( max_length=200)
    duration = models.CharField(max_length=50)
    admission_year = MonthField()
    pass_year = MonthField()
    certificate_provider= models.CharField( max_length=200)
    pass_cert = models.CharField( max_length=500)
 
    
class Dee_Guwahati_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30)

class Dee_Guwahati(models.Model):
    old_status = models.IntegerField(default=0)
    old_ex_id = models.IntegerField(blank=True, null=True,db_index = True)
    new_ex_id = models.IntegerField(blank=True, null=True,db_index = True)
    rtps_trans_id = models.CharField(max_length=200,blank=True, null=True)
    applicant_name =models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=800)
    email = models.EmailField(max_length=255, db_index=True)
    applicant_gender = models.CharField(max_length=20, db_index=True)
    date_of_birth = models.DateField(db_index = True,blank=True, null=True)
    caste = models.CharField(max_length=50, db_index=True)
    economically_weaker_section = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=200, db_index = True)
    marital_status = models.CharField(max_length=50)
    prominent_identification_mark = models.CharField(max_length=200)
    whether_exservicemen = models.CharField(max_length=50)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800)
    weight_kgs = models.CharField(max_length=800)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=50)
    disability_category = models.CharField(max_length=100, blank=True, null=True, db_index = True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300, db_index = True)
    submission_location = models.CharField(max_length=300,blank=True, null=True)
    registration_no = models.CharField(max_length=50, db_index=True)
    renewal_date = models.DateField(blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)
    current_employment_status = models.CharField(max_length=200, db_index = True)
    current_employment_code = models.CharField(max_length=10,blank=True, null=True)
    nco_code = models.CharField(max_length=30, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=30, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=500)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50,blank=True, null=True)
    skill_or_unskill = models.CharField(max_length=50,blank=True, null=True)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200, db_index = True)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800)
    vill_town_ward_city = models.CharField(max_length=800)
    pin_code = models.CharField(max_length=10)
    police_station = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    sub_division = models.CharField(max_length=100)
    revenue_circle= models.CharField(max_length=100)
    residence = models.CharField(max_length=50,blank=True, null=True)
    same_as_permanent_address = models.CharField(max_length=50)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800)
    vill_town_ward_city_p = models.CharField(max_length=800)
    pin_code_p = models.CharField(max_length= 10)
    police_station_p = models.CharField(max_length=200)
    post_office_p = models.CharField(max_length=200)
    district_p = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField(blank=True, null=True,db_index = True)
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    ncsp_id = models.CharField(max_length=50, blank=True, null=True)  
    ncs_api_data_sending_date = models.DateTimeField(blank=True, null=True)
    education_qual = models.ManyToManyField(Dee_Guwahati_Education_Qualification)
    work_exp = models.ManyToManyField(Dee_Guwahati_Work_Experience)
    certi = models.ManyToManyField(Dee_Guwahati_Addl_Certifications)
    lang = models.ManyToManyField(Dee_Guwahati_Language)
    
    def total_experience(self):
        total_years = 0
        total_months = 0

        # Iterate through each work experience associated with the applicant
        for experience in self.work_experience.all():
            # Calculate the experience for each work experience instance
            if experience.end_dt:
                diff = experience.end_dt - experience.doj
            else:
                today = date.today()
                diff = today - experience.doj

            years = diff.days // 365
            remaining_days = diff.days % 365
            months = remaining_days // 30

            # Accumulate the total experience
            total_years += years
            total_months += months

        # Adjust months if they exceed 12
        total_years += total_months // 12
        total_months %= 12

        return total_years, total_months
    
class Dee_Guwahati_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10, db_index = True)
    service_name = models.CharField(max_length=800)
    appl_id = models.CharField(max_length=30)
    appl_ref_no = models.CharField(max_length=200)
    submission_location = models.CharField(max_length=300)
    submission_date = models.DateTimeField(db_index = True)
    submission_date_str = models.DateField(db_index=True,)
    district = models.CharField(max_length=200)
    execution_date_str = models.DateField(db_index=True)
    user_old = models.IntegerField(blank=True, null=True,db_index = True)
    user_new = models.IntegerField(blank=True, null=True,db_index = True)
    
    
#------------------------------ORM CHECK---

class orm_dee_guwahati_Education_Qualification(models.Model):
    qualification = models.CharField(max_length=50)
    course = models.CharField(max_length=300, blank=True,null=True)
    board_university = models.CharField(max_length=300)
    subjects  = models.TextField(null=True, blank=True)
    other_subject = models.TextField(null=True, blank=True)
    major_specialization = models.CharField(max_length=300, blank=True,null=True)
    institution = models.CharField(max_length=300)
    medium = models.CharField(max_length=300)
    course_type = models.CharField( max_length=20)
    admission_year = MonthField()
    pass_year = MonthField()
    stream = models.CharField(max_length=300, blank=True,null=True)
    percentage_grade = models.CharField(max_length=50, blank=True,null=True)
    percentage = models.FloatField(blank=True,null=True)
    pass_cert = models.CharField(max_length=500)
    mark_cert = models.CharField(max_length=500)
    
    
    
class orm_dee_guwahati_Work_Experience(models.Model):
    org_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    doj = models.DateField()
    end_dt = models.DateField(blank=True,null=True) 
    gross_sal = models.CharField(max_length=10, blank=True,null=True)
    notice_period = models.CharField( blank=True,null=True, max_length=100)
    work_location = models.CharField( blank=True,null=True, max_length=100)
    nature_of_work = models.CharField( blank=True,null=True, max_length=100)
    job_profile = models.CharField( blank=True,null=True, max_length=3000)
        
class orm_dee_guwahati_Addl_Certifications(models.Model):
    category = models.CharField(max_length=200)
    exam_pass_course = models.CharField( max_length=200)
    duration = models.CharField(max_length=50)
    admission_year = MonthField()
    pass_year = MonthField()
    certificate_provider= models.CharField( max_length=200)
    pass_cert = models.CharField( max_length=500)

    
    
    
class orm_dee_guwahati_Language(models.Model):
    language = models.CharField(max_length=200)
    r_option = models.CharField(max_length=20, blank=True,null=True,)
    w_option = models.CharField(max_length=20,blank=True,null=True,)
    s_option = models.CharField(max_length=20,blank=True,null=True,)
    proficiency = models.CharField(max_length=30)
    
   
class orm_dee_guwahati(models.Model):
    rtps_trans_id = models.CharField(max_length=200)
    applicant_name =models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=800)
    email = models.EmailField(max_length=255, db_index=True)
    applicant_gender = models.CharField(max_length=20, db_index=True)
    date_of_birth = models.DateField(db_index = True)
    caste = models.CharField(max_length=50, db_index=True)
    economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
    religion = models.CharField(max_length=200, db_index = True)
    marital_status = models.CharField(max_length=50)
    prominent_identification_mark = models.CharField(max_length=200)
    whether_exservicemen = models.CharField(max_length=50)
    category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
    fathers_name = models.CharField(max_length=200)
    mothers_name = models.CharField(max_length=200)
    fathers_name_guardians_name = models.CharField(blank=True, null=True, max_length=200)
    height_in_cm = models.CharField(max_length=800)
    weight_kgs = models.CharField(max_length=800)
    eye_sight= models.CharField(max_length=800, blank=True, null=True)
    chest_inch = models.CharField(max_length=800, blank=True, null=True)
    are_you_differently_abled_pwd = models.CharField(max_length=10)
    disability_category = models.CharField(max_length=100, blank=True, null=True, db_index = True)
    additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
    disability_percentage = models.CharField(max_length=100, blank=True, null=True)
    employment_exchange = models.CharField(max_length=300, db_index = True)
    submission_location = models.CharField(max_length=300)
    registration_no = models.CharField(max_length=50, db_index=True)
    renewal_date = models.DateField()
    date_of_registration = models.DateField()
    current_employment_status = models.CharField(max_length=200, db_index = True)
    current_employment_code = models.CharField(max_length=10)
    nco_code = models.CharField(max_length=30, blank=True, null=True)
    govt_suppt_type = models.CharField(max_length=30, blank=True, null=True)
    other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
    self_emp_type = models.CharField(max_length=200, blank=True, null=True)
    specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
    is_below_18 = models.CharField(max_length=50, blank=True, null=True)
    state_work_location = models.CharField(max_length=100, blank=True, null=True)
    country_work_location = models.CharField(max_length=200, blank=True, null=True)
    state_only_domicile_of_assam_can_apply = models.CharField(max_length=50, blank=True, null=True)
    rereg_type = models.CharField(blank=True, null=True, max_length=200)
    type_of_re_reg = models.CharField(blank=True, null=True, max_length=10)
    old_appl_ref_no = models.CharField(blank=True, null=True, max_length=200)
    fresher_experience_sts = models.CharField(max_length=50)
    skill_or_unskill = models.CharField(max_length=50)
    job_preference_key_skills = models.TextField(null=True, blank=True)
    email_verify_status = models.CharField(max_length=10, null=True, blank=True)
    aadhaar_verify_status = models.CharField(max_length=10, null=True, blank=True)
    mobile_verify_status = models.CharField(max_length=10, null=True, blank=True)
    highest_educational_level = models.CharField(max_length=200, db_index = True)
    highest_educational_level_id = models.CharField(max_length=10, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    name_of_the_house_apartment = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc = models.CharField(max_length=800)
    vill_town_ward_city = models.CharField(max_length=800)
    pin_code = models.CharField(max_length=10)
    police_station = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    sub_division = models.CharField(max_length=100)
    revenue_circle= models.CharField(max_length=100)
    residence = models.CharField(max_length=50)
    same_as_permanent_address = models.CharField(max_length=10)
    name_of_the_house_apartment_p = models.CharField(max_length=200, blank=True, null=True)
    house_no_apartment_no_p = models.CharField(max_length=200, blank=True, null=True)
    address_locality_street_etc_p = models.CharField(max_length=800)
    vill_town_ward_city_p = models.CharField(max_length=800)
    pin_code_p = models.CharField(max_length= 10)
    police_station_p = models.CharField(max_length=200)
    post_office_p = models.CharField(max_length=200)
    district_p = models.CharField(max_length=100)
    insert_date = models.DateField(auto_now_add=True)
    nic_api_date = models.DateField()
    other_qualification = models.CharField(max_length=50, blank=True, null=True)
    is_diploma_checked = models.CharField(max_length=10, blank=True, null=True)
    is_iti_checked = models.CharField(max_length=10, blank=True, null=True)
    addl_cert = models.CharField(max_length=10, blank=True, null=True)
    ncsp_id = models.CharField(max_length=50, blank=True, null=True)  
    ncs_api_data_sending_date = models.DateTimeField(blank=True, null=True)
    education_qualification_django = models.ManyToManyField(orm_dee_guwahati_Education_Qualification)
    work_experience_django = models.ManyToManyField(orm_dee_guwahati_Work_Experience)
    certification_django = models.ManyToManyField(orm_dee_guwahati_Addl_Certifications)
    language_django = models.ManyToManyField(orm_dee_guwahati_Language)
    
    def total_experience(self):
        total_years = 0
        total_months = 0

        # Iterate through each work experience associated with the applicant
        for experience in self.work_experience.all():
            # Calculate the experience for each work experience instance
            if experience.end_dt:
                diff = experience.end_dt - experience.doj
            else:
                today = date.today()
                diff = today - experience.doj

            years = diff.days // 365
            remaining_days = diff.days % 365
            months = remaining_days // 30

            # Accumulate the total experience
            total_years += years
            total_months += months

        # Adjust months if they exceed 12
        total_years += total_months // 12
        total_months %= 12

        return total_years, total_months

    
    
class orm_dee_guwahati_Additional_Info(models.Model):
    service_id = models.CharField(max_length=10, db_index = True)
    service_name = models.CharField(max_length=800)
    appl_id = models.CharField(max_length=30)
    appl_ref_no = models.CharField(max_length=200)
    submission_location = models.CharField(max_length=300)
    submission_date = models.DateTimeField(db_index = True)
    submission_date_str = models.DateField(db_index=True,)
    district = models.CharField(max_length=200)
    execution_date_str = models.DateField(db_index=True)
    user = models.ForeignKey(orm_dee_guwahati, related_query_name="orm_dee_guwahati_additional_info", related_name='orm_dee_guwahati_additional_info', on_delete=models.CASCADE, db_index=True)
    

#------------------------------models for career counselling-----------------------------------------------------------------------------------------
#-----commeneted
# USER_TYPE_counsellor = (
#     ('JS', 'Job Seeker'),
#     ('RR', 'Recruiter'),
#     ('RA', 'Recruiter Admin'),
#     ('AA', 'Agency Admin'),   #Consultancy
#     ('AR', 'Agency Recruiter'),
#     ('DEE', 'DistrictEmploymentExchange'),
#     ('D', 'Department'),
#     ('Zonal', 'ZonalUser'),
#     ('GUSER', 'GuestUser'),
# 	('CS', 'counsellor'),
# )


# MARTIAL_STATUS_counsellor = (
#     ('Single', 'Single'),
#     ('Married', 'Married'),
#     ('Divorced', 'Divorced'),
#     ('Widowed', 'Widowed')
# )

# REGISTERED_FROM_counsellor = (
#     ('Email', 'Email'),
#     ('Social', 'Social'),
#     ('ResumePool', 'ResumePool'),
#     ('Resume', 'Resume'),
#     ('Careers', 'Careers'),
# )


# class EducationDetails_counsellor(models.Model):
#     # institute = models.ForeignKey(EducationInstitue, on_delete=models.CASCADE)
#     date_from = MonthField(null=True, blank=True)
#     # to_date = models.DateField(null=True, blank=True)
#     institute =models.CharField(max_length=300)
#     date_of_passing = MonthField(null=True, blank=True)
#     # degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
#     education_level = models.CharField(max_length=300, blank=True, null= True)
#     medium = models.CharField(max_length=300, blank=True, null= True)
#     degree = models.CharField(max_length=300)
#     board = models.CharField(max_length=300, blank=True, null= True)
#     course_type = models.CharField(max_length=300, blank=True, null= True)
#     percentage_grade = models.CharField(max_length=50, blank=True,null=True)
#     score = models.FloatField(max_length=50, blank = True, null = True)
#     specialization = models.CharField(max_length=200, blank = True, null = True)
#     qualification = models.CharField(max_length=50, blank = True, null = True)
#     subjects  = models.TextField(null=True, blank=True)
#     other_subject = models.TextField(null=True, blank=True)

# class TechnicalSkill_counsellor(models.Model):
#     skill = models.ForeignKey(Skill, on_delete=models.CASCADE,null=True, blank=True)
#     year = models.IntegerField(null=True, blank=True)
#     month = models.IntegerField(null=True, blank=True)
#     last_used = models.DateField(null=True, blank=True)
#     version = models.CharField(max_length=100, null=True, blank=True)
#     proficiency = models.CharField(
#         choices=TechnicalSkill_STATUS, max_length=100, null=True, blank=True)
#     is_major = models.BooleanField(default=False)
    
# class UserLanguage_counsellor(models.Model):
#     # language = models.CharField(Language, on_delete=models.CASCADE)
#     language = models.CharField(max_length=200,null=True, blank=True)
#     # ability = models.CharField(max_length=50)
#     read = models.BooleanField(default=False)
#     write = models.BooleanField(default=False)
#     speak = models.BooleanField(default=False)
#     proficiency = models.CharField(max_length=30, blank=True,null=True)

# class Employment_Exchange_counsellor(models.Model):
#     name= models.CharField(unique=True, max_length=100)
#     abbreviation = models.CharField(max_length=30, blank = True, null = True)
#     city_name = models.CharField(max_length=500, blank = True, null = True)
    
# class User_counsellor(models.Model):
#     file_prepend = "user/img/"
#     username = models.CharField(max_length=300)
#     applicant_name = models.CharField(max_length=300, blank=True)
#     recruiter_name = models.CharField(max_length=300, blank=True)
#     fathers_name = models.CharField(max_length=300, blank=True, null=True)
#     mothers_name = models.CharField(max_length=300, blank=True, null=True)
#     guardians_name = models.CharField(blank=True, null=True, max_length=200)
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     password = models.CharField(max_length=15)
#     company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
#     profile_pic = models.ImageField(
#         max_length=1000, upload_to='profile', null=True, blank=True)
#     user_type = models.CharField(choices=USER_TYPE_counsellor, max_length=10)
#     signature = models.CharField(max_length=2000, default='')
#     is_active = models.BooleanField(default=False)
#     is_feedback_submitted = models.BooleanField(default=True)
#     is_staff = models.BooleanField(_('staff status'), default=False)
#     # gender = models.CharField(
#     #     choices=GENDER_TYPES, max_length=10, blank=True, null=True)
#     gender = models.CharField(max_length=30, blank=True, null=True)
#     address = models.TextField(max_length=1000, blank=True, null=True)
#     permanent_address = models.TextField(
#         max_length=1000, blank=True, null=True)
#     nationality = models.TextField(max_length=50, blank=True, null=True)
#     mobile = models.CharField(max_length=20, blank=True, null=True)
#     employment_exchange_registration_no = models.CharField(max_length=50)
#     aadhaar_no = models.CharField(max_length=16, blank=True, null=True)
#     alternate_mobile = models.BigIntegerField(blank=True, null=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     email_verified = models.BooleanField(default=False)
#     highest_educational_level = models.CharField(max_length=200, blank=True, null=True)
#     highest_examination_passed = models.CharField(max_length=800, blank=True, null=True)
#     religion = models.CharField(max_length=200, blank=True, null=True)
#     caste = models.CharField(max_length=50, blank=True, null=True)
#     economically_weaker_section = models.CharField(max_length=10, blank=True, null=True)
#     prominent_identification_mark = models.CharField(max_length=200, blank=True, null=True)
#     district = models.CharField(max_length=200, blank=True, null=True)
#     physically_handicapped = models.CharField(max_length=20, blank=True, null=True)
#     disability_category = models.CharField(max_length=200, blank=True, null=True)
#     additional_disability_type = models.CharField(max_length=200, blank=True, null=True)
#     disability_percentage = models.CharField(max_length=100, blank=True, null=True)
#     whether_exservicemen = models.CharField(max_length=50, blank=True, null=True)
#     category_of_exservicemen = models.CharField(max_length=50, blank=True, null=True)
#     height_in_cm = models.CharField(max_length=800, blank=True, null=True)
#     weight_kgs = models.CharField(max_length=800, blank=True, null=True)
#     eye_sight= models.CharField(max_length=800, blank=True, null=True)
#     chest_inch = models.CharField(max_length=800, blank=True, null=True)
#     renewal_date = models.DateField(blank=True, null=True)
#     current_employment_status = models.CharField(max_length=200, blank=True, null=True)
#     fresher_experience_sts = models.CharField(max_length=50, blank=True, null=True)
#     skill_or_unskill = models.CharField(max_length=50, blank=True, null=True)
#     nco_code = models.CharField(max_length=12, blank=True, null=True)
#     govt_suppt_type = models.CharField(max_length=12, blank=True, null=True)
#     other_self_employed_type = models.CharField(max_length=200, blank=True, null=True)
#     self_emp_type = models.CharField(max_length=200, blank=True, null=True)
#     specify_govt_suppt = models.CharField(max_length=100, blank=True, null=True)
#     is_below_18 = models.CharField(max_length=50, blank=True, null=True)
#     state_work_location = models.CharField(max_length=100, blank=True, null=True)
#     # city = models.ForeignKey(City, null=True, blank=True, related_name='user_city', on_delete=models.CASCADE)
#     # state = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE)
#     # district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
#     # country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
#     # current_pincode = models.ForeignKey(Pincode, null=True, related_name='current_pincode', on_delete=models.CASCADE)
#     current_pincode = models.CharField(null=True, max_length=50)
#     current_location = models.CharField(null=True, max_length=300)
#     # police_station = models.ForeignKey(Police_Station, null=True, related_name='police_station', on_delete=models.CASCADE)
#     location = models.CharField(null=True, max_length=300,blank=True)
#     pincode = models.CharField(null=True, max_length=12,blank=True)
#     police_station = models.CharField(null=True, max_length=100,blank=True)
#     post_office = models.CharField(null=True, max_length=100,blank=True)
#     sub_division = models.CharField(max_length=100, blank=True, null=True)
#     revenue_circle= models.CharField(max_length=100, blank=True, null=True)
#     residence = models.CharField(max_length=50, blank=True, null=True)
#     last_password_reset_on = models.DateTimeField(auto_now_add=True)
#     photo = models.CharField(max_length=500,blank=True, null=True)
#     # TODO: this needs to be choice field
#     marital_status = models.CharField(
#         choices=MARTIAL_STATUS_counsellor, max_length=50, blank=True, null=True)
#     #employment_history = models.ManyToManyField(EmploymentHistory) commented for counsellor
#     #current_city = models.ForeignKey(City, blank=True, null=True, related_name='current_city', on_delete=models.CASCADE) commeneted for counsellor
#     # preferred_city = models.ManyToManyField(
#     #     City, related_name='preferred_city')
#     # functional_area = models.ManyToManyField(FunctionalArea) commeneted for counsellor
#     job_role = models.CharField(max_length=500, default='')
#     education_counsellor = models.ManyToManyField(EducationDetails_counsellor)
#     #project = models.ManyToManyField(Project)
#     skills_counsellor = models.ManyToManyField(TechnicalSkill_counsellor)
#     language_counsellor = models.ManyToManyField(UserLanguage_counsellor)
#     current_salary = models.CharField(max_length=50, blank=True, null=True)
#     expected_salary = models.CharField(max_length=500, blank=True, null=True)
#     skill_qualification = models.ManyToManyField(Skill_Qualification)
#     certification = models.ManyToManyField(Training_Courses)
#     # prefered_industry = models.ForeignKey(Industry, blank=True, null=True, on_delete=models.CASCADE)
#     #industry = models.ManyToManyField(industry, related_name='recruiter_industries')
#     #technical_skills = models.ManyToManyField(Skill, related_name='recruiter_skill')
#     dob = models.DateField(blank=True, null=True)
#     profile_description = models.CharField(max_length=2000, default='')
#     # this must be s3 file key
#     resume = models.CharField(max_length=2000, default='')
#     NOC = models.CharField(max_length=2000, default='')
#     affidavit = models.CharField(max_length=2000, default='')
#     relocation = models.BooleanField(default=False)
#     notice_period = models.CharField(max_length=50, blank=True, null=True)
#     year = models.CharField(max_length=50, blank=True, null=True)
#     # month = models.CharField(max_length=50, default='')
#     month = models.CharField(max_length=50, blank=True, null=True)
#     show_email = models.BooleanField(default=False)
#     resume_title = models.TextField(max_length=2000, blank=True, null=True)
#     resume_text = models.TextField(blank=True, null=True)
#     mobile_verification_code = models.CharField(max_length=50, default='')
#     last_mobile_code_verified_on = models.DateTimeField(auto_now_add=True)
#     mobile_verified = models.BooleanField(default=False)
#     is_login = models.BooleanField(default=False)
#     email_notifications = models.BooleanField(default=True)
#     profile_updated = models.DateTimeField(auto_now_add=True)
#     is_admin = models.BooleanField(default=False)  # agency created user
#     profile_completeness = models.CharField(max_length=500, default='')
#     activation_code = models.CharField(max_length=100, null=True, blank=True)
#     # is_register_through_mail = models.BooleanField(default=False)
#     registered_from = models.CharField(choices=REGISTERED_FROM_counsellor, max_length=15, default='')
#     is_unsubscribe = models.BooleanField(default=False)
#     is_bounce = models.BooleanField(default=False)
#     unsubscribe_code = models.CharField(max_length=100, null=True, blank=True)
#     # Other admins in agency other than agency created user
#     agency_admin = models.BooleanField(default=False)
#     referer = models.TextField(null=True, blank=True)
#     unsubscribe_reason = models.TextField(default='')
#     emp_exchange_counsellor = models.ForeignKey(Employment_Exchange_counsellor, null=True, blank=True, on_delete=models.CASCADE)
#     employment_exchange_name = models.CharField(max_length=300, null=True, blank=True)
#     occupation = models.CharField(max_length=100, null=True, blank=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     is_user_enabled = models.BooleanField(default=True)
#     is_account_activation_request = models.BooleanField(default=False)
#     account_activation_applied_on = models.DateTimeField(null=True, blank=True)
#     is_employed = models.BooleanField(default=False)
#     zone = models.ForeignKey(Ex_Zone, blank = True, null = True, on_delete=models.CASCADE)
#     # skills_used = ArrayField(models.CharField(max_length=200, blank=True),size=20, null = True, blank = True)
#     skills_used = models.TextField(null=True, blank=True)
#     type_of_establishment = models.CharField(max_length=100, null=True, blank=True)
#     #establishment_code = models.ForeignKey(NIC_code_of_establishment, null=True, blank=True, on_delete=models.CASCADE) commneted for councellor
#     economic_activity_details = models.CharField(max_length=1000, null=True, blank=True)
#     scanned_signature = models.ImageField(
#         max_length=1000, upload_to='signature_file', null=True, blank=True)
#     scanned_seal = models.ImageField(
#         max_length=1000, upload_to='scanned_seal', null=True, blank=True)
#     test_data = models.CharField(max_length=20, null=True, blank=True)
#     insert_date = models.DateField(auto_now_add=True)
#     nic_api_date = models.DateField(blank = True, null = True)
#     session_id = models.CharField(max_length=100, blank=True, null=True)
    


#     def has_perm(self, perm, obj=None):
#         if self.is_active and self.is_staff:
#             return True

#         # return _user_has_perm(self, perm, obj)
#         else:
#             try:
#                 user_perm = self.user_permissions.get(codename=perm)
#             except ObjectDoesNotExist:
#                 user_perm = False
#             if user_perm:
#                 return True
#             else:
#                 return False

#     class Meta:
#         permissions = (
#             ('blog_view', 'can view blog posts and categories'),
#             ('blog_edit', 'can edit blog category and post'),
#             ("support_view", "can view tickets"),
#             ("support_edit", "can edit tickets"),
#             ("activity_view",
#              "can view recruiters, applicants, data, posts"),
#             ("activity_edit", "can edit data"),
#             ("jobposts_edit", "can manage jobposts"),
#             ("jobposts_invoice_access", "can manage invoice"),
#             ("jobposts_resume_profiles", "can manage resume profiles"),
#         )



#     @property
#     def generate_session_id(self):
#         # Generate a UUID (version 4) as the session identifier
#         return str(uuid.uuid4())
    
#     def get_full_username(self):
#         return " ".join(re.findall("[a-zA-Z]+", self.username))

#     def get_first_name(self):
#         name = (self.applicant_name).split(' ', 1)
#         return name[0]

#     @property
#     def is_fb_connected(self):
#         if self.facebook_user.all():
#             return True
#         else:
#             return False

#     @property
#     def is_gp_connected(self):
#         if self.google_user.all():
#             return True
#         else:
#             return False

#     @property
#     def is_tw_connected(self):
#         if self.twitter.all():
#             return True
#         else:
#             return False

#     @property
#     def is_ln_connected(self):
#         if self.linkedin.all():
#             return True
#         else:
#             return False

#     @property
#     def is_gh_connected(self):
#         if self.github.all():
#             return True
#         else:
#             return False

#     @property
#     def is_recruiter(self):
#         if str(self.user_type) == 'RR' or str(self.user_type) == 'RA' or str(self.user_type) == 'RA':
#             return True
#         else:
#             return False

#     @property
#     def is_so_connected(self):
#         if self.stackoverflow.all():
#             return True
#         else:
#             return False

#     @property
#     def is_connect_social_networks(self):
#         if self.facebook_user.all() and self.google_user.all() and self.linkedin.all() and self.twitter.all():
#             return True
#         else:
#             return False

    

#     @property
#     def is_recruiter_active(self):
#         if self.is_connect_social_networks and self.is_active and self.mobile_verified:
#             return True
#         else:
#             return False

#     def is_company_recruiter(self):
#         if self.is_recruiter:
#             return True
#         else:
#             return False

#     @property
#     def is_agency_recruiter(self):
#         if self.company and str(self.company.company_type) == 'Consultant':
#             return True
#         return False

#     @property
#     def is_agency_admin(self):
#         if self.company and self.agency_admin:
#             return True
#         return False

#     @property
#     def is_jobseeker(self):
#         if str(self.user_type) == 'JS':
#             return True
#         return False

#     @property
#     def is_employment_exchange_officer(self):
#         if str(self.user_type) == 'DEE':
#             return True
#         return False
    
#     @property
#     def is_department(self):
#         if str(self.user_type) == 'D':
#             return True
#         return False
    
#     @property
#     def is_zonal_officer(self):
#         if str(self.user_type) == 'Zonal':
#             return True
#         return False

#     @property
#     def is_guest_user(self):
#         if str(self.user_type) == 'GUSER':
#             return True
#         return False
    
#     @property
#     def profile_completion_percentage(self):
#         complete = 0
#         if self.year:
#             complete += 10
#         if self.mobile:
#             complete += 20
#         if self.is_active:
#             complete += 10
#         if self.user_type == 'JS':
#             if len(self.resume):
#                 complete += 15
#             if len(self.profile_description):
#                 complete += 5
#             if self.education.all():
#                 complete += 10
#             if self.project.all():
#                 complete += 10
#             if self.skills.all():
#                 complete += 15
#             if self.language.all():
#                 complete += 5
#         else:
#             if self.job_role:
#                 complete += 10
#             if self.industry.all():
#                 complete += 10
#             if self.profile_description:
#                 complete += 15
#             if self.technical_skills.all():
#                 complete += 15
#             if self.functional_area.all():
#                 complete += 10
#         return complete
    
#     def get_age(self):
#         birth_date = self.dob
#         today = datetime.today()
#         age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
#         return age
        
#     def calculate_experience(self):
#         employment_history_records = self.employment_history.all()

#         total_experience = 0  # in days

#         for record in employment_history_records:
#             date_from = record.from_date
#             date_to = record.to_date if record.to_date else date.today()

#             experience_duration = (date_to - date_from).days
#             total_experience += experience_duration
        
#         # Convert total_experience from days to months
#         total_experience_months = total_experience // 30  # assuming 30 days per month for simplicity

#         return total_experience_months

#         # # Convert total_experience from days to years
#         # total_experience_years = total_experience / 365.25  # accounting for leap years

#         # return self.format_experience(total_experience_years)
        
#     def format_experience(self, total_experience_months):
#         # Convert total_experience_months to years and months
#         years = total_experience_months // 12
#         months = total_experience_months % 12

#         # Format the result
#         if years == 1:
#             year_str = "1 yr"
#         else:
#             year_str = f"{years} yrs"

#         if months == 1:
#             month_str = "1 month"
#         else:
#             month_str = f"{months} months"

#         if years == 0:
#             return month_str
#         elif months == 0:
#             return year_str
#         else:
#             return f"{year_str} {month_str}"


# career counselling part by sakil=====================
class CounsellorDetails(models.Model):
    user_id = models.IntegerField()  # Storing user ID as an integer instead of ForeignKey
    name = models.CharField(max_length=255)
    fathers_name = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    caste = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=30, blank=True, null=True)

    # Address
    permanent_address = models.TextField()
    district = models.CharField(max_length=255)
    police_station = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    current_address = models.TextField()
    c_district = models.CharField(max_length=255)
    c_police_station = models.CharField(max_length=255)
    c_pin = models.CharField(max_length=10)

    # Education
    highest_qualification = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    passing_year = models.CharField(max_length=255)

    # Career Details
    # counseling_categories = models.TextField(help_text="Comma-separated categories")
    counsellor_type = models.CharField(max_length=100, null=True, blank=True)
    experience_in_career_counselling = models.CharField(max_length=100, null=True, blank=True)
    experience_in_year_month = models.CharField(max_length=100, null=True, blank=True)

    # Fees
    online_one_one_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offline_one_one_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    online_group_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offline_group_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    online_per_day_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    offline_per_day_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    #For User form submition status check " YES or NO"
    form_status= models.CharField(max_length=100, default='No', null=True, blank=True)
    # Regibstation no
    reg_no = models.CharField(max_length=100, null=True, blank=True)
    # Status
    status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Revert", "Revert")],
        default="Pending"
    )
    about_me = models.TextField(null=True, blank=True)
    about_highlight = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    ACCOUNT_STATUS_CHOICES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Suspended', 'Suspended'),
    ]

    account_status = models.CharField(
        max_length=255,
        choices=ACCOUNT_STATUS_CHOICES,
        default='Inactive'
    )
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.status}"

class CounsellorDoc(models.Model):
    user_id = models.IntegerField()  # Storing user ID as an integer instead of ForeignKey
    file_name = models.CharField(max_length=255)  # Name of the file
    file_path = models.CharField(max_length=500)  # Path where the file is stored
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name}"
    
class Counselling_session(models.Model):
    counselling_session_id = models.CharField(max_length=50)  # NOT unique anymore
    user_js_id = models.CharField(max_length=50, unique=False)  # Allows multiple entries per session
    session_date = models.DateField()
    session_time = models.TimeField()
    counsellor_id = models.CharField(max_length=50, null = True,blank = True)
    #If we want to connect as foreign key
    #booking = models.ForeignKey(Counselling_Booking, on_delete=models.CASCADE, related_name="sessions")
    #Connecting manually
    booking_id = models.CharField(max_length=50,null = True,blank = True)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),  
    ]
    
    counselling_session_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    session_type = models.CharField(max_length=100)
    counselling_mode = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null = True,blank = True)
    session_name = models.CharField(max_length=100, null = True,blank = True)
    feedback_mail = models.IntegerField(default='0')
    
    payment_status = models.TextField(max_length=100, null=True, blank=True)
    main_reason = models.TextField(max_length=500, null=True, blank=True)
    complete_feedback = models.TextField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)  # Set when created
    updated_at = models.DateTimeField(auto_now=True)  # Set when updated

    def __str__(self):
        return f"Session {self.counselling_session_id} - {self.user_js_id} ({self.session_type})"

class counselling_session_feedback(models.Model):
    counsellor_id = models.CharField(max_length=50, null = True,blank = True)
    js_id = models.CharField(max_length=50,null = True,blank = True)  #jobseeker id
    counselling_session_id = models.CharField(max_length=50,null = True,blank = True)
    q1_rating = models.IntegerField()
    q2_rating = models.IntegerField()
    q3_rating = models.IntegerField()
    q4_rating = models.IntegerField()
    #q5_rating = models.IntegerField()
    q6_rating = models.IntegerField()
    
class ncs_vacancy_api_job_data(models.Model):
    job_id = models.IntegerField()
    employer_name = models.CharField(max_length = 200)
    job_title = models.CharField(max_length = 100)
    min_exp = models.IntegerField()
    max_exp = models.IntegerField()
    avg_exp= models.IntegerField()
    job_start_date = models.DateTimeField()
    job_expiry_date = models.DateTimeField()
    maximum_wages = models.IntegerField(null = True,blank = True)
    minimum_wages = models.IntegerField(null = True,blank = True)
    average_wage = models.IntegerField()
    number_of_openings = models.IntegerField()
    industry_id = models.IntegerField()
    industry_name = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100)
    qualification = models.TextField()
    state_name = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100)
    job_description = models.TextField()
    vacancy_url = models.URLField(max_length=500)
    posted_date = models.DateTimeField()
    skills = models.TextField()
    employer_mobile = models.CharField(max_length=15)
    employer_email = models.EmailField()
    sector_id = models.IntegerField()
    sector_name = models.CharField(max_length=100)
    functional_area = models.CharField(max_length=100)
    functional_role = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    click_count = models.IntegerField(default = 0)
    
    
class institution_request(models.Model):
    college_name = models.CharField(max_length=255)
    university_name = models.CharField(max_length=255)
    address = models.TextField()
    district = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    counseling_date = models.DateField()
    max_students = models.PositiveIntegerField()
    contact_phone = models.CharField(max_length=15)
    college_email = models.EmailField()
    approval_pdf = models.CharField(max_length=500)
    assigned_counsellor = models.CharField(max_length=15, null = True,blank = True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),  
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.college_name


class ncs_data_sending_history(models.Model):
    data_sending_date = models.DateTimeField(default=timezone.now)
    applicants_data_date = models.DateField()
    total_data = models.IntegerField()
    not_sent = models.IntegerField()