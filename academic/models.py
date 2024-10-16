from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from center_manager.models import Center

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    SUBJECT_CHOICES = [
        ('Mathematics', 'Mathematics'),
        ('Mathematics Exam', 'Mathematics Examination'),
        ('Physical Science', 'Physical Science'),
        ('Physical Science Exam', 'Physical Science Examination')
    ]
    subject = models.CharField(max_length=21, choices=SUBJECT_CHOICES, default='Mathematics', unique=True)  # Added default valu
    created = models.DateField(default=now)

    def __str__(self):
        return self.subject
    
class Grade(models.Model):
    GRADE_CHOICES = [
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, default='10', unique=True)  # Already had default value
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.grade

class Session(models.Model):
    DAY_CHOICES = [
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday')
    ]
    START_TIME = [
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('12:00', '12:00'),
        ('14:00', '14:00'),
    ]
    END_TIME = [
        ('12:00', '12:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
    ]
    day = models.CharField(max_length=4, choices=DAY_CHOICES, default='SAT')
    start_time = models.TimeField(choices=START_TIME, default='10:00')
    end_time = models.TimeField(choices=END_TIME,default='16:00')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        subject_str = str(self.subject) if self.subject else "No Subject"
        grade_str = str(self.grade) if self.grade else "No Grade"
        return f"{subject_str} - {grade_str}- {self.get_day_display()} ({self.start_time} - {self.end_time})"
    
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")



class Registration(models.Model):  # Corrected from models.Models
    learner = models.ForeignKey('learner.Learner', on_delete=models.CASCADE)
    registration_number = models.PositiveIntegerField(unique=True, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date and time of registration
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.registration_number is None and self.status == 'Completed':
            last_learner = Registration.objects.order_by('registration_number').last()
            self.registration_number = last_learner.registration_number + 1 if last_learner else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.learner.name} {self.learner.surname} - {self.status}"
    
    
class Nationality(models.Model):
    nationality = CountryField(blank_label="(select country)")
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nationality.name                             

