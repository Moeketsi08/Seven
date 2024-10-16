from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import ValidationError

from learner.models import Learner, ParentGuardian, EmergencyContact
from academic.models import Registration
from address.models import Address

class LearnerForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_certificate_no': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': CountryField().formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'})),
            'race': forms.Select(attrs={'class': 'form-control'}),
            'home_language': forms.Select(attrs={'class': 'form-control'}),
            'disability': forms.Select(attrs={'class': 'form-control'}),
            'disabilities': forms.CheckboxSelectMultiple(),
        }
    def clean(self):
        cleaned_data = super().clean()
        disability_status = cleaned_data.get('disability')
        disabilities = cleaned_data.get('disabilities')

        # Validation logic for disability association
        if disability_status == 'N' and disabilities:
            raise ValidationError("A learner without a disability cannot have associated disabilities.")

        if disability_status == 'Y' and not disabilities:
            raise ValidationError("A learner marked as having a disability must have at least one associated disability.")

        return cleaned_data

class LearnerAddressInfoForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'unit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            
        }


class GuardianInfoForm(forms.ModelForm):
    class Meta:
        model = ParentGuardian
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'work_number': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_employment': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'relationship_with_learner': forms.Select(attrs={'class': 'form-control'}),
        }

class EmergencyContactDetailsForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'relationship_with_learner': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'work_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class LearnerSearchForm(forms.Form):
    registration_no = forms.CharField(label='Registration No', max_length=20, required=False)
