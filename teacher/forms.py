from django import forms
from django.forms import formset_factory
from .models import Teacher, TeacherCenterAssignment, Timesheet  # Add this import at the top of the file
from academic.models import Department, ClassInfo, Session
#from .models import Timesheet


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = {'centers', 'is_active'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'highest_degree': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'subjects_taught': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control'}),
        }

class TeacherCenterAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherCenterAssignment
        fields = '__all__'
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'center': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AttendanceTimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['date', 'atp_hours']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'atp_hours': forms.NumberInput(attrs={'step': '0.5'}),
        }

class StudentAttendanceForm(forms.Form):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    student_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    status = forms.ChoiceField(choices=ATTENDANCE_CHOICES, widget=forms.RadioSelect)

StudentAttendanceFormSet = formset_factory(StudentAttendanceForm, extra=0)

class TimesheetForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Start Time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'End Time'}))
    subjects = forms.ChoiceField(choices=ClassInfo.SUBJECT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grades = forms.ChoiceField(choices=ClassInfo.GRADE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
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
