import pandas as pd
from datetime import datetime
from teacher.models import ATPSchedule  # Replace 'yourapp' with your actual app name
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Imports ATP data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Import script executed successfully."))


# Load Excel file
file_path = "mnt/data/Final 2025 ATP GRADES 11 KUTLWANONG  PROMATHS ANNUAL TEACHING  PROGRAMME GRADE 11 (Final Jan  - Nov 2025).xlsx"
df = pd.read_excel(file_path)

# Read the Excel file, setting row 11 (0-based index = 10) as the header
df = pd.read_excel(file_path, header=10)

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Print the column names to check if "DATE" is now recognized
print("Column Names:", df.columns.tolist())


# Rename 'Unnamed: 0' to 'DATE' if it corresponds to the date column
df.rename(columns={'Unnamed: 0': 'DATE'}, inplace=True)

# Now, you should be able to access the "DATE" column
print(df["DATE"].head())

from datetime import datetime
import pandas as pd

def parse_date(date_str):
    if pd.isna(date_str) or not isinstance(date_str, str):  # Handle NaN and non-string values
        return None
    try:
        # Try parsing the expected 'YYYY-MM-DD HH:MM:SS' format
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
    except ValueError:
        print(f"Skipping invalid date: {date_str}")
        return None  # Skip invalid date formats

# Iterate over rows and insert into the database
for index, row in df.iterrows():
    try:
        print(f"Row {index} - Raw Date Value: {row['DATE']}")  # Debugging line

        date_obj = parse_date(str(row['DATE']))  # Convert date safely
        if not date_obj:
            continue  # Skip invalid dates

        atp_event = ATPSchedule(
            date=date_obj,  # Use the parsed date
            day=row['Day'],
            mode=row['Mode'],
            paper=row['Paper'] if pd.notna(row['Paper']) else None,
            topic=row['Topic'],
            subject="Mathematics",  # Adjust if multiple subjects exist
            term="Term 1"  # Adjust dynamically if necessary
        )
        atp_event.save()
    except Exception as e:
        print(f"Error saving row {index}: {e}")

