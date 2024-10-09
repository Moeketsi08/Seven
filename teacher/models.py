from django.db import models
from django.contrib.auth.models import User
from academic.models import Department, Center, ClassInfo, Session
from center_manager.models import Designation  # Add this line
from student.models import Student

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

# class TeacherQualification(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='qualifications')
#     qualification_name = models.CharField(max_length=200)
#     institution = models.CharField(max_length=200)
#     year_obtained = models.IntegerField()

#     def __str__(self):
#         return f"{self.teacher.name} - {self.qualification_name}"

# class TeacherPerformance(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='performances')
#     evaluation_date = models.DateField()
#     rating = models.DecimalField(max_digits=3, decimal_places=2)
#     comments = models.TextField()

#     def __str__(self):
#         return f"{self.teacher.name} - {self.evaluation_date}"

class Timesheet(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    session = models.ForeignKey('academic.Session', on_delete=models.CASCADE)
    date = models.DateField()  # Add this line
    atp_hours = models.DecimalField(max_digits=4, decimal_places=2)
    date_submitted = models.DateTimeField(auto_now_add=True)
    attendance_marked = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return f"{self.teacher.name} - {self.session} - {self.date}"

class ClassGroup(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, related_name='class_groups')  # Link to ClassInfo
    students = models.ManyToManyField(Student, related_name='class_groups')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_groups')  # Changed to ForeignKey

    def __str__(self):
        return str(self.class_info)  # Returns the string representation from ClassInfo