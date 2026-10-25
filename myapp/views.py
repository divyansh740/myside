import random
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Course, Enrollment, EmailOTP, Enquiry

# 1. Main Landing Page View
# 1. Main Landing Page View


def index(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        course = request.POST.get("course")
        message = request.POST.get("message")
        
        if full_name and phone:
            Enquiry.objects.create(
                full_name=full_name,
                phone=phone,
                email=email,
                course=course,
                message=message
            )
            messages.success(request, 'Aapka enquiry form submit ho gaya hai!')
            return redirect('index')
            
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses': courses})

# 2. Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username pehle se maujood hai!')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account kamyabi se ban gaya! Ab login karein.')
        return redirect('login')

    return render(request, 'signup.html')

# 3. Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login kamyabi se ho gaya!')
            return redirect('index')
        else:
            messages.error(request, 'Galat username ya password!')

    return render(request, 'login.html')

# 4. Logout View
def logout_view(request):
    logout(request)
    messages.info(request, 'Aap logout ho chuke hain.')
    return redirect('index')

# 5. Dashboard View
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# 6. Send OTP View
def send_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            username = email.split('@')[0]
            user = User.objects.create_user(username=username, email=email)

        otp_obj, created = EmailOTP.objects.get_or_create(user=user)
        otp_code = otp_obj.generate_otp()

        send_mail(
            'Your LMS Login OTP',
            f'Your OTP for LMS Login is: {otp_code}',
            'divyanshbhai695@gmail.com',
            [email],
            fail_silently=False,
        )
        request.session['otp_email'] = email
        return redirect('verify_otp')

    return render(request, 'send_otp.html')

# 7. Create Order View
@login_required
def create_order(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        'course': course,
        'order_id': 'order_dummy_123456',
        'amount': int(course.price * 100),
    }
    return render(request, 'payment.html', context)

# 8. Payment Success View
@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('dashboard')

# 9. Course Detail View
@login_required
def course_detail(request, course_id):
    enrollment = get_object_or_404(Enrollment, user=request.user, course__id=course_id)
    return render(request, 'course_detail.html', {'course': enrollment.course})

# 10. Verify OTP View
# Is tarah ka code hoga aapke verify_otp view me:
def verify_otp_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        email = request.session.get('otp_email')
        
        # EmailOTP check karo
        otp_obj = EmailOTP.objects.filter(user__email=email, otp=otp_input).last()
        
        if otp_obj:
            # ⚠️ PURANA CODE: user = User.objects.get(email=email) <-- Iss line par error aa raha tha
            
            # ✅ NAYA FIX CODE:
            user = User.objects.filter(email=email).first()
            
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid OTP.")
            
    return render(request, 'verify_otp.html')