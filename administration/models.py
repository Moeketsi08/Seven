from django.db import models

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

