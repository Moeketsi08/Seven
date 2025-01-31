from collections import defaultdict
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from attendance.models import LearnerAttendance
from center_manager.models import Center, CenterManager
from center_manager.forms import CenterManagerLoginForm, AllocateTeacherForm, ClassroomFormSet, LearnerRegistrationForm
from learner.forms import LearnerForm, LearnerSearchForm
from teacher.forms import LearnerAttendanceForm, TimesheetForm
from teacher.models import Teacher, Classroom, Timesheet, TeacherCenterAssignment
from academic.models import Nationality, Registration
from learner.models import Learner
from django.db.models.functions import TruncDate  # Import TruncDate
from django.db.models import Count
from django.shortcuts import redirect

def is_admin(user):
    return user.is_staff or user.is_superuser or user.groups.filter(name='Center Manager').exists()


def root_redirect_view(request):
    return redirect('/login')

@login_required
@user_passes_test(is_admin)
def center_dashboard(request):
    center = get_object_or_404(Center, center_manager=request.user.center_managers)
    teachers = Teacher.objects.filter(centers=center).count()



    
    # Get distinct grade and subject combinations for the teacher's classrooms
    classrooms = Classroom.objects.filter(teacher=teachers)
    grade_subject_combinations = classrooms.values('grade__grade', 'subject__subject').distinct()

        # Get the total number of classrooms taught by the teacher
    total_classes = Classroom.objects.filter(teacher=teachers).count()

     # Get the total number of learners in each classroom
    classroom_learners = {}
    for classroom in classrooms:
        learner_count = classroom.learners.count()
        classroom_learners[f"{classroom.grade.grade} - {classroom.subject.subject}"] = learner_count


    
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


    return render(request, 'center_manager/center-dashboard.html', {
        'teachers':teachers,
        'total_classes': total_classes,  # Total number of classes taught by the teacher
        })

def admin_login(request):
    forms = CenterManagerLoginForm()
    if request.method == 'POST':
        forms = CenterManagerLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user.is_superuser:
                admin = user.is_superuser
                login(request, user)

                # Fetch the admin's name 
                first_name = user.username

                # Display a welcome message with the admin's full name
                messages.success(request, f'Welcome, Administrator {first_name}')

                return redirect('home')
    context = {'forms': forms}
    return render(request, 'center_manager/login.html', context)

def admin_logout(request):
    logout(request)
    return redirect('login')

class CenterLoginView(SuccessMessageMixin, FormView):
    template_name = 'center_manager/center-login.html'
    form_class = AuthenticationForm
    
    def form_valid(self, form): 
        user = form.get_user()

        
        # Check if the user is valid
        if not user:
           messages.error(self.request, "Invalid user. Please try again.")
           return self.form_invalid(form)  # Redirect back to the form with an error

        # Check if the user is a center manager
        if not hasattr(user, 'center_managers'):
            messages.error(self.request, "You are not registered as a Center Manager.")
            return self.form_invalid(form)  # Redirect back to the form with an error


        center_managers = user.center_managers
        login(self.request, user)

        #Fetch center-managers center
        center = center_managers.center

        #Fetch teachers at the center
        teachers = TeacherCenterAssignment.objects.filter(center=center).values('teacher')

        # Fetch all centers and their teacher counts
        all_centers = Center.objects.annotate(
            teacher_count=Count('teachercenterassignment')
        ).values('id', 'name', 'teacher_count')

        # Fetch existing timesheets for all teachers at a Center
        teacher_ids = teachers.values_list('teacher', flat=True)
        timesheets = Timesheet.objects.filter(teacher__id__in=teacher_ids).order_by('-date')


        # Group timesheets by main heading per center then sub-heading per teacher and calculate total hours for each date
        total_hours_by_teacher = {
            teacher: {
                date: sum(t.atp_hours for t in timesheets if t.teacher == teacher and t.date == date)
                for date in set(t.date for t in timesheets if t.teacher == teacher)
            }
            for teacher in set(t.teacher for t in timesheets)
        }

        # Calculate total hours across all timesheets at the center
        total_hours = sum(t.atp_hours for t in timesheets)

        # Get the total number of classrooms taught by teachers at the center
        total_classes = Classroom.objects.filter(center=center).count()

        # Get distinct grade and subject combinations for the classrooms at the center
        classrooms = Classroom.objects.filter(center=center)
        grade_subject_combinations = classrooms.values('grade__grade', 'subject__subject').distinct()

        # Get the total number of learners in each classroom at the center
        classroom_learners = {}
        for classroom in classrooms:
            learner_count = classroom.learners.count()
            classroom_learners[f"{classroom.grade.grade} - {classroom.subject.subject}"] = learner_count

        # Get the total number of learners in each classroom and their attendance percentage by date at the center
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

        # Fetch the center manager's first and last name
        name = center_managers.name
        surname = center_managers.surname

        messages.success(self.request, f'Welcome, Center Manager {name} {surname}')

        return render( self.request,'center_manager/center-dashboard.html', {
            'timesheets': timesheets,
            'total_hours_by_teacher': total_hours_by_teacher,  # Dictionary of teacher: {date: total_hours}
            'total_hours': total_hours,
            # 'total_classes_count': total_classes.count(),  # Use .count() for the total
            'total_classes': total_classes,  # Total number of classes taught at the center
            'grade_subject_combinations': grade_subject_combinations,  # Pass distinct grade-subject combinations
            'classroom_learners': classroom_learners,  # Pass the classroom learners count
            'classroom_attendance': classroom_attendance,  # Pass the attendance percentage for each classroom
            'total_teachers': teachers.count(),  # Total teachers at the logged-in manager's center
            'centers': all_centers,  # List of all centers with teacher counts

        })

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse('center-dashboard')


