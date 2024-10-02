from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from . import forms
from .models import Teacher, TeacherCenterAssignment, TeacherQualification, TeacherPerformance, Timesheet
from academic.models import Center, ClassInfo, Session, ClassRegistration, Student
from administration.models import Designation
from attendance.models import StudentAttendance
from django.utils import timezone

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
    else:
        form = forms.TeacherForm(instance=teacher)
    
    context = {
        'form': form,
    }
    return render(request, 'teacher/teacher-edit.html', context)

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
