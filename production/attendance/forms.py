from django import forms
from academic.models import ClassRegistration

class SearchEnrolledLearnerForm(forms.Form):
    reg_class = forms.ModelChoiceField(queryset=ClassRegistration.objects.all())