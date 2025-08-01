//JavaScript for toggling password visibility and validating password strength

// Combined toggle password function
function togglePassword(fieldId, iconId) {
    var passwordInput = document.getElementById(fieldId);
    var eyeIcon = document.getElementById(iconId);
  
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    }
  }
  
  // Password validation function
  function validatePassword() {
    const password = document.getElementById("password").value;
    const strengthDiv = document.getElementById("passwordStrength");
    const errorDiv = document.getElementById("passwordError");
    
    // Clear messages when empty
    if (password.length === 0) {
        strengthDiv.textContent = "";
        errorDiv.classList.add("d-none");
        return;
    }
    
    // Check password strength
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[$&+,:;=?@#|'<>.^*()%!-]/.test(password);
    const isLongEnough = password.length >= 8;
    
    let strength = 0;
    if (hasLower) strength++;
    if (hasUpper) strength++;
    if (hasNumber) strength++;
    if (hasSpecial) strength++;
    
    // Display appropriate message
    if (!isLongEnough) {
        strengthDiv.textContent = "Password must be at least 8 characters long";
        strengthDiv.style.color = "red";
        errorDiv.classList.remove("d-none");
    } else if (strength < 4) {
        const missing = [];
        if (!hasLower) missing.push("lowercase letter");
        if (!hasUpper) missing.push("uppercase letter");
        if (!hasNumber) missing.push("number");
        if (!hasSpecial) missing.push("special character");
        
        strengthDiv.textContent = `Password needs at least one ${missing.join(", ")}`;
        strengthDiv.style.color = "red";
        errorDiv.classList.remove("d-none");
    } else {
        strengthDiv.textContent = "Strong password!";
        strengthDiv.style.color = "green";
        errorDiv.classList.add("d-none");
    }
    
    // Also validate confirmation if it has value
    const confirmPassword = document.getElementById("confirm_password").value;
    if (confirmPassword.length > 0) {
        validateConfirmPassword();
    }
  }
  
  // Confirm password validation
  function validateConfirmPassword() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    const errorDiv = document.getElementById("confirmPasswordError");
    
    if (confirmPassword.length === 0) {
        errorDiv.classList.add("d-none");
        return;
    }
    
    if (password !== confirmPassword) {
        errorDiv.classList.remove("d-none");
    } else {
        errorDiv.classList.add("d-none");
    }
  }
  

  document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const form = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const mobileInput = document.getElementById('mobile');
    const sendOtpBtn = document.getElementById('sendOtp');
    const otpSection = document.getElementById('otpSection');
    const otpInput = document.getElementById('otp');
    const verifyOtpBtn = document.getElementById('verifyOtp');
    const resendOtpBtn = document.getElementById('resendOtp');
    const countdownText = document.getElementById('countdownText');
    const countdownSpan = document.getElementById('countdown');
    
    // Error elements
    const errorElements = {
        'company_name': document.getElementById('company_nameError'),
        'email': document.getElementById('emailError'),
        'mobile': document.getElementById('mobileError'),
        'address': document.getElementById('addressError'),
        'pin_code': document.getElementById('pinError'),
        'establishment_type': document.getElementById('establishmentError'),
        'establishment_code': document.getElementById('establishmentCodeError'),
        'economic_activity_details': document.getElementById('economicActivityError'),
        'company_registration_no': document.getElementById('companyRegError'),
        'company_pan_no': document.getElementById('panError'),
        'company_gst_no': document.getElementById('gstError'),
        'logo': document.getElementById('logoError'),
        'seal': document.getElementById('sealError'),
        'gst_certificate': document.getElementById('gstCertError'),
        'pan_card': document.getElementById('panCardError'),
        'otp': document.getElementById('otpError')
    };
    
    // OTP variables
    let otpVerified = false;
    let countdownInterval;
    let countdown = 180; // 3 minutes
    
    // Validate mobile number format
    function validateMobile() {
        const mobile = mobileInput.value.trim();
        const isValid = /^[0-9]{10}$/.test(mobile);
        
        if (!isValid) {
            errorElements.mobile.classList.remove('d-none');
            return false;
        } else {
            errorElements.mobile.classList.add('d-none');
            return true;
        }
    }
    
    // Validate all required fields
    function validateForm() {
        let isValid = true;
        
        // Check all required fields
        const requiredFields = [
            'company_name', 'email', 'mobile', 'address', 'pin_code',
            'establishment_type', 'establishment_code', 'economic_activity_details',
            'company_registration_no', 'company_pan_no'
        ];
        
        requiredFields.forEach(field => {
            const element = document.getElementById(field);
            const errorElement = errorElements[field];
            
            if (!element.value.trim()) {
                errorElement.classList.remove('d-none');
                isValid = false;
            } else {
                errorElement.classList.add('d-none');
                
                // Field-specific validations
                if (field === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(element.value)) {
                    errorElement.classList.remove('d-none');
                    isValid = false;
                }
                
                if (field === 'pin_code' && !/^[0-9]{6}$/.test(element.value)) {
                    errorElement.classList.remove('d-none');
                    isValid = false;
                }
                
                if (field === 'company_pan_no' && !/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test(element.value)) {
                    errorElement.classList.remove('d-none');
                    isValid = false;
                }
            }
        });
        
        // Check OTP verification
        if (!otpVerified) {
            errorElements.otp.classList.remove('d-none');
            isValid = false;
        } else {
            errorElements.otp.classList.add('d-none');
        }
        
        // File validations
        const logoInput = document.getElementById('logo');
        if (logoInput.files.length > 0) {
            const file = logoInput.files[0];
            if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
                errorElements.logo.classList.remove('d-none');
                isValid = false;
            }
        }
        
        // Similar validations for other files...
        
        return isValid;
    }
    
    // Start OTP countdown
    function startCountdown() {
        countdown = 180;
        countdownText.classList.remove('d-none');
        resendOtpBtn.classList.add('d-none');
        
        countdownInterval = setInterval(() => {
            countdownSpan.textContent = countdown;
            countdown--;
            
            if (countdown < 0) {
                clearInterval(countdownInterval);
                countdownText.classList.add('d-none');
                resendOtpBtn.classList.remove('d-none');
            }
        }, 1000);
    }
    

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    // Send OTP
    sendOtpBtn.addEventListener('click', function() {
        if (!validateMobile()) return;
        
        const mobile = mobileInput.value.trim();
        const csrftoken = getCookie('csrftoken');
        fetch('/send-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ mobile: mobile })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                otpSection.style.display = 'block';
                startCountdown();
                Swal.fire('Success','OTP sent successfully! Please check your phone.', 'success');
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Failed to send OTP: ' + (data.message || 'Unknown error'),
                    icon: 'error',
                    confirmButtonText: 'OK',
                    customClass: {
                      confirmButton: 'btn btn-primary'
                    }
                  });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error', 'An error occurred while sending OTP.', 'error');
        });
    });
    
    // Verify OTP
    verifyOtpBtn.addEventListener('click', function() {
        const mobile = document.getElementById('mobile').value.trim();
        const otp = otpInput.value.trim();
        const csrftoken = getCookie('csrftoken');
        if (!otp || otp.length !== 6) {
            errorElements.otp.classList.remove('d-none');
            return;
        }
        
        fetch('/verify-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 
                mobile: mobile,
                otp: otp
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                otpVerified = true;
                errorElements.otp.classList.add('d-none');
                Swal.fire('Success', 'OTP verified successfully!', 'success');
                otpSection.style.display = 'none';
                document.getElementById('mobileError').classList.remove('text-danger');
                document.getElementById('mobileError').classList.remove('d-none');
                document.getElementById('mobileError').classList.add('text-success');
                document.getElementById('mobileError').textContent = 'OTP verified successfully!';
                // Enable the submit button
                sendOtpBtn.disabled = true;
                verifyOtpBtn.disabled = true;
                submitBtn.disabled = false;
            } else {
                errorElements.otp.classList.remove('d-none');
                Swal.fire('Error', 'Wrong OTP. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error', 'An error occurred while sending OTP.', 'error');
        });
    });
    
    // Resend OTP
    resendOtpBtn.addEventListener('click', function() {
        if (!validateMobile()) return;
        
        const mobile = mobileInput.value.trim();
        
        fetch('/send-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ mobile: mobile })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                startCountdown();
                Swal.fire('Info', 'New OTP sent successfully!', 'success');
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Failed to send OTP: ' + (data.message || 'Unknown error'),
                    icon: 'error',
                    confirmButtonText: 'OK',
                    customClass: {
                      confirmButton: 'btn btn-primary'
                    }
                  });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error', 'An error occurred while processing your request.', 'error');
        });
    });
    
    // Form submission
    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            alert('Form is valid! Submitting...');
            // If all validations pass, submit the form
            form.submit();
        } else {
            Swal.fire('Error', 'Please fill all required fields correctly.', 'error');
        }
    });
    
    // Real-time validation for mobile
    mobileInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
        if (this.value.length > 10) {
            this.value = this.value.slice(0, 10);
        }
        validateMobile();
    });
    
    // Real-time validation for PIN code
    const pinInput = document.getElementById('pin_code');
    pinInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '');
        if (this.value.length > 6) {
            this.value = this.value.slice(0, 6);
        }
    });
    
    // Real-time validation for PAN number (uppercase)
    const panInput = document.getElementById('company_pan_no');
    panInput.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });
  });