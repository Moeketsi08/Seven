from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.db import transaction


from center_manager.models import Designation
from center_manager.forms import CenterManagerLoginForm, AllocateTeacherForm, AddDesignationForm
from teacher.forms import TeacherForm
from teacher.models import Teacher, Classroom

def is_admin(user):
    return user.is_staff or user.is_superuser

def is_center_manager(user):
    return user.groups.filter(name='Center Manager').exists()

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

def center_login(request):
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
    return render(request, 'center_manager/center_login.html', context)

class CenterLoginView(SuccessMessageMixin,FormView):
    template_name = 'center_manager/center_login.html'  # Update the path
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f'Welcome  Center Manager')
        #print("Form data:", self.request.POST)  # Debug line
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials. Please try again.')

        # Re-render the form with the error messages
        return redirect('/center_manager/center_login')
    def get_success_url(self):
        return reverse('center_dashboard')  # Redirect to the Center manager's dashboard


def center_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def center_dashboard(request):
    teachers = Teacher.objects.all().count()
    return render(request, 'center_manager/center_dashboard.html', {'teachers':teachers})

@login_required
@user_passes_test(is_admin)
def allocate_teacher(request):
    if request.method == 'POST':
         teacher_allocation_form = AllocateTeacherForm(request.POST) if request.POST.get('form_type') == 'teacher_allocation_form' else AllocateTeacherForm()
         if request.POST.get('form_type') == 'teacher_allocation_form':
            if teacher_allocation_form.is_valid():
                with transaction.atomic():
                    classroom = Classroom.objects.create(
                        grade=teacher_allocation_form.cleaned_data['grade'],
                        subject=teacher_allocation_form.cleaned_data['subject'],
                        teacher=teacher_allocation_form.cleaned_data['teacher'],
                        center=teacher_allocation_form.cleaned_data['center']
                    )
                    classroom.learners.set(teacher_allocation_form.cleaned_data['learners'])
                    
                return redirect('allocate_teacher')
    else:
            teacher_allocation_form = AllocateTeacherForm()
    return render(request, 'center_manager/allocate_teacher.html', {'teacher_allocation_form': teacher_allocation_form})
    



@login_required
@user_passes_test(is_admin)
def add_designation(request):
    forms = AddDesignationForm()
    if request.method == 'POST':
        forms = AddDesignationForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('designation')
    designation = Designation.objects.all()
    context = {'forms': forms, 'designation': designation}
    return render(request, 'center_manager/designation.html', context)

# New teacher management views

@login_required
@user_passes_test(is_admin)
def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            return redirect('admin_teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'center_manager/teacher_registration.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher/teacher-list.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def admin_teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'center_manager/teacher_profile.html', {'teacher': teacher})

@login_required
@user_passes_test(is_admin)
def admin_teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.is_active = False
    teacher.save()
    return redirect('admin_teacher_list')

@login_required
@user_passes_test(is_admin)
def admin_teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('admin_teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'center_manager/teacher_edit.html', {'form': form})


def designation_view(request):
    designations = Designation.objects.all()
    return render(request, 'center_manager/designation.html', {'designations': designations})

