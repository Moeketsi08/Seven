<<<<<<< Updated upstream
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from . import forms
from .models import Teacher, TeacherCenterAssignment, TeacherQualification, TeacherPerformance, Timesheet
from academic.models import Center, ClassInfo, Session, ClassRegistration, Student
from administration.models import Designation
from attendance.models import StudentAttendance
from django.utils import timezone
>>>>>>> Stashed changes

# Remove the import for District, Upazilla, Union as they're not relevant for Kutlwanong

# Create your views here.

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            return render(request, 'teacher/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'teacher/login.html')

def teacher_registration(request):
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            return redirect('teacher-list')
    else:
        form = forms.TeacherForm()
    
    context = {
        'form': form,
    }
    return render(request, 'teacher/teacher-registration.html', context)

def teacher_list(request):
    teachers = Teacher.objects.filter(is_active=True)
    context = {'teachers': teachers}
    return render(request, 'teacher/teacher-list.html', context)


def teacher_profile(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    context = {
        'teacher': teacher
    }
    return render(request, 'teacher/teacher-profile.html', context)


def teacher_delete(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.is_active = False
    teacher.save()
    return redirect('teacher-list')


def teacher_edit(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher-list')
<<<<<<< Updated upstream

=======
    else:
        form = forms.TeacherForm(instance=teacher)
    
>>>>>>> Stashed changes
    context = {
        'form': form,
    }
    return render(request, 'teacher/teacher-edit.html', context)

<<<<<<< Updated upstream

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
=======
@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    timesheets = Timesheet.objects.filter(teacher=teacher)
    attendances = StudentAttendance.objects.filter(class_name__session__class_info__teacher=teacher)
    students = Student.objects.filter(class_registration__session__class_info__teacher=teacher)
    
    # Extract sessions from timesheets
    sessions = {timesheet.session for timesheet in timesheets}


    # Debug information
    print(f"Timesheets: {timesheets}")
    print(f"Attendances: {attendances}")
    print(f"Students: {students}")
    print(f"Sessions: {sessions}")
    
    return render(request, 'teacher/dashboard.html', {
        'timesheets': timesheets,
        'attendances': attendances,
        'students': students,
        'sessions': sessions,
    })

@login_required
def submit_attendance_and_timesheet(request, session_id):
    teacher = request.user.teacher
    session = get_object_or_404(Session, id=session_id, class_info__in=teacher.subjects_taught.all())
    if request.method == 'POST':
        form = forms.AttendanceTimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.teacher = teacher
            if not timesheet.session:
                timesheet.session = session
            if not timesheet.date:
                timesheet.date = timezone.now().date()
            timesheet.save()
            return redirect('teacher_dashboard')
    else:
        form = forms.AttendanceTimesheetForm(initial={'session': session, 'date': timezone.now().date()})
    return render(request, 'teacher/submit_attendance_and_timesheet.html', {'form': form, 'session': session})
>>>>>>> Stashed changes
