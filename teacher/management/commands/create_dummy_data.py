# In your_app/management/commands/create_dummy_data.py

import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django_countries import countries
import random

from academic.models import Subject, Grade, Registration, Nationality, Department
from address.models import Address, Province
from center_manager.models import CenterManager, Center
from learner.models import Learner
from teacher.models import Teacher, Classroom
from address.models import Address

class Command(BaseCommand):
    help = 'Generate dummy data for the database'

    def handle(self, *args, **kwargs):
        # Generate sample Nationalities
        country_code = random.choice(list(countries))
        nationality, created = Nationality.objects.get_or_create(nationality=country_code)

        # Generate sample Departments
        department_names = ["Math Department", "Physical Science Department"]
        for dept_name in department_names:
            Department.objects.get_or_create(name=dept_name)
        
        # Create Provinces
        provinces = [
            ('EC', 'Eastern Cape'), ('GP', 'Gauteng'), ('KZN', 'KwaZulu-Natal'), ('WC', 'Western Cape'),
            ('FS', 'Free State'), ('NW', 'North West'), ('NC', 'Northern Cape'), ('MP', 'Mpumalanga')
        ]
        for code, name in provinces:
            Province.objects.get_or_create(province=code)
        
        # Sample addresses
        for _ in range(5):
            Address.objects.create(
                unit_number=str(random.randint(1, 20)),
                street="Main Street",
                city="Cape Town",
                postal_code="8001",
                province=Province.objects.order_by('?').first()
            )

        # Generate Centers and Center Managers
        center_managers = []
        for i in range(1, 4):
            user = User.objects.create(username=f'center_manager{i}')
            center_manager = CenterManager.objects.create(
                user=user,
                name=f"Manager{i}",
                surname=f"Surname{i}",
                phone_number="0721234567",
                email=f"manager{i}@example.com",
                address=Address.objects.order_by('?').first()
            )
            center = Center.objects.create(
                name=f"Center {i}",
                contact_info="0123456789",
                center_manager=center_manager,
                email=f"center{i}@example.com",
                address=Address.objects.order_by('?').first()
            )
            center_managers.append(center_manager)
        
        # Sample Subjects and Grades
        subject_names = ['Mathematics', 'Physical Science']
        for subj in subject_names:
            Subject.objects.get_or_create(subject=subj)
        grades = ['10', '11', '12']
        for grade in grades:
            Grade.objects.get_or_create(grade=grade)
        
        # Sample Teachers
        for i in range(5):
            user = User.objects.create(username=f'teacher{i}')
            Teacher.objects.create(
                user=user,
                name=f"Teacher{i}",
                surname=f"Surname{i}",
                date_of_birth=datetime(1990, 1, 1),
                gender='Male' if i % 2 == 0 else 'Female',
                phone_no=f"083000{i}567",
                email=f"teacher{i}@example.com",
                id_number=f"900101000000{i}",
                department=Department.objects.order_by('?').first(),
                nationality=nationality,
                date_joined=datetime.now().date(),
                address=Address.objects.order_by('?').first()
            )
        
        # Sample Learners
        for i in range(10):
            Learner.objects.create(
                name=f"Learner{i}",
                surname=f"Surname{i}",
                date_of_birth=datetime(2006, 1, 1),
                gender='M' if i % 2 == 0 else 'F',
                phone_no=f"07212345{i}",
                email=f"learner{i}@example.com",
                birth_certificate_no=f"BC{i}",
                nationality=nationality,
                race='B' if i % 2 == 0 else 'W',
                home_language='english',
                disability='N',
                center=Center.objects.order_by('?').first()
            )
        
        # Sample Classrooms
        for i in range(3):
            Classroom.objects.create(
                grade=Grade.objects.order_by('?').first(),
                subject=Subject.objects.order_by('?').first(),
                teacher=Teacher.objects.order_by('?').first(),
                center=Center.objects.order_by('?').first()
            )
        
        # Sample Registrations
        for learner in Learner.objects.all():
            Registration.objects.create(
                learner=learner,
                status=random.choice(['Pending', 'Completed']),
                fees_paid=random.uniform(0, 1000),
                center=Center.objects.order_by('?').first()
            )
        
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully'))
