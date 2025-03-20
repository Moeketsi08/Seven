from django.db import models
from django.contrib.auth.models import User
from academic.models import Department, Subject, Grade, Subject, Nationality, Session
from center_manager.models import Center
from address.models import Address
from learner.models import Learner

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    employee_code = models.PositiveIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    date_of_birth = models.DateField()
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    
    phone_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    id_number = models.CharField(max_length=20, unique=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    centers = models.ManyToManyField(Center, through='TeacherCenterAssignment')
    subjects_taught = models.ManyToManyField(Subject)
    grade_taught = models.ManyToManyField(Grade)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Generate a new employee_code only if it's not already set
        if self.employee_code is None:
            last_teacher = Teacher.objects.order_by('employee_code').last()
            self.employee_code = last_teacher.employee_code + 1 if last_teacher else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

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

class ATPSchedule(models.Model):
    date = models.DateField()
    day = models.CharField(max_length=10)
    mode = models.CharField(max_length=20, choices=[('Face-to-Face', 'Face-to-Face'), ('Online', 'Online')])
    paper = models.CharField(max_length=50, blank=True, null=True)
    topic = models.TextField()
    subject = models.CharField(max_length=50, default="Mathematics")
    term = models.CharField(max_length=10, default="Term 1")

    def __str__(self):
        return f"{self.date} - {self.topic}"

class Timesheet(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date = models.DateField()  # Date of the timesheet
    atp_hours = models.DecimalField(max_digits=4, decimal_places=2)  # Hours spent
    date_submitted = models.DateTimeField(auto_now_add=True)  # Auto-submitted timestamp
    attendance_marked = models.BooleanField(default=False)  # Indicates if attendance is marked
    approved = models.BooleanField(default=False)  # Field to indicate approval status

    def __str__(self):
        return f"{self.teacher.name} - {self.session} - {self.date}"

class Classroom(models.Model):
    grade =  models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='classrooms')
    learners = models.ManyToManyField(Learner, related_name='classrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('grade', 'subject', 'teacher')
    

    def __str__(self):
        return f"{self.teacher.name} {self.teacher.surname}: Grade {self.grade.grade} - {self.subject.subject}"