def center_logout(request):
    logout(request)
    return redirect('login')

from django.contrib import messages

@login_required
@user_passes_test(is_admin)
def allocate_teacher(request):
    # Get the center manager's center from the logged-in user
    try:
        center = Center.objects.get(center_manager=request.user.center_managers)
        print(f"Center: {center.name}")  # Log the center name
    except Center.DoesNotExist:
        messages.error(request, "No center associated with this manager.")
        return redirect('dashboard')  # Redirect to a suitable page

    if request.method == 'POST':
        teacher_allocation_form = AllocateTeacherForm(request.POST, center=center)
        if request.POST.get('form_type') == 'teacher_allocation_form':
            if teacher_allocation_form.is_valid():
                with transaction.atomic():
                    classroom = Classroom.objects.create(
                        grade=teacher_allocation_form.cleaned_data['grade'],
                        subject=teacher_allocation_form.cleaned_data['subject'],
                        teacher=teacher_allocation_form.cleaned_data['teacher'],
                        center=center
                    )
                    classroom.learners.set(teacher_allocation_form.cleaned_data['learner'])
                messages.success(request, "Teacher allocated successfully.")
                return redirect('allocate_teacher')
            else:
                messages.error(request, "Form is invalid. Please check the fields.")
    else:
        teacher_allocation_form = AllocateTeacherForm(center=center)

        # Debug the teacher and learner querysets
        print(f"Teachers available: {teacher_allocation_form.fields['teacher'].queryset}")
        print(f"Learners available: {teacher_allocation_form.fields['learner'].queryset}")

    return render(request, 'center_manager/allocate_teacher.html', {'teacher_allocation_form': teacher_allocation_form})

@login_required
@user_passes_test(is_admin)
def edit_teacher_allocation(request):
    center = get_object_or_404(Center, center_manager=request.user.center_managers)
    classrooms = Classroom.objects.filter(center=center)  # Get all classrooms associated with the center

    if request.method == 'POST':
        formset = ClassroomFormSet(request.POST, queryset=classrooms)
        if formset.is_valid():
            formset.save()  # Save all the updated classroom instances
            return redirect('classroom_list')  # Redirect to the classroom list or appropriate page
    else:
        formset = ClassroomFormSet(queryset=classrooms)  # Pre-fill the formset with current classroom data

    return render(request, 'center_manager/edit_teacher_allocation.html', {
        'formset': formset,
        'center': center,
    })


