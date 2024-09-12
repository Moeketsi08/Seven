from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from academic.models import ClassRegistration
from .forms import ClassRegistrationForm
from .models import District, Upazilla, Union




@login_required(login_url='login')
def add_department(request):
    forms = DepartmentForm()
    if request.method == 'POST':
        forms = DepartmentForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('add-department')
    department = Department.objects.all()
    context = {'forms': forms, 'department': department}
    return render(request, 'academic/add-department.html', context)

def add_class(request):
    forms = ClassForm()
    if request.method == 'POST':
        forms = ClassForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-class')
    class_obj = ClassInfo.objects.all()
    context = {
        'forms': forms,
        'class_obj': class_obj
    }
    return render(request, 'academic/create-class.html', context)

def create_class(request):
    form = ClassRegistrationForm()
    districts = District.objects.all()  # Add this line to get the districts
    if request.method == 'POST':
        form = ClassRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class-list')
    context = {
        'form': form,
        'districts': districts  # Pass the districts to the template
    }
    return render(request, 'academic/create-class.html', context)

def create_section(request):
    forms = SectionForm()
    if request.method == 'POST':
        forms = SectionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-section')
    section = Section.objects.all()
    context = {
        'forms': forms,
        'section': section
    }
    return render(request, 'academic/create-section.html', context)

def create_session(request):
    forms = SessionForm()
    if request.method == 'POST':
        forms = SessionForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-session')
    session = Session.objects.all()
    context = {
        'forms': forms,
        'session': session
    }
    return render(request, 'academic/create-session.html', context)

def create_shift(request):
    forms = ShiftForm()
    if request.method == 'POST':
        forms = ShiftForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-shift')
    shift = Shift.objects.all()
    context = {
        'forms': forms,
        'shift': shift
    }
    return render(request, 'academic/create-shift.html', context)

def class_registration(request):
    forms = ClassRegistrationForm()
    if request.method == 'POST':
        forms = ClassRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('class-list')
    context = {'forms': forms}
    return render(request, 'academic/class-registration.html', context)

def class_list(request):
    register_class = ClassRegistration.objects.all()
    context = {'register_class': register_class}
    return render(request, 'academic/class-list.html', context)

def create_guide_teacher(request):
    forms = GuideTeacherForm()
    if request.method == 'POST':
        forms = GuideTeacherForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('guide-teacher')
    guide_teacher = GuideTeacher.objects.all()
    context = {
        'forms': forms,
        'guide_teacher': guide_teacher
    }
    return render(request, 'academic/create-guide-teacher.html', context)

# AJAX view for loading Upazillas based on District
def load_upazilla(request):
    district_id = request.GET.get('district')
    upazillas = Upazilla.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'academic/upazilla_dropdown_list_options.html', {'upazillas': upazillas})

# AJAX view for loading Unions based on Upazilla
def load_union(request):
    upazilla_id = request.GET.get('upazilla')
    unions = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
    return render(request, 'academic/union_dropdown_list_options.html', {'unions': unions})


