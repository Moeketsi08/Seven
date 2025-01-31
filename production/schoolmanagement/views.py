from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from learner.models import Learner
from academic.models import Registration
#import learner
from teacher import models as teacher_models
#import employee
#import academic

@login_required(login_url='login')
def home_page(request):
    total_learner = Learner.objects.all() # Needs to be accessed differently from the learner in academic appp
    total_teacher = teacher_models.Teacher.objects.all()
    #total_employee = employee_models.PersonalInfo.objects.count()
    total_class = Registration.objects.all()
    context = {
        'learner': total_learner,
        'teacher': total_teacher,
        #'employee': total_employee,
        'total_class': total_class,
    }
    return render(request, 'home.html', context)
