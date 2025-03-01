from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django_select2.forms import Select2MultipleWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from teacher.models import Department, Classroom, Teacher, Timesheet
from learner.models import Learner
from center_manager.models import Center, Designation
from academic.models import Grade, Nationality, Session, Subject

class CenterManagerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddDesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['designation_type', 'name_surname', 'contact_number', 'email_address', 'physical_address', 'documents']
        widgets = {
            'designation_type': forms.Select(attrs={'class': 'form-control'}),
            'name_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documents': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class AllocateTeacherForm(forms.ModelForm):
    learner = forms.ModelMultipleChoiceField(
        queryset=Learner.objects.none(),  # Set an initial empty queryset
        widget=Select2MultipleWidget(attrs={'class': 'form-control'})  # Correct widget configuration
    )
    subject = forms.ChoiceField(choices=Subject.SUBJECT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject", widget=forms.Select(attrs={'class': 'form-control'}))
    #grade = forms.ChoiceField(choices=Grade.GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(), empty_label="Select Grade", widget=forms.Select(attrs={'class': 'form-control'})
    )
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Classroom  # Specify the model
        fields = ['subject', 'grade', 'learner', 'teacher'] 

    def __init__(self, *args, **kwargs):
        center = kwargs.pop('center', None)  # Retrieve center from kwargs
        super().__init__(*args, **kwargs)
        if center:
            # Filter teachers and learners by the center
            self.fields['teacher'].queryset = Teacher.objects.filter(
                teachercenterassignment__center=center,
                teachercenterassignment__is_current=True
            ).distinct()
            self.fields['learner'].queryset = Learner.objects.filter(center=center)
        else:
            self.fields['teacher'].queryset = Teacher.objects.none()  # No center, no options
            self.fields['learner'].queryset = Learner.objects.none()  # No center, no options

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ['document_file']
        
class TimesheetForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_time = forms.ChoiceField(choices=Session.START_TIME, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Start Time'}))
    end_time = forms.ChoiceField(choices=Session.END_TIME, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'End Time'}))
    subjects = forms.ChoiceField(choices=Subject.SUBJECT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grades = forms.ChoiceField(choices=Grade.GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    day = forms.ChoiceField(choices=Session.DAY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        subjects = cleaned_data.get("subjects")
        grades = cleaned_data.get("grades")
        day = cleaned_data.get("day")
        
        if start_time and end_time:
            if end_time <= start_time:
                self.add_error('end_time', 'End time must be after start time.')

class LearnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = [
            'name', 'surname', 'photo', 'date_of_birth', 'gender',
            'phone_no', 'email', 'id_no', 'nationality',
            'race', 'home_language', 'disability', 'disabilities', 'center',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control','placeholder':'surname'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control','placeholder':'photo'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','placeholder':'date_of_birth'}),
            'gender': forms.TextInput(attrs={'class': 'form-control','placeholder':'gender'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control','placeholder':'phone_no'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'email'}),
            'id_no': forms.TextInput(attrs={'class': 'form-control','placeholder':'ID No'}),
            'nationality': CountryField().formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'})),
            'race': forms.TextInput(attrs={'class': 'form-control'}),
            'home_language': forms.TextInput(attrs={'class': 'form-control'}),
            'disability': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'disabilities': forms.Select(attrs={'class': 'form-control'}),
            'center': forms.TextInput(attrs={'class': 'form-control'}),
        }

     # ForeignKey fields: use ModelChoiceField for nationality and center
    nationality = forms.ModelChoiceField(
        queryset=Nationality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    center = forms.ModelChoiceField(
        queryset=Center.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # Choice fields: use ChoiceField for predefined choices like gender, race, home language, disability
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    RACE_CHOICES = (
        ('B', 'Black African'),
        ('W', 'White'),
        ('C', 'Coloured'),
        ('A', 'Asian/Indian'),
        ('O', 'Other')
    )
    race = forms.ChoiceField(
        choices=RACE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    HOME_LANGUAGE_CHOICES = (
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
    home_language = forms.ChoiceField(
        choices=HOME_LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    DISABILITY_CHOICES = [
        ('hearing_impairment', 'Hearing Impairment - Difficulties hearing properly (Needs to sit near/far)'),
        ('visual_impairment', 'Visual Impairment - Near/far sighted'),
        ('physical_disability', 'Physical Disability - Physically impaired'),
        ('cognitive_impairment', 'Cognitive Impairment'),
    ]
    disabilities = forms.ChoiceField(
        choices=DISABILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    DISABILITY_CHOICES_YES_NO = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    disability = forms.ChoiceField(
        choices=DISABILITY_CHOICES_YES_NO,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        disability = cleaned_data.get('disability')
        disabilities = cleaned_data.get('disabilities')

        if disability == 'Y':  # If disability is 'Yes'
            if not disabilities:
                self.add_error('disabilities', 'This field is required if you have a disability.')
        else:
            # If disability is not 'Yes', clear the disabilities field
            cleaned_data['disabilities'] = None

        return cleaned_data      

class ClassroomFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets for each form in the formset
        for form in self.forms:
            form.fields['subject'].widget.attrs.update({'class': 'form-control'})
            form.fields['grade'].widget.attrs.update({'class': 'form-control'})
            form.fields['teacher'].widget.attrs.update({'class': 'form-control'})
            form.fields['learners'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})  # Checkbox select for multiple learners
            form.fields['learners'].queryset = Learner.objects.all()  # Default queryset, can be filtered later

# Create the formset using the custom formset class
ClassroomFormSet = modelformset_factory(
    Classroom,
    formset=ClassroomFormSet,
    fields=('grade', 'subject', 'teacher', 'learners'),
    extra=0,  # No extra forms
)