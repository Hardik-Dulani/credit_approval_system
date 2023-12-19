import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer, Loan

class Command(BaseCommand):
    help = 'Import data from Excel files into database'

    def handle(self, *args, **options):
        # Specify the paths to your Excel files
        

        # Import data from Excel files
        customers_data = pd.read_excel(r"customer_data.xlsx")
        loans_data = pd.read_excel(r"loan_data.xlsx")

        # Save data to the database
        self.save_to_database(Customer, customers_data)
        self.save_to_database(Loan, loans_data)

    def save_to_database(self, model, data):
        # Drop existing records to avoid duplicates (optional)
        model.objects.all().delete()

        # Convert DataFrame to list of dictionaries
        records = data.to_dict(orient='records')

        # Bulk create records in the database
        model.objects.bulk_create([model(**record) for record in records])

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data into {model._meta.db_table}'))