@login_required
@user_passes_test(is_admin)
def learner_list(request):
    search_query = request.GET.get('search', '')
    
    # Prefetch learners related to classrooms and their registration data
    classrooms = Classroom.objects.prefetch_related('learners').filter(center__center_manager=request.user.center_managers)

    if search_query:
        # Filter by registration number through the related Registration model
        classrooms = classrooms.filter(learners__registration__registration_number__icontains=search_query)

    paginator = Paginator(classrooms, 10)  # Show 10 classrooms per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all registrations
    registrations = Registration.objects.select_related('learner').all()

    context = {
        'classrooms': page_obj,  # Paginated classrooms
        'page_obj': page_obj,    # For pagination control
        'registrations': registrations,  # List of all registrations
    }
    
    return render(request, 'center_manager/learner-list.html', context)

@login_required
@user_passes_test(is_admin)
def learner_search(request):
    forms = LearnerSearchForm()
    learner = None
    #reg_no = request.GET.get('registration_no', None)
    id_no = request.GET.get('birth_certificate_no', None)
    
    if id_no:  # Check if a registration number was provided
        #learner = Registration.objects.filter(registration_number=reg_no).first()  # Get the first matching learner
        learner = Registration.objects.filter(id_number=id_no).first()  # Get the first matching learner
    context = {
        'forms': forms,
        'learner': learner
    }
    return render(request, 'center_manager/learner-search.html', context)


@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    center = Center.objects.get(center_manager=request.user.center_managers)

    query = request.GET.get('search', '')

    teachers = Teacher.objects.filter(
        Q(centers=center.id) & 
        (Q(name__icontains=query) | Q(email__icontains=query))
    )

    # Paginate the filtered teachers
    paginator = Paginator(teachers, 10)  # Show 10 teachers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'center_manager/teacher-list.html', {'page_obj': page_obj, 'query': query})

@login_required
@user_passes_test(is_admin)
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'center_manager/teacher-profile.html', {'teacher': teacher})

@login_required
@user_passes_test(is_admin)
def teacher_timesheets(request):
    timesheets = Timesheet.objects.select_related('teacher', 'session__grade', 'session__subject')\
                                   .order_by('teacher__id', '-date')
    
    # Handle POST request for marking timesheets as approved
    if request.method == 'POST':
        timesheet_id = request.POST.get('timesheet_id')
        timesheet = Timesheet.objects.get(id=timesheet_id)
        timesheet.approved = not timesheet.approved  # Toggle approval status
        timesheet.save()

    # Calculate total hours across all timesheets
    total_hours = sum(t.atp_hours for t in timesheets)

    # Group timesheets by teacher
    grouped_timesheets = {}
    for teacher, teacher_timesheets in groupby(timesheets, key=attrgetter('teacher')):
        teacher_timesheets_list = list(teacher_timesheets)
        total_hours_by_teacher = sum(t.atp_hours for t in teacher_timesheets_list)
        grouped_timesheets[teacher] = {
            'timesheets': teacher_timesheets_list,
            'total_hours': total_hours_by_teacher,
        }

    return render(request, 'center_manager/teachers-timesheets.html', {
        'total_hours': total_hours,
        'timesheets': grouped_timesheets,
    })

@login_required
@user_passes_test(is_admin)
def admin_allocate_teacher(request):
    # Get the center manager's center from the logged-in user
    try:
        center = Center.objects.get(center_manager=request.user.center_managers)
        print(f"Center: {center.name}")  # Log the center name
    except Center.DoesNotExist:
        messages.error(request, "No center associated with this manager.")
        return redirect('dashboard')  # Redirect to a suitable page

    if request.method == 'POST':
        teacher_allocation_form = AllocateTeacherForm(request.POST, center=center)
        if request.POST.get('form_type') == 'teacher_allocation_form':
            if teacher_allocation_form.is_valid():
                with transaction.atomic():
                    classroom = Classroom.objects.create(
                        grade=teacher_allocation_form.cleaned_data['grade'],
                        subject=teacher_allocation_form.cleaned_data['subject'],
                        teacher=teacher_allocation_form.cleaned_data['teacher'],
                        center=center
                    )
                    classroom.learners.set(teacher_allocation_form.cleaned_data['learner'])
                messages.success(request, "Teacher allocated successfully.")
                return redirect('allocate_teacher')
            else:
                messages.error(request, "Form is invalid. Please check the fields.")
    else:
        teacher_allocation_form = AllocateTeacherForm(center=center)

        # Debug the teacher and learner querysets
        print(f"Teachers available: {teacher_allocation_form.fields['teacher'].queryset}")
        print(f"Learners available: {teacher_allocation_form.fields['learner'].queryset}")

    return render(request, 'center_manager/admin_allocate_teacher.html', {'teacher_allocation_form': teacher_allocation_form})

