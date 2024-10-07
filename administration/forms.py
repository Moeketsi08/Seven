from django import forms
from teacher import models

class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AddDesignationForm(forms.ModelForm):
    class Meta:
        model = models.Designation
        fields = ['designation_type', 'name_surname', 'contact_number', 'email_address', 'physical_address', 'documents']
        widgets = {
            'designation_type': forms.Select(attrs={'class': 'form-control'}),
            'name_surname': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documents': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

""" class AllocateTeacherForm(forms.ModelForm):
    class Meta:
        model = models.Designation
        fields = ['designation_type','center', 'teacher', 'session']
        widgets = {
            'designation_type': forms.Select(attrs={'class': 'form-control'}),
            'center': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
        }  """       
