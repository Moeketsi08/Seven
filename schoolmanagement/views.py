from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academic import models as academic_models
#import student
from teacher import models as teacher_models
#import employee
#import academic

@login_required(login_url='login')
def home_page(request):
    total_student = academic_models.Student.objects.count() # Needs to be accessed differently from the student in academic appp
    total_teacher = teacher_models.Teacher.objects.count()
    #total_employee = employee_models.PersonalInfo.objects.count()
    total_class = academic_models.ClassRegistration.objects.count()
    context = {
        'student': total_student,
        'teacher': total_teacher,
        #'employee': total_employee,
        'total_class': total_class,
    }
    return render(request, 'home.html', context)
