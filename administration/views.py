from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Designation
from teacher.models import Teacher, Department
from .forms import *
from teacher.forms import TeacherForm

def is_admin(user):
    return user.is_staff or user.is_superuser

def admin_login(request):
    forms = AdminLoginForm()
    if request.method == 'POST':
        forms = AdminLoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {'forms': forms}
    return render(request, 'administration/login.html', context)

def admin_logout(request):
    logout(request)
    return redirect('login')

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
    return render(request, 'administration/designation.html', context)

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
    return render(request, 'administration/teacher_registration.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'administration/teacher_list.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def admin_teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'administration/teacher_profile.html', {'teacher': teacher})

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
    return render(request, 'administration/teacher_edit.html', {'form': form})


def designation_view(request):
    designations = Designation.objects.all()
    return render(request, 'administration/designation.html', {'designations': designations})

