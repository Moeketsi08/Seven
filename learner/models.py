from django.db import models
import random
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from address.models import Address
from academic.models import Nationality
from center_manager.models import Center

class Learner(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    photo = models.ImageField(upload_to='learner-photos/')
    date_of_birth = models.DateField()
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    gender = models.CharField(choices=GENDER_CHOICE, max_length=10)
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank=True, null=True)
    birth_certificate_no = models.CharField(max_length=50)  # Changed to CharField to accommodate alphanumeric certificates
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    RACE_CHOICE = (
        ('B', 'Black African'),
        ('W', 'White'),
        ('C', 'Coloured'),
        ('A', 'Asian/Indian'),
        ('O', 'Other')
    )
    race = models.CharField(choices=RACE_CHOICE, max_length=45)
    HOME_LANUAGE_CHOICE = (
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
    home_language = models.CharField(choices=HOME_LANUAGE_CHOICE, max_length=45)
    disability_choices = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    disability = models.CharField(choices=disability_choices, max_length=10)
    disabilities = models.OneToOneField('Disability', on_delete=models.SET_NULL, null=True, blank=True) 
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='learners')  # Center relationship
    joined_programme = models.DateField(auto_now_add=True, null=True)
    exited_programme = models.DateField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    
    def clean(self):
        # If disability is 'No', ensure no disability is associated
        if self.disability == 'N' and self.disabilities is not None:
            raise ValidationError("A learner without a disability cannot have an associated disability.")
        
        # If disability is 'Yes', ensure a disability is assigned
        if self.disability == 'Y' and self.disabilities is None:
            raise ValidationError("A learner marked as having a disability must have an associated disability.")


    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Disability(models.Model):
    disability_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    accommodations = models.TextField(blank=True, null=True)  # Specify any needed accommodations
    # learners = models.ManyToManyField(Learner, related_name='learner_disabilities')  # Many-to-many relationship with Learner
    
    def __str__(self):
        return self.disability_type
    
    
class ParentGuardian(models.Model):
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    RELATIONSHIP_CHOICE = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_learner = models.CharField(choices=RELATIONSHIP_CHOICE, max_length=45)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    learners = models.ManyToManyField(Learner, related_name='parents')  # Many-to-Many relationship with Learner
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    work_number = models.CharField(max_length=15)
    employment_place = models.CharField(max_length=25)  # Corrected spelling
    
    def __str__(self):
        return f"{self.name} {self.surname}"


class EmergencyContact(models.Model):
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    RELATIONSHIP_CHOICE = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
    )
    relationship_with_learner = models.CharField(choices=RELATIONSHIP_CHOICE, max_length=45)
    phone_number = models.CharField(max_length=15)
    place_of_employment = models.CharField(max_length=25)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='emergency_contact')  # One emergency contact per learner
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    work_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=15)
    
    def __str__(self):
        return f"{self.name} {self.surname}"

class SupportDocument(models.Model):
    document_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='support_documents/')
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)


    

# class AcademicInfo(models.Model):
#     class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
#     registration_no = models.IntegerField(unique=True, default=random.randint(100000, 999999))
#     status_select = (
#         ('not enrolled', 'Not Enrolled'),
#         ('enrolled', 'Enrolled'),
#         ('regular', 'Regular'),
#         ('irregular', 'Irregular'),
#         ('passed', 'Passed'),
#     )
#     status = models.CharField(choices=status_select, default='not enrolled', max_length=15)
#     personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
#     address_info = models.ForeignKey(LearnerAddressInfo, on_delete=models.CASCADE, null=True)
#     guardian_info = models.ForeignKey(GuardianInfo, on_delete=models.CASCADE, null=True)
#     emergency_contact_info = models.ForeignKey(EmergencyContactDetails, on_delete=models.CASCADE, null=True)
#     # previous_academic_info = models.ForeignKey(PreviousAcademicInfo, on_delete=models.CASCADE, null=True)
#     previous_academic_certificate = models.ForeignKey(PreviousAcademicCertificate, on_delete=models.CASCADE, null=True)
#     joined_programme = models.DateField(auto_now_add=True, null=True)
#     date = models.DateField(auto_now_add=True)
#     is_delete = models.BooleanField(default=False)
#     learner_provice_choice = (
#         ('EC', 'Eastern Cape'),
#         ('GP', 'Gauteng'),
#         ('KZN', 'KwaZulu-Natal'),
#         ('LP', 'Limpopo'),
#         ('MP', 'Mpumalanga'),
#         ('NC', 'Northern Cape'),
#         ('NW', 'North West'),
#         ('WC', 'Western Cape'),
#         ('FS', 'Free State')
#     )
#     learner_provice = models.CharField(choices=learner_provice_choice, max_length=50, null=True)

#     def __str__(self):
#         return str(self.registration_no)