@login_required
@user_passes_test(is_admin)
def admin_edit_teacher_allocation(request):
    center = get_object_or_404(Center, center_manager=request.user.center_managers)
    classrooms = Classroom.objects.filter(center=center)  # Get all classrooms associated with the center

    if request.method == 'POST':
        formset = ClassroomFormSet(request.POST, queryset=classrooms)
        if formset.is_valid():
            formset.save()  # Save all the updated classroom instances
            return redirect('classroom_list')  # Redirect to the classroom list or appropriate page
    else:
        formset = ClassroomFormSet(queryset=classrooms)  # Pre-fill the formset with current classroom data

    return render(request, 'center_manager/admin_edit_teacher_allocation.html', {
        'formset': formset,
        'center': center,
    })


@login_required
@user_passes_test(is_admin)
def admin_learner_list(request):
    search_query = request.GET.get('search', '')
    
    # Prefetch learners related to classrooms and their registration data
    classrooms = Classroom.objects.prefetch_related('learners').filter(center__center_manager=request.user.center_managers)

    if search_query:
        # Filter by registration number through the related Registration model
        classrooms = classrooms.filter(learners__registration__registration_number__icontains=search_query)

    paginator = Paginator(classrooms, 10)  # Show 10 classrooms per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all registrations
    registrations = Registration.objects.select_related('learner').all()

    context = {
        'classrooms': page_obj,  # Paginated classrooms
        'page_obj': page_obj,    # For pagination control
        'registrations': registrations,  # List of all registrations
    }
    
    return render(request, 'center_manager/admin-learner-list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_learner_search(request):
    forms = LearnerSearchForm()
    learner = None
    #reg_no = request.GET.get('registration_no', None)
    id_no = request.GET.get('birth_certificate_no', None)
    
    if id_no:  # Check if a registration number was provided
        #learner = Registration.objects.filter(registration_number=reg_no).first()  # Get the first matching learner
        learner = Registration.objects.filter(id_number=id_no).first()  # Get the first matching learner
    context = {
        'forms': forms,
        'learner': learner
    }
    return render(request, 'center_manager/admin-learner-search.html', context)


@login_required
@user_passes_test(is_admin)
def admin_teacher_list(request):
    center = Center.objects.get(center_manager=request.user.center_managers)

    query = request.GET.get('search', '')

    teachers = Teacher.objects.filter(
        Q(centers=center.id) & 
        (Q(name__icontains=query) | Q(email__icontains=query))
    )

    # Paginate the filtered teachers
    paginator = Paginator(teachers, 10)  # Show 10 teachers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'center_manager/admin_teacher_list.html', {'page_obj': page_obj, 'query': query})

@login_required
@user_passes_test(is_admin)
def admin_teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'center_manager/admin_teacher_profile.html', {'teacher': teacher})

@login_required
@user_passes_test(is_admin)
def admin_teacher_timesheets(request):
    timesheets = Timesheet.objects.select_related('teacher', 'session__grade', 'session__subject')\
                                   .order_by('teacher__id', '-date')
    
    # Handle POST request for marking timesheets as approved
    if request.method == 'POST':
        timesheet_id = request.POST.get('timesheet_id')
        timesheet = Timesheet.objects.get(id=timesheet_id)
        timesheet.approved = not timesheet.approved  # Toggle approval status
        timesheet.save()

    # Calculate total hours across all timesheets
    total_hours = sum(t.atp_hours for t in timesheets)

    # Group timesheets by teacher
    grouped_timesheets = {}
    for teacher, teacher_timesheets in groupby(timesheets, key=attrgetter('teacher')):
        teacher_timesheets_list = list(teacher_timesheets)
        total_hours_by_teacher = sum(t.atp_hours for t in teacher_timesheets_list)
        grouped_timesheets[teacher] = {
            'timesheets': teacher_timesheets_list,
            'total_hours': total_hours_by_teacher,
        }

    return render(request, 'center_manager/admin_teacher_timesheets.html', {
        'total_hours': total_hours,
        'timesheets': grouped_timesheets,
    })


