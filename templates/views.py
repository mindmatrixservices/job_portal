from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

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

# def save_user_data(request):
#     if request.method == 'POST':
#         try:
#             # Get form data
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             mobile = request.POST.get('mobile')
#             address = request.POST.get('address')
#             pin = request.POST.get('pin')
#             establishment = request.POST.get('establishment')
#             establishment_code = request.POST.get('establishment_code')
#             economic_activity_details = request.POST.get('economic_activity_details')
#             password = request.POST.get('password')
            
#             # Handle file uploads
#             logo = request.FILES.get('logo')
#             seal = request.FILES.get('seal')
            
#             # Save files to media folder
#             fs = FileSystemStorage()
#             logo_path = fs.save(f'logos/{logo.name}', logo)
#             seal_path = fs.save(f'seals/{seal.name}', seal)