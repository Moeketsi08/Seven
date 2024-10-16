from django.shortcuts import render, redirect
from academic.models import Registration
from learner.forms import *
from learner.models import *

# def load_upazilla(request):
#     district_id = request.GET.get('district')
#     upazilla = Upazilla.objects.filter(district_id=district_id).order_by('name')

#     upazilla_id = request.GET.get('upazilla')
#     union = Union.objects.filter(upazilla_id=upazilla_id).order_by('name')
#     context = {
#         'upazilla': upazilla,
#         'union': union
#     }
#     return render(request, 'others/upazilla_dropdown_list_options.html', context)


# def class_wise_learner_registration(request):
#     register_class = ClassRegistration.objects.all()
#     context = {'register_class': register_class}
#     return render(request, 'learner/class-wise-learner-registration.html', context)

# def learner_registration(request):
#     academic_info_form = AcademicInfoForm(request.POST or None)
#     personal_info_form = PersonalInfoForm(request.POST or None, request.FILES or None)
#     learner_address_info_form = LearnerAddressInfoForm(request.POST or None)
#     guardian_info_form = GuardianInfoForm(request.POST or None)
#     emergency_contact_details_form = EmergencyContactDetailsForm(request.POST or None)
#     previous_academic_info_form = PreviousAcademicInfoForm(request.POST or None)
#     previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST or None, request.FILES)

#     if request.method == 'POST':
#         if academic_info_form.is_valid() and personal_info_form.is_valid() and learner_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
#             s1 = personal_info_form.save()
#             s2 = learner_address_info_form.save()
#             s3 = guardian_info_form.save()
#             s4 = emergency_contact_details_form.save()
#             s5 = previous_academic_info_form.save()
#             s6 = previous_academic_certificate_form.save()
#             academic_info = academic_info_form.save(commit=False)
#             academic_info.personal_info = s1
#             academic_info.address_info = s2
#             academic_info.guardian_info = s3
#             academic_info.emergency_contact_info = s4
#             academic_info.previous_academic_info = s5
#             academic_info.previous_academic_certificate = s6
#             academic_info.save()
#             return redirect('learner-list')

#     context = {
#         'academic_info_form': academic_info_form,
#         'personal_info_form': personal_info_form,
#         'learner_address_info_form': learner_address_info_form,
#         'guardian_info_form': guardian_info_form,
#         'emergency_contact_details_form': emergency_contact_details_form,
#         'previous_academic_info_form': previous_academic_info_form,
#         'previous_academic_certificate_form': previous_academic_certificate_form
#     }
#     return render(request, 'learner/learner-registration.html', context)

# def learner_profile(request, reg_no):
#     learner = AcademicInfo.objects.get(registration_no=reg_no)
#     context = {
#         'learner': learner
#     }
#     return render(request, 'learner/learner-profile.html', context)

# def learner_edit(request, reg_no):
#     learner = AcademicInfo.objects.get(registration_no=reg_no)
#     academic_info_form = AcademicInfoForm(instance=learner)
#     personal_info_form = PersonalInfoForm(instance=learner.personal_info)
#     learner_address_info_form = LearnerAddressInfoForm(instance=learner.address_info)
#     guardian_info_form = GuardianInfoForm(instance=learner.guardian_info)
#     emergency_contact_details_form = EmergencyContactDetailsForm(instance=learner.emergency_contact_info)
#     previous_academic_info_form = PreviousAcademicInfoForm(instance=learner.previous_academic_info)
#     previous_academic_certificate_form = PreviousAcademicCertificateForm(instance=learner.previous_academic_certificate)

#     if request.method == 'POST':
#         academic_info_form = AcademicInfoForm(request.POST, instance=learner)
#         personal_info_form = PersonalInfoForm(request.POST, request.FILES, instance=learner.personal_info)
#         learner_address_info_form = LearnerAddressInfoForm(request.POST, instance=learner.address_info)
#         guardian_info_form = GuardianInfoForm(request.POST, instance=learner.guardian_info)
#         emergency_contact_details_form = EmergencyContactDetailsForm(request.POST, instance=learner.emergency_contact_info)
#         previous_academic_info_form = PreviousAcademicInfoForm(request.POST, instance=learner.previous_academic_info)
#         previous_academic_certificate_form = PreviousAcademicCertificateForm(request.POST, request.FILES, instance=learner.previous_academic_certificate)
#         if academic_info_form.is_valid() and personal_info_form.is_valid() and learner_address_info_form.is_valid() and guardian_info_form.is_valid() and emergency_contact_details_form.is_valid() and previous_academic_info_form.is_valid() and previous_academic_certificate_form.is_valid():
#             s1 = personal_info_form.save()
#             s2 = learner_address_info_form.save()
#             s3 = guardian_info_form.save()
#             s4 = emergency_contact_details_form.save()
#             s5 = previous_academic_info_form.save()
#             s6 = previous_academic_certificate_form.save()
#             academic_info = academic_info_form.save(commit=False)
#             academic_info.personal_info = s1
#             academic_info.address_info = s2
#             academic_info.guardian_info = s3
#             academic_info.emergency_contact_info = s4
#             academic_info.previous_academic_info = s5
#             academic_info.previous_academic_certificate = s6
#             academic_info.save()
#             return redirect('learner-list')

#     context = {
#         'academic_info_form': academic_info_form,
#         'personal_info_form': personal_info_form,
#         'learner_address_info_form': learner_address_info_form,
#         'guardian_info_form': guardian_info_form,
#         'emergency_contact_details_form': emergency_contact_details_form,
#         'previous_academic_info_form': previous_academic_info_form,
#         'previous_academic_certificate_form': previous_academic_certificate_form
#     }
#     return render(request, 'learner/learner-edit.html', context)

# def learner_delete(request, reg_no):
#     learner = AcademicInfo.objects.get(registration_no=reg_no)
#     learner.is_delete = True
#     learner.save()
#     return redirect('learner-list')



# def enrolled_learner(request):
#     forms = EnrolledLearnerForm()
#     cls = request.GET.get('class_name', None)
#     learner = AcademicInfo.objects.filter(class_info=cls, status='not enroll')
#     context = {
#         'forms': forms,
#         'learner': learner
#     }
#     return render(request, 'learner/enrolled.html', context)

# def learner_enrolled(request, reg):
#     learner = AcademicInfo.objects.get(registration_no=reg)
#     forms = LearnerEnrollForm()
#     if request.method == 'POST':
#         forms = LearnerEnrollForm(request.POST)
#         if forms.is_valid():
#             roll = forms.cleaned_data['roll_no']
#             class_name = forms.cleaned_data['class_name']
#             EnrolledLearner.objects.create(class_name=class_name, learner=learner, roll=roll)
#             learner.status = 'enrolled'
#             learner.save()
#             return redirect('enrolled-learner-list')
#     context = {
#         'learner': learner,
#         'forms': forms
#     }
#     return render(request, 'learner/learner-enrolled.html', context)

# def enrolled_learner_list(request):
#     learner = EnrolledLearner.objects.all()
#     forms = SearchEnrolledLearnerForm()
#     class_name = request.GET.get('reg_class', None)
#     roll = request.GET.get('roll_no', None)
#     if class_name:
#         learner = EnrolledLearner.objects.filter(class_name=class_name)
#         context = {
#             'forms': forms,
#             'learner': learner
#         }
#         return render(request, 'learner/enrolled-learner-list.html', context)
#     context = {
#         'forms': forms,
#         'learner': learner
#     }
#     return render(request, 'learner/enrolled-learner-list.html', context)
