from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from learner.models import Learner, ParentGuardian, EmergencyContact
from address.models import Address


class LearnerForm(forms.ModelForm):
    #confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = Learner
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_certificate_no': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality':CountrySelectWidget(attrs={'class': 'form-control'}),
            'race': forms.Select(attrs={'class': 'form-control'}),
            'home_language': forms.Select(attrs={'class': 'form-control'}),
            'disability': forms.Select(attrs={'class': 'form-control'}),
            'disabilities': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically hide the disabilities field if disability is not 'Y'
        if self.instance and self.instance.disability != 'Y':
            self.fields['disabilities'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        cleaned_data = super().clean()
        #password = cleaned_data.get("birth_certificate_no")  # Set password to birth_certificate_no
        #confirm_password = cleaned_data.get("confirm_password")
        
        disability_status = cleaned_data.get('disability')
        disabilities = cleaned_data.get('disabilities')

        # Validate password confirmation
        """ if password != confirm_password:
            raise ValidationError("Passwords do not match.") """

        # Validation logic for disability association
        if disability_status == 'N' and disabilities:
            raise ValidationError("A learner without a disability cannot have associated disabilities.")

        if disability_status == 'Y' and not disabilities:
            raise ValidationError("A learner marked as having a disability must have at least one associated disability.")

        return cleaned_data

    def save(self, commit=True):
        # Save Learner model first
        learner = super().save(commit=False)

        # Create the User object, setting name as username and birth_certificate_no as password
        
        user = User.objects.create_user(
            username=learner.name,  # Use name as the username
            password=learner.birth_certificate_no,  # Set password to birth_certificate_no
        )
        learner.user = user

        if commit:
            learner.save()
        
        return learner



"""     def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        disability_status = cleaned_data.get('disability')
        disabilities = cleaned_data.get('disabilities')

        # Validation logic for password
        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        # Validation logic for disability association
        if disability_status == 'N' and disabilities:
            raise ValidationError("A learner without a disability cannot have associated disabilities.")

        if disability_status == 'Y' and not disabilities:
            raise ValidationError("A learner marked as having a disability must have at least one associated disability.")

        return cleaned_data """

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
    #registration_no = forms.CharField(label='Registration No', max_length=20, required=False),
    birth_certificate_no = forms.CharField(label='ID no', max_length=50, required=False),

