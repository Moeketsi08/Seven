import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from teacher.models import Teacher  

def validate_password(password):
    # Custom password validation
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if password.isnumeric():
        raise ValidationError("Password cannot be entirely numeric.")
    return password

class Command(BaseCommand):
    help = 'Uploads teachers from a CSV file and creates User and Teacher objects'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\moeke\Documents\RoyalMcgrady-KDMS\Teachers.csv'  # Path to your CSV
        data = pd.read_csv(file_path)

        data.columns = data.columns.str.strip()

        data['Name'] = data['Name'].fillna('').astype(str)

        data['Name'] = data['Name'].apply(lambda x: x.strip() if isinstance(x, str) else '')

        data['Employee Code'] = pd.to_numeric(data['Employee Code'], errors='coerce')
        data['ID Number'] = pd.to_numeric(data['ID Number'], errors='coerce')

        # Loop through the CSV data and add users and teachers
        for _, row in data.iterrows():
            try:
                # Step 1: Check if the user already exists by username (which is'Name in your case)
                user, created = User.objects.get_or_create(
                    username=row['Name'],  
                    defaults={
                        'first_name': row['Name'],  # Assuming Name is the full name
                        'last_name': row['Surname'],  # Surname is used for the last name
                        'email': row['Name'] + '@example.com',  # Placeholder email
                        'password': validate_password(row['ID Number']),  # Use ID Number as password
                    }
                )

                # Optional: Ensure the user is active
                user.is_active = True
                user.save()

                # Step 2: Create the Teacher object and link it to the user
                teacher = Teacher.objects.create(
                    user=user,
                    employee_code=row['Employee Code'],
                    surname=row['Surname'],
                    name=row['Name'],
                    id_number=row['ID Number'],
                    is_active=True  # All teachers are active
                )

            except Exception as e:
                print(f"Error adding teacher {row['Name']} : {str(e)}")

        self.stdout.write(self.style.SUCCESS('Teachers uploaded successfully.'))