@login_required
@user_passes_test(is_admin)
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.is_active = False
    teacher.save()
    return redirect('teacher_list')


@login_required
@user_passes_test(is_admin)
def profile(request):
    try:
        # Fetch the CenterManager instance for the logged-in user
        center_manager = request.user.center_managers  # Uses the 'related_name'
        center = center_manager.center 
    except CenterManager.DoesNotExist:
        center_manager = None  # Handle case where no CenterManager is associated
        center = None

    return render(request, 'center_manager/profile.html', {
        'center_manager': center_manager,
        'center': center
        })

@login_required
@user_passes_test(is_admin)
def update_profile(request):
    center_manager = request.user
    return render(request, 'center_manager/update_profile.html', {'center_manager': center_manager})


class LearnerLoginView(SuccessMessageMixin,FormView):
    template_name = 'center_manager/learner-login.html'  # Update the path
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()

        # Check if the user is valid
        if not user:
           messages.error(self.request, "Invalid user. Please try again.")
           return self.form_invalid(form)  # Redirect back to the form with an error

        # Check if the user is a learner
        if not hasattr(user, 'learner'):
            messages.error(self.request, "You are not registered as a learner.")
            return self.form_invalid(form)  # Redirect back to the form with an error

        # If the user is valid and a learner, proceed with login
        learner = user.learner
        login(self.request, user)

        # Fetch the learner's first and last name
        first_name = learner.name
        last_name = learner.surname

        messages.success(self.request, f'Welcome Learner {first_name} {last_name}')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials. Please try again.')
        # Re-render the form with the error messages
        return redirect('learner-login')
    def get_success_url(self):
        return reverse('learner-dashboard')  # Redirect to the learner's dashboard

@login_required
def learner_dashboard(request):
    # Get the Learner instance related to the user
    learner = get_object_or_404(Learner, user=request.user)
    request.learner = learner

    return render(request, 'center_manager/learner-dashboard.html',{'learner':learner})  # Redirect to avoid resubmission

def learner_registration(request):
    if request.method == 'POST':
        form = LearnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            learner = form.save()  # Save the learner object
            
            # Create a User object with the learner's details
            user = User.objects.create_user(
                username=learner.name,  # Use learner's name as the username
                password=learner.birth_certificate_no,  # Use learner's birth certificate number as the password
            )
            
            # Link the User object to the Learner (optional, assuming a 'user' field in Learner)
            learner.user = user
            learner.save()

            messages.success(request, "Registration successful! User account created.")
            return redirect('learner-login')  # Redirect to the login page after registration
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LearnerRegistrationForm()

    # Pass dynamic choices for Nationality and Center
    nationalities = Nationality.objects.all()
    centers = Center.objects.all()

    return render(
        request, 
        'center_manager/learner-registration.html', 
        {
            'form': form,
            'nationalities': nationalities,
            'centers': centers,
        }
    )


@login_required
def learner_attendance(request):
    # Fetch all classrooms and related teachers
    classrooms = Classroom.objects.select_related('teacher').prefetch_related('learners')
    
    # Create a dictionary to hold forms for each learner grouped by teacher
    teacher_learner_forms = {}

    # Process each classroom
    for classroom in classrooms:
        teacher = classroom.teacher
        learners = classroom.learners.all()

        # Create an empty dictionary for this teacher's learners
        learner_forms = {}
        for learner in learners:
            # Create a form for each learner, with a unique prefix
            learner_forms[learner] = LearnerAttendanceForm(prefix=str(learner.id))

        # Group the forms under the teacher
        teacher_learner_forms[teacher] = learner_forms

    return render(request, 'center_manager/learner-attendance.html', {
        'teacher_learner_forms': teacher_learner_forms,
    })


    
