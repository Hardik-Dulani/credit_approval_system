import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer, Loan

class Command(BaseCommand):
    help = 'Import data from Excel files into database'

    def handle(self, *args, **options):
        # Specify the paths to your Excel files
        

        # Import data from Excel files
        customers_data = pd.read_excel(r"customer_data.xlsx", header=None)
        loans_data = pd.read_excel(r"loan_data.xlsx", header=None)

        # Save data to the database
        self.save_to_database(Customer, customers_data)
        self.save_to_database(Loan, loans_data)

    def save_to_database(self, model, data):
        try:
            # Drop existing records to avoid duplicates (optional)
            model.objects.all().delete()

            # Assuming model._meta.fields returns the model's fields in the desired order
            columns = [field.name for field in model._meta.fields]

            # Convert DataFrame to list of dictionaries with generated column names
            data.columns = columns
            records = data.reset_index(drop=True).to_dict(orient='records')

            # Bulk create records in the database
            if model == Loan:
    # Handle the 'customer' field by converting the customer_id to a Customer instance
                model_objects = [
        model(
            customer_id=Customer.objects.get(pk=int(record['customer_id'])),
            start_date=datetime.strptime(record['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(record['end_date'], '%Y-%m-%d'),
            **{str(key): str(value) for key, value in record.items() if key not in ['customer_id', 'start_date', 'end_date']}
        ) for record in records
    ]
            else:
                # For other models, use a generic approach
                model_objects = [
                    model(**{str(key): str(value) for key, value in record.items()})
                    for record in records
                ]

            # Bulk create the model objects
            model.objects.bulk_create(model_objects)


            self.stdout.write(self.style.SUCCESS(f'Successfully imported data into {model._meta.db_table}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {e}'))
            self.stdout.write(self.style.ERROR(f'Structure of records: {records}'))


