import re
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from django.core.files.storage import FileSystemStorage
from django.views import View
import json
from django.db.models import Q

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import check_password
from django.db.models import Q, Count
from django.contrib.auth import update_session_auth_hash
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Permission, ContentType
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')
def about(request):
    return render(request, 'about.html')

def guidelines(request):
    return render(request, 'guidelines.html')

def tnc(request):
    return render(request, 'tnc.html')

def contactus(request):
    return render(request, 'contactus.html')

def faq(request):
    return render(request, 'faq.html')
def register(request):
    if request.method == 'POST':
        errors = {}
        data = request.POST
        files = request.FILES
        
        print("Starting form processing...")  # Debug print

        # Required field validation
        required_fields = [
            'company_name', 'email', 'mobile', 'address', 'pin_code',
            'establishment_type', 'establishment_code', 'economic_activity_details', 'employment_exchange',
            'company_registration_no', 'company_pan_no', 'password', 'confirm_password'
        ]
        
        for field in required_fields:
            if not data.get(field):
                errors[field] = 'This field is required'
                print(f"Missing required field: {field}")  # Debug print

        # Password validation
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                errors['confirm_password'] = 'Passwords do not match'
                print("Password mismatch detected")  # Debug print
            elif len(data['password']) < 8:
                errors['password'] = 'Password must be at least 8 characters'
                print("Password too short")  # Debug print

        # Field-specific validation
        validation_rules = {
            'mobile': (validate_mobile, 'Invalid mobile number (must be 10 digits)'),
            'email': (validate_email, 'Invalid email format'),
            'pin_code': (validate_pin, 'Invalid PIN code (must be 6 digits)'),
            'company_pan_no': (validate_pan, 'Invalid PAN format (e.g., ABCDE1234F)'),
            'company_gst_no': (validate_gst, 'Invalid GST format')
        }

        for field, (validator, error_msg) in validation_rules.items():
            if field in data and data[field] and not validator(data[field]):
                errors[field] = error_msg
                print(f"Validation failed for {field}: {data[field]}")  # Debug print

        # File validation
        file_validations = {
            'logo': (['image/jpeg', 'image/png'], 'Logo must be JPEG or PNG'),
            'seal': (['image/jpeg', 'image/png'], 'Seal must be JPEG or PNG'),
            'gst_certificate': (['application/pdf'], 'GST certificate must be PDF'),
            'pan_card': (['image/jpeg', 'image/png'], 'PAN card must be JPEG or PNG')
        }

        for field, (allowed_types, error_msg) in file_validations.items():
            if field in files and not validate_file(files[field], allowed_types):
                errors[field] = error_msg
                print(f"Invalid file type for {field}")  # Debug print

        if errors:
            print(f"Form validation failed with errors: {errors}")  # Debug print
            for field, error in errors.items():
                messages.error(request, f"{field}: {error}")
            return render(request, 'register.html', {
                'errors': errors,
                'form_data': data
            })

        print("All validations passed. Attempting to save data...")  # Debug print

        try:
            # Create User
            user_data = {
                'password': data['password'],
                'username': data['company_name'],
                'email': data['email'],
                'mobile': data['mobile'],
                'mobile_verified': True,
                'address': data['address'],
                'pincode': data['pin_code'],
                'type_of_establishment': data['establishment_type'],
                'establishment_code_id': data['establishment_code'],
                'economic_activity_details': data['economic_activity_details'],
                'employment_exchange_name': data['employment_exchange'],
                'user_type': 'RR'  # Assuming this is for recruiters
            }

            company_user = User(**user_data)
            company_user.save()
            print(f"User created with ID: {company_user.id}")  # Debug print

            # Handle file uploads
            fs = FileSystemStorage()
            file_fields = {
                'logo': 'logos',
                'seal': 'scanned_signature',
                'gst_certificate': 'gst_certificate',
                'pan_card': 'pan_card'
            }

            for field, attr in file_fields.items():
                if field in files:
                    try:
                        file = files[field]
                        filename = fs.save(f'{file_fields[field]}/{file.name}', file)
                        setattr(company_user, attr, filename)
                        print(f"File {field} saved as {filename}")  # Debug print
                    except Exception as e:
                        logger.error(f"Error saving {field}: {str(e)}")
                        messages.warning(request, f"Error saving {field.replace('_', ' ')}")

            company_user.save()

            # Create Company
            company_data = {
                'company_registration_no': data['company_registration_no'],
                'company_pan_no': data['company_pan_no'],
                'company_gst_no': data.get('company_gst_no'),
                'name': company_user
            }

            company = Company.objects.create(**company_data)
            print(f"Company created with ID: {company.id}")  # Debug print

            messages.success(request, 'Registration successful!')
            print("Registration completed successfully")  # Debug print
            return redirect('success_page')

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred during registration. Please try again.')
            print(f"Error occurred: {str(e)}")  # Debug print
            return render(request, 'register.html', {
                'errors': {'__all__': str(e)},
                'form_data': data
            })
    else:
        return render(request, 'register.html')


# Validation functions
def validate_mobile(mobile):
    """Validate a mobile number with proper error handling"""
    if mobile is None:
        raise ValueError("Mobile number cannot be None")
    
    if not isinstance(mobile, (str, bytes)):
        # Convert to string if it's a number
        mobile = str(mobile)
    
    return bool(re.fullmatch(r'^[0-9]{10}$', mobile))

def validate_pin(pin):
    return re.match(r'^[0-9]{6}$', pin)

def validate_pan(pan):
    return re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan)

def validate_gst(gst):
    if not gst:  # GST is optional
        return True
    return re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', gst)

def validate_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email)

def validate_file(file, allowed_types):
    if not file:
        return True
    return file.content_type in allowed_types

    

class SendOTPView(View):
    def post(self, request):
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            mobile = data.get('mobile')
            
            if not mobile:
                return JsonResponse({
                    'success': False, 
                    'message': 'Mobile number is required'
                }, status=400)

            if not re.match(r'^[0-9]{10}$', str(mobile)):
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid mobile number (must be 10 digits)'
                }, status=400)

            # Rest of your OTP generation logic here
            otp = str(random.randint(100000, 999999))
            cache.set(f'otp_{mobile}', otp, timeout=300)
            
            # In production, send the OTP via SMS here
            print(f"OTP for {mobile}: {otp}")  # For development only
            users = User.objects.filter(Q(mobile=mobile) & Q(user_type='RR'))
            if not users.exists():
                return JsonResponse({
                    'success': True, 
                    'message': 'OTP sent successfully'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Mobile number already registered'
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
def verify_otp(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            mobile = data.get('mobile')
            otp = data.get('otp')
            
            if not mobile or not otp:
                return JsonResponse({
                    'success': False, 
                    'message': 'Mobile and OTP are required'
                })
                
            # Your verification logic here
            cached_otp = cache.get(f'otp_{mobile}')
            
            if cached_otp and cached_otp == otp:
                # Clear OTP after successful verification
                cache.delete(f'otp_{mobile}')
                return JsonResponse({
                    'success': True,
                    'message': 'OTP verified successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid OTP or OTP expired'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })