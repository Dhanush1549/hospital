from django.shortcuts import render,redirect
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages 
from django.contrib.auth import authenticate,login
from hospitalapp.models import CustomUser,Patient,Appointment,Department,Doctor,Consultation,Pharmacy
import os
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import uuid 
from django.core.mail import send_mail
from django.urls import reverse
import random   
import string
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
import logging
from django.contrib.auth import update_session_auth_hash

def index(request):
    return render(request, 'nav.html')

def logout_view(request):
    logout(request)
    return redirect('nav')
def nav(request):
    return render(request, 'nav.html')

def nav2(request):
    return render(request, 'nav2.html')

def nav21(request):
    return render(request, 'nav21.html')

def nav3(request):
    return render(request, 'nav3.html')

def nav4(request):
    return render(request, 'nav4.html')

def login_all(request):
    return render(request,'admin_login.html')

def doctor_home1(request):
    return render(request,'doctor_home1.html')

def pharmacy_home1(request):
    return render(request,'pharmacy_home1.html')


def reception(request):
    return render(request,'admin_login.html')

@login_required
def doctor_home(request):
    return render(request, 'doctor_home.html')

@login_required
def pharmacy_home(request):
    return render(request, 'pharmacy_home.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.user_type == '1':
                login(request, user)
                return redirect('nav21')
            elif user.user_type == '2':
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('nav21')
            elif user.user_type == '3':
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('doctor_home1')
            elif user.user_type == '4':
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('pharmacy_home1')
            else:
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return redirect('index')
        else:
            messages.error(request, "Invalid username or password!!!")
            return redirect('admin_login')

    return render(request, 'admin_login.html')

def add_department(request):
        return render(request,'add_dept.html')

def department(request):
    if request.method == 'POST':
        name = request.POST['department']
        description = request.POST['description']
        
        department = Department(department=name, description=description)
        department.save()

        messages.success(request, 'Department added successfully.')
        return redirect('all_departments')

    return render(request, 'add_dept.html')

def all_departments(request):
    departments = Department.objects.all()
    return render(request, 'all_departments.html', {'departments': departments})

def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)   

    if request.method == 'POST':
        department.department = request.POST.get('department')
        department.description = request.POST.get('description')
        department.save()
        return redirect('all_departments')

    return render(request, 'edit_department.html', {'department': department})


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete() 
    return redirect('all_departments')


def register_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')

        if Patient.objects.filter(email=email).exists():
            messages.info(request, 'This email address exists.')
            return redirect('register_patient')
        
        elif not mobile_number.isdigit() or len(mobile_number) != 10:
            messages.info(request,'Invalid phone number. Please enter a 10-digit number.')
            return redirect('register_patient') 


        patient_id = str(uuid.uuid4())[:8]

        patient = Patient(
            patient_id=patient_id,
            name=name,
            address=address,
            mobile_number=mobile_number,
            email=email,
        )
        patient.save()

        token_number = get_random_string(length=6)

        send_mail(
            'Patient Registration Successful',
            f'Thank you for registering! Your Patient ID is: {patient_id}\nYour Token Number is: {token_number}',
            'your_email@example.com',
            [email],
            fail_silently=False,
        )

        return redirect(reverse('appointment_form', kwargs={'patient_id': patient_id}))

    return render(request, 'patient_reg.html')


def appointment_form(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    departments = Department.objects.all()
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        department_id = request.POST.get('department')
        doctor_id = request.POST.get('doctor')

        
        token_number = int(get_random_string(length=6, allowed_chars='0123456789'))

        appointment = Appointment(
            patient=patient,
            department_id=department_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            token_number=token_number
        )
        appointment.save()

        return redirect('appointment_details', appointment_id=appointment.id)

    return render(request, 'appointment_form.html', {'patient': patient, 'departments': departments, 'doctors': doctors})



def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    context = {
        'appointment': appointment,
    }

    return render(request, 'appointment_details.html', context)

def search_patient(request):
    patient = None

    if request.method == 'GET':
        patient_id = request.GET.get('patient_id')

        if patient_id:
        
            patient = get_object_or_404(Patient, patient_id=patient_id)
            return redirect('patient_details', patient_id=patient_id)

    return render(request, 'search_patient.html', {'patient': patient})

def patient_details(request, patient_id):
    
    patient = get_object_or_404(Patient, patient_id=patient_id)


    appointments = Appointment.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'appointments': appointments,
    }

    return render(request, 'patient_details.html', context)










def get_doctors_by_department(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id).values('id', 'D_name')
    return JsonResponse(list(doctors), safe=False)


def doctor_signup(request):
        department=Department.objects.all()
        return render(request,'doctor_signup.html',{'department':department})

