from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django.db import transaction


from teacher.models import Teacher, Timesheet, Classroom
from academic.models import Session, Grade, Subject, Registration
from learner.models import Learner
from attendance.models import LearnerAttendance
from teacher.forms import LearnerAttendanceForm, TimesheetForm
from learner.forms import LearnerSearchForm


from datetime import datetime


class TeacherLoginView(SuccessMessageMixin,FormView):
    template_name = 'teacher/teacher-login.html'  # Update the path
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Welcome  Teacher')
        #print("Form data:", self.request.POST)  # Debug line
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials. Please try again.')
        # Re-render the form with the error messages
        return redirect('teacher-login')
    def get_success_url(self):
        return reverse('teacher-dashboard')  # Redirect to the teacher's dashboard

def teacher_dashboard(request):
    # Get the Teacher instance related to the user
    teacher = get_object_or_404(Teacher, user=request.user)
    request.teacher = teacher
    if request.method == 'POST':
        timesheet_form = TimesheetForm(request.POST) if request.POST.get('form_type') == 'timesheet_form' else TimesheetForm()
        if request.POST.get('form_type') == 'timesheet_form':
            if timesheet_form.is_valid():
                # Calculate total hours
                start_time = datetime.strptime(timesheet_form.cleaned_data['start_time'], '%H:%M').time() 
                end_time = datetime.strptime(timesheet_form.cleaned_data['end_time'], '%H:%M').time()
                today = datetime.today().date()
                start_datetime = datetime.combine(today, start_time)
                end_datetime = datetime.combine(today, end_time)
                total_hours = (end_datetime - start_datetime).seconds / 3600   # Convert seconds to hours
                subject_instance, subject_created = Subject.objects.get_or_create(subject=timesheet_form.cleaned_data['subjects'])
                grade_instance, grade_created = Grade.objects.get_or_create(grade=timesheet_form.cleaned_data['grades'])

                session = Session.objects.create(start_time=start_time, end_time=end_time, subject=subject_instance, grade=grade_instance)

                Timesheet.objects.create(
                    teacher=teacher,
                    session=session,
                    date=timesheet_form.cleaned_data['date'],
                    atp_hours=total_hours,  # Assuming atp_hours corresponds to total_hours
                    attendance_marked=False  # Set this as per your logic
                )
                messages.success(request, 'Timesheet saved successfully.')
                return redirect('teacher-dashboard')  # Redirect to avoid resubmission
    else:
        timesheet_form = TimesheetForm()
    # Fetch existing timesheets for the logged-in user
    timesheets = Timesheet.objects.filter(teacher=teacher).order_by('-date')

    return render(request, 'teacher/teacher-dashboard.html', {
        'timesheet_form': timesheet_form,
        'timesheets': timesheets,
    })

@login_required
def teacher_profile(request):
    teacher = request.user.teacher
    context = {
        'teacher': teacher
    }
    return render(request, 'teacher/teacher-profile.html', context)

@login_required
def learner_list(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    search_query = request.GET.get('search', '')
    
    # Prefetch learners related to classrooms and their registration data
    classrooms = Classroom.objects.prefetch_related('learners').filter(teacher=teacher)

    if search_query:
        # Filter by registration number through the related Registration model
        classrooms = classrooms.filter(learners__registration__registration_number__icontains=search_query)

    paginator = Paginator(classrooms, 10)  # Show 10 classrooms per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all registrations
    registrations = Registration.objects.select_related('learner').filter(center=teacher.centers.first())
    print(registrations)

    context = {
        'classrooms': page_obj,  # Paginated classrooms
        'page_obj': page_obj,    # For pagination control
        'registrations': registrations,  # List of all registrations
    }
    
    return render(request, 'teacher/learner-list.html', context)

@login_required
def learner_search(request):
    forms = LearnerSearchForm()
    learner = None
    reg_no = request.GET.get('registration_no', None)
    
    if reg_no:  # Check if a registration number was provided
        learner = Registration.objects.filter(registration_number=reg_no).first()  # Get the first matching learner
    
    context = {
        'forms': forms,
        'learner': learner
    }
    return render(request, 'teacher/learner-search.html', context)

@login_required
def learner_attendance(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classroom = Classroom.objects.filter(teacher=teacher).first()  # Assuming one classroom per teacher for now
    learners = classroom.learners.all()
    # Create an empty dictionary to hold forms for each learner
    learner_forms = {}

    if request.method == 'POST':
        # Process form submission for each learner
        for learner in learners:
            learner_form = LearnerAttendanceForm(request.POST, prefix=str(learner.id))

            if learner_form.is_valid():
                attendance = learner_form.save(commit=False)
                attendance.teacher = teacher
                attendance.classroom = classroom
                attendance.learner = learner
                attendance.save()
            else:
                learner_forms[learner] = learner_form  # Re-populate the form with errors if not valid

        messages.success(request, 'Attendance saved successfully.')
        return redirect('teacher-dashboard')
    else:
        # Initialize empty forms for GET requests
        for learner in learners:
            learner_forms[learner] = LearnerAttendanceForm(prefix=str(learner.id))

    return render(request, 'teacher/learner-attendance.html', {
        'learner_forms': learner_forms,
    })

    
@login_required
def learner_report(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    request.teacher = teacher

    # Fetch all attendance records for the teacher's learners
    attendance = LearnerAttendance.objects.filter(teacher=teacher).order_by('-date')

    # Set up pagination
    paginator = Paginator(attendance, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    attendance_page = paginator.get_page(page_number)

    return render(request, 'teacher/learner-report.html', {
        'attendance': attendance_page,
    })