from collections import defaultdict
import csv
from itertools import groupby
from operator import attrgetter
from django.http import HttpResponse
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
from center_manager.forms import CenterManagerLoginForm, AllocateTeacherForm, ClassroomFormSet, DocumentUploadForm, LearnerRegistrationForm
from learner.forms import LearnerForm, LearnerSearchForm
from teacher.forms import LearnerAttendanceForm, TimesheetForm
from teacher.models import Teacher, Classroom, Timesheet, TeacherCenterAssignment
from academic.models import Nationality, Registration
from teacher import models as teacher_models
from learner.models import Learner
from django.db.models.functions import TruncDate  # Import TruncDate
from django.db.models import Count
from django.shortcuts import redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def is_admin(user):
    return user.is_staff or user.is_superuser or user.groups.filter(name='Center Manager').exists()


# def root_redirect_view(request):
#     return redirect('/login')

@login_required
@user_passes_test(is_admin)
def center_dashboard(request):
    center_manager = request.user.center_managers
    center = get_object_or_404(Center, center_manager=center_manager)

    # Get all teachers assigned to the center
    teachers = TeacherCenterAssignment.objects.filter(center=center).values_list('teacher', flat=True)

    # Fetch teachers count
    total_teachers = teachers.count()

    # Fetch timesheets for teachers at the center
    timesheets = Timesheet.objects.filter(teacher__id__in=teachers).order_by('-date')

    # Calculate total hours per teacher by date
    total_hours_by_teacher = {
        teacher: {
            date: sum(t.atp_hours for t in timesheets if t.teacher == teacher and t.date == date)
            for date in set(t.date for t in timesheets if t.teacher == teacher)
        }
        for teacher in set(t.teacher for t in timesheets)
    }

    # Calculate total hours across all timesheets at the center
    total_hours = sum(t.atp_hours for t in timesheets)

    # Get all classrooms in the center
    classrooms = Classroom.objects.filter(center=center)

    # Get distinct grade and subject combinations for classrooms at the center
    grade_subject_combinations = classrooms.values('grade__grade', 'subject__subject').distinct()

    # Get the total number of classrooms at the center
    total_classes = classrooms.count()

    # Get the total number of learners in each classroom
    classroom_learners = {
        f"{classroom.grade.grade} - {classroom.subject.subject}": classroom.learners.count()
        for classroom in classrooms
    }

    # Get the total number of learners in each classroom and their attendance percentage by date
    classroom_attendance = {}
    for classroom in classrooms:
        total_learners = classroom.learners.count()
        class_dates = LearnerAttendance.objects.filter(classroom=classroom).values_list('date', flat=True).distinct()
        
        date_attendance = {
            date: round(
                (LearnerAttendance.objects.filter(classroom=classroom, status='P', date=date).count() / total_learners) * 100, 2
            ) if total_learners > 0 else 0
            for date in class_dates
        }

        total_classes = len(class_dates)
        total_attendance = sum(date_attendance.values())
        overall_percentage = round((total_attendance / total_classes), 2) if total_classes > 0 else 0

        classroom_attendance[f"{classroom.grade.grade} - {classroom.subject.subject}"] = {
            'date_attendance': date_attendance,
            'overall_percentage': overall_percentage,
        }

    # Fetch all centers with teacher counts for comparison
    all_centers = Center.objects.annotate(
        teacher_count=Count('teachercenterassignment')
    ).values('id', 'name', 'teacher_count')

    return render(request, 'center_manager/center-dashboard.html', {
        'timesheets': timesheets,
        'total_hours_by_teacher': total_hours_by_teacher,  
        'total_hours': total_hours,
        'total_classes': total_classes,
        'grade_subject_combinations': grade_subject_combinations,
        'classroom_learners': classroom_learners,
        'classroom_attendance': classroom_attendance,
        'total_teachers': total_teachers,
        'centers': all_centers,  
    })

from django.db.models import Count, Q

def admin_login(request):
    forms = CenterManagerLoginForm()

    if request.method == 'POST':
        forms = CenterManagerLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, f'Welcome, Administrator {user.username}')
                    return redirect('admin_dashboard')  # Redirect to dashboard instead of rendering

                else:
                    messages.error(request, "You do not have admin privileges.")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'center_manager/login.html', {'forms': forms})

