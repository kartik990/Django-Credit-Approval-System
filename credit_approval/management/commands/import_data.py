from django.core.management.base import BaseCommand
import pandas as pd
from credit_approval.models import Customer, Loan

class Command(BaseCommand):
    help = 'Import data from Excel files into the database'

    def handle(self, *args, **kwargs):
        # Read customer data from Excel
        customer_df = pd.read_excel('customer_data.xlsx')
        for _, row in customer_df.iterrows():
            Customer.objects.create(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                age=row['Age'],
                approved_limit=row['Approved Limit'],
            )

          

        # Read loan data from Excel
        loan_df = pd.read_excel('loan_data.xlsx')

        loan_df.drop_duplicates(subset=['Loan ID'], inplace=True)

        for _, row in loan_df.iterrows():
            customer_id = row['Customer ID']
            customer = Customer.objects.get(customer_id=customer_id)
            Loan.objects.create(
                customer=customer,
                loan_id=row['Loan ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_repayment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],
                end_date=row['End Date']
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
