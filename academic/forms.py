from django import forms
from . import models
from academic.models import Registration



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class ClassForm(forms.ModelForm):
#     class Meta:
#         model = models.
#         fields = '__all__'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'display_name': forms.TextInput(attrs={'class': 'form-control'}),
#         }

class SessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = '__all__'
        widgets = {
            'name': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ClassRegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        widgets = {
            'learner': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'fees_paid': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Select(attrs={'class': 'form-control'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

#class GuideTeacherForm(forms.ModelForm):
    #class Meta:
        #model = models.GuideTeacher
        #fields = '__all__'
        #widgets = {
            #'name': forms.Select(attrs={'class': 'form-control'}),
        #}