@login_required
def upload_document(request):
    learner = request.user.learner  # Get the learner associated with the logged-in user
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=learner)
        if form.is_valid():
            form.save()
            return redirect('center_manager/learner_dashboard')  # Redirect back to the dashboard
        
    else:
        form = DocumentUploadForm(instance=learner)

    return render(request, 'center_manager/upload_document.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can access
def admin_dashboard(request):
    centers = Center.objects.prefetch_related("classrooms").all()
    all_centers = centers.count()
    all_learners = Learner.objects.count()
    total_timesheets = Timesheet.objects.count()
    total_attendance = LearnerAttendance.objects.count()

    # **Total learners per center**
    learners_per_center = (
        Center.objects.annotate(total_learners=Count("classrooms__learners"))
        .values("id", "name", "total_learners")
    )

    # **Total attendance per center**
    attendance_per_center = (
        Center.objects.annotate(total_attendance=Count("classrooms__learnerattendance"))
        .values("id", "name", "total_attendance")
    )

    # **Calculate overall attendance percentage**
    overall_percentage = (total_attendance / all_learners) * 100 if all_learners > 0 else 0

    return render(request, 'home.html', {
        'centers': centers,
        'total_learners': all_learners,
        'learners_per_center': learners_per_center,
        'total_timesheets': total_timesheets,
        'total_attendance': total_attendance,
        'attendance_per_center': attendance_per_center,
        'all_centers': all_centers,
        'overall_attendance_percentage': round(overall_percentage, 2),  # Rounded percentage
    })

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

        # Check if the center manager has a center assigned
        if not hasattr(center_managers, 'center') or center_managers.center is None:
            messages.error(self.request, "No center associated with this center manager.")
            return self.form_invalid(form)

        login(self.request, user)


        # Fetch the center manager's first and last name
        name = center_managers.name
        surname = center_managers.surname

        messages.success(self.request, f'Welcome, Center Manager {name} {surname}')

        return redirect(self.get_success_url())

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

    except Center.DoesNotExist:
        messages.error(request, "No center associated with this manager.")
        return redirect('center_manager/center-dashboard')  # Redirect to a suitable page


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
    center_manager = getattr(request.user, 'center_managers', None)

    if center_manager is None:
        messages.error(request, "No Center Manager is associated with your account.")
        return redirect('center-dashboard')  # Ensure 'center-dashboard' exists in urls.py

    try:
        center = Center.objects.get(center_manager=center_manager)
    except Center.DoesNotExist:
        messages.error(request, "No Center is linked to your account.")
        return redirect('center-dashboard')

    query = request.GET.get('search', '')

    # Use correct field lookup depending on relationship type
    teachers = Teacher.objects.filter(centers=center).filter(
        Q(name__icontains=query) | Q(email__icontains=query)
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
def export_timesheet_csv(request):
    timesheets = Timesheet.objects.select_related('teacher', 'session__grade', 'session__subject')\
                                   .order_by('teacher__id', '-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timesheets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Teacher', 'Start Time', 'End Time', 'Class', 'Subject', 'Hours', 'Date', 'Approved'])

    for teacher, teacher_timesheets in groupby(timesheets, key=attrgetter('teacher')):
        for timesheet in teacher_timesheets:
            writer.writerow([
                f"{timesheet.teacher.name} {timesheet.teacher.surname}",
                timesheet.session.start_time.strftime("%H:%M"),
                timesheet.session.end_time.strftime("%H:%M"),
                timesheet.session.grade.grade,
                timesheet.session.subject.subject,
                timesheet.atp_hours,
                timesheet.date.strftime("%Y-%m-%d"),
                'Approved' if timesheet.approved else 'Pending',
            ])

    return response


@login_required
@user_passes_test(is_admin)
def export_timesheet_pdf(request):
    timesheets = Timesheet.objects.select_related('teacher', 'session__grade', 'session__subject')\
                                   .order_by('teacher__id', '-date')

    grouped_timesheets = {}
    for teacher, teacher_timesheets in groupby(timesheets, key=attrgetter('teacher')):
        teacher_timesheets_list = list(teacher_timesheets)
        total_hours_by_teacher = sum(t.atp_hours for t in teacher_timesheets_list)
        grouped_timesheets[teacher] = {
            'timesheets': teacher_timesheets_list,
            'total_hours': total_hours_by_teacher,
        }

    html_string = render_to_string('center_manager/timesheet_pdf.html', {
        'timesheets': grouped_timesheets,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="timesheets.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response

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


# @login_required
# @user_passes_test(is_admin)
# def admin_learner_list(request):
#     search_query = request.GET.get('search', '')
    
#     # Prefetch learners related to classrooms and their registration data
#     classrooms = Classroom.objects.prefetch_related('learners').filter(center__center_manager=request.user.center_managers)

#     if search_query:
#         # Filter by registration number through the related Registration model
#         classrooms = classrooms.filter(learners__registration__registration_number__icontains=search_query)

#     paginator = Paginator(classrooms, 10)  # Show 10 classrooms per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Fetch all registrations
#     registrations = Registration.objects.select_related('learner').all()

#     context = {
#         'classrooms': page_obj,  # Paginated classrooms
#         'page_obj': page_obj,    # For pagination control
#         'registrations': registrations,  # List of all registrations
#     }
    
#     return render(request, 'center_manager/admin-learner-list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_learner_list(request):
    search_query = request.GET.get('search', '')

    # Get the center manager if it exists
    center_manager = getattr(request.user, "center_managers", None)
    center = Center.objects.filter(center_manager=center_manager).first() if center_manager else None

    # Fetch classrooms only if a center exists; otherwise, return an empty queryset
    classrooms = Classroom.objects.prefetch_related('learners').filter(center=center) if center else Classroom.objects.none()

    if search_query:
        classrooms = classrooms.filter(learners__registration__registration_number__icontains=search_query)

    paginator = Paginator(classrooms, 10)  # Show 10 classrooms per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all registrations
    registrations = Registration.objects.select_related('learner').all() if center else Registration.objects.none()

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

def admin_teacher_list(request):
    center_manager = getattr(request.user, "center_managers", None)

    # if center_manager is None:
    #     messages.error(request, "You are not assigned to any center.")
        #return redirect("center_manager/admin_teacher_list.html")  # Redirect to a relevant admin page

    center = Center.objects.filter(center_manager=center_manager).first()

    # if center is None:
    #     messages.error(request, "No center found for this user.")
        #return redirect("center_manager/admin_teacher_list.html")  # Redirect to a relevant admin page

    query = request.GET.get("search", "")

    # teachers = Teacher.objects.filter(
    #     Q(centers=center.id) & 
    #     (Q(name__icontains=query) | Q(email__icontains=query))
    # )
       # Only fetch teachers if a valid center exists
    teachers = Teacher.objects.filter(
        Q(centers=center.id) & 
        (Q(name__icontains=query) | Q(email__icontains=query))
    ) if center else Teacher.objects.none()  # Return an empty queryset if no center

    # Paginate the filtered teachers
    paginator = Paginator(teachers, 10)  # Show 10 teachers per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "center_manager/admin_teacher_list.html", {
        "page_obj": page_obj,
        "query": query
    })

# @login_required
# @user_passes_test(is_admin)
# def admin_teacher_list(request):
#     center = Center.objects.get(center_manager=request.user.center_managers)

#     query = request.GET.get('search', '')

#     teachers = Teacher.objects.filter(
#         Q(centers=center.id) & 
#         (Q(name__icontains=query) | Q(email__icontains=query))
#     )

#     # Paginate the filtered teachers
#     paginator = Paginator(teachers, 10)  # Show 10 teachers per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'center_manager/admin_teacher_list.html', {'page_obj': page_obj, 'query': query})

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
        #return super().form_valid(form)
        return render(self.request,'center_manager/learner-dashboard.html',{
            'learner': learner,
        })
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
                password=learner.id_no,  # Use learner's birth certificate number as the password
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

