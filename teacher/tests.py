from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from academic.models import ClassInfo, Session, Center, ClassRegistration, Student
from attendance.models import StudentAttendance
from teacher.models import Teacher, Timesheet

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

        # Create a student
        self.student = Student.objects.create(
            first_name='Alice',
            last_name='Johnson',
            class_registration=self.class_reg
        )

        # Create an attendance record
        self.attendance = StudentAttendance.objects.create(
            student=self.student,
            class_name=self.class_reg,
            status=1
        )

        # Create a client for testing
        self.client = Client()

    def test_teacher_login(self):
        # Test teacher login
        response = self.client.post(reverse('teacher_login'), {'username': 'teacher1', 'password': 'password'})
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

    def test_teacher_view_student_information(self):
        # Log in the teacher
        self.client.login(username='teacher1', password='password')

        # Access the teacher dashboard
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Johnson")