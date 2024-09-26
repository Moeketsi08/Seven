from django.db import models
<<<<<<< Updated upstream
from academic.models import Department
from administration.models import Designation
from address.models import District, Upazilla, Union
from django.contrib.auth.models import User

=======
from django.contrib.auth.models import User
from academic.models import Department, Center, Session, ClassInfo
from administration.models import Designation  # Add this line
>>>>>>> Stashed changes

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', default=2)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    date_of_birth = models.DateField()
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    phone_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    
    # Educational background
    highest_degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    
    # Kutlwanong specific fields
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    centers = models.ManyToManyField(Center, through='TeacherCenterAssignment')
    subjects_taught = models.ManyToManyField(ClassInfo)
    
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TeacherCenterAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        unique_together = ['teacher', 'center', 'start_date']

    def __str__(self):
        return f"{self.teacher.name} at {self.center.name}"

class TeacherQualification(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='qualifications')
    qualification_name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year_obtained = models.IntegerField()

    def __str__(self):
        return f"{self.teacher.name} - {self.qualification_name}"

class TeacherPerformance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='performances')
    evaluation_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comments = models.TextField()

    def __str__(self):
        return f"{self.teacher.name} - {self.evaluation_date}"

<<<<<<< Updated upstream
class PersonalInfo(models.Model):
    name = models.CharField(max_length=45)
    photo = models.ImageField()
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=45)
    nationality_choice = (
        ('South African', 'South African'),
        ('Others', 'Others')
    )
    nationality = models.CharField(max_length=45, choices=nationality_choice)
    religion_choice = (
        ('Christianity', 'Christianity'),
        ('Others', 'Others')
    )
    religion = models.CharField(max_length=45, choices=religion_choice)
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
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
    e_tin = models.IntegerField(unique=True)
    nid = models.IntegerField(unique=True)
    driving_license_passport = models.IntegerField(unique=True)
    phone_no = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=255, unique=True)
    father_name = models.CharField(max_length=45)
    mother_name = models.CharField(max_length=45)
    marital_status_choice = (
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('divorced', 'Divorced'),
        ('single', 'Single')
    )
    marital_status = models.CharField(choices=marital_status_choice, max_length=10)
    address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, null=True)
    education = models.ForeignKey(EducationInfo, on_delete=models.CASCADE, null=True)
    training = models.ForeignKey(TrainingInfo, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(JobInfo, on_delete=models.CASCADE, null=True)
    experience = models.ForeignKey(ExperienceInfo, on_delete=models.CASCADE, null=True)
    is_delete = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.start_time} to {self.end_time} ({self.total_hours} hours)'
=======
class Timesheet(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    session = models.ForeignKey('academic.Session', on_delete=models.CASCADE)
    date = models.DateField()  # Add this line
    atp_hours = models.DecimalField(max_digits=4, decimal_places=2)
    date_submitted = models.DateTimeField(auto_now_add=True)
    attendance_marked = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return f"{self.teacher.name} - {self.session} - {self.date}"
>>>>>>> Stashed changes
