from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .models import Teacher, Timesheet
from academic.models import Session, ClassInfo
from student.models import Student, AcademicInfo
from attendance.models import StudentAttendance
from django.utils import timezone
from .forms import AttendanceTimesheetForm, StudentAttendanceFormSet, TimesheetForm
from student.forms import StudentSearchForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import AttendanceTimesheetForm, StudentAttendanceFormSet
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.urls import reverse

from datetime import datetime

""" def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher-dashboard')
        else:
            return render(request, 'teacher/teacher_login.html', {'error': 'Invalid username or password'})
            return render(request, 'teacher/teacher_login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'teacher/teacher_login.html') """

# @login_required
# def teacher_dashboard(request):
#     # Logic for the teacher's dashboard
#     return render(request, 'teacher/teacher-dashboard.html')

@login_required
def teacher_dashboard(request):
    # Try to retrieve the Teacher instance related to the user
    teacher = get_object_or_404(Teacher, user=request.user)
    request.teacher = teacher

    if request.method == 'POST':
        timesheet_form = TimesheetForm(request.POST) if request.POST.get('form_type') == 'timesheet_form' else TimesheetForm()
        attendance_form = AttendanceTimesheetForm(request.POST) if request.POST.get('form_type') == 'attendance_form' else AttendanceTimesheetForm()
        if request.POST.get('form_type') == 'timesheet_form':
            if timesheet_form.is_valid():
                # Calculate total hours
                start_time = timesheet_form.cleaned_data['start_time']
                end_time = timesheet_form.cleaned_data['end_time']
                today = datetime.today().date()
                start_datetime = datetime.combine(today, start_time)
                end_datetime = datetime.combine(today, end_time)
                total_hours = (end_datetime - start_datetime).seconds / 3600   # Convert seconds to hours
                classInfo = ClassInfo.objects.create(subject=timesheet_form.cleaned_data['subjects'], grade=timesheet_form.cleaned_data['grades'])
                session = Session.objects.create(start_time=start_time, end_time=end_time, class_info=classInfo)

                # Create and save the new Timesheet record
                Timesheet.objects.create(
                    teacher=teacher,
                    session=session,
                    date=timesheet_form.cleaned_data['date'],
                    atp_hours=total_hours,  # Assuming atp_hours corresponds to total_hours
                    attendance_marked=False  # Set this as per your logic
                )
                messages.success(request, 'Timesheet saved successfully.')
                return redirect('teacher_dashboard')  # Redirect to avoid resubmission
        if request.POST.get('form_type') == 'attendance_form':
            if attendance_form.is_valid():
                attendance_form.save()
                messages.success(request, 'Attendance saved successfully.')
                return redirect('teacher_dashboard')  # Redirect to avoid resubmission
    else:
        timesheet_form = TimesheetForm()
        attendance_form = AttendanceTimesheetForm()
    # Fetch existing timesheets for the logged-in user
    timesheets = Timesheet.objects.filter(teacher=teacher).order_by('-date')
    attendances = StudentAttendance.objects.filter(class_name__session__class_info__teacher=teacher)
    students = Student.objects.filter(class_registration__session__class_info__teacher=teacher)
    
    # Extract sessions from timesheets
    sessions = {timesheet.session for timesheet in timesheets}

    return render(request, 'teacher/teacher-dashboard.html', {
        'timesheet_form': timesheet_form,
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

def student_list(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    students = teacher.students.all()
    context = {'students': students}
    return render(request, 'teacher/student-list.html', context)

def student_search(request):
    forms = StudentSearchForm()
    cls_name = request.GET.get('class_info', None)
    reg_no = request.GET.get('registration_no', None)
    if cls_name:
        student = AcademicInfo.objects.filter(class_info=cls_name)
        if reg_no:
            student = student.filter(registration_no=reg_no)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'teacher/student-search.html', context)
    else:
        student = AcademicInfo.objects.filter(registration_no=reg_no)
        context = {
            'forms': forms,
            'student': student
        }
        return render(request, 'teacher/student-search.html', context)

# def create_class(request):
#     form = ClassRegistrationForm()
#     districts = District.objects.all()  # Add this line to get the districts
#     if request.method == 'POST':
#         form = ClassRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('class-list')
#     context = {
#         'form': form,
#         'districts': districts  # Pass the districts to the template
#     }
#     return render(request, 'teacher/create-class.html', context)
class TeacherLoginView(SuccessMessageMixin,FormView):
    template_name = 'teacher/teacher_login.html'  # Update the path
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
        return redirect('/teacher/teacher_login')
    def get_success_url(self):
        return reverse('teacher_dashboard')  # Redirect to the teacher's dashboard
