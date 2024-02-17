from credit_approval.models import Customer, Loan
from django.db import connection
import pandas as pd


def calculate_monthly_installment(loan_amount,  interest_rate, tenure):
    # Convert annual interest rate to monthly interest rate
    monthly_interest_rate = interest_rate / 12 / 100
    
    # Calculate total number of payments (loan tenure in months)
    total_payments = tenure
    
    # Calculate EMI using the formula
    emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**total_payments) / ((1 + monthly_interest_rate)**total_payments - 1)
    
    return emi



def calculate_credit_score(customer_id):
    db_conn = connection

    query = f"SELECT * FROM public.credit_approval_loan WHERE customer_id = {customer_id};"
    loan_data = pd.read_sql_query(query, db_conn)

    total_loans = len(loan_data)
    loans_paid_on_time = loan_data['emis_paid_on_time'].sum()
    current_year = pd.Timestamp.now().year
    
    loans_this_year = loan_data[pd.to_datetime(loan_data['start_date']).dt.year == current_year]
    loan_activity_this_year = len(loans_this_year)
    total_approved_volume = loan_data['loan_amount'].sum()

    sum_current_loans = loan_data['loan_amount'].sum()
    approved_limit = get_approved_limit(customer_id)  # Get approved limit from customer data
    if sum_current_loans > approved_limit:
        credit_score = 0
    else:
        credit_score = (
            (loans_paid_on_time / total_loans) * 20 +
            (total_loans / 10) +
            (loan_activity_this_year / 2) +
            (total_approved_volume / 10000)
        )
        credit_score = min(credit_score, 100)

    return credit_score


def get_approved_limit(customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        return customer.approved_limit
    
    except Customer.DoesNotExist:
        return None

