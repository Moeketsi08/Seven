from django.db import models
import random
from django.utils.timezone import now

from academic.models import ClassInfo, ClassRegistration
from address.models import District, Upazilla, Union
from teacher.models import Teacher

class PersonalInfo(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    photo = models.ImageField(upload_to='student-photos/')
    blood_group_choice = (
        ('a+', 'A+'),
        ('o+', 'O+'),
        ('b+', 'B+'),
        ('ab+', 'AB+'),
        ('a-', 'A-'),
        ('o-', 'O-'),
        ('b-', 'B-'),
        ('ab-', 'AB-')
    )
    blood_group = models.CharField(choices=blood_group_choice, max_length=5)
    date_of_birth = models.DateField()
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)
    birth_certificate_no = models.CharField(max_length=50)  # Changed to CharField to accommodate alphanumeric certificates
    religion_choice = (
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Christianity', 'Christianity'),
        ('Others', 'Others')
    )
    religion = models.CharField(choices=religion_choice, max_length=45)
    nationality_choice = (
        ('SA', 'South African'),
        ('ZW', 'Zimbabwe')
    )
    nationality = models.CharField(choices=nationality_choice, max_length=45)
    race_choices = (
        ('B', 'Black African'),
        ('W', 'White'),
        ('C', 'Coloured'),
        ('A', 'Asian/Indian'),
        ('O', 'Other')
    )
    race = models.CharField(choices=race_choices, max_length=45)
    home_language_choices = (
        ('english', 'English'),
        ('zulu', 'Zulu'),
        ('xhosa', 'Xhosa'),
        ('afrikaans', 'Afrikaans'),
        ('pedi', 'Pedi'),
        ('tswana', 'Tswana'),
        ('sotho', 'Sotho'),
        ('tsonga', 'Tsonga'),
        ('swati', 'Swati'),
        ('venda', 'Venda'),
        ('ndebele', 'Ndebele'),
        ('other', 'Other')        
    )
    home_language = models.CharField(choices=home_language_choices, max_length=45)
    disability_choices = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    disability = models.CharField(choices=disability_choices, max_length=10)

    def __str__(self):
        return self.name

class StudentAddressInfo(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)
    village = models.TextField()

    def __str__(self):
        return self.village


class GuardianInfo(models.Model):
    student = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    guardian_name = models.CharField(max_length=45)
    guardian_surname = models.CharField(max_length=45)
    relationship_choice = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)
    guardian_phone_no = models.CharField(max_length=11)
    guardian_email = models.EmailField(blank=True, null=True)
    place_of_work =models.CharField(max_length=100)
    guardian_work_no = models.CharField(max_length=11)
    
    def __str__(self):
        return self.guardian_name

class EmergencyContactDetails(models.Model):
    student = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    emergency_guardian_name = models.CharField(max_length=100)
    address = models.TextField()
    relationship_choice = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_student = models.CharField(choices=relationship_choice, max_length=45)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.emergency_guardian_name


class PreviousAcademicInfo(models.Model):
    institute_name = models.CharField(max_length=100)
    name_of_exam = models.CharField(max_length=100)
    group = models.CharField(max_length=45)
    gpa = models.CharField(max_length=10)
    board_roll = models.CharField(max_length=50)  # Changed to CharField for flexibility
    passing_year = models.IntegerField()

    def __str__(self):
        return self.institute_name

class PreviousAcademicCertificate(models.Model):
    birth_certificate = models.FileField(upload_to='documents/', blank=True)
    release_letter = models.FileField(upload_to='documents/', blank=True)
    testimonial = models.FileField(upload_to='documents/', blank=True)
    marksheet = models.FileField(upload_to='documents/', blank=True)
    stipen_certificate = models.FileField(upload_to='documents/', blank=True)
    other_certificate = models.FileField(upload_to='documents/', blank=True)


class AcademicInfo(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    registration_no = models.IntegerField(unique=True, default=random.randint(100000, 999999))
    status_select = (
        ('not enrolled', 'Not Enrolled'),
        ('enrolled', 'Enrolled'),
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('passed', 'Passed'),
    )
    status = models.CharField(choices=status_select, default='not enrolled', max_length=15)
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    address_info = models.ForeignKey(StudentAddressInfo, on_delete=models.CASCADE, null=True)
    guardian_info = models.ForeignKey(GuardianInfo, on_delete=models.CASCADE, null=True)
    emergency_contact_info = models.ForeignKey(EmergencyContactDetails, on_delete=models.CASCADE, null=True)
    previous_academic_info = models.ForeignKey(PreviousAcademicInfo, on_delete=models.CASCADE, null=True)
    previous_academic_certificate = models.ForeignKey(PreviousAcademicCertificate, on_delete=models.CASCADE, null=True)
    joined_programme = models.DateField(auto_now_add=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    learner_provice_choice = (
        ('EC', 'Eastern Cape'),
        ('GP', 'Gauteng'),
        ('KZN', 'KwaZulu-Natal'),
        ('LP', 'Limpopo'),
        ('MP', 'Mpumalanga'),
        ('NC', 'Northern Cape'),
        ('NW', 'North West'),
        ('WC', 'Western Cape'),
        ('FS', 'Free State')
    )
    learner_provice = models.CharField(choices=learner_provice_choice, max_length=50, null=True)

    def __str__(self):
        return str(self.registration_no)

class EnrolledStudent(models.Model):
    class_name = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    student_record = models.OneToOneField(AcademicInfo, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['class_name', 'student_record']
    
    def __str__(self):
        return str(self.roll)


class Student(models.Model):
    student = models.ForeignKey(EnrolledStudent, on_delete=models.CASCADE)
    class_registration = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


