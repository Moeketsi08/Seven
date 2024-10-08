# Generated by Django 3.1.14 on 2024-10-07 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0003_auto_20241007_2359'),
        ('address', '0002_auto_20241005_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyContactDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_guardian_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('relationship_with_student', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt')], max_length=45)),
                ('phone_no', models.CharField(max_length=11)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GuardianInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=100)),
                ('father_phone_no', models.CharField(max_length=11)),
                ('father_occupation', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Banker', 'Banker'), ('Business', 'Business'), ('Doctor', 'Doctor'), ('Farmer', 'Farmer'), ('Fisherman', 'Fisherman'), ('Public Service', 'Public Service'), ('Private Service', 'Private Service'), ('Shopkeeper', 'Shopkeeper'), ('Driver', 'Driver'), ('Worker', 'Worker'), ('N/A', 'N/A')], max_length=45)),
                ('father_yearly_income', models.IntegerField()),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_phone_no', models.CharField(max_length=11)),
                ('mother_occupation', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Banker', 'Banker'), ('Business', 'Business'), ('Doctor', 'Doctor'), ('Farmer', 'Farmer'), ('Fisherman', 'Fisherman'), ('Public Service', 'Public Service'), ('Private Service', 'Private Service'), ('Shopkeeper', 'Shopkeeper'), ('Driver', 'Driver'), ('Worker', 'Worker'), ('N/A', 'N/A')], max_length=45)),
                ('guardian_name', models.CharField(max_length=100)),
                ('guardian_phone_no', models.CharField(max_length=11)),
                ('guardian_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('relationship_with_student', models.CharField(choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Brother', 'Brother'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='student-photos/')),
                ('blood_group', models.CharField(choices=[('a+', 'A+'), ('o+', 'O+'), ('b+', 'B+'), ('ab+', 'AB+'), ('a-', 'A-'), ('o-', 'O-'), ('b-', 'B-'), ('ab-', 'AB-')], max_length=5)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('phone_no', models.CharField(max_length=11)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birth_certificate_no', models.CharField(max_length=50)),
                ('religion', models.CharField(choices=[('Islam', 'Islam'), ('Hinduism', 'Hinduism'), ('Buddhism', 'Buddhism'), ('Christianity', 'Christianity'), ('Others', 'Others')], max_length=45)),
                ('nationality', models.CharField(choices=[('South African', 'South African'), ('Zimbabwe', 'Zimbabwe')], max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='PreviousAcademicCertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_certificate', models.FileField(blank=True, upload_to='documents/')),
                ('release_letter', models.FileField(blank=True, upload_to='documents/')),
                ('testimonial', models.FileField(blank=True, upload_to='documents/')),
                ('marksheet', models.FileField(blank=True, upload_to='documents/')),
                ('stipen_certificate', models.FileField(blank=True, upload_to='documents/')),
                ('other_certificate', models.FileField(blank=True, upload_to='documents/')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousAcademicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute_name', models.CharField(max_length=100)),
                ('name_of_exam', models.CharField(max_length=100)),
                ('group', models.CharField(max_length=45)),
                ('gpa', models.CharField(max_length=10)),
                ('board_roll', models.CharField(max_length=50)),
                ('passing_year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentAddressInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('village', models.TextField()),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.district')),
                ('union', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.union')),
                ('upazilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.upazilla')),
            ],
        ),
        migrations.CreateModel(
            name='AcademicInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_no', models.IntegerField(default=959338, unique=True)),
                ('status', models.CharField(choices=[('not enrolled', 'Not Enrolled'), ('enrolled', 'Enrolled'), ('regular', 'Regular'), ('irregular', 'Irregular'), ('passed', 'Passed')], default='not enrolled', max_length=15)),
                ('date', models.DateField(auto_now_add=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('address_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.studentaddressinfo')),
                ('class_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classinfo')),
                ('emergency_contact_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.emergencycontactdetails')),
                ('guardian_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.guardianinfo')),
                ('personal_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.personalinfo')),
                ('previous_academic_certificate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.previousacademiccertificate')),
                ('previous_academic_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.previousacademicinfo')),
            ],
        ),
        migrations.CreateModel(
            name='EnrolledStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.classregistration')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.academicinfo')),
            ],
            options={
                'unique_together': {('class_name', 'roll')},
            },
        ),
    ]
