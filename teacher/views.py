from collections import defaultdict
from itertools import groupby
from operator import attrgetter
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


from teacher.models import ATPSchedule, Teacher, Timesheet, Classroom
from academic.models import Session, Grade, Subject, Registration
from learner.models import Learner
from attendance.models import LearnerAttendance
from teacher.forms import LearnerAttendanceForm, TimesheetForm
from learner.forms import LearnerSearchForm


from datetime import date, datetime, timedelta


class TeacherLoginView(SuccessMessageMixin,FormView):
    template_name = 'teacher/teacher-login.html'  # Update the path
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()

        
        # Check if the user is valid
        if not user:
           messages.error(self.request, "Invalid user. Please try again.")
           return self.form_invalid(form)  # Redirect back to the form with an error

        # Check if the user is a teacher
        if not hasattr(user, 'teacher'):
            messages.error(self.request, "You are not registered as a teacher.")
            return self.form_invalid(form)  # Redirect back to the form with an error


        teacher = user.teacher
        login(self.request, user)
        
        # Fetch the teacher's first and last name
        first_name = teacher.name
        last_name = teacher.surname
        
        # Display a welcome message with the teacher's full name
        messages.success(self.request, f'Welcome, Teacher {first_name} {last_name}')
        
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
        # Initialize the form
        timesheet_form = TimesheetForm(request.POST) if request.POST.get('form_type') == 'timesheet_form' else TimesheetForm()

        if request.POST.get('form_type') == 'timesheet_form':
            if timesheet_form.is_valid():
                # Get the session date from the form
                session_date = timesheet_form.cleaned_data['date']
                today = datetime.today().date()
                # Check if the session date is more than 7 days ago
                if session_date < today - timedelta(days=6):
                    # If the date is more than 7 days old, show an error and stop form submission
                    messages.error(request, 'You cannot fill in a timesheet for a session that occurred more than 7 days ago.')
                else:
                    # Proceed with saving the timesheet only if the date is valid
                    start_time = datetime.strptime(timesheet_form.cleaned_data['start_time'], '%H:%M').time()
                    end_time = datetime.strptime(timesheet_form.cleaned_data['end_time'], '%H:%M').time()
                    start_datetime = datetime.combine(session_date, start_time)
                    end_datetime = datetime.combine(session_date, end_time)
                    total_hours = (end_datetime - start_datetime).seconds / 3600  # Convert seconds to hours

                    # Create or get instances of Subject and Grade
                    subject_instance, _ = Subject.objects.get_or_create(subject=timesheet_form.cleaned_data['subjects'])
                    grade_instance, _ = Grade.objects.get_or_create(grade=timesheet_form.cleaned_data['grades'])

                    # Create a session and timesheet
                    session = Session.objects.create(
                        start_time=start_time,
                        end_time=end_time,
                        subject=subject_instance,
                        grade=grade_instance
                    )
                    Timesheet.objects.create(
                        teacher=teacher,
                        session=session,
                        date=session_date,
                        atp_hours=total_hours,
                        attendance_marked=False,  # Set this as per your logic
                        approved=False  # Default to False
                    )
                    messages.success(request, 'Timesheet saved successfully.')
                    return redirect('teacher-dashboard')  # Redirect to avoid resubmission
    else:
        timesheet_form = TimesheetForm()

    # Fetch existing timesheets for the logged-in user
    timesheets = Timesheet.objects.filter(teacher=teacher).order_by('-date')

    # Calculate total hours across all timesheets
    total_hours = sum(t.atp_hours for t in timesheets)

    # Group timesheets by date and calculate total hours for each date
    total_hours_by_date = {
        date: sum(t.atp_hours for t in timesheets if t.date == date)
        for date in set(t.date for t in timesheets)
    }

    # Get the total number of classrooms taught by the teacher
    total_classes = Classroom.objects.filter(teacher=teacher).count()
    
    # Get distinct grade and subject combinations for the teacher's classrooms
    classrooms = Classroom.objects.filter(teacher=teacher)
    grade_subject_combinations = classrooms.values('grade__grade', 'subject__subject').distinct()

     # Get the total number of learners in each classroom
    classroom_learners = {}
    for classroom in classrooms:
        learner_count = classroom.learners.count()
        classroom_learners[f"{classroom.grade.grade} - {classroom.subject.subject}"] = learner_count


    overall_percentage = 0
    # Get the total number of learners in each classroom and their attendance percentage by date
    classroom_attendance = {}
    for classroom in classrooms:
        # Get the total number of learners in the classroom
        total_learners = classroom.learners.count()

        # Get distinct dates for classes taught in this classroom
        class_dates = LearnerAttendance.objects.filter(classroom=classroom).values('date').distinct()

        # Prepare a dictionary to store attendance for each date
        date_attendance = {}

        for class_date in class_dates:
            date = class_date['date']

            # Get the number of present learners for each class on this date
            present_count = LearnerAttendance.objects.filter(
                classroom=classroom,
                status='P',
                date=date
            ).count()

            # Calculate the attendance percentage for this class on this date
            attendance_percentage = (present_count / total_learners) * 100 if total_learners > 0 else 0
            date_attendance[date] = round(attendance_percentage, 2)  # Round to 2 decimal places for clarity

        # Add total attendance percentage for the classroom
        total_classes = len(class_dates)
        total_attendance = sum(date_attendance.values())
        overall_percentage = (total_attendance / total_classes) if total_classes > 0 else 0

        # Store the attendance per class (date) and overall percentage
        classroom_attendance[f"{classroom.grade.grade} - {classroom.subject.subject}"] = {
            'date_attendance': date_attendance,
            'overall_percentage': round(overall_percentage, 2),  # Round to 2 decimal places
        }
    if classrooms.exists():
        classroom = classrooms.first()  # Assign the first classroom before using it
        totalL = classroom.learners.count()
        
    else:
        classroom = None  # Prevent unbound variable error
        totalL = 0  # Default value

    ttotal_classes = 0
    ttotal_classes = classrooms.count()  

    return render(request, 'teacher/teacher-dashboard.html', {
        'timesheet_form': timesheet_form,
        'timesheets': timesheets,
        'total_hours_by_date': total_hours_by_date,  # Dictionary of date: total_hours
        'total_hours': total_hours,
        'total_classes': total_classes,  # Total number of classes taught by the teacher
        'grade_subject_combinations': grade_subject_combinations,  # Pass distinct grade-subject combinations
        'classroom_learners': classroom_learners,  # Pass the classroom learners count
        'classroom_attendance': classroom_attendance,  # Pass the attendance percentage for each classroom
        'totalL': totalL,
        'overall_percentage': overall_percentage,
        'ttotal_classes ': ttotal_classes 
    })

