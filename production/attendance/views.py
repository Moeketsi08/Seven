from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#from .forms import SearchEnrolledLearnerForm
#from learner.models import EnrolledLearner
from .models import LearnerAttendance

#def learner_attendance(request):
    #forms = SearchEnrolledLearnerForm()
    #class_name = request.GET.get('reg_class', None)
    #if class_name:
        #class_info = ClassRegistration.objects.get(id=class_name)
        #learner = EnrolledLearner.objects.filter(class_name=class_name)
        #context = {
            #'forms': forms,
            #'learner': learner,
            #'class_info': class_info
        #}
        #return render(request, 'attendance/learner-attendance.html', context)
    #context = {
        #'forms': forms,
    #}
    #return render(request, 'attendance/learner-attendance.html', context)

class SetAttendance(APIView):
    def get(self, request, std_class, std_roll):
        try:
            LearnerAttendance.objects.create_attendance(std_class, std_roll)
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)