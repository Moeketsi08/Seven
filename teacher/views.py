from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from . import forms
from .models import District, Upazilla, Union, PersonalInfo
from .forms import TimesheetForm  # Import the TimesheetForm
from .models import Timesheet
from django.utils import timezone




# Create your views here.

def load_upazilla(request):
    district_id = request.GET.get('district')
    upazilla = Upazilla.objects.filter(district_id=district_id).order_by('name')

    upazilla_id = request.GET.get('upazilla')
    union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
    context = {
        'upazilla': upazilla,
        'union': union
    }
    return render(request, 'others/upazilla_dropdown_list_options.html', context)


def teacher_registration(request):
    form = forms.PersonalInfoForm()
    address_forms = forms.AddressInfoForm()
    education_form = forms.EducationInfoForm()
    training_form = forms.TrainingInfoForm()
    job_form = forms.JobInfoForm()
    experience_form = forms.ExperienceInfoForm()
    if request.method == 'POST':
        form = forms.PersonalInfoForm(request.POST, request.FILES)
        address_form = forms.AddressInfoForm(request.POST)
        education_form = forms.EducationInfoForm(request.POST)
        training_form = forms.TrainingInfoForm(request.POST)
        job_form = forms.JobInfoForm(request.POST)
        experience_form = forms.ExperienceInfoForm(request.POST)
        if form.is_valid() and address_form.is_valid() and education_form.is_valid() and training_form.is_valid() and job_form.is_valid() and experience_form.is_valid():
            address_info = address_form.save()
            education_info = education_form.save()
            training_info = training_form.save()
            job_info = job_form.save()
            experience_info = experience_form.save()
            personal_info = form.save(commit=False)
            personal_info.address = address_info
            personal_info.education = education_info
            personal_info.training = training_info
            personal_info.job = job_info
            personal_info.experience = experience_info
            personal_info.save()
            return redirect('teacher-list')

    context = {
        'form': form,
        'address_forms': address_forms,
        'education_form': education_form,
        'training_form': training_form,
        'job_form': job_form,
        'experience_form': experience_form
    }
    return render(request, 'teacher/teacher-registration.html', context)


def teacher_list(request):
    teacher = PersonalInfo.objects.filter(is_delete=False)
    context = {'teacher': teacher}
    return render(request, 'teacher/teacher-list.html', context)


def teacher_profile(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    context = {
        'teacher': teacher
    }
    return render(request, 'teacher/teacher-profile.html', context)


def teacher_delete(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    teacher.is_delete = True
    teacher.save()
    return redirect('teacher-list')


def teacher_edit(request, teacher_id):
    teacher = PersonalInfo.objects.get(id=teacher_id)
    form = forms.PersonalInfoForm(instance=teacher)
    address_forms = forms.AddressInfoForm(instance=teacher.address)
    education_form = forms.EducationInfoForm(instance=teacher.education)
    training_form = forms.TrainingInfoForm(instance=teacher.training)
    job_form = forms.JobInfoForm(instance=teacher.job)
    experience_form = forms.ExperienceInfoForm(instance=teacher.experience)
    if request.method == 'POST':
        form = forms.PersonalInfoForm(request.POST, request.FILES, instance=teacher)
        address_form = forms.AddressInfoForm(request.POST, instance=teacher.address)
        education_form = forms.EducationInfoForm(request.POST, instance=teacher.education)
        training_form = forms.TrainingInfoForm(request.POST, instance=teacher.training)
        job_form = forms.JobInfoForm(request.POST, instance=teacher.job)
        experience_form = forms.ExperienceInfoForm(request.POST, instance=teacher.experience)
        if form.is_valid() and address_form.is_valid() and education_form.is_valid() and training_form.is_valid() and job_form.is_valid() and experience_form.is_valid():
            address_info = address_form.save()
            education_info = education_form.save()
            training_info = training_form.save()
            job_info = job_form.save()
            experience_info = experience_form.save()
            personal_info = form.save(commit=False)
            personal_info.address = address_info
            personal_info.education = education_info
            personal_info.training = training_info
            personal_info.job = job_info
            personal_info.experience = experience_info
            personal_info.save()
            return redirect('teacher-list')

    context = {
        'form': form,
        'address_form': address_forms,
        'education_form': education_form,
        'training_form': training_form,
        'job_form': job_form,
        'experience_form': experience_form
    }
    return render(request, 'teacher/teacher-edit.html', context)


class TeacherLoginView(FormView):
    template_name = 'teacher/teacher_login.html'  # Update the path
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return '/teacher/dashboard/'  # Redirect to the teacher's dashboard


def teacher_dashboard(request):
    # Logic for the teacher's dashboard
    return render(request, 'teacher/teacher-dashboard.html')

def teacher_dashboard(request):
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            # Calculate total hours
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            total_hours = (end_time - start_time).seconds / 3600  # Convert seconds to hours

            # Create and save the new Timesheet record
            Timesheet.objects.create(
                user=request.user,
                date=form.cleaned_data['date'],
                start_time=start_time,
                end_time=end_time,
                total_hours=total_hours,
            )
            return redirect('teacher_dashboard')  # Redirect to the same page to avoid resubmission

    else:
        form = TimesheetForm()

    # Fetch existing timesheets for the logged-in user
    timesheets = Timesheet.objects.filter(user=request.user).order_by('-date')

    context = {
        'timesheet_form': form,
        'timesheets': timesheets
    }

    return render(request, 'teacher/teacher-dashboard.html', context)