def calendar_view(request):
    upcoming_events = ATPSchedule.objects.filter(date__gte=date.today()).order_by('date')[:5]  # Fetch next 5 events
    return render(request, "teacher-dashboard.html", {"upcoming_events": upcoming_events})

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
    
    if not classroom:
        messages.error(request, "No classroom found for this teacher.")
        return redirect('teacher-dashboard')  # Redirect to a safer page
        
    learners = classroom.learners.all()

    # Get today's date
    today = timezone.now().date()

    # Check if attendance has already been recorded today
    existing_attendance = LearnerAttendance.objects.filter(teacher=teacher, classroom=classroom, date=today)

    # Create an empty dictionary to hold forms for each learner
    learner_forms = {}

    if request.method == 'POST':
        if existing_attendance.exists():
            messages.error(request, 'Attendance has already been marked for today.')
            return redirect('teacher-dashboard')

        # Process form submission for each learner
        for learner in learners:
            learner_form = LearnerAttendanceForm(request.POST, prefix=str(learner.id), learner=learner, classroom=classroom)

            if learner_form.is_valid():
                attendance = learner_form.save(commit=False)
                attendance.teacher = teacher
                attendance.classroom = classroom
                attendance.learner = learner
                attendance.date = today  # Set the current date for the attendance record
                attendance.save()
            else:
                learner_forms[learner] = learner_form  # Re-populate the form with errors if not valid

        messages.success(request, 'Attendance saved successfully.')
        return redirect('teacher-dashboard')
    else:
        # Initialize empty forms for GET requests
        for learner in learners:
            learner_forms[learner] = LearnerAttendanceForm(prefix=str(learner.id), learner=learner, classroom=classroom)

    return render(request, 'teacher/learner-attendance.html', {
        'learner_forms': learner_forms,
        'classroom': classroom,
    })

@login_required
def teacher_timesheets(request):
    # Get timesheets for a specific teacher
    teacher = get_object_or_404(Teacher, user=request.user)
    timesheets = Timesheet.objects.filter(teacher=teacher)\
                                   .select_related('session__grade', 'session__subject')\
                                   .order_by('-date')
    
    # Group timesheets by date
    grouped_timesheets = defaultdict(list)
    for timesheet in timesheets:
        grouped_timesheets[timesheet.date].append(timesheet)

    # Calculate total hours for each date
    grouped_data = {}
    for date, date_timesheets in grouped_timesheets.items():
        total_hours = sum(t.atp_hours for t in date_timesheets)
        grouped_data[date] = {
            'timesheets': date_timesheets,
            'total_hours': total_hours,
        }

    return render(request, 'teacher/teachers-timesheet.html', {
        'grouped_timesheets': grouped_data,
    })
    
@login_required
def learner_report(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    request.teacher = teacher

    # Fetch all attendance records for the teacher's learners
    attendance = LearnerAttendance.objects.filter(teacher=teacher).order_by('-date')

    # Group attendance records by date
    attendance_by_date = {}
    for att in attendance:
        date = att.date
        if date not in attendance_by_date:
            attendance_by_date[date] = []
        attendance_by_date[date].append(att)

    # Pagination setup
    # Flatten the grouped attendance into a list for pagination
    all_attendance = [att for date_attendance in attendance_by_date.values() for att in date_attendance]
    paginator = Paginator(all_attendance, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    attendance_page = paginator.get_page(page_number)

    # Group the attendance again for displaying on the template
    grouped_by_page = {}
    for att in attendance_page.object_list:
        if att.date not in grouped_by_page:
            grouped_by_page[att.date] = []
        grouped_by_page[att.date].append(att)

    return render(request, 'teacher/learner-report.html', {
        'attendance_by_date': grouped_by_page,  # Grouped by date for display
        'attendance': attendance_page,  # For pagination
    })