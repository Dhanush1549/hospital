from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import render
from django.views import View
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('1', 'Type 1'),
        ('2', 'Type 2'),
        ('3', 'Type 3'),
        ('4', 'Type 4'),
    )

    user_type = models.CharField(default='1', max_length=1, choices=USER_TYPE_CHOICES)

class Department(models.Model):
    department = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.department
    

class Doctor(models.Model):
    D_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.D_name
    
class Patient(models.Model):
    patient_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  

    def __str__(self):
        return self.name
    
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    token_number = models.IntegerField(unique=True, blank=True, null=True)

@receiver(pre_save, sender=Appointment)
def generate_token_number(sender, instance, **kwargs):
    # Check if the token_number is not already set
    if instance.token_number is None:
        # Generate a unique token_number containing only numbers
        instance.token_number = int(get_random_string(length=6, allowed_chars='0123456789'))    


    def __str__(self):
        return f"{self.patient.name}'s Appointment on {self.appointment_date} at {self.appointment_time}"
    
class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='consultations',null=True)
    reason = models.TextField()
    medicine_name = models.CharField(max_length=255)
    consumption_time_choices = (
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    )
    consumption_time = models.CharField(max_length=7, choices=consumption_time_choices)


class Pharmacy(models.Model):
    username = models.CharField(max_length=50, unique=True)
    pharmacy_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.pharmacy_name}'s Pharmacy"
    