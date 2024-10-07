from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import Teacher, Timesheet
from academic.models import Session, Student
from attendance.models import StudentAttendance
from django.utils import timezone
from .forms import AttendanceTimesheetForm, StudentAttendanceFormSet, TimesheetForm, TeacherForm

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher-dashboard')
        else:
            return render(request, 'teacher/teacher_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'teacher/teacher_login.html')

@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    timesheets = Timesheet.objects.filter(teacher=teacher)
    attendances = StudentAttendance.objects.filter(class_name__session__class_info__teacher=teacher)
    students = Student.objects.filter(class_registration__session__class_info__teacher=teacher)
    
    # Extract sessions from timesheets
    sessions = {timesheet.session for timesheet in timesheets}

    return render(request, 'teacher/teacher-dashboard.html', {
        'timesheets': timesheets,
        'attendances': attendances,
        'students': students,
        'sessions': sessions,
    })

@login_required
def submit_attendance_and_timesheet(request, session_id):
    teacher = request.user.teacher
    session = get_object_or_404(Session, id=session_id, class_info__in=teacher.subjects_taught.all())
    students = Student.objects.filter(class_registration__session=session)

    if request.method == 'POST':
        timesheet_form = AttendanceTimesheetForm(request.POST)
        attendance_formset = StudentAttendanceFormSet(request.POST)
        
        if timesheet_form.is_valid() and attendance_formset.is_valid():
            timesheet = timesheet_form.save(commit=False)
            timesheet.teacher = teacher
            timesheet.session = session
            timesheet.save()

            for form in attendance_formset:
                student_id = form.cleaned_data['student_id']
                status = form.cleaned_data['status']
                StudentAttendance.objects.create(
                    student_id=student_id,
                    class_name=session.class_info,
                    date=timesheet.date,
                    status=status
                )

            return redirect('teacher_dashboard')
    else:
        timesheet_form = AttendanceTimesheetForm(initial={'date': timezone.now().date()})
        attendance_formset = StudentAttendanceFormSet(initial=[
            {'student_id': student.id, 'student_name': f"{student.first_name} {student.last_name}"}
            for student in students
        ])

    return render(request, 'teacher/submit_attendance_and_timesheet.html', {
        'timesheet_form': timesheet_form,
        'attendance_formset': attendance_formset,
        'session': session
    })

@login_required
def teacher_profile(request):
    teacher = request.user.teacher
    context = {
        'teacher': teacher
    }
    return render(request, 'teacher/teacher-profile.html', context)
