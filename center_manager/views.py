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

from center_manager.models import Center, CenterManager
from center_manager.forms import CenterManagerLoginForm, AllocateTeacherForm, ClassroomFormSet
from learner.forms import LearnerSearchForm
from teacher.models import Teacher, Classroom
from academic.models import Registration

def is_admin(user):
    return user.is_staff or user.is_superuser or user.groups.filter(name='Center Manager').exists()

@login_required
@user_passes_test(is_admin)
def center_dashboard(request):
    center = get_object_or_404(Center, center_manager=request.user.center_managers)
    teachers = Teacher.objects.filter(centers=center).count()
    return render(request, 'center_manager/center-dashboard.html', {'teachers':teachers})

def admin_login(request):
    forms = CenterManagerLoginForm()
    if request.method == 'POST':
        forms = CenterManagerLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
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
        login(self.request, user)
        messages.success(self.request, f'Welcome, Center Manager')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse('center-dashboard')


def center_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def allocate_teacher(request):
    # Get the center manager's center from the logged-in user
    try:
        center = Center.objects.get(center_manager=request.user.center_managers)
    except Center.DoesNotExist:
        # Handle case where center manager has no center
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
                        center=center  # Ensures the center is assigned to the classroom
                    )
                    classroom.learners.set(teacher_allocation_form.cleaned_data['learners'])
                return redirect('allocate_teacher')
    else:
        teacher_allocation_form = AllocateTeacherForm(center=center)

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
    print(registrations)

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
    reg_no = request.GET.get('registration_no', None)
    
    if reg_no:  # Check if a registration number was provided
        learner = Registration.objects.filter(registration_number=reg_no).first()  # Get the first matching learner
    
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

