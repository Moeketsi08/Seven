from django import forms
from .models import Teacher, TeacherCenterAssignment, TeacherQualification, Timesheet  # Add this import at the top of the file
from academic.models import Department
from .models import Timesheet


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

class TeacherQualificationForm(forms.ModelForm):
    class Meta:
        model = TeacherQualification
        fields = '__all__'
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'qualification_name': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'year_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AttendanceTimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['session', 'date', 'atp_hours', 'attendance_marked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'atp_hours': forms.NumberInput(attrs={'step': '0.5'}),
            'attendance_marked': forms.CheckboxInput(),
        }

class TimesheetForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Start Time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'End Time'}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        
        if start_time and end_time:
            if end_time <= start_time:
                self.add_error('end_time', 'End time must be after start time.')