def generate_random_password(length=6):
    return get_random_string(length)

def register_doctor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        random_password = request.POST.get('password')
        age = request.POST.get('age')
        contact_number = request.POST.get('number')
        department_id = request.POST.get('sel')


        if CustomUser.objects.filter(username=username).exists():
            messages.info(request,'This username exits..')
            return redirect('doctor_signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'This email address exists.')
            return redirect('doctor_signup')
        
        elif not contact_number.isdigit() or len(contact_number) != 10:
            messages.info(request,'Invalid phone number. Please enter a 10-digit number.')
            return redirect('doctor_signup') 
        
        else:
            random_password = get_random_string(length=8)



            user = CustomUser.objects.create_user(username=username, email=email, password=random_password)
            user.user_type = '3'  
            user.save()

        
        doctor = Doctor(D_name=name,age=age, contact_number=contact_number, username=username,email=email,department_id=department_id)
        doctor.save()

        subject = 'Your Account Information'

        message = f'Hello {user.username},\n\nYour account has been created. Here are your login details:\n\nUsername: {user.username}\n Password: {random_password}\n\nPlease change your password after logging in.'
        send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
        messages.success(request, 'Signup successful. You can now login.')
        return redirect('admin_login')
        
    return render(request,'doctor_signup.html')

@login_required
def appointment_list(request):
    logged_in_user = request.user


    if logged_in_user.user_type == '3':
        doctor_profile = get_object_or_404(Doctor, username=logged_in_user.username)

        appointments = Appointment.objects.filter(doctor=doctor_profile)

        return render(request, 'appointment_list.html', {'appointments': appointments})


    return render(request, 'appointment_list.html', {'appointments': []})


@login_required
def consultation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        consultation = Consultation.objects.create(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment,
            reason=request.POST.get('reason'),
            medicine_name=request.POST.get('medicine_name'),
            consumption_time=request.POST.get('consumption_time')
        )


        appointment.consulted = True
        appointment.save()
        return redirect('doctor_consulted_patients')

    return render(request, 'consultation.html', {'appointment': appointment})


def reassign_patient(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        new_doctor_id = request.POST.get('new_doctor')

    
        new_doctor = get_object_or_404(Doctor, id=new_doctor_id)

        appointment.doctor = new_doctor
        appointment.save()

        return redirect(reverse('appointment_list'))

    doctors = Doctor.objects.all()
    return render(request, 'reassign_patient.html', {'appointment': appointment, 'doctors': doctors})

@login_required
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')            
            if not request.user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            else:                
                if new_password != confirm_password:
                    messages.error(request, 'New password and confirm password do not match.')
                else:                    
                    if not any(char.isdigit() for char in new_password):
                        messages.error(request, 'Password must contain at least one digit.')
                    elif not any(char.isalpha() for char in new_password):
                        messages.error(request, 'Password must contain at least one alphabet character.')
                    elif len(new_password) < 8:
                        messages.error(request, 'Password must be at least 8 characters long.')
                    elif not any(char in '!@#$%^&*()_+' for char in new_password):
                        messages.error(request, 'Password must contain at least one special character (!@#$%^&*()_+).')
                    else:                        
                        request.user.set_password(new_password)
                        request.user.save()
                        update_session_auth_hash(request, request.user)                    
                        messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        return render(request, 'change_password.html')
    return redirect('/')


@login_required
def change_password_pharmacy(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')            
            if not request.user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            else:                
                if new_password != confirm_password:
                    messages.error(request, 'New password and confirm password do not match.')
                else:                    
                    if not any(char.isdigit() for char in new_password):
                        messages.error(request, 'Password must contain at least one digit.')
                    elif not any(char.isalpha() for char in new_password):
                        messages.error(request, 'Password must contain at least one alphabet character.')
                    elif len(new_password) < 8:
                        messages.error(request, 'Password must be at least 8 characters long.')
                    elif not any(char in '!@#$%^&*()_+' for char in new_password):
                        messages.error(request, 'Password must contain at least one special character (!@#$%^&*()_+).')
                    else:                        
                        request.user.set_password(new_password)
                        request.user.save()
                        update_session_auth_hash(request, request.user)                    
                        messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_pharmacy')
        return render(request, 'change_password_pharmacy.html')
    return redirect('/')

def signup_pharmacy(request):
    if request.method == 'POST':
    
        username = request.POST.get('username')
        email = request.POST.get('email')
        pharmacy_name = request.POST.get('pharmacy_name')
        phone_number = request.POST.get('phone_number')
        
     
        if CustomUser.objects.filter(username=username).exists() or Pharmacy.objects.filter(email=email).exists():
            messages.error(request, 'Username or Email is already taken.')
            return redirect('signup_pharmacy')
        elif not phone_number.isdigit() or len(phone_number) != 10:
            messages.info(request,'Invalid phone number. Please enter a 10-digit number.')
            return redirect('signup_pharmacy')

        random_password = get_random_string(length=8)

        user = CustomUser.objects.create_user(username=username, email=email, password=random_password)
        user.user_type = '4'
        user.save()

        pharmacy = Pharmacy(username=username, pharmacy_name=pharmacy_name, phone_number=phone_number, email=email)
        pharmacy.save()

   
        subject = 'Your Pharmacy Account Information'
        message = f'Hello {user.username},\n\nYour pharmacy account has been created.\n\nUsername: {user.username}\nPassword: {random_password}\n\nPlease change your password after logging in.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        # Log in the user
        authenticated_user = authenticate(request, username=username, password=random_password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, f'Welcome {username}! You are now signed up.')
            return redirect('admin_login')
        else:
            messages.error(request, 'Failed to authenticate. Please log in.')

    return render(request, 'pharmacy_signup.html')

def consulted_patient_details(request):
    consulted_patients = Consultation.objects.select_related('patient', 'doctor', 'appointment__department').all()

    for consultation in consulted_patients:
        print(f"Patient: {consultation.patient.name}, Doctor: {consultation.doctor.D_name}")
        print(f"Appointment: {consultation.appointment}")
        print(f"Appointment Department: {consultation.appointment.department if consultation.appointment else 'N/A'}")
        print(f"Appointment Date: {consultation.appointment.appointment_date if consultation.appointment else 'N/A'}")

    context = {
        'consulted_patients': consulted_patients,
    }

    return render(request, 'consulted_patient_details.html', context)


def doctor_consulted_patients(request):

    logged_in_user = request.user
    if logged_in_user.user_type != '3':
  
        return redirect('index')  

    
    try:
        logged_in_doctor = Doctor.objects.get(username=logged_in_user.username)
    except Doctor.DoesNotExist:
        
        return redirect('index') 

   
    doctor_consultations = Consultation.objects.filter(doctor=logged_in_doctor)

 
    consulted_patients = []
    for consultation in doctor_consultations:
        consulted_patients.append({
            'patient': consultation.patient,
            'medicine_name': consultation.medicine_name,
            'consumption_time': consultation.consumption_time,
            'appointment_date': consultation.appointment.appointment_date,
            'appointment_time': consultation.appointment.appointment_time,
        })

    context = {
        'doctor': logged_in_doctor,
        'consulted_patients': consulted_patients,
    }

    return render(request, 'doctor_consulted_patients.html', context)

def all_consulted_patients(request):
    consulted_patients = Consultation.objects.all()

    context = {
        'consulted_patients': consulted_patients,
    }

    return render(request, 'all_consulted_patients.html', context)

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            new_password = generate_random_password()
            user.set_password(new_password)
            user.save()

            send_mail(
                'Password Recovery',
                f'Your new password is: {new_password}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'New password sent to your email. Check your inbox.')
            return redirect(reverse('admin_login'))
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect(reverse('forgotpassword'))

    return render(request, 'forgotpassword.html')


def doctor_home_search(request):
    logged_in_doctor = Doctor.objects.get(username=request.user.username)
    assigned_patients = Patient.objects.filter(appointment__doctor=logged_in_doctor)
    
    return render(request, 'doctor_home.html', {'assigned_patients': assigned_patients})

@login_required
def doctor_search_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        logged_in_doctor = get_object_or_404(Doctor, username=request.user.username)

        try:
            patient = get_object_or_404(Patient, patient_id=patient_id, appointment__doctor=logged_in_doctor)
            appointment_details = Appointment.objects.filter(patient=patient, doctor=logged_in_doctor).first()

            return render(request, 'doctor_home_search.html', {'patient': patient, 'appointment_details': appointment_details})

        except Http404:
            messages.warning(request, 'Patient not assigned to the doctor.')

    return render(request, 'doctor_search_patient.html')

def pharmacy_search(request):

    patient = None

    if request.method == 'POST':
        patient_id = request.GET.get('patient_id')

        if patient_id:
        
            patient = get_object_or_404(Patient, patient_id=patient_id)
            return redirect('pharmacy_home_search', patient_id=patient_id)

    return render(request, 'pharmacy_search.html', {'patient': patient})

def pharmacy_home_search(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        if patient_id:
            patient = get_object_or_404(Patient, patient_id=patient_id)
            consultations = Consultation.objects.filter(patient=patient)
            return render(request, 'pharmacy_home_search.html', {'patient': patient, 'consultations': consultations})

    return render(request, 'search_patient.html', {})