@login_required
def learner_report(request):
    # Fetch all attendance records grouped by date
    attendance = (
        LearnerAttendance.objects.select_related('learner', 'classroom')
        .order_by('-date')  # Order by date (descending)
    )

    # Group attendance records by date in Python
    grouped_attendance = defaultdict(list)
    for record in attendance:
        date_only = record.date  # Extract just the date part
        grouped_attendance[date_only].append(record)

    # Convert defaultdict to a regular dictionary for the template
    grouped_attendance = dict(grouped_attendance)

    return render(request, 'center_manager/learner-report.html', {
        'grouped_attendance': grouped_attendance,
    })

def admin_learner_registration(request):
    if request.method == 'POST':
        form = LearnerForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                learner = form.save(commit=False)
                learner.user = user
                learner.save()

                return redirect('home')
    else:
        form = LearnerForm()
    return render(request, 'center_manager/admin-learner-registration.html', {'form': form})

@login_required
def admin_learner_attendance(request):
    # Fetch all classrooms and related teachers
    classrooms = Classroom.objects.select_related('teacher').prefetch_related('learners')
    
    # Create a dictionary to hold forms for each learner grouped by teacher
    teacher_learner_forms = {}

    # Process each classroom
    for classroom in classrooms:
        teacher = classroom.teacher
        learners = classroom.learners.all()

        # Create an empty dictionary for this teacher's learners
        learner_forms = {}
        for learner in learners:
            # Create a form for each learner, with a unique prefix
            learner_forms[learner] = LearnerAttendanceForm(prefix=str(learner.id))

        # Group the forms under the teacher
        teacher_learner_forms[teacher] = learner_forms

    return render(request, 'center_manager/admin-learner-attendance.html', {
        'teacher_learner_forms': teacher_learner_forms,
    })


    
@login_required
def admin_learner_report(request):
    # Fetch all attendance records grouped by date
    attendance = (
        LearnerAttendance.objects.select_related('learner', 'classroom')
        .order_by('-date')  # Order by date (descending)
    )

    # Group attendance records by date in Python
    grouped_attendance = defaultdict(list)
    for record in attendance:
        date_only = record.date  # Extract just the date part
        grouped_attendance[date_only].append(record)

    # Convert defaultdict to a regular dictionary for the template
    grouped_attendance = dict(grouped_attendance)

    return render(request, 'center_manager/admin-learner-report.html', {
        'grouped_attendance': grouped_attendance,
    })





# Old code at the bottom Nash


# @login_required
# @user_passes_test(is_admin)
# def add_designation(request):
#     forms = AddDesignationForm()
#     if request.method == 'POST':
#         forms = AddDesignationForm(request.POST, request.FILES)
#         if forms.is_valid():
#             forms.save()
#             return redirect('designation')
#     designation = Designation.objects.all()
#     context = {'forms': forms, 'designation': designation}
#     return render(request, 'center_manager/designation.html', context)

# @login_required
# @user_passes_test(is_admin)
# def teacher_registration(request):
#     if request.method == 'POST':
#         form = TeacherForm(request.POST, request.FILES)
#         if form.is_valid():
#             teacher = form.save()
#             return redirect('admin_teacher_list')
#     else:
#         form = TeacherForm()
#     return render(request, 'center_manager/teacher_registration.html', {'form': form})

# @login_required
# @user_passes_test(is_admin)
# def admin_teacher_edit(request, teacher_id):
#     teacher = get_object_or_404(Teacher, id=teacher_id)
#     if request.method == 'POST':
#         form = TeacherForm(request.POST, request.FILES, instance=teacher)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_teacher_list')
#     else:
#         form = TeacherForm(instance=teacher)
#     return render(request, 'center_manager/teacher_edit.html', {'form': form})


# def designation_view(request):
#     designations = Designation.objects.all()
#     return render(request, 'center_manager/designation.html', {'designations': designations})

