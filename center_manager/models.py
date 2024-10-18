from django.db import models
from django.contrib.auth.models import User

from address.models import Address

class Designation(models.Model):
    DESIGNATION_CHOICES = [
        ('Finance Manager', 'Finance Manager'),
        ('Centre Manager', 'Centre Manager'),
        ('Teacher', 'Teacher'),
    ]

    designation_type = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, default='Teacher')
    name_surname = models.CharField(max_length=100, default='Name & Surname')
    contact_number = models.CharField(max_length=10, default='062 123 4472')
    email_address = models.EmailField(default='example@gmail.com')
    physical_address = models.TextField(default='No Address')
    documents = models.FileField(upload_to='documents/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.designation_type} - {self.name_surname}"
    
    
class CenterManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='center_managers')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)  # Fixed typo
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='center_managers')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Center(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)  # Optional
    center_manager = models.OneToOneField(CenterManager, on_delete=models.CASCADE, related_name='center')  # Changed to OneToOneField
    email = models.EmailField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='centers')

    def __str__(self):
        return self.name
    


class Report(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='reports/')  # Field to upload files
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date/time when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update the date/time when modified
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='reports')  # Link to the center
    center_manager = models.ForeignKey(CenterManager, on_delete=models.CASCADE, related_name='reports')  # Link to the manager

    def __str__(self):
        return self.title

