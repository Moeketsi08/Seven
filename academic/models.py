from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ClassInfo(models.Model):
    SUBJECT_CHOICES = [
        ('Mathematics', 'Mathematics'),
        ('Mathematics Exam', 'Mathematics Examination'),
        ('Physical Science', 'Physical Science'),
        ('Physical Science Exam', 'Physical Science Examination')
    ]
    GRADE_CHOICES = [
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    subject = models.CharField(max_length=21, choices=SUBJECT_CHOICES, default='Mathematics')  # Added default value
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, default='10')  # Already had default value

    # class Meta:
    #     unique_together = ['subject', 'grade']

    def __str__(self):
        return f"{self.get_subject_display()} - Grade {self.grade}"

class Section(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    DAY_CHOICES = [
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THUR', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    day = models.CharField(max_length=4, choices=DAY_CHOICES, default='SAT')
    start_time = models.TimeField(default='09:00')
    end_time = models.TimeField(default='17:00')
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, default=1)  # Add this line

    class Meta:
        unique_together = ['day', 'start_time', 'end_time', 'class_info']

    def __str__(self):
        return f"{self.class_info} - {self.get_day_display()} ({self.start_time} - {self.end_time})"

class Shift(models.Model):
    name = models.CharField(max_length=45, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

#class GuideTeacher(models.Model):
    #name = models.OneToOneField('teacher.PersonalInfo', on_delete=models.CASCADE, null=True)
    #date = models.DateField(auto_now_add=True)

    #def __str__(self):
        #PersonalInfo = apps.get_model('teacher', 'PersonalInfo')
        #return str(self.name)

class Center(models.Model):
    name = models.CharField(max_length=100, default='Default Center')
    address = models.TextField(default='Default Address')

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


#class Union(models.Model):
    #name = models.CharField(max_length=100, unique=True)
    #upazilla = models.ForeignKey(Upazilla, on_delete=models.CASCADE)
    #date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
class ClassRegistration(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ['center', 'session']

    def __str__(self):
        center_name = self.center.name if self.center else "No Center"
        session_name = str(self.session) if self.session else "No Session"
        return f"{center_name} - {session_name}"



#class ClassRegistrationNew(models.Model):
    #center = models.ForeignKey(Center, on_delete=models.CASCADE)
    #session = models.ForeignKey(Session, on_delete=models.CASCADE)

    #class Meta:
        #unique_together = ['center', 'session']

    #def __str__(self):
        #return f"{self.center} - {self.session}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_registration = models.ForeignKey(ClassRegistration, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
