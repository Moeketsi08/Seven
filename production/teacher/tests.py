from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from academic.models import ClassInfo, Session, Center, ClassRegistration, Learner
from attendance.models import LearnerAttendance
from teacher.models import Teacher, Timesheet
from django.utils import timezone
from datetime import timedelta
from django.test import override_settings

class TeacherFunctionalityTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='teacher1', password='password')

        # Create a teacher
        self.teacher = Teacher.objects.create(
            user=self.user,
            name="John Doe",
            date_of_birth="1980-01-01",
            gender="male",
            phone_no="1234567890",
            email="johndoe@example.com",
            address="123 Main St",
            highest_degree="PhD",
            institution="University of Education",
            specialization="Mathematics",
            date_joined="2020-01-01",
            is_active=True
        )

        # Create a center
        self.center = Center.objects.create(name="Main Center", address="123 Main St")

        # Create a class info
        self.class_info = ClassInfo.objects.create(subject='Mathematics', grade='10')

        # Create a session
        self.session = Session.objects.create(
            day='SAT',
            start_time='09:00',
            end_time='10:00',
            class_info=self.class_info
        )

        # Create a class registration
        self.class_reg = ClassRegistration.objects.create(center=self.center, session=self.session)

        # Associate the teacher with the class info
        self.teacher.subjects_taught.add(self.class_info)

        # Create a timesheet
        self.timesheet = Timesheet.objects.create(
            teacher=self.teacher,
            session=self.session,
            date="2023-01-01",
            atp_hours=5.0
        )

        # Create a learner
        self.learner = Learner.objects.create(
            first_name='Alice',
            last_name='Johnson',
            class_registration=self.class_reg
        )

        # Create an attendance record
        self.attendance = LearnerAttendance.objects.create(
            learner=self.learner,
            class_name=self.class_reg,
            status=1
        )

        # Create a client for testing
        self.client = Client()

        # Calculate tomorrow's date
        self.tomorrow = timezone.now().date() + timedelta(days=1)

    def test_teacher_login(self):
        # Test teacher login
        response = self.client.post(reverse('teacher-login'), {'username': 'teacher1', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirects to dashboard

    def test_teacher_dashboard_access(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, John Doe")

    def test_teacher_view_classes_and_sessions(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mathematics - 10")
        self.assertContains(response, "SAT (9 a.m. - 10 a.m.)")

    def test_teacher_manage_timesheet(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "5.0")

    def test_teacher_track_attendance(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)

        # Debug information
        print(f"Response content: {response.content.decode()}")

        self.assertContains(response, "Alice Johnson")

    def test_teacher_view_learner_information(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Johnson")

    # New tests to add:(These migh need to be modified. The modifications are mainly changing how the templates in the frontend are
    #referencing the names of the views and urls)

    #@override_settings(TEMPLATE_DIRS=())
    #def test_teacher_create_timesheet(self):
    #    self.client.login(username='teacher1', password='password')
    #    data = {
    #        'session': self.session.id,
     #         'date': self.tomorrow,
     #         'atp_hours': 4.0
     #    }
     #        response = self.client.post(reverse('submit_attendance_and_timesheet', kwargs={'session_id': self.session.id}), data)
     #     self.assertRedirects(response, reverse('teacher_dashboard'))
     #    self.assertTrue(Timesheet.objects.filter(teacher=self.teacher, date=self.tomorrow).exists())

   # @override_settings(TEMPLATE_DIRS=())
    #def test_teacher_edit_timesheet(self):
      #  self.client.login(username='teacher1', password='password')
        
        # First, create a timesheet
        #timesheet = Timesheet.objects.create(
        #    teacher=self.teacher,
        #    session=self.session,
        #    date=self.tomorrow,
        #    atp_hours=3.0
       # )
        
        # Now edit it
        #data = {
        #    'date': self.tomorrow.strftime('%Y-%m-%d'),
        #    'atp_hours': 5.0,
        #    'form-TOTAL_FORMS': '1',
        #    'form-INITIAL_FORMS': '0',
        #    'form-0-learner_id': self.learner.id,
        #    'form-0-status': 'present'
        #}
       # response = self.client.post(reverse('submit_attendance_and_timesheet', kwargs={'session_id': self.session.id}), data)
        
        # Check if the response redirects to the dashboard
        #self.assertRedirects(response, reverse('teacher_dashboard'), fetch_redirect_response=False)
        
        # Check if a new timesheet was created (since we're not actually editing, but creating a new one)
        #new_timesheet = Timesheet.objects.filter(teacher=self.teacher, date=self.tomorrow, atp_hours=5.0).first()
     #   self.assertIsNotNone(new_timesheet)
     #   self.assertEqual(new_timesheet.atp_hours, 5.0)
        
        # Check if the attendance was created
     #   attendance = LearnerAttendance.objects.filter(learner=self.learner, class_name=self.session.class_info, date=self.tomorrow).first()
     #   self.assertIsNotNone(attendance)
     #   self.assertEqual(attendance.status, 'present')

    #@override_settings(TEMPLATE_DIRS=())
    #def test_teacher_mark_attendance(self):
    #    self.client.login(username='teacher1', password='password')
    #    data = {
    #        'session': self.session.id,
    #        'date': self.tomorrow,
    #        'atp_hours': 3.0,
    #        'form-TOTAL_FORMS': '1',
    #        'form-INITIAL_FORMS': '0',
    #        'form-0-learner_id': self.learner.id,
    #        'form-0-status': 'present'
    #    }
    #    response = self.client.post(reverse('submit_attendance_and_timesheet', kwargs={'session_id': self.session.id}), data)
    #    self.assertRedirects(response, reverse('teacher_dashboard'))
    #    self.assertTrue(Timesheet.objects.filter(teacher=self.teacher, date=self.tomorrow, atp_hours=3.0).exists())
    #    self.assertTrue(LearnerAttendance.objects.filter(learner=self.learner, class_name=self.class_reg, date=self.tomorrow, status='present').exists())

    #def test_teacher_view_class_details(self):
    #    self.client.login(username='teacher1', password='password')
    #    response = self.client.get(reverse('class_details', kwargs={'pk': self.class_reg.id}))
     #   self.assertEqual(response.status_code, 200)
     #   self.assertContains(response, "Mathematics - 10")
    #    self.assertContains(response, "Main Center")
    #    self.assertContains(response, "Alice Johnson")




    #@override_settings(TEMPLATE_DEBUG=True)
    #def test_teacher_create_timesheet(self):
    #    self.client.login(username='teacher1', password='password')
    #    data = {
    #        'session': self.session.id,
    #        'date': self.tomorrow,
    #        'atp_hours': 4.0
    #    }
        
        # Capture template rendering logs
    #    with self.assertLogs('django.template', level='DEBUG') as cm:
    #        response = self.client.post(reverse('submit_attendance_and_timesheet', kwargs={'session_id': self.session.id}), data)
        
        # Print out the captured logs
    #    print("Template rendering logs:")
    #    for log in cm.output:
    #        print(log)

        # Original assertions
    #    self.assertRedirects(response, reverse('teacher_dashboard'))
    #    self.assertTrue(Timesheet.objects.filter(teacher=self.teacher, date=self.tomorrow).exists())

        # Additional check for the 'logout' URL in the response content
    #    if 'logout' in response.content.decode():
    #        print("'logout' found in response content")
    #        print(response.content.decode())S