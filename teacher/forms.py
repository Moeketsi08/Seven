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
<<<<<<< Updated upstream
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'e_tin': forms.NumberInput(attrs={'class': 'form-control'}),
            'nid': forms.NumberInput(attrs={'class': 'form-control'}),
            'driving_license_passport': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),

        }


class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = models.AddressInfo
        fields = ('district', 'upazilla', 'union', 'village')
        widgets = {
            'district': forms.Select(attrs={'class': 'form-control'}),
            'upazilla': forms.Select(attrs={'class': 'form-control'}),
            'union': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['upazilla'].queryset = models.Upazilla.objects.none()

            if 'upazilla' in self.data:
                try:
                    district_id = int(self.data.get('district'))
                    self.fields['upazilla'].queryset = models.Upazilla.objects.filter(district_id=district_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['upazilla'].queryset = self.instance.district.upazilla_set.order_by('name')

            self.fields['union'].queryset = models.Union.objects.none()

            if 'union' in self.data:
                try:
                    upazilla_id = int(self.data.get('upazilla'))
                    self.fields['union'].queryset = models.Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['union'].queryset = self.instance.upazilla.union_set.order_by('name')



class EducationInfoForm(forms.ModelForm):
    class Meta:
        model = models.EducationInfo
        fields = '__all__'
        widgets = {
            'name_of_exam': forms.TextInput(attrs={'class': 'form-control'}),
            'institute': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'board': forms.TextInput(attrs={'class': 'form-control'}),
            'passing_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TrainingInfoForm(forms.ModelForm):
    class Meta:
        model = models.TrainingInfo
        fields = '__all__'
        widgets = {
            'training_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
=======
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
>>>>>>> Stashed changes
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
